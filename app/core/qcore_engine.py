from typing import List, Dict, Any

def process_question(question: str, file_paths: List[str]) -> Dict[str, Any]:
    # TODO: ler/parsear file_paths e gerar resultados reais
    return {
        "resumo_executivo": f"Pergunta: {question}. {len(file_paths)} arquivo(s) recebido(s).",
        "detalhe_tecnico": "Versão MVP: analisador stub.",
        "cenarios_alternativos": ["Cenário A", "Cenário B"],
        "recomendacoes": ["Ajustar limites", "Coletar mais dados"],
        "explicabilidade": "Baseado em regras demo.",
        "confianca": 0.82,
        "entidades": ["demo_entidade_1", "demo_entidade_2"],
        "limitacoes": "Modelo ainda não treinado com os dados do cliente."
    }
