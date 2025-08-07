# presentation_mode.py
"""
Gera relatórios executivos e automáticos com os resultados do Q-Core (predição, simulação, análise quântica).
Formato final: PDF com gráfico, resultado e explicação detalhada para decisão estratégica.
"""

from fpdf import FPDF
import base64
import io
from typing import Dict

class ReportGenerator:
    def __init__(self, title="Relatório Inteligente Q-Core"):
        self.title = title

    def generate(self, prediction: Dict, simulation: Dict, quantum: Dict, graph_base64: str, filename="relatorio_qcore.pdf") -> str:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, self.title, ln=True, align='C')
        pdf.set_font("Arial", size=12)

        pdf.ln(10)
        pdf.multi_cell(0, 10, f"Resultado da Predição:\n{prediction.get('explanation', '')}")
        pdf.ln(5)
        pdf.multi_cell(0, 10, f"Intervalo de Confiança: {prediction.get('confidence_interval', '')}")

        pdf.ln(5)
        pdf.multi_cell(0, 10, f"Simulação de Cenário:\n{simulation.get('explanation', '')}")
        pdf.ln(5)
        pdf.multi_cell(0, 10, f"Impacto Simulado: {simulation.get('impact', ''):.2f}")

        pdf.ln(5)
        pdf.multi_cell(0, 10, f"Análise Quântica:\n{quantum.get('apex_analysis', {}).get('interpretation', '')}")

        if graph_base64:
            image_data = base64.b64decode(graph_base64)
            with open("temp_plot.png", "wb") as img_file:
                img_file.write(image_data)
            pdf.ln(10)
            pdf.image("temp_plot.png", w=150)

        pdf.output(filename)
        return filename
