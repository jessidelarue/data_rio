import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Função para carregar e armazenar dados em cache
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

# Inicializar session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'ano' not in st.session_state:
    st.session_state.ano = None
if 'filtro_mes' not in st.session_state:
    st.session_state.filtro_mes = []

# Personalização de cores
st.subheader('Personalização de Interface')
cor_fundo = st.color_picker('Escolha a cor de fundo', '#1A0148', key='cor_fundo')
cor_texto = st.color_picker('Escolha a cor do texto', '#ffffff', key='cor_texto')

# Aplicar o CSS para personalização de cores
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {cor_fundo};
        color: {cor_texto};
    }}
    </style>
    """, unsafe_allow_html=True)

# Objetivo e Motivação
st.title('Análise dos Dados de Visitação ao CCBB - Data.Rio')
st.write('''
    O objetivo deste dashboard é fornecer uma interface interativa para análise dos dados de visitantes mensais ao Centro Cultural do Banco do Brasil (CCBB) no Rio de Janeiro.\n
    A motivação por trás da escolha desses dados é permitir uma análise detalhada das tendências de visitação ao longo dos anos.\n
    A aplicação oferece funcionalidades como upload de arquivos CSV, filtragem dos dados, personalização da interface, visualização gráfica e métricas básicas para facilitar a análise dos dados de turismo.
    ''')

# Importação e exibição dos dados
st.subheader('Importação e exibição dos dados')
arquivo = st.file_uploader('Escolha um arquivo CSV para fazer o upload:', type=['csv'])

if arquivo is not None:
    with st.spinner('Carregando dados...'):
        df = load_data(arquivo)
        st.session_state.df = df

        # Atualiza a lista de anos e meses disponíveis
        ano_opcoes = df.columns[1:].tolist() if df.shape[1] > 1 else []
        if not ano_opcoes:
            st.session_state.ano = None
        elif st.session_state.ano not in ano_opcoes:
            st.session_state.ano = ano_opcoes[0]

        # Inicializa o filtro de meses se necessário
        st.session_state.filtro_mes = list(df['Mês'].unique())
        st.success('Dados carregados com sucesso!')
        st.write(df)

# Exibir dados e filtros se o DataFrame estiver disponível no session state
if st.session_state.df is not None:
    df = st.session_state.df

    # Configuração do filtro
    st.subheader('Seleção de filtros:')

    # Seleção do ano
    ano_opcoes = df.columns[1:].tolist() if df.shape[1] > 1 else []
    ano = st.selectbox(
        'Escolha o ano para visualizar',
        ano_opcoes,
        index=ano_opcoes.index(st.session_state.ano) if st.session_state.ano in ano_opcoes else 0,
        key='ano'
    )
    
    # Atualiza o session state somente se o valor do filtro mudar
    if ano != st.session_state.ano:
        st.session_state.ano = ano

    # Seleção dos meses
    st.subheader('Escolha os meses:')
    filtro_mes = []
    for mes in df['Mês'].unique():
        if st.checkbox(mes, key=f'checkbox_{mes}', value=False):
            filtro_mes.append(mes)

    # Atualiza o session state somente se o valor do filtro mudar
    if filtro_mes != st.session_state.filtro_mes:
        st.session_state.filtro_mes = filtro_mes

    # Aplicar filtros
    if st.session_state.ano and st.session_state.ano in df.columns:
        data = df[['Mês', st.session_state.ano]]
        if st.session_state.filtro_mes:
            st.write(f"Meses filtrados: {st.session_state.filtro_mes}")  # Depuração
            data = data[data['Mês'].isin(st.session_state.filtro_mes)]
        
        # Tabela Interativa 
        st.subheader('Tabela Interativa')
        st.data_editor(data, use_container_width=True)  # Habilita a ordenação e filtragem

        # Download dos dados filtrados
        csv_data = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label='Download dos dados filtrados como CSV',
            data=csv_data,
            file_name='dados_filtrados.csv',
            mime='text/csv'
        )

        # Gráficos simples
        st.subheader('Gráficos Simples')
        st.write('Gráfico de linhas:')
        fig, ax = plt.subplots()
        sns.lineplot(x='Mês', y=st.session_state.ano, data=data, ax=ax)
        plt.xticks(rotation=90)
        st.pyplot(fig)

        st.write('Gráfico de barras:')
        fig, ax = plt.subplots()
        sns.barplot(x='Mês', y=st.session_state.ano, data=data, ax=ax)
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Gráficos avançados
        st.subheader('Gráficos Avançados')
        st.write('Histograma:')
        fig, ax = plt.subplots()
        sns.histplot(data[st.session_state.ano], kde=True, ax=ax)
        st.pyplot(fig)

        st.write('Gráfico de dispersão:')
        fig, ax = plt.subplots()
        sns.scatterplot(x='Mês', y=st.session_state.ano, data=data, ax=ax)
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # Métricas básicas
        st.subheader('Métricas Básicas')
        st.write(f'Contagem de registros: {data.shape[0]}')
        st.write(f'Média: {data[st.session_state.ano].mean():.2f}')
        st.write(f'Soma: {data[st.session_state.ano].sum():.2f}')
