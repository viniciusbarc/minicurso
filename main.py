import datetime
import pandas
import yfinance
from flask import Flask
from flask import Response
from markupsafe import escape
from datetime import date
from ta.trend import TRIXIndicator
from ta.trend import EMAIndicator
from ta.trend import MACD


app = Flask(__name__)


@app.route("/ativo/<ativo>")
def obtercotacoes(ativo):
    # Definição de datas para captura via yfinance
    datafinal = date.today()
    diasreduzir = datetime.timedelta(days=800)
    datainicial = datafinal - diasreduzir
    diasaumentar = datetime.timedelta(days=1)
    datafinal = datafinal + diasaumentar

    # Obtendo cotações do ativo
    df = yfinance.download(ativo,datainicial,datafinal)

    # Calculando indicadores
    df["trix"] = TRIXIndicator(close=df["Close"], window=8, fillna=False).trix()
    df["ema21"] = EMAIndicator(close=df["Close"], window=21, fillna=False).ema_indicator()
    df["hmacd"] = (MACD(close=df["Close"], window_slow=26, window_fast=12, window_sign=9, fillna=False)).macd_diff()

    # Apagando algumas linhas e colunas
    df = df.iloc[43:].dropna()
    df = df.drop(columns=["Adj Close","Volume"])

    # Retornando um JSON
    return Response(df.to_json(orient="index", double_precision=2, date_format="iso"), mimetype='application/json')


if __name__ == "__main__":
    app.run(host="0.0.0.0")