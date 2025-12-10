# app/services/logistics.py

def get_logistics_status(order_id: str) -> dict:
    """
    [Mock] 模擬查詢物流狀態的企業 API
    """
    if "9527" in order_id:
        return {
            "status": "shipped",
            "message": f"訂單 {order_id} 已出貨，預計明日送達。"
        }
    else:
        return {
            "status": "processing",
            "message": f"訂單 {order_id} 正在備貨中。"
        }