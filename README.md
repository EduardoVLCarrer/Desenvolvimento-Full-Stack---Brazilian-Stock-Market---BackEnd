# Stock Analysis API

API desenvolvida em Flask para análise de ações com base em dados do Alpha Vantage, persistência dos resultados em banco de dados SQLite e disponibilização das informações para consumo via Front-End.

A API também conta com documentação interativa utilizando Swagger (OpenAPI 3).

---

## 🚀 Funcionalidades

- Analisar um ticker e registrar o resultado da análise de compra (`SIM` ou `NAO`)
- Consultar ações analisadas por status (`SIM` / `NAO`)
- Consultar análises de um ticker específico
- Remover análises do banco de dados
- Documentação da API via Swagger UI (OpenAPI 3)

---

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- Flask
- Flask-CORS
- SQLAlchemy
- SQLite
- Requests
- Swagger UI (OpenAPI 3)

---

## 📋 Pré-requisitos

- Python 3.x instalado
- Git (opcional, para clonar o repositório)

---

## ⚙️ Instalação e Execução (Ambiente Local)

### 1️⃣ Clonar o repositório
```bash
git clone <URL_DO_REPOSITORIO_BACKEND>
cd <PASTA_DO_BACKEND>
```

### 2️⃣ Criar e ativar ambiente virtual

**Windows (PowerShell):**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Windows (CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Executar a aplicação
```bash
flask --app app/routes run
```

A API estará disponível em:
```
http://localhost:5000
```

---

## 📑 Documentação da API (Swagger)

- Swagger UI:  
  http://localhost:5000/swagger

- Arquivo OpenAPI (YAML):  
  http://localhost:5000/static/openapi.yaml

---

## 🔗 Principais Rotas

- `POST /analisar/{ticker}`  
- `GET /acoes_viaveis/{comprar}`  
- `GET /acoes_especifica/{ticker}`  
- `DELETE /delete/{ticker}`  

---

## ℹ️ Observações

- A análise utiliza dados da API Alpha Vantage, que pode possuir limite de requisições.
- O banco de dados utilizado é SQLite, armazenado localmente.
- O ambiente virtual (`venv`) não deve ser versionado no repositório.
