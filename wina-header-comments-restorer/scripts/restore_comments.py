import sys
import json
import os
import win32com.client

def restore(filepath):
    print(f"Loading {filepath}...")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, 'resources', 'comments_config.json')
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    excel = win32com.client.Dispatch('Excel.Application')
    excel.Visible = False
    excel.DisplayAlerts = False
    wb = excel.Workbooks.Open(os.path.abspath(filepath))

    try:
        sheet = wb.Worksheets('GWS Report template')
        for cell_ref, text in config.items():
            cell_range = sheet.Range(cell_ref)
            try: cell_range.Comment.Delete()
            except: pass
            try: cell_range.CommentThreaded.Delete()
            except: pass
            cell_range.AddCommentThreaded(text)

        wb.Save()
        print("Comments successfully restored using threaded comments!")
    finally:
        wb.Close(False)
        excel.Quit()

if __name__ == "__main__":
    restore(sys.argv[1])
