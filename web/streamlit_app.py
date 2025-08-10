import os
import sys
import platform
import streamlit as st
import requests
from dotenv import load_dotenv
from io import BytesIO

# =========================
# 1) CONFIGURAÇÃO FIXA E TRAVADA
# =========================
st.set_page_config(page_title="Q-Core SaaS", layout="wide")
load_dotenv()

# Endpoints fixos (travados)
BACKEND_BASE_URL = "https://qcoresystem-production.up.railway.app".rstrip("/")
BACKEND_ANALYZE_URL = f"{BACKEND_BASE_URL}/api/analyze"
BACKEND_UPLOAD_URL = f"{BACKEND_BASE_URL}/api/upload"

# Se tentar sobrescrever por env, força travamento
if os.getenv("BACKEND_BASE_URL") not in (None, "", BACKEND_BASE_URL):
    st.error("Configuração inválida detectada. BACKEND_BASE_URL alterada.")
    st.stop()

# =========================
# 2) VERIFICAÇÃO DO BACKEND
# =========================
try:
    resp = requests.get(BACKEND_BASE_URL, timeout=5)
    if resp.ok:
        st.success("✅ Backend online")
    else:
        st.warning("⚠️ Backend offline")
except Exception as e:
    st.warning(f"⚠️ Backend offline: {e}")

# =========================
# 3) INTERFACE
# =========================
st.title("Q-Core AI :: Simulador Preditivo")
st.caption(f"🐍 Python: {platform.python_version()}")

# Upload
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
                files = {"file": (file.name, BytesIO(file.getvalue()), file.type or "application/octet-stream")}
                r = requests.post(BACKEND_UPLOAD_URL, files=files, timeout=60)
                r.raise_for_status()
                saved_paths.append(r.json().get("file_path"))
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao enviar {file.name}: {e}")
        if saved_paths:
            st.success("Arquivos enviados!")
            st.session_state["uploaded_paths"] = saved_paths

# Pergunta
question = st.text_input("Agora, digite uma pergunta analítica:")

if st.button("Enviar pergunta"):
    if not question:
        st.warning("Digite uma pergunta antes de enviar.")
    elif not st.session_state.get("uploaded_paths"):
        st.warning("Faça upload de arquivos antes de perguntar!")
    else:
        try:
            payload = {"question": question, "file_paths": st.session_state["uploaded_paths"]}
            r = requests.post(BACKEND_ANALYZE_URL, json=payload, timeout=60)
            r.raise_for_status()
            result = r.json()

            st.success("✅ Resposta recebida!")
            st.subheader("Resumo Executivo")
            st.info(result.get("resumo_executivo", ""))

            st.subheader("Detalhe Técnico")
            st.write(result.get("detalhe_tecnico", ""))

            if result.get("cenarios_alternativos"):
                st.subheader("Cenários Alternativos")
                st.write(result["cenarios_alternativos"])

            if result.get("recomendacoes"):
                st.subheader("Recomendações")
                st.write(result["recomendacoes"])

            st.subheader("Explicabilidade")
            st.write(result.get("explicabilidade", ""))

            st.subheader("Confiança")
            conf = result.get("confianca")
            st.write(f"{conf*100:.1f}%") if isinstance(conf, (int, float)) else st.write(conf or "—")

            if result.get("entidades"):
                st.subheader("Entidades Extraídas")
                st.write(result["entidades"])

            if result.get("limitacoes"):
                st.subheader("Limitações")
                st.warning(result["limitacoes"])

        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao conectar com o servidor: {e}")
