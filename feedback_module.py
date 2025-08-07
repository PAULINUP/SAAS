# feedback_module.py
"""
Módulo de Feedback Inteligente do Q-Core
Permite que o usuário avalie a predição recebida, corrija resultados e retroalimente o sistema para aprendizado futuro.
"""
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

FEEDBACK_DIR = "app/feedback_logs"

if not os.path.exists(FEEDBACK_DIR):
    os.makedirs(FEEDBACK_DIR)

def save_feedback(session_id: str, prediction_output: Dict[str, Any], user_feedback: Dict[str, Any]) -> str:
    """
    Salva o feedback fornecido pelo usuário junto com o resultado original da predição.
    """
    timestamp = datetime.utcnow().isoformat()
    record = {
        "session_id": session_id,
        "timestamp": timestamp,
        "prediction_output": prediction_output,
        "user_feedback": user_feedback
    }
    filename = f"{FEEDBACK_DIR}/feedback_{session_id}_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(record, f, indent=2)
    return filename

def load_feedback_history(session_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Carrega todos os feedbacks ou apenas os de uma sessão específica.
    """
    logs = {}
    for file in os.listdir(FEEDBACK_DIR):
        if file.endswith(".json") and (not session_id or session_id in file):
            with open(os.path.join(FEEDBACK_DIR, file), "r") as f:
                logs[file] = json.load(f)
    return logs

def apply_manual_correction(original_output: Dict[str, Any], correction: Dict[str, Any]) -> Dict[str, Any]:
    """
    Aplica uma correção manual ao resultado original.
    Exemplo: {'prediction': 0.67} → novo valor fornecido pelo usuário.
    """
    corrected_output = original_output.copy()
    for key, value in correction.items():
        corrected_output[key] = value
    corrected_output["explanation"] += " [Correção manual aplicada pelo usuário.]"
    return corrected_output
