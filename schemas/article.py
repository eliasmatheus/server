from typing import List
from pydantic import BaseModel

from model.article import Article


class ArticleSchema(BaseModel):
    """Define a estrutura para criação de um novo artigo.

    A classe BaseModel da biblioteca Pydantic é usada para definir a estrutura
        dos dados esperados.
    """

    title: str = "Título do artigo"
    subtitle: str = "Subtítulo do artigo"
    author_id: int = 1
    content: str = "Conteúdo do artigo"


class ArticleIDsSchema(BaseModel):
    """Define a estrutura para criação de um novo artigo."""

    id: List[str] = ["ID do artigo"]


class ArticleSearchSchema(BaseModel):
    """Define a estrutura para busca de um artigo no banco.

    A busca é feita pelo ID do artigo.
    """

    id: str = "ID do artigo"


class ArticleListSchema(BaseModel):
    """Define a estrutura que representa a lista de artigos."""

    articles: List[ArticleSchema]


class ArticleUpdateSchema(ArticleSchema):
    """Define a estrutura de um artigo retornada no post ou get."""

    id: str = "ID do artigo"


class ArticleViewSchema(ArticleSchema):
    """Define a estrutura de um artigo retornada no post ou get."""

    id: str = "ID do artigo"
    date_posted: str = "Data de postagem do artigo"


def show_articles(articles: List[Article]) -> dict:
    """Retorna uma lista de artigos com a estrutura definida em
        ArticleViewSchema.

    Args:
        articles (list): Lista de objetos Article.

    Returns:
        dict: Dicionário contendo uma lista de artigos com a estrutura
            definida em ArticleViewSchema.

    """
    result = []
    for article in articles:
        result.append(
            {
                "id": article.id,
                "title": article.title,
                "subtitle": article.subtitle,
                "author_id": article.author_id,
                "content": article.content,
                "date_posted": article.date_posted,
            }
        )

    return {"articles": result}


def show_article(article: Article) -> dict:
    """Retorna um artigo com a estrutura definida em ArticleViewSchema.

    Args:
        article (Article): Objeto Article.

    Returns:
        dict: Dicionário contendo um artigo com a estrutura definida em
            ArticleViewSchema.

    """
    return {
        "id": article.id,
        "title": article.title,
        "subtitle": article.subtitle,
        "author_id": article.author_id,
        "content": article.content,
        "date_posted": article.date_posted,
    }


class ArticleDeletionSchema(BaseModel):
    """Define a estrutura para remoção de um artigo no banco.

    A busca é feita pelo ID do artigo.
    """

    message: str
    id: str
