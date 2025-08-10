# web/utils/status.py
import os
import requests
import streamlit as st

@st.cache_data(ttl=60)  # evita pingar o backend a cada rerun; revalida a cada 60s
def _ping(url: str) -> bool:
    try:
        r = requests.get(url, timeout=5)
        return r.ok
    except Exception:
        return False

def backend_guard(base_url: str | None = None, stop_on_fail: bool = True) -> bool:
    """
    Mostra um badge fixo com o estado do backend e, se quiser, para a página
    quando o backend estiver offline (stop_on_fail=True).
    Retorna True/False para quem quiser usar programaticamente.
    """
    # base_url pode vir das Secrets/ENV
    base_url = base_url or os.getenv("BACKEND_BASE_URL", "")
    if not base_url:
        st.warning("BACKEND_BASE_URL ausente nas Secrets/ENV.")
        if stop_on_fail:
            st.stop()
        return False

    # endpoint de saúde
    health = base_url.rstrip("/")  # pode ser "/" ou "/health"
    if health.endswith("/api") or health.endswith("/api/"):
        health = health[:-4]  # corta "/api" se vier

    # tenta /health; se não existir, tenta /
    ok = _ping(f"{health}/health") or _ping(health)

    # badge único e silencioso (sem “help” gigante)
    holder = st.empty()
    if ok:
        holder.success("Backend online ✅")
    else:
        holder.warning("Backend offline ⚠️")
        if stop_on_fail:
            st.stop()

    return ok
