from flask_openapi3 import Tag, APIBlueprint

from ..schemas import *
from ..services import *
from shared.schemas import ErrorSchema


article_tag = Tag(
    name="Artigo",
    description="Adição, edição, visualização e remoção de artigos à base",
)

article_bp = APIBlueprint("article", __name__)


@article_bp.get(
    "/articles",
    tags=[article_tag],
    responses={"200": ArticleListSchema, "404": ErrorSchema},
)
def get_articles():
    """Faz a busca por todos os artigos cadastrados.

    Retorna uma representação da listagem de artigos.
    """
    return get_all_articles()


@article_bp.get(
    "/article/<string:id>",
    tags=[article_tag],
    responses={"200": ArticleDetailsViewSchema, "404": ErrorSchema},
)
def get_article(path: ArticleSearchSchema):
    """Busca um artigo específico à partir do id.

    Retorna uma representação do artigo.
    """

    return get_article_by_id(path)


@article_bp.post(
    "/article",
    tags=[article_tag],
    responses={
        "200": ArticleViewSchema,
        "409": ErrorSchema,
        "400": ErrorSchema,
    },
)
def post_article(form: ArticleSchema):
    """Adiciona um novo artigo à base de dados.

    Retorna uma representação dos artigos.
    """
    return add_article(form)


@article_bp.put(
    "/article",
    tags=[article_tag],
    responses={
        "200": ArticleViewSchema,
        "409": ErrorSchema,
        "400": ErrorSchema,
    },
)
def put_article(form: ArticleUpdateSchema):
    """Edita um artigo já existente na base de dados.

    Retorna uma representação dos artigos.
    """
    return edit_article(form)


@article_bp.delete(
    "/article/<string:id>",
    tags=[article_tag],
    responses={"200": ArticleDeletionSchema, "404": ErrorSchema},
)
def delete_article(path: ArticleSearchSchema):
    """Remove um article à partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    return delete_article_by_id(path)
