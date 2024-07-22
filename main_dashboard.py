# main_dashboard.py

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from config.log_config import log
from controllers.course_controller import load_dashboard

# Configurar a largura do layout
st.set_page_config(layout="wide")

# Ocultar cabeçalho
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 {
                padding: 1rem 1rem 5rem 1rem !important;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Carregar as configurações do arquivo config.yaml
log.info("Loading configuration from config.yaml")
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

log.info("Initializing authenticator")
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Tela de login
log.info("Displaying login screen")
name, authentication_status, username = authenticator.login('main')
log.info("Authentication status: %s", authentication_status)

if authentication_status:
    log.info("User %s authenticated successfully", name)
    authenticator.logout('Logout', 'main')
    st.sidebar.write(f'Welcome *{name}*')
    load_dashboard()
elif authentication_status == False:
    log.error('Username/password is incorrect')
    st.error('Username/password is incorrect')
elif authentication_status == None:
    log.warning('Please enter your username and password')
    st.warning('Please enter your username and password')
