"""Arquivo com a estrutura da classe Article."""

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from datetime import datetime
from typing import Union
from model import Base
from shared.utils.strings import (
    add_date_prefix,
    limit_length,
    remove_special_chars,
    replace_spaces,
)


class Article(Base):
    """Define a estrutura da tabela de artigos.

    Args:
        Base (Type[_DeclarativeBase]): Classe base para a criação de novas
            tabelas.
    """

    __tablename__ = "articles"

    id = Column(String(50), primary_key=True)
    title = Column(String(90), unique=True)
    subtitle = Column(String(200), nullable=False)
    date_posted = Column(DateTime, default=datetime.now())
    content = Column(Text, nullable=False)

    # Definição do relacionamento entre o comentário e um produto.
    # Aqui está sendo definido a coluna 'produto' que vai guardar
    # a referencia ao produto, a chave estrangeira que relaciona
    # um produto ao comentário.
    author = Column(Integer, ForeignKey("authors.pk_author"), nullable=False)

    def __init__(
        self,
        title: str,
        subtitle: str,
        author: str,
        content: str,
        id: str = None,
        date_posted: Union[DateTime, None] = None,
    ):
        """
        Cria um novo artigo.

        Args:
            id (str, optional): ID do artigo. Se não for especificado, será
                gerado um ID baseado no título do artigo.
            title (str): Título do artigo.
            subtitle (str): Subtítulo do artigo.
            author (str): Autor do artigo.
            content (str): Conteúdo do artigo.
            date_posted (datetime, optional): Data de publicação do artigo. Se
                não for especificada, a data de publicação será a data atual.

        Returns:
            None
        """
        # Se não for informado um ID, será gerado um baseado no título
        if not id:
            id = self.generate_id(title)

        # Se o ID for informado, o valor não será alterado mesmo que o título
        # seja, para evitar problemas de integridade referencial
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.content = content

        # se não for informada, será o data exata da inserção no banco
        if date_posted:
            self.date_posted = date_posted

    def generate_id(self, title):
        print(title)
        """Gera um id para o artigo baseado no título."""
        id_string = remove_special_chars(title)
        id_string = replace_spaces(id_string)
        id_string = add_date_prefix(id_string)
        id_string = limit_length(id_string, 50)
        return id_string.lower()
