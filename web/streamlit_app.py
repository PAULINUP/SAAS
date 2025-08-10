# web/streamlit_app.py
import os
import sys
import platform
from io import BytesIO

import requests
import streamlit as st
from dotenv import load_dotenv

# ---------------------------------------------------------------------
# 1) Config da página - TEM que ser a 1ª chamada do Streamlit
# ---------------------------------------------------------------------
st.set_page_config(page_title="Q-Core SaaS", layout="wide")

# ---------------------------------------------------------------------
# 2) Bootstrap
# ---------------------------------------------------------------------
load_dotenv()
st.caption(f"🐍 Python: {platform.python_version()}")

# ---------------------------------------------------------------------
# 3) URLs do backend (derivadas de uma BASE única)
#    -> defina BACKEND_BASE_URL nas Secrets do Streamlit
# ---------------------------------------------------------------------
BACKEND_BASE_URL = os.getenv(
    "BACKEND_BASE_URL",
    "https://seu-app.up.railway.app"  # troque localmente se quiser
).rstrip("/")

BACKEND_ANALYZE_URL = os.getenv(
    "BACKEND_API_URL",
    f"{BACKEND_BASE_URL}/api/analyze"
)
BACKEND_UPLOAD_URL = os.getenv(
    "BACKEND_API_UPLOAD_URL",
    f"{BACKEND_BASE_URL}/api/upload"
)

# ---------------------------------------------------------------------
# 4) Guardião de backend (badge único + trava se offline)
#    importa a função, com fallback para garantir que utils/ seja achado
# ---------------------------------------------------------------------
try:
    from utils.status import backend_guard
except ModuleNotFoundError:
    # se o app estiver dentro de web/, adiciona esse diretório ao sys.path
    WEB_DIR = os.path.dirname(__file__)
    if WEB_DIR not in sys.path:
        sys.path.insert(0, WEB_DIR)
    from utils.status import backend_guard  # agora deve funcionar

backend_guard(base_url=BACKEND_BASE_URL, stop_on_fail=True)

# ---------------------------------------------------------------------
# 5) UI
# ---------------------------------------------------------------------
st.title("Q-Core AI :: Simulador Preditivo")
st.write("Faça upload de múltiplos arquivos e uma pergunta analítica.")

# (Opcional) debug discreto
with st.expander("⚙️ Endpoints ativos (debug)"):
    st.caption(f"BASE → {BACKEND_BASE_URL}")
    st.caption(f"UPLOAD → {BACKEND_UPLOAD_URL}")
    st.caption(f"ANALYZE → {BACKEND_ANALYZE_URL}")

# ====== U P L O A D ======
uploaded_files = st.file_uploader(
    "Selecione arquivos (PDF, Excel, Word, CSV, JSON, TXT)",
    type=["pdf", "csv", "xlsx", "xls", "docx", "json", "txt"],
    accept_multiple_files=True,
    key="uploader"
)

if uploaded_files:
    st.info(f"{len(uploaded_files)} arquivo(s) selecionado(s).")
    if st.button("Enviar arquivos para processamento"):
        saved_paths = []
        for file in uploaded_files:
            try:
                files = {
                    "file": (
                        file.name,
                        BytesIO(file.getvalue()),
                        file.type or "application/octet-stream",
                    )
                }
                r = requests.post(BACKEND_UPLOAD_URL, files=files, timeout=60)
                r.raise_for_status()
                saved_paths.append(r.json().get("file_path"))
            except requests.exceptions.HTTPError as e:
                st.error(f"Erro ao enviar {file.name}: {e} | {r.status_code} | {r.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao enviar {file.name}: {e}")
        if saved_paths:
            st.success("Arquivos enviados!")
            st.session_state["uploaded_paths"] = saved_paths

# ====== P E R G U N T A ======
st.write("Agora, digite uma pergunta analítica:")
question = st.text_input("Ex: Qual o risco de inadimplência?")

if st.button("Enviar pergunta"):
    if not question:
        st.warning("Digite uma pergunta antes de enviar.")
    else:
        paths = st.session_state.get("uploaded_paths", [])
        if not paths:
            st.warning("Faça upload de arquivos antes de perguntar!")
        else:
            try:
                payload = {"question": question, "file_paths": paths}
                r = requests.post(BACKEND_ANALYZE_URL, json=payload, timeout=60)
                r.raise_for_status()
                result = r.json()

                st.success("✅ Resposta recebida!")
                st.subheader("Resumo Executivo");  st.info(result.get("resumo_executivo", ""))
                st.subheader("Detalhe Técnico");   st.write(result.get("detalhe_tecnico", ""))
                if result.get("cenarios_alternativos"):
                    st.subheader("Cenários Alternativos"); st.write(result["cenarios_alternativos"])
                if result.get("recomendacoes"):
                    st.subheader("Recomendações"); st.write(result["recomendacoes"])
                st.subheader("Explicabilidade");   st.write(result.get("explicabilidade", ""))
                st.subheader("Confiança")
                conf = result.get("confianca")
                st.write(f"{conf*100:.1f}%") if isinstance(conf, (int, float)) else st.write(conf or "—")
                if result.get("entidades"):
                    st.subheader("Entidades Extraídas"); st.write(result["entidades"])
                if result.get("limitacoes"):
                    st.subheader("Limitações"); st.warning(result["limitacoes"])
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao conectar com o servidor: {e}")
