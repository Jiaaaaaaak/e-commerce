# app/utils/llm_client.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() # 確保環境變數已載入

class LLMClient:
    """
    LLM API 呼叫的通用 Client，目前支援 OpenAI。
    """
    def __init__(self):
        # 從 .env 取得 API Key 和模型名稱
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.chat_model = os.getenv("CHAT_MODEL", "gpt-4-turbo") # 預設模型

    def get_completion(self, system_prompt: str, user_prompt: str) -> str:
        """
        呼叫 LLM 進行對話補齊 (Completion)
        """
        try:
            response = self.client.chat.completions.create(
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.0,  # 分類任務，我們希望結果穩定，所以設定為 0.0
                max_tokens=50     # 只需要輸出一兩個單詞的分類結果，所以限制長度
            )
            # LLM 的回應通常會包含額外的訊息，我們只需要它的文字內容
            return response.choices[0].message.content.strip().lower()
        except Exception as e:
            print(f"LLM API 呼叫失敗: {e}")
            # 發生錯誤時，回傳一個安全值，讓系統走 RAG 處理
            return "fallback"

# 初始化一個全域的 Client 實例供其他模組使用
llm_client = LLMClient()