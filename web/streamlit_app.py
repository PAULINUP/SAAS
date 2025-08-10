import os, sys, platform
import streamlit as st
import requests
from dotenv import load_dotenv

# bootstrap: garantir import da raiz do repo
ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# >>> PRIMEIRA e ÚNICA chamada de Streamlit <<<
st.set_page_config(page_title="Q-Core SaaS", layout="wide")

# diag rápido
st.caption(f"🐍 Python: {platform.python_version()}")

# secrets .env
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))
load_dotenv()

st.title("Q-Core AI :: Simulador Preditivo")
st.write("Faça upload de múltiplos arquivos e uma pergunta analítica.")

# URLs do backend
BACKEND_ANALYZE_URL = os.getenv("BACKEND_API_URL", "https://qcoresystem-production.up.railway.app/api/analyze")
BACKEND_UPLOAD_URL  = os.getenv("BACKEND_API_UPLOAD_URL", "https://qcoresystem-production.up.railway.app/api/upload")

# status do backend
try:
    base = BACKEND_ANALYZE_URL.split("/api")[0] or BACKEND_ANALYZE_URL
    ok = requests.get(base, timeout=5).ok
    st.success("Backend online ✅") if ok else st.warning("Backend offline ⚠️")
except Exception:
    st.warning("Backend offline ⚠️")

# upload
uploaded_files = st.file_uploader(
    "Selecione arquivos (PDF, Excel, Word, CSV, JSON, TXT)",
    type=["pdf","csv","xlsx","xls","docx","json","txt"],
    accept_multiple_files=True,
    key="uploader"
)

if uploaded_files:
    st.info(f"{len(uploaded_files)} arquivo(s) selecionado(s).")
    if st.button("Enviar arquivos para processamento"):
        saved_paths = []
        for file in uploaded_files:
            try:
                files = {"file": (file.name, file.getvalue())}
                r = requests.post(BACKEND_UPLOAD_URL, files=files, timeout=30)
                r.raise_for_status()
                saved_paths.append(r.json().get("file_path"))
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao enviar {file.name}: {e}")
        if saved_paths:
            st.success("Arquivos enviados!")
            st.session_state["uploaded_paths"] = saved_paths

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

                st.subheader("Resumo Executivo");  st.info(result.get("resumo_executivo",""))
                st.subheader("Detalhe Técnico");   st.write(result.get("detalhe_tecnico",""))
                if result.get("cenarios_alternativos"):
                    st.subheader("Cenários Alternativos"); st.write(result["cenarios_alternativos"])
                if result.get("recomendacoes"):
                    st.subheader("Recomendações"); st.write(result["recomendacoes"])
                st.subheader("Explicabilidade");   st.write(result.get("explicabilidade",""))
                st.subheader("Confiança")
                conf = result.get("confianca")
                st.write(f"{conf*100:.1f}%") if isinstance(conf,(int,float)) else st.write(conf or "—")
                if result.get("entidades"):
                    st.subheader("Entidades Extraídas"); st.write(result["entidades"])
                if result.get("limitacoes"):
                    st.subheader("Limitações"); st.warning(result["limitacoes"])
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao conectar com o servidor: {e}")
