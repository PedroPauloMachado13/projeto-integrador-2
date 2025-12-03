import streamlit as st
import pandas as pd
import plotly.express as px
import pymysql
    

conexao = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="projeto_integrador_2",
)

query = "SELECT a.id AS amostra_id, a.nome, a.obs, a.link_foto, c.latitude, c.longitude, c.nome_local, c.data_coleta, c.temperatura_fonte, c.id AS coleta_id, m.pH, m.temperatura_externa, m.umidade_externa, m.ntu_turbidez, m.nivel, m.data_medida FROM `amostras` a JOIN `amostra_coletas` c ON a.id = c.amostra_id JOIN `amostra_medidas` m ON a.id = m.amostra_id;"
df = pd.read_sql(query, con=conexao)

# Fechando a conexão com o banco
conexao.close()

st.set_page_config(layout="wide", page_title="Dashboard PI2")

st.title('Dashboard Projeto Integrador 2')

st.dataframe(df)

###> Montando o mosaico do dashboard:
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

###> Gráfico de Barras:
fig_date = px.bar(df, x="amostra_id", y="pH", title="Quantidade Vendida", color="pH")
col1.plotly_chart(fig_date)

# ###> Gráfico de Dispersão:
# fig_date3 = px.scatter(df, x="produto", y="valor_faturado", title="Valor Faturado", color="produto")
# col2.plotly_chart(fig_date3)

# ###> Gráfico de Linha:
# fig_date4 = px.line(df, x="Date", y="valor_faturado", title="Valor Faturado", color="produto")
# col3.plotly_chart(fig_date4)

# ###> Gráfico de Pizza:
# fig_date5 = px.pie(df, values="valor_faturado", names="produto", title="Percentual Vendido")
# col4.plotly_chart(fig_date5)