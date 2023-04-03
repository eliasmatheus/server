import re
from sqlalchemy import Column, String, Integer, DateTime, Text
from datetime import datetime
from typing import Union
from unidecode import unidecode
from model import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(90), unique=True)
    url_compatible_title = Column(String(50), unique=True)
    subtitle = Column(String(200), nullable=False)
    author = Column(String(50), nullable=False)
    date_posted = Column(DateTime, default=datetime.now())
    content = Column(Text, nullable=False)

    def __init__(
        self,
        title: str,
        subtitle: str,
        author: str,
        content: str,
        date_posted: Union[DateTime, None] = None,
    ):
        """
        Cria um novo artigo.

        Arguments:
            title {str}: Título do artigo
            subtitle {str}: Subtítulo do artigo
            author {str}: Autor do artigo
            content {str}: Conteúdo do artigo

        """
        self.title = title
        self.url_compatible_title = self.generate_id(title)
        self.subtitle = subtitle
        self.author = author
        self.content = content

        # se não for informada, será o data exata da inserção no banco
        if date_posted:
            self.date_posted = date_posted

    def generate_id(self, title):
        """Gera um id para o artigo baseado no título."""
        # Cria uma string com a data atual no formato YYYY-MM-DD
        date = datetime.now().strftime("%Y-%m-%d")

        # Transforma em ASCII
        id_string = unidecode(title)
        # Remove os espaços em branco duplicados
        id_string = re.sub(r"[^a-zA-Z0-9\s]", "", id_string)
        # Remove todos os caracteres que não são letras ou números
        id_string = re.sub("[^a-zA-Z0-9]+$", "", id_string)
        # Substitui todos os espaços em branco por hífens
        id_string = re.sub(r"\s+", "-", id_string)
        # Converte toda a string para letras minúsculas
        id_string = id_string.lower()

        return date + "-" + id_string
