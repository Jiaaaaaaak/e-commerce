# app/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    query: str = Field(..., description="使用者輸入的自然語言問題")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="LLM 或 Agent 生成的最終回答")
    intent: str = Field(..., description="系統判斷的使用者意圖")
    source: List[str] = Field(..., description="引用來源")
    meta: Optional[dict] = Field(None, description="額外資訊")