from pydantic import BaseModel
from typing import Optional, List
from model.article import Article


class ArticleSchema(BaseModel):
    """Define estrutura para um novo artigo a ser inserido no banco."""

    title: str = "Título do artigo"
    subtitle: str = "Subtítulo do artigo"
    author: str = "Autor do artigo"
    content: str = "Conteúdo do artigo"


class ArticleSearchSchema(BaseModel):
    """Define estrutura para busca de um artigo no banco.

    A busca é feita pelo id do artigo.
    """

    id: int = 2


class ArticleListSchema(BaseModel):
    """Define estrutura que representa a lista de artigos."""

    articles: List[ArticleSchema]


class ArticleViewSchema(BaseModel):
    """Define estrutura de um artigo retornado no post ou get."""

    id: int = 1
    title: str = "Título do artigo"
    url_compatible_title: str = (
        "Alternativa de ID com base no título do artigo"
    )
    subtitle: str = "Subtítulo do artigo"
    author: str = "Autor do artigo"
    content: str = "Conteúdo do artigo"
    date_posted: str = "Data de postagem do artigo"


def show_articles(article: List[Article]):
    """Retorna uma representação do artigo.

    Segue o schema definido em ArticleViewSchema.
    """
    result = []
    for article in article:
        result.append(
            {
                "id": article.id,
                "title": article.title,
                "url_compatible_title": article.url_compatible_title,
                "subtitle": article.subtitle,
                "author": article.author,
                "content": article.content,
                "date_posted": article.date_posted,
            }
        )

    return {"articles": result}


def show_article(article: Article):
    """Retorna uma representação do artigo.

    Segue o schema definido em ArticleViewSchema.
    """
    return {
        "id": article.id,
        "title": article.title,
        "url_compatible_title": article.url_compatible_title,
        "subtitle": article.subtitle,
        "author": article.author,
        "content": article.content,
        "date_posted": article.date_posted,
    }


class ArticleDeletionSchema(BaseModel):
    """Define estrutura para remoção de um artigo no banco.

    A busca é feita pelo id do artigo.
    """

    message: str
    id: str
