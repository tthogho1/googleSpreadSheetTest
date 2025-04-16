import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv

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