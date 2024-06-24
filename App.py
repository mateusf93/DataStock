import yfinance as yf 
import streamlit as st 
import pandas as pd 
import plotly.express as pl 
from utils import utils
import datetime
st.set_page_config(layout='wide')
st.title("DataInvest")

conn = utils.connect_db()
options = pd.read_sql_query ("select stockdescription from stocks", conn)
intervalData = ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo') 
stocks = st.sidebar.multiselect("Informar nome da ação", options['stockdescription'],label_visibility="hidden")
startDate = st.sidebar.date_input("Data Inicial")
endDate = st.sidebar.date_input("Data Final")
interval = st.sidebar.selectbox("Intervalo de Tempo",intervalData)
tab1, tab2 = st.tabs(['Gráficos', 'Informações Históricas'])


with tab1:
    for stock in stocks:
        
        ticker = yf.Ticker(stock)
        st.title(stock)
        df = pd.DataFrame.from_dict(ticker.history(start=startDate, end=endDate, interval=interval))
        df.reset_index(inplace=True)
        dateColumn = df.columns[0]
        dfClose = df[[dateColumn,'Close']]
        df[dateColumn] = pd.to_datetime(df[dateColumn], format = '%d/%m/%Y')

        column1, column2 = st.columns(2)
        try:
            
            with column1:
                st.metric('Maior Volume', utils.formata_numero(df['Volume'].max().round(2), ''))
            with column2:    
                st.metric('Maior Preço de Fechamento', utils.formata_numero(df['Close'].max().round(2), '$'))
            st.plotly_chart(utils.monta_grafico(dfClose,dateColumn, 'Close'),use_container_width = True)
        except:
            st.write("Aguardando ser informada a ação!")
          
with tab2:
    for stock in stocks:
        ticker = yf.Ticker(stock)
        st.title(stock)
        df = pd.DataFrame.from_dict(ticker.history(start=startDate, end=endDate, interval=interval))
        df.reset_index(inplace=True)
        
        
        try:
            st.dataframe(df)
        except:
            st.write("Aguardando ser informada a ação!")  
    obs = st.text_area("Observações")
    print(obs)
    if st.button("Salvar Histórico"):
        utils.salvar_dados(startDate,endDate,stocks,interval,obs, conn)
        
query_params = st.experimental_user
print(query_params.email)       