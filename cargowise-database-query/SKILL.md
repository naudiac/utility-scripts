---
name: cargowise-database-query
description: Queries the CargoWise read-only SQL Server replica for shipment statuses, consignments, or reporting data based on user natural language prompts. Trigger this when the user asks to check CargoWise for a shipment, find a consignment, or query CargoWise data.
---

# CargoWise Database Query Skill

This skill enables you to connect to the CargoWise SQL Server replica and run read-only queries.

## Instructions
1. Analyze the user's natural language request (e.g. "What is the status of shipment SHP12345?").
2. Formulate a valid Microsoft SQL Server query to retrieve the necessary data. If you don't know the exact schema, formulate a query to inspect the schema first (e.g., querying `INFORMATION_SCHEMA.TABLES` or `INFORMATION_SCHEMA.COLUMNS`).
3. Run the python script located at `./scripts/query_cw.py` relative to this skill folder, passing the SQL query as an argument:
   `python C:\Users\whanusiewicz\.gemini\config\skills\cargowise-database-query\scripts\query_cw.py "YOUR SQL QUERY HERE"`
4. Review the returned JSON data.
5. Summarize the findings clearly for the user.

## Important Notes
- **CRITICAL VPN REQUIREMENT**: The database requires a dedicated whitelisted IP. If the connection fails or times out, immediately ask the user to verify that their VPN is active.
- The database connection requires the `pyodbc` python package.
- Credentials must be set via environment variables on the host system: `CW_DB_SERVER`, `CW_DB_NAME`, `CW_DB_USER`, and `CW_DB_PASS`.
- This is a read-only replica. Do NOT attempt to run UPDATE, INSERT, or DELETE commands.
