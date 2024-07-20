import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler
import sys
from config.settings import Settings

# Inicializa os detalhes do arquivo de log
nomeArquivoCompleto = sys.argv[0]
fileNamePython = nomeArquivoCompleto.split('\\')[-1]
try:
    index = fileNamePython.index('.')
except ValueError:
    index = -1
nomeArquivo = fileNamePython[:index]

# Configura o log
logging.getLogger('').setLevel(logging.NOTSET)

# Handler para o arquivo
rotatingHandler = ConcurrentRotatingFileHandler(
    filename=nomeArquivo + '.log',
    mode='a',
    maxBytes=10 * 1024 * 1024,
    backupCount=10,
    encoding='utf8'  # Especifica a codificação como UTF-8
)

# Handler para stdout
streamHandler = logging.StreamHandler(sys.stdout)

# Define o nível de log com base no ambiente
if Settings.AMBIENTE == 'DEV':
    rotatingHandler.setLevel(logging.DEBUG)
    streamHandler.setLevel(logging.DEBUG)  # Mais detalhes para ambiente de desenvolvimento
else:
    rotatingHandler.setLevel(logging.INFO)
    streamHandler.setLevel(logging.INFO)  # Menos detalhes para outros ambientes

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotatingHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

logging.getLogger('').addHandler(rotatingHandler)
logging.getLogger('').addHandler(streamHandler)

# Define o logger aqui para ser usado em todo o aplicativo
log = logging.getLogger()

log.info("Logging setup complete")
