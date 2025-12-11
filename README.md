#  E-Commerce Intelligent Agent (RAG + Intent Agent)

 電商智能客服系統，結合了 **Intent Analysis (意圖識別)** 與 **RAG (檢索增強生成)** 技術。本專案展示了 LLM 應用從核心邏輯到 Docker 容器化交付的完整流程。

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://imgshields.io/badge/FastAPI-0.110-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT4-orange)
![Docker](https://img.shields.io/badge/Containerization-Docker-blue)
![VectorDB](https://img.shields.io/badge/VectorDB-FAISS-lightgrey)

---

##  專案核心亮點

1.  **Agent / Tool Use 架構：** 系統能判斷使用者意圖，並自動選擇呼叫 **RAG 知識庫 (FAQ)** 或 **Mock API (物流/訂單)**。
2.  **企業級 RAG 實作：** 完整的 Ingestion（OpenAI Embedding + FAISS 向量儲存）和 Retrieval 流程。
3.  **微服務化交付：** 使用 **FastAPI** 獨立運行 Agent 後端，使用 **Streamlit** 運行前端 UI，並透過 **Docker Compose** 一鍵啟動。
4.  **可視化 Debugging：** 前端 UI 透過 Expander 顯示 **準確的意圖 (Intent)** 和 **引用來源 (Source)**，證明系統決策過程透明。

##  系統架構圖 (Architecture)

整個系統分為三個層次：Frontend (UI)、Backend (Agent Logic)、Data/Tooling (Knowledge/Service)。

```mermaid
graph TD
    User[Web User] -->|Streamlit UI| Frontend[Frontend (Port 8501)]
    Frontend -->|HTTP POST /api/chat| Backend[FastAPI Backend (Port 8000)]
    Backend --> Intent{Intent Classifier (LLM)}
    
    Intent -->|Logistics/Order| Service[Mock Service (Python)]
    Intent -->|Refund/FAQ/Product| RAG[RAG Pipeline]
    
    RAG -->|Vector Search| FAISS[(FAISS Index)]
    RAG -->|Context + Query| GPT[LLM Generator]
    
    Service --> Response[Response Formatter]
    GPT --> Response
    Response --> Backend
    Backend --> Frontend
```

部署與啟動 (Docker / 本地)
方案 A: 推薦使用 Docker (一鍵啟動)
Docker 是最推薦的啟動方式，它確保了環境的可重現性，是面試時的加分項。

安裝 Docker：確保您已經安裝並運行了 Docker Desktop。

建構與啟動： 在專案根目錄下執行：

Bash

# 第一次建構會比較久，因為需要安裝所有依賴
docker-compose up --build
訪問： 打開瀏覽器訪問 http://localhost:8501。

方案 B: 本地 Python 環境啟動
如果您不使用 Docker，可以手動在 Python 環境中啟動：

安裝與設定：

Bash

# 假設已在 Python 3.11 虛擬環境中
pip install -r requirements.txt

# 確保 .env 已填入 OPENAI_API_KEY
python -m app.rag.ingest # 建立知識庫索引
啟動系統 (需開兩個終端機):

Bash

# 終端機 1 (後端 Agent)
uvicorn app.main:app --reload

# 終端機 2 (前端 UI)
streamlit run frontend.py
 知識庫擴充指南 (Ingestion)
要擴充 Agent 的知識庫，只需修改 data/faq.json 檔案，然後重新建立索引。

編輯檔案： 修改 data/faq.json，新增或修改 QA 資料。

重新 Ingest： 執行以下指令，系統將使用 OpenAI 重新生成向量並更新 FAISS 索引。

Bash

python -m app.rag.ingest
🛠 技術棧 (Tech Stack)
類別	技術	用途
Agent Core	Python 3.11	主程式語言
Backend API	FastAPI, Uvicorn	建立高性能 Agent 接口
Frontend UI	Streamlit	快速搭建聊天介面 (無需寫 JS/CSS)
LLM / Embedding	OpenAI (GPT-4/GPT-3.5)	意圖分類、回答生成、向量化
Vector DB	FAISS (CPU)	輕量、高效的本地向量搜尋與儲存
DevOps	Docker / Docker Compose	容器化部署，確保環境一致性