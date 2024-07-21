# services/course_service.py

import pandas as pd
from config.log_config import log


# Função para carregar dados das novas planilhas
def load_data():
    try:
        df_frequencia = pd.read_excel('data/FINAL_FREQUENCIA_CURSOS_FORAM_MENCIONADOS.xlsx', engine='openpyxl')
        df_skills = pd.read_excel('data/FINAL_SKILLS_POR_DIRETORIA.xlsx', engine='openpyxl')
        log.info("Data loaded successfully from the provided files")
        log.info("Columns in Frequencia DataFrame: %s", df_frequencia.columns.tolist())
        log.info("Columns in Skills DataFrame: %s", df_skills.columns.tolist())
        log.info("Data in Skills DataFrame:\n%s", df_skills.head().to_string())
        return df_frequencia, df_skills
    except Exception as e:
        log.error("Error loading data: %s", str(e), exc_info=True)
        return pd.DataFrame(), pd.DataFrame()  # Retorna DataFrames vazios em caso de erro


# Função para calcular métricas gerais
def get_general_metrics(df_skills):
    try:
        total_courses = df_skills['Skill'].nunique()
        total_hard_skills = df_skills[df_skills['Tipo'] == 'HardSkill'].shape[0]
        total_soft_skills = df_skills[df_skills['Tipo'] == 'SoftSkill'].shape[0]
        log.info("General metrics calculated successfully")
        return total_courses, total_hard_skills, total_soft_skills
    except KeyError as e:
        log.error("Error calculating general metrics: %s", str(e), exc_info=True)
        return 0, 0, 0  # Retorna zeros em caso de erro


# Função para obter os principais cursos
def get_top_courses(df_skills):
    try:
        top_hard_skill_courses = df_skills[df_skills['Tipo'] == 'HardSkill'].head(5).reset_index(drop=True)
        top_soft_skill_courses = df_skills[df_skills['Tipo'] == 'SoftSkill'].head(5).reset_index(drop=True)
        log.info("Top courses calculated successfully")
        return top_hard_skill_courses, top_soft_skill_courses
    except KeyError as e:
        log.error("Error calculating top courses: %s", str(e), exc_info=True)
        return pd.DataFrame(), pd.DataFrame()  # Retorna DataFrames vazios em caso de erro



