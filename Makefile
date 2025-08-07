run-backend:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-streamlit:
	streamlit run web/streamlit_app.py

test:
	pytest tests/
