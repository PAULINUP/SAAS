@echo off
echo 🚀 Iniciando o backend FastAPI (porta 8000)...
start cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3 >nul
echo ✅ Backend rodando!

echo 🌐 Iniciando interface Streamlit (porta 8501)...
start streamlit run web/streamlit_app.py
