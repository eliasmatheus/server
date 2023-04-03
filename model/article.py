import re
from sqlalchemy import Column, String, Integer, DateTime, Text
from datetime import datetime
from typing import Union
from unidecode import unidecode
from model import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(String(50), primary_key=True)
    title = Column(String(90), unique=True)
    subtitle = Column(String(200), nullable=False)
    author = Column(String(50), nullable=False)
    date_posted = Column(DateTime, default=datetime.now())
    content = Column(Text, nullable=False)

    def __init__(
        self,
        id: str,
        title: str,
        subtitle: str,
        author: str,
        content: str,
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
        """Gera um id para o artigo baseado no título."""
        id_string = self.remove_special_chars(title)
        id_string = self.replace_spaces(id_string)
        id_string = self.add_date_prefix(id_string)
        id_string = self.limit_length(id_string, 50)
        return id_string.lower()

    def remove_special_chars(self, title):
        """Remove caracteres especiais do título."""
        return re.sub(r"[^a-zA-Z0-9\s]", "", unidecode(title))

    def replace_spaces(self, id_string):
        """Substitui espaços em branco por hífens."""
        return re.sub(r"\s+", "-", id_string)

    def add_date_prefix(self, id_string):
        """Adiciona a data no início da string."""
        date = datetime.now().strftime("%Y-%m-%d")
        return f"{date}-{id_string}"

    def limit_length(self, id_string, length):
        """Limita o comprimento da string."""
        return id_string[:length]
