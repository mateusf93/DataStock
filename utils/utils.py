import plotly.express as px
import sqlalchemy
import yfinance as yf 
import pandas as pd
import streamlit as st
from sqlalchemy import text
def formata_numero(valor, prefixo = ''):
    for unidade in['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'

def monta_grafico(dados, x_col, y_col):
    fig_closePrice = px.line(dados,
                             x=x_col,
                             y=y_col,
                             markers=True,
                             title='Preço de Fechamento por Intervalo')
    fig_closePrice.update_layout(yaxis_title='Preço Fechamento')
    return fig_closePrice

def connect_db():
    username = 'postgres'
    password = '123456'
    host = 'localhost'
    port = '5432'
    db_name = 'postgres'

    db_url = f"postgresql://{username}:{password}@{host}:{port}/{db_name}"

    engine = sqlalchemy.create_engine(db_url)

    try:
        conn = engine.connect()
        print("Connected to PostgreSQL!")
    except Exception as e:
        print("Error:", e)
    return conn

def salvar_dados(startDate,endDate,stocks,interval,obs,conn):
    st.session_state.clicked = True
    for stock in stocks:
        ticker = yf.Ticker(stock)
        df = pd.DataFrame.from_dict(ticker.history(start=startDate, end=endDate, interval=interval))
        df.reset_index(inplace=True)
        for key, value in df.iterrows():
            date = value[0]
            open = value[1]
            high = value[2]
            low = value[3]
            close = value[4]
            volume = value[5]
            try:
                query = (f"INSERT INTO historical(historicaldate,openprice, highprice, lowprice,closeprice,volume) VALUES('{date}', {open}, {high}, {low}, {close}, {volume})")
                conn.execute(text(query))
                conn.commit()
                print(query)
            except Exception as e:
                print(e)
        queryObs = (f"insert into observations (observation) values('{obs}')")
        try:
            conn.execute(text(queryObs))
            conn.commit()
        except Exception as e:
            print(e)
            
    return print("Dados Salvos com sucesso!")    
            
            
            
        