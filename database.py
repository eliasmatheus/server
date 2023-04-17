from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from config import DATABASE_URI
import os


# importando os elementos definidos no modelo
from shared.models.base import Base


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Ativa o suporte a foreign keys no sqlite3."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


db_url = os.getenv("DB_URL", DATABASE_URI)


# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instância um criador de sessão com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir
if not database_exists(engine.url):
    create_database(engine.url)

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)
