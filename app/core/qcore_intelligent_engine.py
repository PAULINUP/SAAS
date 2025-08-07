"""
🧠 QCoreEngine - Núcleo de Predição Explicável, Simulação de Cenários e Análise de Variáveis Ocultas.

Compatível com expansão para modelos quânticos ou ML futuramente.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.inspection import permutation_importance
from sklearn.decomposition import PCA
from scipy.stats import zscore
import logging
import json
import matplotlib.pyplot as plt
import io
import base64

class QCoreEngine:
    def __init__(self, log_enabled: bool = True, n_estimators: int = 100, random_state: int = 42):
        self.model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
        self.is_fitted = False
        self.columns = []
        self.feature_importances_ = None
        self.base_prediction_ = None
        self.confidence_interval_ = None
        self.input_data_ = None
        self.log_enabled = log_enabled
        self.logs = []
        if self.log_enabled:
            logging.basicConfig(level=logging.INFO)

    def _log(self, msg: str):
        if self.log_enabled:
            self.logs.append(msg)
            logging.info(msg)

    def fit(self, df: pd.DataFrame, target: str):
        X = df.drop(columns=[target])
        y = df[target]
        self.model.fit(X, y)
        self.is_fitted = True
        self.columns = X.columns.tolist()
        self.input_data_ = df.copy()
        self.base_prediction_ = self.model.predict(X)
        self.confidence_interval_ = self._calc_confidence_interval(self.base_prediction_)
        self.feature_importances_ = self.model.feature_importances_
        self._log(f"Model trained. Features: {self.columns}")

    def _calc_confidence_interval(self, preds: np.ndarray, alpha=0.05):
        mean_pred = np.mean(preds)
        std_pred = np.std(preds)
        n = preds.shape[0]
        ci = 1.96 * std_pred / np.sqrt(n)
        return (mean_pred - ci, mean_pred + ci)

    def predict(self, input_data: pd.DataFrame) -> Dict[str, Any]:
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before prediction.")
        preds = self.model.predict(input_data)
        mean_pred = np.mean(preds)
        ci = self._calc_confidence_interval(preds)
        importances = permutation_importance(self.model, input_data, preds, n_repeats=10, random_state=42)
        importances_dict = dict(zip(self.columns, importances.importances_mean))
        top_vars = sorted(importances_dict.items(), key=lambda x: abs(x[1]), reverse=True)[:5]

        explanation = (
            f"Predição baseada em RandomForestRegressor. Principais variáveis: "
            f"{', '.join([f'{var} (impacto: {imp:.3f})' for var, imp in top_vars])}. "
            f"Intervalo de confiança calculado com 95% de certeza estatística."
        )

        output = {
            "prediction": mean_pred,
            "confidence_interval": ci,
            "top_variables": top_vars,
            "explanation": explanation,
            "raw_predictions": preds.tolist()
        }
        self._log(f"Prediction performed. Output: {json.dumps(output, default=str)}")
        return output

    def simulate_what_if(self, variations: Dict[str, float]) -> Dict[str, Any]:
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before simulation.")
        X = self.input_data_.drop(columns=[self.input_data_.columns[-1]]).copy()
        base_preds = self.model.predict(X)
        X_sim = X.copy()

        # Apply variations
        for col, delta in variations.items():
            if col in X_sim.columns:
                if np.issubdtype(X_sim[col].dtype, np.number):
                    X_sim[col] = X_sim[col] * (1 + delta/100)
                else:
                    # For categorical, could implement custom logic
                    continue

        sim_preds = self.model.predict(X_sim)
        mean_base = np.mean(base_preds)
        mean_sim = np.mean(sim_preds)
        impact = mean_sim - mean_base

        # Gera gráfico de comparação (base64)
        fig, ax = plt.subplots()
        ax.hist(base_preds, alpha=0.5, label="Base")
        ax.hist(sim_preds, alpha=0.5, label="Simulação")
        ax.legend()
        ax.set_title("Comparação de Predições (Base vs Simulação)")
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode("utf-8")

        output = {
            "mean_base_prediction": mean_base,
            "mean_simulated_prediction": mean_sim,
            "impact": impact,
            "comparison_chart_base64": image_base64,
            "explanation": f"Simulação realizada com variações: {variations}. Impacto médio: {impact:.2f}."
        }
        self._log(f"Simulation performed. Output: {json.dumps(output, default=str)}")
        return output

    def infer_hidden_variables(self) -> Dict[str, Any]:
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before analysis.")

        X = self.input_data_.drop(columns=[self.input_data_.columns[-1]]).copy()
        # Outlier detection (Z-score)
        z_scores = np.abs(zscore(X.select_dtypes(include=[np.number])))
        outlier_mask = (z_scores > 3)
        outliers = {}
        for idx, col in enumerate(X.select_dtypes(include=[np.number]).columns):
            outlier_rows = X[outlier_mask[:, idx]]
            if not outlier_rows.empty:
                outliers[col] = outlier_rows.index.tolist()

        # PCA for hidden correlations
        pca = PCA(n_components=min(3, X.shape[1]))
        pca.fit(X.select_dtypes(include=[np.number]))
        explained = pca.explained_variance_ratio_
        suggestion = ""
        if np.max(explained) > 0.7:
            suggestion = (
                f"Variável '{X.select_dtypes(include=[np.number]).columns[np.argmax(explained)]}' domina o padrão dos dados. "
                "Pode haver fator externo ou variável oculta correlacionada."
            )

        # Correlation analysis
        corr_matrix = X.corr()
        hidden_corrs = []
        for col in corr_matrix.columns:
            for row in corr_matrix.index:
                val = corr_matrix.loc[row, col]
                if 0.5 < abs(val) < 1 and row != col:
                    hidden_corrs.append((row, col, val))

        output = {
            "outliers": outliers,
            "hidden_correlations": hidden_corrs,
            "suggestion": suggestion,
            "explanation": (
                "Foram detectados possíveis outliers e correlações não óbvias. "
                "Análise PCA sugere variáveis explicativas ocultas."
            )
        }
        self._log(f"Hidden variable inference performed. Output: {json.dumps(output, default=str)}")
        return output

    def export_logs(self) -> List[str]:
        return self.logs

    def export_results(self, filename: str = "qcore_results.json"):
        with open(filename, "w") as f:
            json.dump(self.logs, f, indent=2)
        self._log(f"Results exported to {filename}")

# Exemplo de uso:
if __name__ == "__main__":
    # Mock dataframe
    df = pd.DataFrame({
        "diesel": np.random.normal(100, 10, 100),
        "volume": np.random.normal(5000, 500, 100),
        "cliente_tipo": np.random.choice([0, 1], 100),
        "risco": np.random.normal(0.5, 0.1, 100)
    })
    engine = QCoreEngine()
    engine.fit(df, target="risco")
    print(engine.predict(df.drop(columns=["risco"])))
    print(engine.simulate_what_if({"diesel": 10, "volume": -5}))
    print(engine.infer_hidden_variables())
