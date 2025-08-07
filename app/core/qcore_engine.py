"""Núcleo preditivo: orquestra parsing, curadoria e simulação inteligente."""

from app.ingestion.parser import extract_text_from_pdf, extract_entities, classify_intent
from app.curator.curator import validate_entities
from app.simulation.predictor import simulate_risk


def process_question(question, arquivos_processados):
    # NLP: extrai intenção e contexto da pergunta
    intent, entities_from_question = classify_intent(question)

    all_text = []
    all_entities = []

    for item in arquivos_processados:
        if "df" in item:
            # Placeholder: extrair entidades de DataFrame (futuramente NLP + heurísticas)
            all_entities.extend(list(item['df'].columns))
        elif "conteudo" in item:
            text = item["conteudo"]
            all_text.append(text)
            ents = extract_entities(text)
            curated = validate_entities(ents)
            all_entities.extend(curated)

    all_entities.extend(entities_from_question)

    result = simulate_risk(all_entities, question, intent=intent)
    return result
