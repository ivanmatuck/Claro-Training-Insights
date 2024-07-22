# Use a imagem base oficial do Python leve.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Permitir que declarações e mensagens de log apareçam imediatamente nos logs do Cloud Run
ENV PYTHONUNBUFFERED True

# Definir variáveis de ambiente para o Streamlit
ENV STREAMLIT_SERVER_HEADLESS True
ENV STREAMLIT_SERVER_PORT 8080
ENV STREAMLIT_SERVER_ADDRESS 0.0.0.0

# Copiar o código local para a imagem do contêiner.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Instalar dependências de produção.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Configure a execução do Streamlit para escutar em 0.0.0.0
CMD ["streamlit", "run", "main_dashboard.py", "--server.port=8080", "--server.address=0.0.0.0"]
