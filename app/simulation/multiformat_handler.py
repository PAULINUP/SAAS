# multiformat_handler.py
"""
Módulo de parsing inteligente e unificação de arquivos multiformato para o Q-Core AI.
Suporta: PDF, Excel, CSV, DOCX, JSON, TXT
"""

import pandas as pd
import json
import docx
import os
import mimetypes
from typing import List, Tuple, Dict

from pdfminer.high_level import extract_text as extract_text_pdf


def parse_pdf(file_path: str) -> str:
    return extract_text_pdf(file_path)


def parse_excel(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path)


def parse_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def parse_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])


def parse_json(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def classify_content(text: str) -> str:
    # Heurística simples por palavras-chave
    text_lower = text.lower()
    if "km" in text_lower and "placa" in text_lower:
        return "telemetria"
    if "diesel" in text_lower or "combust" in text_lower:
        return "combustível"
    if "fornecedor" in text_lower or "pagamento" in text_lower:
        return "financeiro"
    if "evento" in text_lower and "data" in text_lower:
        return "operacional"
    return "desconhecido"


def process_file(file_path: str) -> Dict:
    ext = os.path.splitext(file_path)[-1].lower()
    try:
        if ext in [".csv"]:
            df = parse_csv(file_path)
            tipo = classify_content(" ".join(df.columns))
            return {"tipo": tipo, "df": df, "fonte": file_path}
        elif ext in [".xlsx", ".xls"]:
            df = parse_excel(file_path)
            tipo = classify_content(" ".join(df.columns))
            return {"tipo": tipo, "df": df, "fonte": file_path}
        elif ext == ".json":
            data = parse_json(file_path)
            return {"tipo": "json", "conteudo": data, "fonte": file_path}
        elif ext == ".docx":
            text = parse_docx(file_path)
            tipo = classify_content(text)
            return {"tipo": tipo, "conteudo": text, "fonte": file_path}
        elif ext == ".pdf":
            text = parse_pdf(file_path)
            tipo = classify_content(text)
            return {"tipo": tipo, "conteudo": text, "fonte": file_path}
        elif ext == ".txt":
            text = parse_txt(file_path)
            tipo = classify_content(text)
            return {"tipo": tipo, "conteudo": text, "fonte": file_path}
        else:
            return {"tipo": "desconhecido", "erro": f"Extensão não suportada: {ext}"}
    except Exception as e:
        return {"tipo": "erro", "erro": str(e), "fonte": file_path}


def process_multiple_files(file_paths: List[str]) -> List[Dict]:
    return [process_file(fp) for fp in file_paths]
