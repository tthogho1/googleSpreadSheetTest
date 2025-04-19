import gspread
from google.oauth2.service_account import Credentials
import os
import time
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

def get_sheet_names(file_id):
    # 新しい認証方法を使用（oauth2clientは非推奨）
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file(os.getenv('JSON_KEY_PATH'), scopes=scope)
    client = gspread.authorize(credentials)
    
    try:
        # fileIDを使用してスプレッドシートを開く
        spreadsheet = client.open_by_key(file_id)
        sheet_names = [worksheet.title for worksheet in spreadsheet.worksheets()]
        
        # Google Sheets API v4を使用してデータを取得する場合
        service = build('sheets', 'v4', credentials=credentials)
        sheets = service.spreadsheets()
        
        range_name = f"{sheet_names[0]}!A:AE"
        
        # 時間計測開始
        start_time = time.time()
        
        # API呼び出し
        result = sheets.values().get(spreadsheetId=file_id, range=range_name).execute()
        
        # 時間計測終了
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # 実行時間を出力
        print(f"API実行時間: {elapsed_time:.4f}秒")
        
        values = result.get("values", [])
        print(values)
        return sheet_names
    except gspread.exceptions.APIError as e:
        print(f"APIエラー: {e}")
        # エラー詳細を確認
        print("スプレッドシートへのアクセス権限を確認してください")
        return []

# 使用例
file_id = os.getenv('FILE_ID')  # 正しいIDであることを確認
sheet_names = get_sheet_names(file_id)
print(sheet_names)
