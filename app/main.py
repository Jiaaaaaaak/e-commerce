
from fastapi import FastAPI
from app.router_chat import router as chat_router # 匯入聊天路由
from dotenv import load_dotenv

load_dotenv() # 載入 .env 檔案中的環境變數

# 初始化 FastAPI 應用
app = FastAPI(title="Customer Service Agent")

app.include_router(chat_router, prefix="/api", tags=["Chat"])

@app.get("/")
def root():
    return {"message": "Agent System is Running!"}