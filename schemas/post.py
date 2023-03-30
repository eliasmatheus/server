from pydantic import BaseModel
from typing import Optional, List
from model.post import BlogPost


class BlogPostSchema(BaseModel):
    """ Define como um novo post a ser inserido no banco deve ser representado
    """
    title: str = "Título do post"
    subtitle: str = "Subtítulo do post"
    author: str = "Autor do post"
    content: str = "Conteúdo do post"


class BlogPostSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do post.
    """
    id: int = 1


class BlogPostListSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a lista de posts
    """
    posts: List[BlogPostSchema]


class PostViewSchema(BaseModel):
    """ Define como um produto será retornado o post
    """
    id: int = 1
    title: str = "Título do post"
    subtitle: str = "Subtítulo do post"
    author: str = "Autor do post"
    content: str = "Conteúdo do post"


def apresenta_posts(posts: List[BlogPost]):
    """ Retorna uma representação do produto seguindo o schema definido em
        PostViewSchema.
    """
    result = []
    for post in posts:
        result.append({
            "id": post.id,
            "title": post.title,
            "subtitle": post.subtitle,
            "author": post.author,
            "content": post.content,
        })

    return {"posts": result}


def apresenta_post(post: BlogPost):
    """ Retorna uma representação do post seguindo o schema definido em
        PostViewSchema.
    """
    return {
        "id": post.id,
        "title": post.title,
        "subtitle": post.subtitle,
        "author": post.author,
        "content": post.content,
    }


class PostDeletionSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    id: str
