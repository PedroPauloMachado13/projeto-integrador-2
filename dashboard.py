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
st.set_page_config(layout="wide", page_title="AquaSense")
row1, col = st.columns([1, 6])
with row1:
    col.title('AquaSense - Eficiência em tratamento de água e esgoto')

# Configurando a tabela para exibição partindo do DataFrame recuperado do banco
row_header, row_button = st.columns([9, 1])
with row_header:
    st.subheader("Dados das Amostras Coletadas")
with row_button:
    st.button("➕ Nova amostra", on_click=None)
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
st.divider()
with st.container():
    st.header("Estatísticas Gerais das Amostras")
    st.info("Média de pH das amostras: {:.2f}".format(df["pH"].mean()))
    st.info("Média de temperatura da fonte das amostras: {:.1f} °C".format(df["temperatura_fonte"].mean()))

st.divider()
st.header("Amostras e projeto", divider="blue")
st.subheader("Imagens das amostras coletadas e do projeto de sensores desenvolvido")
colImg1, colImg2, colImg3 = st.columns(3)
colImg1.image('http://localhost:8080/app/static/copos-amostra.jpeg', caption='Copos com amostras coletadas')
colImg2.image('http://localhost:8080/app/static/garrafas-amostra.jpeg', caption='Garrafas com amostras coletadas')
colImg3.image('http://localhost:8080/app/static/projeto-sensores.jpeg', caption='Projeto de sensores desenvolvido (protótipo arduino)')
st.subheader("Dashboard para leitura dos sensores")
colImg4, colImg5, colImg6 = st.columns(3)
colImg4.image('http://localhost:8080/app/static/dashboard-leitura-conectar.jpeg', caption='Tela para conectar o arduino')
colImg5.image('http://localhost:8080/app/static/dashboard-leitura.jpeg', caption='Tela com leitura dos sensores em tempo real')
colImg6.image('http://localhost:8080/app/static/dashboard-tabela.jpeg', caption='Tabela com dados previamente coletados')

st.divider()
col1, col2 = st.columns(2)

st.divider()
col3, col4 = st.columns(2)

st.divider()
col5, col6 = st.columns(2)

st.divider()
col7, col8 = st.columns(2)

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
    color=contagem_por_categoria.index,
    color_discrete_map={
        'Ácida': '#EF4444',
        'Neutra': '#10B981',
        'Básica': '#3B82F6',
    },
    hole=0.35,
    width=800,
    height=550,
)

## Adiciona informações de hover e formatação
grafico_acidez_pizza.update_traces(
    textposition='inside',
    textinfo='percent+label',
    hovertemplate='<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{percent}'
)

col1.header("Acidez das amostras de água", divider="blue")
col1.markdown("Este gráfico de pizza mostra a distribuição das amostras de água com base em sua acidez, categorizadas como Ácida, Neutra ou Básica, sendo a classificação feita com base nos parametros de classificação: pH < 6.95 (Ácida), 6.95 ≤ pH ≤ 7.1 (Neutra) e pH > 7.1 (Básica).")
col1.plotly_chart(grafico_acidez_pizza)

# Mapa das coletas
mapa = pd.DataFrame(
    df,
    columns=["latitude", "longitude", "nome_local"],
)

col2.header("Mapa das Coletas", divider="blue")
col2.markdown("O mapa abaixo exibe os locais onde as amostras de água foram coletadas, com base nas coordenadas de latitude e longitude registradas durante o processo de coleta. Ele ajuda a guiar a visualização geográfica das áreas de interesse para a análise da qualidade da água e esgoto.")
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

col3.header("Gráfico de pH vs Temperatura da Fonte", divider="blue")
col3.markdown("O gráfico de dispersão abaixo exibe a relação entre o pH das amostras de água e a temperatura da fonte onde foram coletadas. Essa visualização ajuda a entender como essas duas variáveis podem estar correlacionadas, sendo possível identificar tendências ou padrões entre as medidas.")
col3.plotly_chart(grafico_dispesao_ph_temperatura)

# Gráfico de barras turbidez x umidade
grafico_barras_turbidez_umidade = px.scatter(
    df,
    x="ntu_turbidez",
    y="umidade_externa",
    title="Turbidez vs Umidade Externa",
    labels={
        "ntu_turbidez": "NTU Turbidez",
        "umidade_externa": "Umidade Externa (%)"
    },
)
col4.header("Gráfico de Turbidez vs Umidade Externa", divider="blue")
col4.markdown("O gráfico de barras abaixo ilustra a relação entre a turbidez das amostras de água, medida em NTU (Unidades Nefelométricas de Turbidez), e a umidade externa no momento da coleta. Essa visualização permite a visualização do impacto que a menor umidade (que aumenta o número de partículas suspensas) pode ter na turbidez da água.")
col4.plotly_chart(grafico_barras_turbidez_umidade)

# Histograma pH
grafico_histograma_ph = px.histogram(df, x="pH", nbins=10, title="Histograma de pH das Amostras", labels={"pH": "pH"})
col5.header("Histograma de pH das Amostras", divider="blue")
col5.markdown("O histograma abaixo apresenta a distribuição dos valores de pH das amostras de água coletadas. Ele mostra a frequência de ocorrência de diferentes faixas de pH, permitindo a análise da variação do pH nas amostras e a identificação de tendências ou padrões na acidez ou alcalinidade da água.")
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

col6.header("Número de Coletas por Local", divider="blue")
col6.markdown("O gráfico de linhas abaixo mostra o número de coletas realizadas em cada local específico. Essa visualização ajuda a identificar quais locais tiveram maior ou menor frequência de coletas, fornecendo insights sobre os pontos de interesse para a análise da qualidade da água e esgoto, permitindo controle sobre quais áreas precisam de mais atenção.")
col6.plotly_chart(grafico_barras_locais_coleta)