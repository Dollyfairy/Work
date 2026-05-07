import requests
from datetime import datetime
import urllib3
import json
import os



# 忽略 SSL 安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================= 設定區 =================
EMP_ID = os.environ["EMP_ID"]
PASSWORD = os.environ["PASSWORD"]
TEMP = 36  # 你可以改成想要的體溫

SAVE_URL = "https://websrv01.tpech.gov.tw/ETR/Home/etr_marge" 
# ==========================================

def start_auto_fill():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://websrv01.tpech.gov.tw/ETR/Home/Index"
    })

    # 第一步：登入 (獲取 Session)
    login_url = "https://websrv01.tpech.gov.tw/ETR/Home/adLogin"
    try:
        login_res = session.post(login_url, data={"Account": EMP_ID, "Password": PASSWORD}, verify=False)
        
        if login_res.status_code == 200:
            print("✅ 1. 帳號登入成功")
           
            payload = {
                "user_id": EMP_ID,
                "emp_pwd": PASSWORD,
                "displayName": "許芷瑄",
                "mail": f"{EMP_ID}@tpech.gov.tw",
                "company": "臺北市立聯合醫院",
                "department": "陽明院區-8A病房",
                "emp_no": EMP_ID,
                "body_temperature": TEMP,
                "op_user": EMP_ID
            }

            # 第三步：提交存檔
            # 使用 json.dumps 確保格式為字串化後的 JSON
            save_res = session.post(SAVE_URL, data=json.dumps(payload), verify=False)
            
            print(f"DEBUG - 伺服器回傳狀態: {save_res.status_code}")
            print(f"DEBUG - 伺服器回傳內容: {save_res.text}")

            if save_res.status_code == 200:
                print(f"🚀 成功！體溫 {TEMP} 已存入系統。請重新整理網頁檢查。")
            else:
                print("❌ 存檔失敗，請確認是否在醫院內網環境執行。")
        else:
            print("❌ 登入失敗，請檢查帳密。")
            
    except Exception as e:
        print(f"💥 執行錯誤: {e}")

if __name__ == "__main__":
    start_auto_fill()