# app/main.py
"""
Ponto de entrada do backend FastAPI do Q-Core AI System.
"""

from fastapi import FastAPI
from app.api.routes import router as api_routes
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🔧 Inicializando o backend Q-Core AI...")

# Instância da aplicação FastAPI
app = FastAPI(
    title="Q-Core AI System",
    description=(
        "Plataforma SaaS + API para análise preditiva multidocumental com força bruta de cálculo, "
        "feedback simbiótico e simulação explicável."
    ),
    version="1.0.0"
)

# Registra rotas da API
app.include_router(api_routes)

# Health check
@app.get("/")
async def read_root():
    return {"message": "Q-Core AI is running 🚀"}

logger.info("✅ Backend FastAPI carregado com sucesso.")

# ⚠️ IMPORTANTE:
# Execute com:
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# Nunca use `python main.py` diretamente
