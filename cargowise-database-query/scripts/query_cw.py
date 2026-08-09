import sys
import os
import json
import pyodbc
from typing import Any

def execute_query(query: str) -> None:
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    os.environ[k] = v

    server = os.environ.get('CW_DB_SERVER')
    database = os.environ.get('CW_DB_NAME')
    username = os.environ.get('CW_DB_USER')
    password = os.environ.get('CW_DB_PASS')

    if not all([server, database, username, password]):
        print(json.dumps({
            "error": "Missing database credentials. Please ensure CW_DB_SERVER, CW_DB_NAME, CW_DB_USER, and CW_DB_PASS are set in environment variables."
        }))
        sys.exit(1)

    # Standard SQL Server connection string
    conn_str = (
        f"DRIVER={{ODBC Driver 11 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password}"
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        cursor.execute(query)
        
        # Determine if it's a SELECT query or something else
        if cursor.description is not None:
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                # Convert row to dict
                results.append(dict(zip(columns, row)))
            print(json.dumps(results, default=str))
        else:
            # For non-SELECT statements (which shouldn't happen for read-only, but just in case)
            conn.commit()
            print(json.dumps({"status": "Success", "rows_affected": cursor.rowcount}))

    except pyodbc.Error as e:
         print(json.dumps({
            "error": "Database connection or query error. Please ensure your VPN is ACTIVATED, as the database requires a whitelisted dedicated IP.",
            "details": str(e)
         }))
    except Exception as e:
         print(json.dumps({
            "error": "Unexpected error",
            "details": str(e)
         }))
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "No SQL query provided. Usage: python query_cw.py \"<SQL_QUERY>\" OR python query_cw.py --file <path>"
        }))
        sys.exit(1)

    if sys.argv[1] == "--file":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "--file requires a path argument"}))
            sys.exit(1)
        with open(sys.argv[2], "r", encoding="utf-8") as fh:
            sql_query = fh.read().strip()
    else:
        sql_query = sys.argv[1]

    execute_query(sql_query)
