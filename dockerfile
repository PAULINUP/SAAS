# Dockerfile - Q-Core AI System

FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto
COPY . /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala as dependências Python
RUN pip install --upgrade pip
RUN pip install .

# Expõe a porta padrão da API
EXPOSE 8000

# Comando padrão de inicialização da API
CMD ["uvicorn", "api_gateway:app", "--host", "0.0.0.0", "--port", "8080"]
