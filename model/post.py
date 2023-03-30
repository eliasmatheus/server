from sqlalchemy import Column, String, Integer, DateTime,  Text
from datetime import datetime
from typing import Union

from model import Base


class BlogPost(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True)
    subtitle = Column(String(80), nullable=False)
    author = Column(String(50), nullable=False)
    date_posted = Column(DateTime, default=datetime.now())
    content = Column(Text, nullable=False)

    def __init__(self, title: str, subtitle: str, author: str, content: str,
                 date_posted: Union[DateTime, None] = None):
        """
        Cria um novo post 

        Arguments:
            title {str}: Título do post
            subtitle {str}: Subtítulo do post
            author {str}: Autor do post
            content {str}: Conteúdo do post

        """
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.content = content

        # se não for informada, será o data exata da inserção no banco
        if date_posted:
            self.date_posted = date_posted
