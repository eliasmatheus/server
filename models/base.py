from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_repr import PrettyRepresentableBase

# cria uma classe Base para o instanciamento de novos objetos/tabelas
Base = declarative_base(cls=PrettyRepresentableBase)
