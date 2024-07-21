from config.settings import Settings
from config.log_config import log
from dotenv import load_dotenv
import subprocess

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar logging
log.info("Starting the Streamlit server for ClaroTraining Insights...")


def main():
    try:
        # Configurar e iniciar o Streamlit na porta definida em Settings
        streamlit_command = f"streamlit run main_dashboard.py --server.port={Settings.APP_PORT}"
        subprocess.run(streamlit_command, shell=True, check=True)
    except Exception as e:
        log.error("Error starting the Streamlit server: %s", str(e), exc_info=True)


if __name__ == '__main__':
    log.info("Starting the Streamlit server for ClaroTraining Insights...")
    main()
