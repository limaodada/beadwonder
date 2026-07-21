FROM python:3.11-slim

WORKDIR /app

COPY requirements_deploy.txt .
RUN pip install --no-cache-dir -r requirements_deploy.txt

COPY app_v2.py .

# 暴露端口 (HF Spaces / Streamlit Cloud 标准端口)
EXPOSE 7860

# 启动命令
CMD ["streamlit", "run", "app_v2.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.headless=true"]
