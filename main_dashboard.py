import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

from controllers.course_controller import load_dashboard

# Carregar as configurações do arquivo config.yaml
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Tela de login
name, authentication_status, username = authenticator.login('Login', cookie_name='main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.sidebar.write(f'Welcome *{name}*')

    # Iniciar o dashboard
    load_dashboard()
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
