from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_routes

app = FastAPI(title="Q-Core AI – API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # opcionalmente restrinja ao domínio do Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

app.include_router(api_routes)
