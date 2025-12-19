from flask import Flask
from flask_cors import CORS
from datetime import datetime
from sqlalchemy import select
from flask_swagger_ui import get_swaggerui_blueprint

from .models import AnaliseAcoes
from .__init__ import Session
#to run: flask --app app\routes run
app = Flask(__name__)
CORS(app)

SWAGGER_URL = "/swagger"
API_URL = "/static/openapi.yaml"

swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Stock Analysis API"}
)

app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

@app.route("/")
def hello_world():
    return "hello world"


# Função para Analisar Ações e Inserir sua Análise no Banco
@app.route("/analisar/<ticker>", methods=["POST"])
def analisar(ticker):
    
    import requests
    # Chave da API do Alpha Vantage
    API_KEY = '8SHH5H9XPIEFEPAT'

    # Símbolo da ação para a qual você quer os dados de dividendos
    symbol = ticker + str('.SA')

    # Endpoint da API para dados mensais ajustados (incluindo dividendos)
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={API_KEY}'

    # Fazendo a solicitação GET para obter os dados mensais ajustados (incluindo dividendos)
    response = requests.get(url)

    # Verificando se a solicitação foi bem-sucedida (código 200)
    if response.status_code == 200:
        data = response.json()
        time_series = data.get('Monthly Adjusted Time Series', {})

        stock_price = []
        dividends_by_year = {}
        for date, values in time_series.items():
            dividend_amount = float(values.get('7. dividend amount', '0.0'))
            stock_price.append(float(values.get('4. close', '0.0')))
            year = date.split('-')[0]

            if int(year) >= 2018:  # Considerando a partir de 2018
                if year not in dividends_by_year:
                    dividends_by_year[year] = 0.0
                dividends_by_year[year] += dividend_amount
    
    # Calculando a média dos dividendos desde 2018
    dividends_since_2018 = [value for key, value in dividends_by_year.items() if int(key) >= 2018]
    average_dividends_since_2018 = sum(dividends_since_2018) / len(dividends_since_2018)


    print(f'Média dos dividendos desde 2018: R${average_dividends_since_2018:.2f}')
    print(f'Ultima Cotação da Ação: R${stock_price[0]:.2f}')
    print(f"\nPreço Teto da Ação segundo Barsi em R${average_dividends_since_2018/0.06:.2f} e o Valor Atual dela Está em R${stock_price[0]:.2f}")


    if average_dividends_since_2018/0.06 < stock_price[0]:
        print(f"\nPara valer o preço que a ação está a média de dividendos deveria ser R${stock_price[0]*0.06:.2f} ")
        analise = "NAO"
    else:
        analise = "SIM"
    
    session = Session()
    data_analise = datetime.now()
    analiseacao = AnaliseAcoes(acao = ticker, 
                               analise = analise, 
                               data_analise = data_analise)
    session.add(analiseacao)
    session.commit()

    json_post = {
        "acao": ticker,
        "analise": analise,
        "data_analise": data_analise.isoformat()
    }
    return json_post


# Função para Deletar uma Ação no Banco
@app.route("/delete/<ticker>", methods=["DELETE"])
def delete(ticker):
    session = Session()
    result = session.execute(select(AnaliseAcoes).filter_by(acao=ticker)).scalars().all()
    lista_serializada = []
    for obj in result:
        lista_serializada.append({
            "acao": obj.acao,
            "analise": obj.analise,
            "data_analise": obj.data_analise.isoformat()
        })
    session.query(AnaliseAcoes).filter_by(acao=ticker).delete()
    session.commit()
    return lista_serializada


# Função para buscar todas as Ações para Possível Compra
@app.route("/acoes_viaveis/<comprar>")
def acoes_viaveis(comprar):
    session = Session()
    analise = comprar
    result = session.execute(select(AnaliseAcoes).filter_by(analise=analise)).scalars().all()
    lista_serializada = []
    for obj in result:
        lista_serializada.append({
            "acao": obj.acao,
            "analise": obj.analise,
            "data_analise": obj.data_analise.isoformat()
        })
    return lista_serializada


# Função para buscar verificar análise de Ação espécífica
@app.route("/acoes_especifica/<ticker>")
def acao_especifica(ticker):
    session = Session()
    acao = ticker
    result = session.execute(select(AnaliseAcoes).filter_by(acao=acao)).scalars().all()
    lista_serializada = []
    for obj in result:
        lista_serializada.append({
            "acao": obj.acao,
            "analise": obj.analise,
            "data_analise": obj.data_analise.isoformat()
        })
    return lista_serializada