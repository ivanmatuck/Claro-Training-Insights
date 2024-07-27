import plotly.express as px
import streamlit as st

from config.log_config import log
from services.course_service import load_data, save_uploaded_file, get_latest_file, display_qualitative_data


def load_dashboard():
    log.info("Loading dashboard...")

    # Barra lateral para upload de arquivo
    st.sidebar.image('img/png-transparent-claro-hd-logo.png', width=50)  # Ajusta o tamanho do logo
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
    quantitativos_df, qualitativos_df = load_data(latest_file)

    log.info("Data loaded for dashboard from %s", latest_file)

    # Configurações da barra lateral
    diretorias = ['Todas'] + quantitativos_df['diretoria'].unique().tolist()
    diretoria_filter = st.sidebar.multiselect('Selecione as Diretorias', diretorias, default='Todas')
    skill_filter = st.sidebar.radio('Selecione o Tipo de Habilidade', ['Todas', 'HardSkill', 'SoftSkill'])
    display_option = st.sidebar.radio('Opções de Exibição', ['Ambos', 'Tabelas', 'Gráficos'], index=0)

    log.info("Filtro selecionado - Diretoria: %s, Tipo de Habilidade: %s", diretoria_filter, skill_filter)

    # Filtrar dados de acordo com as seleções
    if 'Todas' not in diretoria_filter:
        quantitativos_df = quantitativos_df[quantitativos_df['diretoria'].isin(diretoria_filter)]
        qualitativos_df = qualitativos_df[qualitativos_df['diretoria'].isin(diretoria_filter)]
        log.info("Dados filtrados por Diretorias (%s):\n%s", diretoria_filter, quantitativos_df.head().to_string())
        log.info("Dados qualitativos filtrados por Diretorias (%s):\n%s", diretoria_filter,
                 qualitativos_df.head().to_string())

    if skill_filter != 'Todas':
        quantitativos_df = quantitativos_df[quantitativos_df['tipo'] == skill_filter]
        log.info("Dados filtrados por Tipo (%s):\n%s", skill_filter, quantitativos_df.head().to_string())

    # Filtrar registros com urgencia maior que zero
    treemap_data = quantitativos_df[quantitativos_df['urgencia'] > 0].groupby(['diretoria', 'cursos']).agg(
        {'urgencia': 'sum'}).reset_index().rename(columns={'urgencia': 'Urgência'})

    # Seção de Dados dos Cursos
    if display_option in ['Gráficos', 'Ambos']:
        # Gráficos para skills de equipe
        st.subheader('Necessidades de Educação dos times')
        equipe_skills = quantitativos_df[quantitativos_df['solicitado por equipe'] == 'S']

        if skill_filter == 'Todas' or skill_filter == 'SoftSkill':
            soft_skills_count = equipe_skills[equipe_skills['tipo'] == 'SoftSkill'][
                'cursos'].value_counts().reset_index()
            soft_skills_count.columns = ['cursos', 'Quantidade']
            fig4 = px.bar(soft_skills_count, x='cursos', y='Quantidade', color='Quantidade',
                          color_continuous_scale='RdYlGn_r', title='Proporção de Soft Skills (Equipe)',
                          labels={'Quantidade': 'Quantidade', 'cursos': 'Soft Skills'})
            fig4.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig4, use_container_width=True)
            log.info("Bar chart for 'Proporção de Menções de Cursos Soft Skills (Equipe)' displayed")

        if skill_filter == 'Todas' or skill_filter == 'HardSkill':
            hard_skills_count = equipe_skills[equipe_skills['tipo'] == 'HardSkill'][
                'cursos'].value_counts().reset_index()
            hard_skills_count.columns = ['cursos', 'Quantidade']
            fig3 = px.bar(hard_skills_count, x='cursos', y='Quantidade', color='Quantidade',
                          color_continuous_scale='RdYlGn_r', title='Proporção de Hard Skills (Equipe)',
                          labels={'Quantidade': 'Quantidade', 'cursos': 'Hard Skills'})
            fig3.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig3, use_container_width=True)
            log.info("Bar chart for 'Proporção de Menções de Cursos Hard Skills (Equipe)' displayed")

        # Gráficos para skills de executivos
        st.subheader('Necessidades de Educação dos executivos')
        executivos_skills = quantitativos_df[quantitativos_df['solicitado por  executivos'] == 'S']

        if skill_filter == 'Todas' or skill_filter == 'SoftSkill':
            soft_skills_count = executivos_skills[executivos_skills['tipo'] == 'SoftSkill'][
                'cursos'].value_counts().reset_index()
            soft_skills_count.columns = ['cursos', 'Quantidade']
            fig6 = px.bar(soft_skills_count, x='cursos', y='Quantidade', color='Quantidade',
                          color_continuous_scale='RdYlGn_r', title='Proporção de Soft Skills (Executivos)',
                          labels={'Quantidade': 'Quantidade', 'cursos': 'Soft Skills'})
            fig6.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig6, use_container_width=True)
            log.info("Bar chart for 'Necessidades de Educação dos executivos Soft Skills (Executivos)' displayed")

        if skill_filter == 'Todas' or skill_filter == 'HardSkill':
            hard_skills_count = executivos_skills[executivos_skills['tipo'] == 'HardSkill'][
                'cursos'].value_counts().reset_index()
            hard_skills_count.columns = ['cursos', 'Quantidade']
            fig5 = px.bar(hard_skills_count, x='cursos', y='Quantidade', color='Quantidade',
                          color_continuous_scale='RdYlGn_r', title='Proporção de Hard Skills (Executivos)',
                          labels={'Quantidade': 'Quantidade', 'cursos': 'Hard Skills'})
            fig5.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig5, use_container_width=True)
            log.info("Bar chart for 'Necessidades de Educação dos executivos Hard Skills (Executivos)' displayed")

        # Início dos gráficos treemap

        # Função para adicionar quebras de linha após cada palavra com mais de dois caracteres

        def add_line_breaks_long_words(text):
            words = text.split()
            new_text = []
            for word in words:
                if len(word) > 2:
                    new_text.append(word)
                else:
                    if new_text:
                        new_text[-1] += ' ' + word  # Adiciona palavras curtas à palavra anterior
                    else:
                        new_text.append(word)
            return '<br>'.join(new_text)

            # Adicionar quebras de linha aos rótulos dos cursos

        treemap_data['cursos'] = treemap_data['cursos'].apply(add_line_breaks_long_words)

        # Normalizar a frequência dentro de cada diretoria
        treemap_data['Normalized_Frequency'] = treemap_data.groupby('diretoria')['Urgência'].transform(
            lambda x: (x - x.min()) / (x.max() - x.min())  # Normalizar entre 0 e 1
        )

        # Gráfico treemap: Nível de urgência dos cursos (frequência de menção)
        st.subheader('Necessidades Urgentes de Educação - por Diretoria')
        log.info("Subheader set for 'Nível de Urgência dos Cursos'")

        if not treemap_data.empty:
            fig2 = px.treemap(treemap_data, path=['diretoria', 'cursos'], values='Urgência',
                              color='Normalized_Frequency',
                              color_continuous_scale='RdYlGn_r')

            fig2.update_traces(
                marker=dict(colorscale='RdYlGn_r', line=dict(color='#FFFFFF', width=2)),
                insidetextfont=dict(size=10),
                texttemplate='%{label}<br>%{value}',
                hovertemplate='<b>%{label}</b><br>Urgência: %{value}<extra></extra>'
            )

            fig2.update_layout(
                coloraxis_colorbar=dict(
                    title="",
                    orientation="h",
                    x=0.5,
                    y=-0,  # Ajuste esta linha para mover a legenda para baixo
                    xanchor="center",
                    yanchor="top",
                    tickmode="array",
                    ticks="outside",
                    tickvals=[0, 0.5, 1],  # Valores ajustados para início, meio e fim
                    ticktext=["Baixa", "Média", "Alta"],  # Textos ajustados para início, meio e fim
                    lenmode="pixels",
                    len=600,
                    nticks=3
                ),
                margin=dict(t=25, l=0, r=0, b=0),
                coloraxis_showscale=True,
                paper_bgcolor='white',
                plot_bgcolor='white'
            )

            st.plotly_chart(fig2, use_container_width=True)
            log.info("Treemap chart created")
        else:
            st.write("Nenhum curso encontrado com frequência maior que 0 para a diretoria selecionada.")
            log.info("No data found for the selected filters in treemap")

        # Gráfico de barras: Ranking de cursos solicitados por mais diretorias
        st.subheader('Diretorias que solicitaram urgência por curso')
        log.info("Subheader set for 'Ranking de Cursos Solicitados por Mais Diretorias'")

        # Contar o número de diretorias que solicitaram cada curso
        course_directories_count = quantitativos_df[quantitativos_df['urgencia'] > 0].groupby('cursos')[
            'diretoria'].nunique().reset_index()
        course_directories_count.columns = ['cursos', 'Número de Diretorias']

        # Ordenar por número de diretorias em ordem decrescente
        course_directories_count = course_directories_count.sort_values(by='Número de Diretorias', ascending=False)

        if not course_directories_count.empty:
            fig4 = px.bar(course_directories_count, x='cursos', y='Número de Diretorias', color='Número de Diretorias',
                          color_continuous_scale='RdYlGn_r', title='Ranking de Cursos Solicitados por Mais Diretorias')

            st.plotly_chart(fig4, use_container_width=True)
            log.info("Bar chart for courses requested by most departments created")
        else:
            st.write("Nenhum curso encontrado com frequência maior que 0 para a diretoria selecionada.")
            log.info("No data found for the selected filters in bar chart")

    if display_option in ['Tabelas', 'Ambos']:
        st.subheader('Dados dos Cursos')
        st.dataframe(quantitativos_df.reset_index(drop=True), use_container_width=True, hide_index=True)
        log.info("Dataframe for skills displayed")

    if display_option in ['Tabelas', 'Ambos']:
        # Exibir dados qualitativos
        display_qualitative_data(qualitativos_df)
        log.info("Dataframe for qualitative data displayed")

    log.info("Dashboard loaded successfully.")
