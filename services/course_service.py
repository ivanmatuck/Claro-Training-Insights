# services/course_service.py

import pandas as pd
from config.log_config import log


# Função para carregar dados do novo arquivo
def load_data():
    try:
        df = pd.read_excel('data/FINAL_SKILLS_POR_DIRETORIA.xlsx', engine='openpyxl')
        log.info("Data loaded successfully from FINAL_SKILLS_POR_DIRETORIA.xlsx")
        log.info("Columns in DataFrame: %s", df.columns.tolist())
        log.info("Data in DataFrame:\n%s", df.head().to_string())
        return df
    except Exception as e:
        log.error("Error loading data: %s", str(e), exc_info=True)
        return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro


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
