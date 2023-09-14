from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
import os

# importando os elementos definidos no modelo
from .base import Base
from models.article import Article
from models.author import Author


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Ativa o suporte a foreign keys no sqlite3."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# define o caminho do banco
db_path = "database/"

# Verifica se o diretório não existe
if not os.path.exists(db_path):
    # então cria o diretório
    os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = "sqlite:///%s/db.sqlite3" % db_path

# verifica se a variável de ambiente DB_URL existe
db_url = os.getenv("DB_URL", db_url)


# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instância um criador de sessão com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir
if not database_exists(engine.url):
    create_database(engine.url)

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)
