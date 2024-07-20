# config/settings.py


import os

from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


class Settings:
    # Configurações básicas do ambiente
    AMBIENTE = os.getenv('AMBIENTE', 'DEV')
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'True') == 'True'
    APP_PORT = int(os.getenv('APP_PORT', '5010'))

    # Configurações gerais
    DATA_PATH = os.getenv('DATA_PATH', 'data/cursos_combined_matched.xlsx')

    # Configurações da API OpenAI
    # Carregando a chave da API de uma variável de ambiente por segurança
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_API_KEY_4 = os.getenv('OPENAI_API_KEY_4')

    MODEL_GPT35 = "gpt-3.5-turbo"
    MODEL_GPT4 = "gpt-4-turbo"
    MODEL_GPT4o = "gpt-4o"

    # Caminho do log
    LOG_PATH = os.getenv('LOG_PATH', 'main.log')
