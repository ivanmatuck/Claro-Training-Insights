import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Configurar o manipulador de arquivo
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)

# Configurar o manipulador de saída para o console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatação do log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Adicionar os manipuladores ao logger
log.addHandler(file_handler)
log.addHandler(console_handler)
