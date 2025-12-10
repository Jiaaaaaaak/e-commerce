import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/chat"

def test_query(query_text):
    print(f"\n🤖 測試問題: {query_text}")
    try:
        payload = {"query": query_text}
        response = requests.post(BASE_URL, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 意圖: {data['intent']}")
            print(f"📄 回答: {data['answer']}")
            print(f"🔗 來源: {data['source']}")
        else:
            print(f"❌ 錯誤: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ 連線失敗: {e}")

if __name__ == "__main__":
    # 測試 1: 物流
    test_query("我想查訂單 9527 到哪了")
    
    # 測試 2: 退貨 (走 RAG)
    test_query("請問退貨運費是誰要出？")