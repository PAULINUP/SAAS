# demo_runner.py
"""
Demonstração completa do sistema Q-Core com pipeline unificado:
- Upload e treinamento
- Predição explicada
- Simulação de cenários
- Análise quântica simbólica
- Geração de relatório final
"""

import pandas as pd
from qcore_intelligent_engine import QCoreEngine
from explanation_view import render_explanation_section
from feedback_module import save_feedback
from quantum_bridge import QuantumBridge
from presentation_mode import ReportGenerator

# Etapa 1: Dados simulados (poderia ser carregado via CSV)
df = pd.DataFrame({
    "diesel": [110.0],
    "volume": [4900],
    "cliente_tipo": [1],
    "risco": [0.58]
})

# Etapa 2: Treinamento
engine = QCoreEngine()
engine.fit(df, target="risco")

# Etapa 3: Predição explicada
pred_input = df.drop(columns=["risco"])
pred_output = engine.predict(pred_input)
visuals = render_explanation_section(pred_output)

# Etapa 4: Simulação de cenário
sim_output = engine.simulate_what_if({"diesel": 10, "volume": -5})

# Etapa 5: Análise quântica
quantum = QuantumBridge()
quantum_output = quantum.analyze(pred_input.iloc[0].to_dict())

# Etapa 6: Gerar relatório final
report = ReportGenerator()
report_file = report.generate(
    prediction=pred_output,
    simulation=sim_output,
    quantum=quantum_output,
    graph_base64=visuals["graph_base64"]
)

print(f"Relatório gerado: {report_file}")
