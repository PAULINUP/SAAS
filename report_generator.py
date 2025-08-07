
# report_generator.py
"""
Gera relatórios explicativos por arquivo processado pelo multiformat_handler.
Salvará em ./relatorios_gerados/
"""

import os
from app.simulation.multiformat_handler import process_multiple_files

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(BASE_DIR, "test_data")
OUTPUT_DIR = os.path.join(BASE_DIR, "relatorios_gerados")

os.makedirs(OUTPUT_DIR, exist_ok=True)

if __name__ == "__main__":
    arquivos = [os.path.join(TEST_DIR, f) for f in os.listdir(TEST_DIR) if os.path.isfile(os.path.join(TEST_DIR, f))]
    resultados = process_multiple_files(arquivos)

    for r in resultados:
        nome_base = os.path.basename(r.get("fonte", "arquivo_desconhecido"))
        nome_relatorio = os.path.join(OUTPUT_DIR, f"relatorio_{nome_base}.txt")

        with open(nome_relatorio, "w", encoding="utf-8") as f:
            f.write(f"🔍 Arquivo analisado: {nome_base}\n")
            f.write(f"Tipo detectado: {r.get('tipo', 'indefinido')}\n\n")

            if "df" in r:
                df = r["df"]
                f.write("📊 Colunas detectadas:\n")
                f.write(", ".join(df.columns) + "\n\n")
                f.write("🧪 Primeiras linhas:\n")
                f.write(df.head().to_string(index=False))
                f.write("\n")

            elif "conteudo" in r:
                texto = r["conteudo"][:1000].replace("\n", " ")
                f.write("📝 Preview do texto extraído:\n")
                f.write(texto + "...\n")

            if "erro" in r:
                f.write("⚠️ Erro encontrado:\n")
                f.write(r["erro"] + "\n")

        print(f"✅ Relatório salvo em: {nome_relatorio}")
