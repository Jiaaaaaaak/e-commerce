# app/intent/classifier.py

from app.utils.llm_client import llm_client

# 定義我們支援的所有意圖類別
SUPPORTED_INTENTS = [
    "logistics",  # 物流 / 出貨 / 配送查詢
    "refund",     # 退貨 / 退款問題
    "product",    # 商品規格 / 庫存 / 適用性問題
    "payment",    # 刷卡 / 分期 / 付款失敗問題
    "faq",        # 一般客服問題 (走 RAG 處理)
    "fallback"    # 不確定或無法分類的問題 (走 RAG 處理)
]

def classify_intent(query: str) -> str:
    """
    使用 LLM 判斷使用者問題的意圖。

    Args:
        query: 使用者的輸入問題。

    Returns:
        意圖類別的字串 (e.g., 'logistics', 'faq')。
    """
    # 這是給 LLM 的 System Prompt (角色設定與指令)
    system_prompt = f"""
    你是電商客服意圖分類器。請根據使用者提供的問題，從以下列表中選擇一個最合適的意圖標籤並單獨輸出：
    {', '.join(SUPPORTED_INTENTS)}
    
    請注意：
    1. 如果問題與特定訂單號或個人帳務（如：物流、付款、退款進度）有關，請選 {SUPPORTED_INTENTS[0]}、{SUPPORTED_INTENTS[1]}、{SUPPORTED_INTENTS[3]}。
    2. 如果問題與商品資訊（如：規格、現貨、適用性）有關，請選 {SUPPORTED_INTENTS[2]}。
    3. 如果是常規或廣泛的政策問題（如：如何註冊、運費標準），請選 {SUPPORTED_INTENTS[4]}。
    4. 如果無法判斷或問題模糊，請選 {SUPPORTED_INTENTS[5]}。
    """
    
    # 這是使用者輸入的內容 (我們要分類的資料)
    user_prompt = f"請判斷這句話的意圖：『{query}』"
    
    intent = llm_client.get_completion(system_prompt, user_prompt)
    
    # 簡單的後處理，確保回傳值乾淨
    for supported in SUPPORTED_INTENTS:
        if supported in intent:
            return supported
            
    return "fallback"