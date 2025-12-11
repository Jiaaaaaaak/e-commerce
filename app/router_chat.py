# app/router_chat.py 

from fastapi import APIRouter
# 使用相對路徑 .schemas
from .schemas import ChatRequest, ChatResponse
from .intent.classifier import classify_intent
from .services.logistics import get_logistics_status
# 正確匯入 app/rag/retriever.py 中的 get_rag_answer 函式
from .rag.retriever import get_rag_answer 

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    主要的對話 API 接口，負責 Agent 的意圖分類與流程分派。
    """
    query = request.query
    
   # 1. 判斷意圖
    intent = classify_intent(query)
    print(f" [Intent]: {intent}") # 印出意圖方便除錯
    
    answer = ""
    sources = []
    meta = {}
    
    # 2. 路由分派 (Agent Tool Use)
    if intent == "logistics":
        # 簡單提取數字當作訂單號 (範例用)
        order_id = "9527" if "9527" in query else "unknown"
        data = get_logistics_status(order_id)
        
        answer = data["message"]
        sources = ["logistics_api"]
        meta = data
        
    elif intent in ["refund", "product", "faq", "payment", "fallback"]:
        # 走 RAG 流程
        ans, docs = get_rag_answer(query)
        answer = ans
        sources = docs
        
    else:
        # 例外處理
        answer = "抱歉，我不確定如何處理您的問題。"
        sources = []

    return ChatResponse(
        answer=answer,
        intent=intent,
        source=sources,
        meta=meta
    )