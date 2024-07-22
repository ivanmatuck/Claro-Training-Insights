# controllers/course_controller.py

import plotly.express as px
import streamlit as st

from config.log_config import log
from services.course_service import load_data, get_top_courses, save_uploaded_file, get_latest_file


def load_dashboard():
    log.info("Loading dashboard...")

    # Barra lateral para upload de arquivo
    st.sidebar.image('img/png-transparent-claro-hd-logo.png', width=150)  # Ajusta o tamanho do logo
    st.sidebar.header('Filtros')
    uploaded_file = st.sidebar.file_uploader("Faça o upload de um arquivo .xlsx", type=["xlsx"])
    if uploaded_file is not None:
        save_uploaded_file(uploaded_file)
        st.warning("Arquivo carregado com sucesso! Por favor, atualize a página para ver os dados atualizados.")

    # Obter o arquivo mais recente
    latest_file = get_latest_file()
    if not latest_file:
        st.warning("Nenhum arquivo XLSX válido encontrado na pasta 'data'. Faça o upload de um arquivo válido.")
        return

    # Carregar os dados do arquivo mais recente
    df = load_data(latest_file)
    log.info("Data loaded for dashboard from %s", latest_file)

    # Configurações da barra lateral
    diretoria_filter = st.sidebar.selectbox('Selecione a Diretoria', ['Todas'] + df['diretoria'].unique().tolist())
    skill_filter = st.sidebar.radio('Selecione o Tipo de Habilidade', ['Todas', 'HardSkill', 'SoftSkill'])
    display_option = st.sidebar.radio('Opções de Exibição', ['Ambos', 'Tabelas', 'Gráficos'], index=0)

    log.info("Filtro selecionado - Diretoria: %s, Tipo de Habilidade: %s", diretoria_filter, skill_filter)

    # Filtrar dados de acordo com as seleções
    if diretoria_filter != 'Todas':
        df = df[df['diretoria'] == diretoria_filter]
        log.info("Dados filtrados por Diretoria (%s):\n%s", diretoria_filter, df.head().to_string())

    if skill_filter != 'Todas':
        df = df[df['tipo'] == skill_filter]
        log.info("Dados filtrados por Tipo (%s):\n%s", skill_filter, df.head().to_string())

    # Filtrar registros com frequencia maior que zero
    treemap_data = df[df['frequencia'] > 0].groupby(['diretoria', 'cursos']).agg(
        {'frequencia': 'sum'}).reset_index().rename(columns={'frequencia': 'Frequência'})

    # Gráfico treemap: Nível de urgência dos cursos (frequência de menção)
    st.subheader('Nível de Urgência dos Cursos com base na frequência de citação')
    log.info("Subheader set for 'Nível de Urgência dos Cursos'")

    if not treemap_data.empty:
        fig2 = px.treemap(treemap_data, path=['diretoria', 'cursos'], values='Frequência', color='Frequência',
                          color_continuous_scale='RdYlGn_r')
        fig2.update_traces(marker=dict(colorscale='RdYlGn_r', line=dict(color='#FFFFFF', width=2)))
        fig2.update_layout(coloraxis_colorbar=dict(
            title="Frequência",
            orientation="h",
            x=0.5,
            y=0,
            xanchor="center",
            yanchor="top",
            tickmode="array",
            ticks="outside",
            tickvals=[0, 0.5, 1],
            ticktext=["Baixa", "Média", "Alta"],
            lenmode="pixels",
            len=300,
            nticks=3
        ))
        fig2.update_layout(margin=dict(t=25, l=0, r=0, b=0), coloraxis_showscale=True)
        fig2.update_layout(paper_bgcolor='white')
        st.plotly_chart(fig2, use_container_width=True)
        log.info("Treemap chart created")
    else:
        st.write("Nenhum curso encontrado com frequência maior que 0 para a diretoria selecionada.")
        log.info("No data found for the selected filters in treemap")

    # Seção para adicionar gráficos de pizza dos cursos com maior frequência de menções
    st.subheader('Cursos com Maior Frequência de Solicitações')
    log.info("Subheader set for 'Cursos com Maior Frequência de Solicitações'")

    col1, col2 = st.columns([1, 1], gap="small")

    with col1:
        top_hard_skill_courses = df[df['tipo'] == 'HardSkill'].nlargest(5, 'frequencia').reset_index(drop=True)
        fig_hard_skills = px.pie(top_hard_skill_courses, values='frequencia', names='cursos',
                                 title='TOP Cursos - Hard Skills', color_discrete_sequence=px.colors.sequential.RdBu)
        fig_hard_skills.update_layout(legend=dict(yanchor="bottom", y=0.01, xanchor="center", x=-0))
        st.plotly_chart(fig_hard_skills, use_container_width=True)
        log.info("Pie chart for Hard Skills displayed")

    with col2:
        top_soft_skill_courses = df[df['tipo'] == 'SoftSkill'].nlargest(5, 'frequencia').reset_index(drop=True)
        fig_soft_skills = px.pie(top_soft_skill_courses, values='frequencia', names='cursos',
                                 title='TOP Cursos - Soft Skills', color_discrete_sequence=px.colors.sequential.RdBu)
        fig_soft_skills.update_layout(legend=dict(yanchor="bottom", y=0.01, xanchor="center", x=-0))
        st.plotly_chart(fig_soft_skills, use_container_width=True)
        log.info("Pie chart for Soft Skills displayed")

    # Seção para adicionar insights adicionais com métricas gerais dos cursos
    if display_option in ['Tabelas', 'Ambos']:
        st.subheader('Insights Adicionais')
        col1, col2 = st.columns(2)
        log.info("Subheader set for 'Insights Adicionais'")

        with col1:
            st.write("### Top 5 Cursos de Hard Skills")
            top_hard_skill_courses, top_soft_skill_courses = get_top_courses(df)
            st.dataframe(top_hard_skill_courses[['cursos']], use_container_width=True, hide_index=True)
            log.info("Top 5 Hard Skills displayed")

        with col2:
            st.write("### Top 5 Cursos de Soft Skills")
            st.dataframe(top_soft_skill_courses[['cursos']], use_container_width=True, hide_index=True)
            log.info("Top 5 Soft Skills displayed")

    # Seção de Dados dos Cursos
    if display_option in ['Gráficos', 'Ambos']:
        # Gráficos para skills de equipe
        st.subheader('Cursos Mencionados pelas Equipes')
        equipe_skills = df[df['solicitado por equipe'] == 'S']
        if skill_filter == 'Todas' or skill_filter == 'HardSkill':
            hard_skills_count = equipe_skills[equipe_skills['tipo'] == 'HardSkill'][
                'cursos'].value_counts().reset_index()
            hard_skills_count.columns = ['cursos', 'Quantidade']
            fig3 = px.bar(hard_skills_count, x='cursos', y='Quantidade', title='Proporção de Hard Skills (Equipe)',
                          labels={'Quantidade': 'Quantidade', 'cursos': 'Hard Skills'},
                          color_discrete_sequence=['#ED1C24'])
            fig3.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig3, use_container_width=True)
            log.info("Bar chart for 'Proporção de Menções de Cursos Hard Skills (Equipe)' displayed")

        if skill_filter == 'Todas' or skill_filter == 'SoftSkill':
            soft_skills_count = equipe_skills[equipe_skills['tipo'] == 'SoftSkill'][
                'cursos'].value_counts().reset_index()
            soft_skills_count.columns = ['cursos', 'Quantidade']
            fig4 = px.bar(soft_skills_count, x='cursos', y='Quantidade', title='Proporção de Soft Skills (Equipe)',
                          labels={'Quantidade': 'Quantidade', 'cursos': 'Soft Skills'},
                          color_discrete_sequence=['#ED1C24'])
            fig4.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig4, use_container_width=True)
            log.info("Bar chart for 'Proporção de Menções de Cursos Soft Skills (Equipe)' displayed")

        # Gráficos para skills de executivos
        st.subheader('Skills de Executivos')
        executivos_skills = df[df['solicitado por  executivos'] == 'S']
        if skill_filter == 'Todas' or skill_filter == 'HardSkill':
            hard_skills_count = executivos_skills[executivos_skills['tipo'] == 'HardSkill'][
                'cursos'].value_counts().reset_index()
            hard_skills_count.columns = ['cursos', 'Quantidade']
            fig5 = px.bar(hard_skills_count, x='cursos', y='Quantidade', title='Proporção de Hard Skills (Executivos)',
                          labels={'Quantidade': 'Quantidade', 'cursos': 'Hard Skills'},
                          color_discrete_sequence=['#ED1C24'])
            fig5.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig5, use_container_width=True)
            log.info("Bar chart for 'Proporção de Menções de Cursos Hard Skills (Executivos)' displayed")

        if skill_filter == 'Todas' or skill_filter == 'SoftSkill':
            soft_skills_count = executivos_skills[executivos_skills['tipo'] == 'SoftSkill'][
                'cursos'].value_counts().reset_index()
            soft_skills_count.columns = ['cursos', 'Quantidade']
            fig6 = px.bar(soft_skills_count, x='cursos', y='Quantidade', title='Proporção de Soft Skills (Executivos)',
                          labels={'Quantidade': 'Quantidade', 'cursos': 'Soft Skills'},
                          color_discrete_sequence=['#ED1C24'])
            fig6.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig6, use_container_width=True)
            log.info("Bar chart for 'Proporção de Menções de Cursos Soft Skills (Executivos)' displayed")

    if display_option in ['Tabelas', 'Ambos']:
        st.subheader('Dados dos Cursos')
        st.dataframe(df.reset_index(drop=True), use_container_width=True, hide_index=True)
        log.info("Dataframe for skills displayed")

    log.info("Dashboard loaded successfully.")
