import subprocess
from config.log_config import log

# Configurar logging
log.info("Starting the Streamlit server for ClaroTraining Insights...")


def main():
    try:
        # Configurar e iniciar o Streamlit
        streamlit_command = "streamlit run main_dashboard.py"
        subprocess.run(streamlit_command, shell=True, check=True)
    except Exception as e:
        log.error("Error starting the Streamlit server: %s", str(e), exc_info=True)


if __name__ == '__main__':
    log.info("Starting the Streamlit server for ClaroTraining Insights...")
    main()
