# parser_test.py
"""
Teste local do multiformat_handler para validação de parsing e classificação.
Coloque arquivos em ./test_data antes de rodar.
"""

import os
from app.simulation.multiformat_handler import process_multiple_files

TEST_DIR = "./test_data"

if __name__ == "__main__":
    print(f"🔍 Iniciando análise de arquivos em {TEST_DIR}\n")

    if not os.path.exists(TEST_DIR):
        print("❌ Diretório ./test_data não encontrado.")
        exit()

    arquivos = [os.path.join(TEST_DIR, f) for f in os.listdir(TEST_DIR) if os.path.isfile(os.path.join(TEST_DIR, f))]

    print(f"Encontrados {len(arquivos)} arquivo(s):")
    for a in arquivos:
        print(" -", a)

    print("\n⏳ Processando arquivos...")
    resultados = process_multiple_files(arquivos)

    for r in resultados:
        print("\n📄 Fonte:", r.get("fonte", "N/A"))
        print("🔎 Tipo detectado:", r.get("tipo", "indefinido"))
        if "df" in r:
            print("📊 DataFrame com colunas:", list(r["df"].columns))
            print(r["df"].head())
        elif "conteudo" in r:
            preview = r["conteudo"][:500].replace("\n", " ")
            print("📝 Texto extraído (preview):", preview)
        if "erro" in r:
            print("⚠️ Erro:", r["erro"])
