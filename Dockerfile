# =======================================================
# STAGE 1: BUILDER
# =======================================================
FROM python:3.11-bookworm as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 建立虛擬環境
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =======================================================
# STAGE 2: RUNTIME
# =======================================================
FROM python:3.11-bookworm as runtime

WORKDIR /app

# 複製虛擬環境
COPY --from=builder /opt/venv /opt/venv

# 設定環境變數 (雖然用 python -m 可以繞過，但設定 PATH 仍是好習慣)
ENV PATH="/opt/venv/bin:$PATH"

# 複製程式碼
COPY . .

EXPOSE 8000 8501

# [關鍵修正] 使用 python -m 來啟動，避免 "command not found"
RUN echo '#!/bin/bash\npython -m uvicorn app.main:app --host 0.0.0.0 --port 8000 & \npython -m streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0' > start.sh
RUN chmod +x start.sh

CMD ["./start.sh"]