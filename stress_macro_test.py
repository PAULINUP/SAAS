import os
import tempfile
import shutil
import random
import string
from app.simulation.macro_handler import process_directories

def criar_arquivo_aleatorio(caminho, extensao):
    with open(f"{caminho}.{extensao}", "w", encoding="utf-8") as f:
        f.write("Simulação de conteúdo caótico\n" + "".join(random.choices(string.ascii_letters + string.digits, k=10000)))

def gerar_diretorios_com_arquivos(n=3, arquivos_por_dir=30):
    pastas = []
    for i in range(n):
        pasta = tempfile.mkdtemp(prefix=f"empresa_dir_{i}_")
        pastas.append(pasta)
        for _ in range(arquivos_por_dir):
            ext = random.choice(["pdf", "csv", "xlsx", "json", "docx", "txt"])
            criar_arquivo_aleatorio(os.path.join(pasta, f"arquivo_{random.randint(1000, 9999)}"), ext)
    return pastas

# Gerar diretórios simulados
print("🧪 Gerando diretórios simulados para stress test...")
diretorios = gerar_diretorios_com_arquivos(n=3, arquivos_por_dir=30)

# Processar
print("🚀 Iniciando macro análise simulada...")
resultados = process_directories(diretorios)

# Exibir resultados resumidos
print(f"🔍 Total de arquivos processados: {len(resultados)}")
for r in resultados[:5]:  # Mostrar só os 5 primeiros
    print(f"📁 Fonte: {r.get('fonte')}, Tipo: {r.get('tipo', 'Indefinido')}")

# Limpeza
for pasta in diretorios:
    shutil.rmtree(pasta)