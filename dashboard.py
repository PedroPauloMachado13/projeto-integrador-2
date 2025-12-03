import streamlit as st
import pandas as pd
import plotly.express as px
import pymysql
import matplotlib.pyplot as plt

conexao = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="projeto_integrador_2",
)

query = "SELECT a.id AS amostra_id, a.nome, a.obs, a.link_foto, c.latitude, c.longitude, c.nome_local, c.data_coleta, c.temperatura_fonte, m.pH, m.temperatura_externa, m.umidade_externa, m.ntu_turbidez, m.nivel, m.data_medida FROM `amostras` a JOIN `amostra_coletas` c ON a.id = c.amostra_id JOIN `amostra_medidas` m ON a.id = m.amostra_id;"
df = pd.read_sql(query, con=conexao)

# Fechando a conexão com o banco
conexao.close()

# Transformando colunas de latitude e longitude para numéricas
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

# Configuração da página
st.set_page_config(layout="wide", page_title="Dashboard PI2")
st.title('Dashboard Projeto Integrador 2')

# Configurando a tabela para exibição partindo do DataFrame recuperado do banco
st.dataframe(
    df, 
    column_config={
        "amostra_id": None,
        "link_foto": st.column_config.ImageColumn("Foto do local",),
        "nome": st.column_config.TextColumn("Nome da amostra"),
        "obs": st.column_config.TextColumn("Observações"),
        "latitude": None,
        "longitude": None,
        "nome_local": st.column_config.TextColumn("Local da coleta"),
        "data_coleta": st.column_config.DatetimeColumn("Data da coleta", format="localized"),
        "temperatura_fonte": st.column_config.NumberColumn("Temperatura da fonte (°C)", format="%.1f °C"),
        "pH": st.column_config.NumberColumn("pH", format="%.2f"),
        "temperatura_externa": st.column_config.NumberColumn("Temperatura externa (°C)", format="%.1f °C"),
        "umidade_externa": st.column_config.NumberColumn("Umidade externa (%)", format="%.1f %%"),
        "ntu_turbidez": st.column_config.NumberColumn("NTU Turbidez", format="%d"),
        "nivel": st.column_config.MultiselectColumn(label= "Nível", disabled=True, options=["OK", "Baixo"], color=["green", "red"], format_func=lambda x: x.capitalize(),),
        "data_medida": st.column_config.DatetimeColumn("Data da medida", format="localized"), 
    }, 
    hide_index=True
)

# Criação do Layout
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)

col1.info("Média de pH das amostras: {:.2f}".format(df["pH"].mean()))
col2.info("Média de temperatura da fonte das amostras: {:.1f} °C".format(df["temperatura_fonte"].mean()))

# Gráfico de acidez da água
## Função para categorizar o pH e transformar em string de categoria
def categorizar_ph(pH):
    if pd.isna(pH):
        return 'Desconhecido'
    try:
        pH_val = float(pH)
        if pH_val < 6.95:
            return 'Ácida'
        elif 6.95 <= pH_val <= 7.1:
            return 'Neutra'
        else:
            return 'Básica'
    except:
        return 'Desconhecido'

# Aplica a função para fazer a categorização
df['Categoria pH'] = df['pH'].apply(categorizar_ph)

# Conta a quantidade de amostras em cada categoria
contagem_por_categoria = df['Categoria pH'].value_counts()

## Cria o gráfico de pizza
grafico_acidez_pizza = px.pie(
    values=contagem_por_categoria.values,
    names=contagem_por_categoria.index,
    title='Acidez das Amostras de Água',
    color=contagem_por_categoria.index,
    color_discrete_map={
        'Ácida': '#EF4444',
        'Neutra': '#10B981',
        'Básica': '#3B82F6',
    },
    hole=0.3
)

## Adiciona informações de hover e formatação
grafico_acidez_pizza.update_traces(
    textposition='inside',
    textinfo='percent+label',
    hovertemplate='<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{percent}'
)

col1.plotly_chart(grafico_acidez_pizza)

# Mapa das coletas
mapa = pd.DataFrame(
    df,
    columns=["latitude", "longitude", "nome_local"],
)

col2.map(mapa, size=10, color="#FFFFFF")

# Gráfico de pH x temperatura da fonte
grafico_dispesao_ph_temperatura = px.scatter(
    df,
    x="temperatura_fonte",
    y="pH",
    title="pH vs Temperatura da Fonte",
    labels={
        "temperatura_fonte": "Temperatura da Fonte (°C)",
        "pH": "pH"
    },
)
col3.plotly_chart(grafico_dispesao_ph_temperatura)

# Gráfico de barras turbidez x umidade
grafico_barras_turbidez_umidade = px.bar(
    df,
    x="ntu_turbidez",
    y="umidade_externa",
    title="Turbidez vs Umidade Externa",
    labels={
        "ntu_turbidez": "NTU Turbidez",
        "umidade_externa": "Umidade Externa (%)"
    },
)
col4.plotly_chart(grafico_barras_turbidez_umidade)

# Histograma pH
grafico_histograma_ph = px.histogram(df, x="pH", nbins=10, title="Histograma de pH das Amostras", labels={"pH": "pH"})
col5.plotly_chart(grafico_histograma_ph)

# Gráfico de local de coleta X número de coletas
# Get the counts
local_counts = df['nome_local'].value_counts().reset_index()
# Rename columns properly
local_counts.columns = ['nome_local', 'contagem']

# Create the line chart
grafico_barras_locais_coleta = px.line(
    local_counts,
    x='nome_local',
    y='contagem',
    title='Número de Coletas por Local',
    labels={
        'nome_local': 'Local da Coleta',
        'contagem': 'Número de Coletas'
    },
    markers=True  # Add markers to points
)

col6.plotly_chart(grafico_barras_locais_coleta)