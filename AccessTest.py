import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv

load_dotenv()
def test_access(file_id):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file(os.getenv('JSON_KEY_PATH'), scopes=scope)
    client = gspread.authorize(credentials)
    
    # サービスアカウントのメールアドレスを表示
    print(f"使用中のサービスアカウント: {credentials.service_account_email}")
    
    try:
        # スプレッドシートを開こうとする
        spreadsheet = client.open_by_key(file_id)
        print(f"アクセス成功: スプレッドシート「{spreadsheet.title}」")
        return True
    except gspread.exceptions.SpreadsheetNotFound:
        print("エラー: スプレッドシートが見つかりません")
        return False
    except gspread.exceptions.APIError as e:
        print(f"APIエラー: {e}")
        return False

file_id = os.getenv('FILE_ID')
test_access(file_id)