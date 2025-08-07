import os
from app.simulation.multiformat_handler import process_multiple_files

def process_directories(dir_paths):
    all_results = []
    for dir_path in dir_paths:
        if not os.path.isdir(dir_path):
            all_results.append({
                "fonte": dir_path,
                "erro": "Caminho inválido ou diretório não encontrado."
            })
            continue

        arquivos = [
            os.path.join(dir_path, f)
            for f in os.listdir(dir_path)
            if os.path.isfile(os.path.join(dir_path, f))
        ]
        resultados = process_multiple_files(arquivos)
        all_results.extend(resultados)
    return all_results