# Usa uma imagem base oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY . /app

# Instala dependências do sistema necessárias pro mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libmariadb-dev \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Instala dependências do Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Coleta os arquivos estáticos
RUN python manage.py collectstatic --noinput

# Expõe a porta padrão do Django
EXPOSE 8000

# Comando para rodar o servidor com gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8080"]
