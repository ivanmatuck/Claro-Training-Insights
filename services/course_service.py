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
        df = pd.read_excel(os.path.join('data', selected_file), engine='openpyxl')
        log.info("Data loaded successfully from %s", selected_file)
        log.info("Columns in DataFrame: %s", df.columns.tolist())
        log.info("Data in DataFrame:\n%s", df.head().to_string())
        return df
    except Exception as e:
        log.error("Error loading data: %s", str(e), exc_info=True)
        return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro


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


# Função para obter os principais cursos
def get_top_courses(df):
    try:
        top_hard_skill_courses = df[df['tipo'] == 'HardSkill'].head(5).reset_index(drop=True)
        top_soft_skill_courses = df[df['tipo'] == 'SoftSkill'].head(5).reset_index(drop=True)
        log.info("Top courses calculated successfully")
        return top_hard_skill_courses, top_soft_skill_courses
    except KeyError as e:
        log.error("Error calculating top courses: %s", str(e), exc_info=True)
        return pd.DataFrame(), pd.DataFrame()  # Retorna DataFrames vazios em caso de erro
