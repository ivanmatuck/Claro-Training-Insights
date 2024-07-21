# main_dashboard.py

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from config.log_config import log
from controllers.course_controller import load_dashboard

# Configurar a largura do layout
st.set_page_config(layout="wide")

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
# Tela de login
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
