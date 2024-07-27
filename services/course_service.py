import os
import pandas as pd
from config.log_config import log
import streamlit as st
from datetime import datetime


# Função para verificar e salvar o arquivo carregado
def save_uploaded_file(uploaded_file):
    timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    new_filename = f"FINAL_SKILLS_POR_DIRETORIA_{timestamp}.xlsx"
    with open(os.path.join("data", new_filename), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Arquivo {new_filename} carregado com sucesso!")
    manage_files()


# Função para carregar dados do arquivo selecionado
def load_data(selected_file):
    try:
        quantitativos_df = pd.read_excel(os.path.join('data', selected_file), sheet_name='quantitativos', engine='openpyxl')
        qualitativos_df = pd.read_excel(os.path.join('data', selected_file), sheet_name='qualitativos', engine='openpyxl')
        log.info("Data loaded successfully from %s", selected_file)
        log.info("Quantitativos columns: %s", quantitativos_df.columns.tolist())
        log.info("Qualitativos columns: %s", qualitativos_df.columns.tolist())
        return quantitativos_df, qualitativos_df
    except Exception as e:
        log.error("Error loading data: %s", str(e), exc_info=True)
        return pd.DataFrame(), pd.DataFrame()  # Retorna DataFrame vazio em caso de erro


# Função para validar se o arquivo possui as colunas necessárias
def validate_columns(df, required_columns):
    return all(column in df.columns for column in required_columns)


# Função para listar todos os arquivos XLSX na pasta 'data'
def list_xlsx_files():
    return [f for f in os.listdir("data") if f.endswith(".xlsx")]


# Função para obter o arquivo mais recente
def get_latest_file():
    files = list_xlsx_files()
    if not files:
        return None
    latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join("data", x)))
    return latest_file


# Função para gerenciar arquivos e manter apenas os três mais recentes
def manage_files():
    files = list_xlsx_files()
    if len(files) > 3:
        files.sort(key=lambda x: os.path.getmtime(os.path.join("data", x)))
        for file in files[:-3]:
            os.remove(os.path.join("data", file))
            log.info("Deleted old file: %s", file)


# Função para calcular métricas gerais
def get_general_metrics(df):
    try:
        total_courses = df['cursos'].nunique()
        total_hard_skills = df[df['tipo'] == 'HardSkill'].shape[0]
        total_soft_skills = df[df['tipo'] == 'SoftSkill'].shape[0]
        log.info("General metrics calculated successfully")
        return total_courses, total_hard_skills, total_soft_skills
    except KeyError as e:
        log.error("Error calculating general metrics: %s", str(e), exc_info=True)
        return 0, 0, 0  # Retorna zeros em caso de erro


# Exibição da tabela de dados qualitativos com quebras de linha mantidas
def display_qualitative_data(df):
    st.subheader('Dados Qualitativos')
    styled_df = df.reset_index(drop=True).style.set_table_styles(
        [
            {'selector': 'td', 'props': [('vertical-align', 'top')]},
            {'selector': 'th', 'props': [('vertical-align', 'top')]}
        ]
    ).hide(axis="index").to_html(escape=False).replace("\\n", "<br>")
    st.markdown(
        f"<div style='text-align: left; vertical-align: top; '>{styled_df}</div>",
        unsafe_allow_html=True
    )
    log.info("Dataframe for qualitative data displayed")



