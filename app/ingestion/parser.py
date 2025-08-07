"""Parsing de documentos: OCR, NLP, extração de entidades e classificação de intenção."""

import spacy
from pdfminer.high_level import extract_text as pdfminer_extract_text

# Tenta carregar o modelo spaCy
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    print("🔄 Instalando modelo pt_core_news_sm...")
    import spacy.cli
    spacy.cli.download("pt_core_news_sm")
    nlp = spacy.load("pt_core_news_sm")

def extract_text_from_pdf(pdf_path):
    """Extrai texto real de PDF usando pdfminer.six."""
    try:
        text = pdfminer_extract_text(pdf_path)
        return text if text else ""
    except Exception as e:
        print(f"Erro ao extrair texto do PDF: {e}")
        return ""

def extract_entities(text):
    # Implementação simples usando spaCy
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def classify_intent(question):
    """
    Classifica a intenção da pergunta usando NLP (spaCy) e heurística.
    Retorna (intent, entidades extraídas).
    Pronto para expansão futura com LLM/API.
    """
    doc = nlp(question)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    # Intenções heurísticas (pode ser expandido para LLM)
    keywords = {
        "risco": ["risco", "score", "inadimplência", "perigo", "ameaça"],
        "economia": ["economia", "redução", "otimização", "save", "custo"],
        "fluxo_caixa": ["fluxo de caixa", "cash flow", "saldo", "previsão de caixa"],
        "inadimplencia": ["inadimplência", "pagamento atrasado", "default", "dívida"],
        "demanda": ["demanda", "forecast", "consumo projetado", "pedido", "quantidade"],
        "estoque": ["estoque", "mínimo", "máximo", "reposição", "ruptura"],
        "frete": ["frete", "custo logístico", "roteirização", "transporte", "tarifa", "rota"],
        "explicacao": ["por quê", "explique", "detalhe", "justifique", "como funciona"],
        "outros": []
    }
    question_lower = question.lower()
    intent = "outros"
    for k, v in keywords.items():
        if any(word in question_lower for word in v):
            intent = k
            break
    # Se não encontrou, tenta classificar pelo tipo de entidade dominante
    if intent == "outros" and entities:
        labels = [label for _, label in entities]
        if "ORG" in labels or "LOC" in labels:
            intent = "frete"
        elif "PER" in labels:
            intent = "risco"
    return intent, entities
