from typing import List
from pydantic import BaseModel

from models import Article
from schemas import AuthorViewSchema


class ArticleSchema(BaseModel):
    """Define a estrutura para criação de um novo artigo.

    A classe BaseModel da biblioteca Pydantic é usada para definir a estrutura
        dos dados esperados.
    """

    title: str = "Título do artigo"
    subtitle: str = "Subtítulo do artigo"
    author_id: int = 1
    content: str = "Conteúdo do artigo"


class ArticlePreviewSchema(BaseModel):
    """Define a estrutura de preview de um artigo."""

    id: str = "ID do artigo"
    title: str = "Título do artigo"
    subtitle: str = "Subtítulo do artigo"
    author_id: int = 1
    created_at: str = "Data de postagem do artigo"


class ArticleIDsSchema(BaseModel):
    """Define a estrutura para criação de um novo artigo."""

    id: List[str] = ["ID do artigo"]


class ArticleSearchSchema(BaseModel):
    """Define a estrutura para busca de um artigo no banco.

    A busca é feita pelo ID do artigo.
    """

    id: str = "ID do artigo"


class ArticleUpdateSchema(ArticleSchema):
    """Define a estrutura de um artigo retornada no post ou get."""

    id: str = "ID do artigo"


class ArticleViewSchema(ArticleSchema):
    """Define a estrutura de um artigo retornada no post ou get."""

    id: str = "ID do artigo"
    content: str = "Conteúdo do artigo"
    created_at: str = "Data de postagem do artigo"


class ArticleListSchema(BaseModel):
    """Define a estrutura que representa a lista de artigos."""

    articles: List[ArticlePreviewSchema]


class ArticleDetailsViewSchema(ArticleViewSchema):
    """Define a estrutura de um artigo retornada no post ou get."""

    author: AuthorViewSchema = AuthorViewSchema()


class ArticleDeletionSchema(BaseModel):
    """Define a estrutura para remoção de um artigo no banco.

    A busca é feita pelo ID do artigo.
    """

    message: str
    id: str


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
                "created_at": article.created_at,
            }
        )

    return {"articles": result}


def show_article_details(article: Article) -> dict:
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
        "author": {
            "id": article.author.id,
            "first_name": article.author.first_name,
            "last_name": article.author.last_name,
            # "email": article.author.email,
            "avatar_url": article.author.avatar_url,
            "twitter_username": article.author.twitter_username,
        },
        "content": article.content,
        "created_at": article.created_at,
    }


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
        "created_at": article.created_at,
    }
