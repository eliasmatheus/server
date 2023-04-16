"""Arquivo com a estrutura da classe Article."""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from model import Base


class Author(Base):
    """Define a estrutura da tabela de autores.

    Args:
        Base (Type[_DeclarativeBase]): Classe base para a criação de novas
            tabelas.
    """

    __tablename__ = "authors"

    id = Column("pk_author", Integer, primary_key=True)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    email = Column(EmailType, nullable=False, unique=True)
    avatar_url = Column(String(90))
    twitter_username = Column(String(60))
    created_at = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o produto e o comentário.
    # Essa relação é implicita, não está salva na tabela 'produto',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    articles = relationship(
        "Article",
        back_populates="author",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        twitter_username: str,
        avatar_url: str,
        id: int = None,
        created_at: Union[DateTime, None] = None,
    ):
        """
        Cadastra um novo autor.

        Args:
            id (int, optional): ID do autor. Se não for especificado, será
                gerado um ID automaticamente.
            first_name (str): Primeiro nome do autor.
            last_name (str): Sobrenome do autor.
            twitter_username (str, optional): Usuário do twitter do autor.
            avatar_url (str, optional): URL da imagem de avatar do autor.

        Returns:
            None
        """
        if id:
            self.id = id

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.twitter_username = twitter_username
        self.avatar_url = avatar_url

        # se não for informada, será o data exata da inserção no banco
        if created_at:
            self.created_at = created_at
