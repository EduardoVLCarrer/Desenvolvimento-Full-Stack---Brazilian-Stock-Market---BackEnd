from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import AnaliseAcoes

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///database/database.db'

# cria a engine de conexão com o banco, que é a conexão viva com ele
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url)

# cria as tabelas do banco, caso não existam
AnaliseAcoes.metadata.create_all(engine)