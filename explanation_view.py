# explanation_view.py
"""
Módulo de Visualização Explicativa do Q-Core
Gera gráficos e insights visuais com base nos fatores que mais influenciaram a predição.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import base64
import io
from typing import Dict, List, Tuple

def plot_feature_importance(top_variables: List[Tuple[str, float]]) -> str:
    """
    Gera um gráfico de barras horizontal com as principais variáveis que influenciaram a predição.
    Retorna a imagem codificada em base64 (para exibir em interfaces).
    """
    df = pd.DataFrame(top_variables, columns=["Variável", "Impacto"])
    plt.figure(figsize=(8, 4))
    sns.barplot(data=df, y="Variável", x="Impacto", palette="viridis")
    plt.title("Principais Variáveis que Influenciaram a Predição")
    plt.xlabel("Importância Relativa")
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    plt.close()
    return image_base64

def render_explanation_section(prediction_output: Dict[str, any]) -> Dict[str, str]:
    """
    Gera as representações visuais para serem consumidas na interface (Streamlit ou Web).
    Retorna dict com base64 da imagem e explicação em texto.
    """
    image_base64 = plot_feature_importance(prediction_output.get("top_variables", []))
    return {
        "graph_base64": image_base64,
        "text_explanation": prediction_output.get("explanation", "Explicação indisponível.")
    }
