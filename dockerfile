vFROM python:3.12-slim

# Instala o distutils antes de instalar as dependências
RUN apt-get update && apt-get install -y python3-distutils\
        gcc \
        g++ \
        build-essential \
        libpoppler-cpp-dev \
        pkg-config \
        python3-dev \
        libtesseract-dev \
        tesseract-ocr \
        poppler-utils \
        libmagic-dev \
        libjpeg-dev \
        zlib1g-dev \
        libpq-dev \
        libxml2-dev \
        libxslt1-dev \
        libffi-dev \
        libssl-dev \
        git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos
COPY . .

# Instala as dependências do Python
RUN pip install --upgrade pip
RUN pip install --use-pep517 -r requirements.txt

# Expõe a porta do FastAPI
EXPOSE 8080

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
