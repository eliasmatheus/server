from typing import List
from pydantic import BaseModel

from model.author import Author


class AuthorSchema(BaseModel):
    """Define a estrutura para cadastro de novo autor.

    A classe BaseModel da biblioteca Pydantic é usada para definir a estrutura
        dos dados esperados.
    """

    first_name: str = "John"
    last_name: str = "Doe"
    twitter_username: str = "johndoe"
    avatar_url: str = "https://example.com/avatar.png"


class AuthorSearchSchema(BaseModel):
    """Define a estrutura para busca de um autor no banco.

    A busca é feita pelo ID do autor.
    """

    id: int = 1


class AuthorListSchema(BaseModel):
    """Define a estrutura que representa a lista de autores."""

    authors: List[AuthorSchema]


class AuthorUpdateSchema(AuthorSchema):
    """Define a estrutura de um autor retornada no post ou get."""

    id: str = 1


class AuthorViewSchema(AuthorSchema):
    """Define a estrutura de um autor retornada no post ou get."""

    id: str = 1
    articles_count: int = 1


class AuthorDetailsViewSchema(AuthorViewSchema):
    """Define a estrutura de um autor retornada no post ou get."""

    articles_count: int = 1
    articles: List[str] = ["ID do artigo"]


def show_authors(authors: List[Author]) -> dict:
    """Retorna uma lista de autors com a estrutura definida em
        AuthorViewSchema.

    Args:
        authors (list): Lista de objetos Author.

    Returns:
        dict: Dicionário contendo uma lista de autors com a estrutura
            definida em AuthorViewSchema.

    """
    result = []
    for autor in authors:
        result.append(
            {
                "id": autor.id,
                "first_name": autor.first_name,
                "last_name": autor.last_name,
                "twitter_username": autor.twitter_username,
                "articles_count": len(autor.articles),
                "avatar_url": autor.avatar_url,
                "created_at": autor.created_at,
            }
        )

    return {"authors": result}


def show_author(autor: Author) -> dict:
    """Retorna um autor com a estrutura definida em AuthorViewSchema.

    Args:
        autor (Author): Objeto Author.

    Returns:
        dict: Dicionário contendo um autor com a estrutura definida em
            AuthorViewSchema.

    """
    return {
        "id": autor.id,
        "first_name": autor.first_name,
        "last_name": autor.last_name,
        "twitter_username": autor.twitter_username,
        "avatar_url": autor.avatar_url,
        "created_at": autor.created_at,
    }


def show_author_details(autor: Author) -> dict:
    """Retorna um autor com a estrutura definida em AuthorViewSchema.

    Args:
        autor (Author): Objeto Author.

    Returns:
        dict: Dicionário contendo um autor com a estrutura definida em
            AuthorViewSchema.

    """
    return {
        "id": autor.id,
        "first_name": autor.first_name,
        "last_name": autor.last_name,
        "twitter_username": autor.twitter_username,
        "avatar_url": autor.avatar_url,
        "created_at": autor.created_at,
        "articles_count": len(autor.articles),
        "articles": [c.id for c in autor.articles],
        # "articles": show_articles(autor.articles),
    }


class AuthorDeletionSchema(BaseModel):
    """Define a estrutura para remoção de um autor no banco.

    A busca é feita pelo ID do autor.
    """

    message: str
    id: str
