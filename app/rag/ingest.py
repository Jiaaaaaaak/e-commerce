import json
import os
import pickle
import numpy as np
import faiss
from dotenv import load_dotenv
from openai import OpenAI

# 載入環境變數
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 設定路徑
DATA_PATH = "data/faq.json"
VECTOR_DB_PATH = "data/vector_store/"

def get_embedding(text):
    """
    [Real Mode] 呼叫 OpenAI 取得真實向量
    """
   
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model="text-embedding-3-small").data[0].embedding

def main():
    print(f"🚀 [Real Mode] 開始建立 RAG 索引，讀取資料: {DATA_PATH}...")
    
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        faq_data = json.load(f)
    
    documents = []
    embeddings = []
    
    print(f"📊 正在將 {len(faq_data)} 筆 FAQ 轉為向量 ...")
    for item in faq_data:
        # 組合問題與答案，讓語意更完整
        combined_text = f"問題：{item['question']} 答案：{item['answer']}"
        
        try:
            vector = get_embedding(combined_text)
            embeddings.append(vector)
            documents.append(item)
        except Exception as e:
            print(f"❌ 轉換失敗: {e}")
            return

    # 建立 FAISS 索引
    if not embeddings:
        print("⚠️ 沒有資料被轉換，請檢查 API Key 或額度。")
        return

    dimension = len(embeddings[0]) 
    index = faiss.IndexFlatL2(dimension)
    
    vector_np = np.array(embeddings).astype("float32")
    index.add(vector_np)
    
    # 存檔
    if not os.path.exists(VECTOR_DB_PATH):
        os.makedirs(VECTOR_DB_PATH)
        
    faiss.write_index(index, os.path.join(VECTOR_DB_PATH, "index.faiss"))
    
    with open(os.path.join(VECTOR_DB_PATH, "metadata.pkl"), "wb") as f:
        pickle.dump(documents, f)
        
    print("✅ 真實 RAG 索引建立完成！檔案已儲存。")

if __name__ == "__main__":
    main()