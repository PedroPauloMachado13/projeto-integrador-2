## Passo a passo
1) Baixar a pasta .zip no GitHub
2) Criar o banco de dados `projeto_integrador_2` no phpMyAdmin
3) Importar a estrutura do banco (aba Importar no phpMyAdmin)
   - Escolher o arquivo baixado `schema.sql`
4) Rodar o comando `python db.py` (dentro da pasta `db` para popular os dados
5) Voltar para a pasta anterior (raiz do projeto -> onde ficam todos os arquivos, subpastas, tudo mais)
6) Rodar o comando `python -m streamlit run dashboard.py`

## Comando para rodar o código e abrir o dasboard:

`python -m streamlit run dashboard.py`

## Configuração necessária

- Ter Python instalado
- Ter as libs do projeto (streamlit, pandas, plotly, pymysql) instaladas
- Rodar o comando a partir da raiz do projeto
- Ter usado os arquivos da pasta `db` para, respectivamente:
    - Criar a tabela usando `schema.sql`
    - Popular com dados usando `data.py` (que pode ser feito usando o comando `python data.py`)

