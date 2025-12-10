import os
import pickle
import numpy as np
import faiss
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

VECTOR_DB_PATH = "data/vector_store/"
_index = None
_documents = None

def load_index():
    global _index, _documents
    if _index is None:
        _index = faiss.read_index(os.path.join(VECTOR_DB_PATH, "index.faiss"))
        with open(os.path.join(VECTOR_DB_PATH, "metadata.pkl"), "rb") as f:
            _documents = pickle.load(f)

def get_rag_answer(query: str):
    # 1. 載入索引
    load_index()
    
    # 2. 將使用者的問題轉成向量 (Real Mode)
    # 注意：這裡必須跟 ingest 時用一樣的模型 (text-embedding-3-small)
    query = query.replace("\n", " ")
    response = client.embeddings.create(input=[query], model="text-embedding-3-small")
    query_vector = np.array([response.data[0].embedding]).astype("float32")
    
    # 3. 向量搜尋 (找最相似的 2 筆)
    k = 2 
    distances, indices = _index.search(query_vector, k)
    
    # 4. 整理 Context
    retrieved_docs = []
    source_ids = []
    
    # 檢查距離，如果距離太遠(不相關)，可以過濾掉 (這裡先不設閾值，直接回傳)
    for i, idx in enumerate(indices[0]):
        if idx < len(_documents):
            doc = _documents[idx]
            retrieved_docs.append(f"【參考資料 {i+1}】(ID: {doc['id']})\n問題：{doc['question']}\n答案：{doc['answer']}")
            source_ids.append(doc['id'])
            
    context_text = "\n\n".join(retrieved_docs)
    
    # 5. LLM 生成回答
    system_prompt = "你是一個專業的電商客服。請參考提供的資料以繁體中文回答使用者問題。若參考資料中有答案，請以此為準；若無，請禮貌告知無法回答。"
    user_prompt = f"使用者問題：{query}\n\n參考資料庫檢索結果：\n{context_text}"
    
    chat_response = client.chat.completions.create(
        model="gpt-4-turbo", # 既然付費了，就用聰明的模型！(或 gpt-3.5-turbo 省錢)
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    
    answer = chat_response.choices[0].message.content
    return answer, source_ids