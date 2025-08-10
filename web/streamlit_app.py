if uploaded_files:
    st.info(f"{len(uploaded_files)} arquivo(s) selecionado(s).")
    if st.button("Enviar arquivos para processamento"):
        saved_paths = []
        for file in uploaded_files:
            try:
                files = {
                    "file": (file.name, file.getbuffer(), file.type or "application/octet-stream")
                }
                r = requests.post(BACKEND_UPLOAD_URL, files=files, timeout=60)
                r.raise_for_status()
                saved_paths.append(r.json().get("file_path"))
            except requests.exceptions.HTTPError as e:
                st.error(f"Erro ao enviar {file.name}: {e} | {r.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao enviar {file.name}: {e}")
        if saved_paths:
            st.success("Arquivos enviados!")
            st.session_state["uploaded_paths"] = saved_paths
