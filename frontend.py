import streamlit as st
import requests
import json

# 設定 API 的網址 (就是我們 FastAPI 跑起來的網址)
API_URL = "http://127.0.0.1:8000/api/chat"

st.set_page_config(page_title="電商智能客服 Agent", page_icon="🤖")

st.title("🤖 電商智能客服 Agent")
st.caption("支援意圖：查詢物流 (Mock) / 退換貨政策 (RAG) / 商品資訊")

# 初始化聊天紀錄 (Session State)
# Streamlit 每次重整畫面變數會重置，所以要存在 session_state 裡
if "messages" not in st.session_state:
    st.session_state.messages = []

# 1. 顯示目前的聊天紀錄
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # 如果是 AI 的回答，且有額外資訊 (意圖/來源)，顯示出來
        if "meta" in msg:
            with st.expander("🔧 技術細節 (Intent & Source)"):
                st.json(msg["meta"])

# 2. 接收使用者輸入
if prompt := st.chat_input("請輸入您的問題... (例如：我要怎麼退貨？)"):
    # 顯示使用者的話
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 存入紀錄
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. 呼叫後端 API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤖 思考中...")
        
        try:
            # 發送 POST 請求給 FastAPI
            response = requests.post(API_URL, json={"query": prompt})
            
            if response.status_code == 200:
                data = response.json()
                answer = data["answer"]
                intent = data["intent"]
                source = data["source"]
                
                # 顯示回答
                message_placeholder.markdown(answer)
                
                # 顯示除錯資訊 (這是展示給面試官看的亮點！)
                with st.expander(f"🔧 技術細節: Intent={intent}"):
                    st.write(f"**偵測意圖:** `{intent}`")
                    st.write(f"**資料來源:** `{source}`")
                    if data.get("meta"):
                        st.write("**API 原始數據:**", data["meta"])

                # 存入紀錄
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "meta": {"intent": intent, "source": source}
                })
            else:
                error_msg = f"❌ API 錯誤: {response.status_code}"
                message_placeholder.error(error_msg)
                
        except Exception as e:
            message_placeholder.error(f"❌ 連線失敗: {e}")
            st.caption("請確認 FastAPI 伺服器 (port 8000) 是否有啟動？")