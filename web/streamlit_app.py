# Interface MVP (Streamlit) para perguntas e visualização do Q-Core AI

# --- bootstrap p/ rodar no Streamlit Cloud ---
import os, sys
ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # raiz do repo
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
import requests
from dotenv import load_dotenv

# evitar KeyError se não houver secrets configurados
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))

load_dotenv()  # carrega .env se existir

st.set_page_config(page_title="Q-Core SaaS", layout="wide")
st.title("Q-Core AI :: Simulador Preditivo")
st.write("Faça upload de múltiplos arquivos e uma pergunta analítica.")
# ---------------------------------------------

# URLs finais (produção Railway ou fallback local)
BACKEND_ANALYZE_URL = os.getenv(
    "BACKEND_API_URL",
    "https://qcoresystem-production.up.railway.app/api/analyze"
)
BACKEND_UPLOAD_URL = os.getenv(
    "BACKEND_API_UPLOAD_URL",
    "https://qcoresystem-production.up.railway.app/api/upload"
)

# Upload de múltiplos arquivos
uploaded_files = st.file_uploader(
    "Selecione arquivos para análise (PDF, Excel, Word, CSV, JSON)",
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
                files = {"file": (file.name, file.getvalue())}  # getbuffer() tbm funciona
                resp = requests.post(BACKEND_UPLOAD_URL, files=files, timeout=30)
                resp.raise_for_status()
                result_upload = resp.json()
                saved_paths.append(result_upload.get("file_path"))
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao enviar {file.name}: {e}")
        if saved_paths:
            st.success("Todos os arquivos foram enviados com sucesso!")
            st.session_state['uploaded_paths'] = saved_paths

# Campo de pergunta
st.write("Agora, digite uma pergunta analítica:")
question = st.text_input("Ex: Qual o risco de inadimplência?")

# Envio da pergunta
if st.button("Enviar pergunta"):
    if not question:
        st.warning("Digite uma pergunta antes de enviar.")
    else:
        paths = st.session_state.get('uploaded_paths', [])
        if not paths:
            st.warning("Faça upload de arquivos antes de perguntar!")
        else:
            try:
                payload = {"question": question, "file_paths": paths}
                response = requests.post(BACKEND_ANALYZE_URL, json=payload, timeout=60)
                response.raise_for_status()
                result = response.json()

                st.success("✅ Resposta recebida com sucesso!")

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
                if isinstance(conf, (int, float)):
                    st.write(f"{conf*100:.1f}%")
                else:
                    st.write(conf or "—")

                if result.get("entidades"):
                    st.subheader("Entidades Extraídas")
                    st.write(result["entidades"])

                if result.get("limitacoes"):
                    st.subheader("Limitações")
                    st.warning(result["limitacoes"])

            except requests.exceptions.ConnectionError:
                st.error("❌ Falha de conexão com o backend.")
            except requests.exceptions.Timeout:
                st.error("⏱️ A requisição demorou demais (timeout).")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao conectar com o servidor: {e}")
