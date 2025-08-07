#!/bin/bash

echo "🔧 Inicializando Q-Core AI com backend FastAPI e frontend Streamlit..."

# Inicia o backend em segundo plano
uvicorn app.main:app --host 0.0.0.0 --port 8080 &

# Espera o backend subir
sleep 5

# Inicia o frontend Streamlit
streamlit run web/streamlit_app.py --server.port 8081
