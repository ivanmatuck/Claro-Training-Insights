import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Configurar o manipulador de arquivo
handler = logging.FileHandler('app.log')
handler.setLevel(logging.INFO)

# Formatação do log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Adicionar o manipulador ao logger
log.addHandler(handler)
