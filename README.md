# E-Commerce Intelligent Agent (RAG + Intent Classification)

這是一個企業級的電商智能客服系統，結合了 **Intent Analysis (意圖識別)** 與 **RAG (檢索增強生成)** 技術。
前端使用 **Streamlit** 打造對話介面，後端使用 **FastAPI** 處理邏輯，並透過 **OpenAI GPT-4** 進行決策與生成。

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT4-orange)

## 核心功能

1.  **意圖識別 (Intent Agent)**：自動判斷使用者意圖（物流查詢、退貨政策、商品資訊...）。
2.  **RAG 知識庫 (Knowledge Base)**：基於 `data/faq.json` 的向量檢索，準確回答企業內部政策。
3.  **工具呼叫 (Tool Use)**：
    * **Mock API**：模擬查詢即時訂單狀態。
    * **Vector Search**：檢索 FAQ 文件。
4.  **完整介面**：提供 Streamlit 網頁聊天視窗，展示思維鏈 (Chain of Thought) 與引用來源。

## 系統架構

```mermaid
graph TD
    User[Web User] -->|Streamlit UI| Frontend[Frontend (Port 8501)]
    Frontend -->|HTTP POST| Backend[FastAPI Backend (Port 8000)]
    Backend --> Intent{Intent Classifier}
    
    Intent -->|Logistics| Service[Mock Logistics Service]
    Intent -->|Refund/FAQ| RAG[RAG Pipeline]
    
    RAG -->|Embedding| FAISS[(Vector Store)]
    RAG -->|Context| GPT[LLM Generator]
    
    Service --> Response
    GPT --> Response
    Response --> Frontend
    
快速開始 (Quick Start)
1. 安裝依賴
建議使用 uv 進行快速安裝：

Bash

pip install uv
uv venv venv_uv --python 3.11
source venv_uv/bin/activate  # Windows: venv_uv\Scripts\activate
uv pip install -r requirements.txt
2. 設定環境變數
請複製 .env.example 為 .env 並填入 API Key：

Bash

OPENAI_API_KEY=sk-xxxx...
CHAT_MODEL=gpt-4-turbo
3. 建立知識庫索引
Bash

python -m app.rag.ingest
4. 啟動系統
終端機 1 (後端):

Bash

uvicorn app.main:app --reload
終端機 2 (前端):

Bash

streamlit run frontend.py
打開瀏覽器訪問 http://localhost:8501 即可開始對話。

專案結構
app/: 後端核心邏輯

intent/: 意圖分類模組

rag/: 檢索增強生成模組

services/: 模擬外部服務

data/: 知識庫來源與索引

frontend.py: Streamlit 前端程式