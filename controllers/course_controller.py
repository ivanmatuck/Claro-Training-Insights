# controllers/course_controller.py

import plotly.express as px
import streamlit as st

from config.log_config import log
from services.course_service import load_data, get_general_metrics, get_top_courses


# Função para carregar o dashboard
def load_dashboard():
    try:
        # Carregar os dados
        df_frequencia, df_skills = load_data()

        # Configurar a largura do layout
        st.set_page_config(layout="wide")

        # Título do dashboard
        st.title('ClaroTraining Insights')

        # Barra lateral para filtros
        st.sidebar.image('img/png-transparent-claro-hd-logo.png', use_column_width=True)
        st.sidebar.header('Filtros')
        diretoria_filter = st.sidebar.selectbox('Selecione a Diretoria',
                                                ['Todas'] + df_skills['Diretoria'].unique().tolist())
        skill_filter = st.sidebar.radio('Selecione o Tipo de Habilidade', ['Todas', 'HardSkill', 'SoftSkill'])
        display_option = st.sidebar.radio('Opções de Exibição', ['Ambos', 'Tabelas', 'Gráficos'], index=0)

        log.info("Filtro selecionado - Diretoria: %s, Tipo de Habilidade: %s", diretoria_filter, skill_filter)

        # Filtrar dados de acordo com as seleções
        if diretoria_filter != 'Todas':
            df_skills = df_skills[df_skills['Diretoria'] == diretoria_filter]
            log.info("Dados filtrados por Diretoria (%s):\n%s", diretoria_filter, df_skills.head().to_string())

        if skill_filter != 'Todas':
            df_skills = df_skills[df_skills['Tipo'] == skill_filter]
            log.info("Dados filtrados por Tipo (%s):\n%s", skill_filter, df_skills.head().to_string())

        # Gráfico treemap: Nível de urgência dos cursos (frequência de menção)
        st.subheader('Nível de Urgência dos Cursos')
        if diretoria_filter == 'Todas':
            treemap_data = df_frequencia
        else:
            treemap_data = df_frequencia[df_frequencia['Diretoria'] == diretoria_filter]

        if not treemap_data.empty:
            fig2 = px.treemap(treemap_data, path=['Diretoria', 'Curso'], values='Frequência que foram mencionados',
                              color='Frequência que foram mencionados', color_continuous_scale='RdYlGn_r')
            fig2.update_traces(hovertemplate='<b>Diretoria:</b> %{customdata[0]}<br>' +
                                               '<b>Curso:</b> %{label}<br>' +
                                               '<b>Frequência:</b> %{value}')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.write("Nenhum curso encontrado com frequência maior que 0 para a diretoria selecionada.")

        if display_option in ['Tabelas', 'Ambos']:
            # Exibir a tabela de dados e métricas gerais lado a lado
            st.subheader('Dados dos Cursos e Métricas Gerais')
            col1, col2 = st.columns([1, 3])

            with col1:
                # Métricas gerais
                total_courses, total_hard_skills, total_soft_skills = get_general_metrics(df_skills)
                st.metric(label="Total de Cursos", value=total_courses)
                st.metric(label="Total de Hard Skills", value=total_hard_skills)
                st.metric(label="Total de Soft Skills", value=total_soft_skills)

            with col2:
                # Dados dos Cursos
                st.dataframe(df_skills, use_container_width=True)

        if display_option in ['Gráficos', 'Ambos']:
            # Gráfico de barras: Distribuição de Cursos por Diretoria
            if diretoria_filter == 'Todas':
                director_data = df_skills.groupby('Diretoria').size().reset_index(name='Quantidade')
                fig1 = px.bar(director_data, x='Diretoria', y='Quantidade',
                              title='Distribuição de Cursos por Diretoria',
                              color_discrete_sequence=['#ED1C24'])
                st.plotly_chart(fig1, use_container_width=True)

            # Gráfico de barras: Proporção de Hard Skills e Soft Skills
            log.info("Dados para gráfico de Proporção de Hard Skills:\n%s", df_skills[df_skills['Tipo'] == 'HardSkill'].to_string())
            log.info("Dados para gráfico de Proporção de Soft Skills:\n%s", df_skills[df_skills['Tipo'] == 'SoftSkill'].to_string())
            if skill_filter == 'Todas' or skill_filter == 'HardSkill':
                hard_skills_count = df_skills[df_skills['Tipo'] == 'HardSkill']['Skill'].value_counts().reset_index()
                hard_skills_count.columns = ['Skill', 'Quantidade']
                fig3 = px.bar(hard_skills_count, x='Skill', y='Quantidade',
                              title='Proporção de Hard Skills', labels={'Quantidade': 'Quantidade', 'Skill': 'Hard Skills'},
                              color_discrete_sequence=['#ED1C24'])
                fig3.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig3, use_container_width=True)

            if skill_filter == 'Todas' or skill_filter == 'SoftSkill':
                soft_skills_count = df_skills[df_skills['Tipo'] == 'SoftSkill']['Skill'].value_counts().reset_index()
                soft_skills_count.columns = ['Skill', 'Quantidade']
                fig4 = px.bar(soft_skills_count, x='Skill', y='Quantidade',
                              title='Proporção de Soft Skills', labels={'Quantidade': 'Quantidade', 'Skill': 'Soft Skills'},
                              color_discrete_sequence=['#ED1C24'])
                fig4.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig4, use_container_width=True)

        if display_option in ['Tabelas', 'Ambos']:
            # Insights adicionais
            st.subheader('Insights Adicionais')
            col1, col2 = st.columns(2)

            with col1:
                st.write("### Top 5 Cursos de Hard Skills")
                top_hard_skill_courses, top_soft_skill_courses = get_top_courses(df_skills)
                st.dataframe(top_hard_skill_courses[['Skill']], use_container_width=True, hide_index=True)

            with col2:
                st.write("### Top 5 Cursos de Soft Skills")
                st.dataframe(top_soft_skill_courses[['Skill']], use_container_width=True, hide_index=True)
    except Exception as e:
        log.error("Error loading dashboard: %s", str(e), exc_info=True)
