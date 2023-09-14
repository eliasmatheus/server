from flask_openapi3 import Tag, APIBlueprint

from schemas import *
from services import *

from schemas import ErrorSchema

author_tag = Tag(
    name="Autor",
    description="Adição, edição, visualização e remoção de autores à base",
)

author_bp = APIBlueprint("author", __name__)


@author_bp.get(
    "/authors",
    tags=[author_tag],
    responses={"200": AuthorListSchema, "404": ErrorSchema},
)
def get_authors():
    """Faz a busca por todos os autores cadastrados.

    Retorna uma representação da listagem de autores.
    """
    return get_all_authors()


@author_bp.get(
    "/author/<int:id>",
    tags=[author_tag],
    responses={"200": AuthorDetailsViewSchema, "404": ErrorSchema},
)
def get_author(path: AuthorSearchSchema):
    """Busca um autor específico à partir do id.

    Retorna uma representação do autor.
    """

    return return_author_by_id(path)


@author_bp.post(
    "/author",
    tags=[author_tag],
    responses={
        "200": AuthorViewSchema,
        "409": ErrorSchema,
        "400": ErrorSchema,
    },
)
def post_author(form: AuthorSchema):
    """Adiciona um novo autor à base de dados.

    Retorna uma representação dos autores.
    """
    return add_author(form)


@author_bp.put(
    "/author",
    tags=[author_tag],
    responses={
        "200": AuthorViewSchema,
        "409": ErrorSchema,
        "400": ErrorSchema,
    },
)
def put_author(form: AuthorUpdateSchema):
    """Edita um autor já existente na base de dados.

    Retorna uma representação dos autores.
    """
    return edit_author(form)


@author_bp.delete(
    "/author/<int:id>",
    tags=[author_tag],
    responses={
        "200": AuthorDeletionSchema,
        "404": ErrorSchema,
        "400": ErrorSchema,
    },
)
def delete_author(path: AuthorSearchSchema):
    """Remove um author à partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    return delete_author_by_id(path)
