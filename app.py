from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from sqlalchemy.exc import IntegrityError

from schemas import *
from services import *
from flask_cors import CORS

from services import *

info = Info(title="Flask + React Blog", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
article_tag = Tag(
    name="Artigo",
    description="Adição, edição, visualização e remoção de artigos à base",
)
author_tag = Tag(
    name="Autor",
    description="Adição, edição, visualização e remoção de autores à base",
)


@app.get("/", tags=[home_tag])
def home():
    """
    Redireciona para /openapi.

    Redireciona para a tela do OpenAI que permite a escolha do estilo de
    documentação.
    """
    return redirect("/openapi")


@app.get(
    "/articles",
    tags=[article_tag],
    responses={"200": ArticleListSchema, "404": ErrorSchema},
)
def get_articles():
    """Faz a busca por todos os artigos cadastrados.

    Retorna uma representação da listagem de artigos.
    """
    return get_all_articles()


@app.get(
    "/article/<string:id>",
    tags=[article_tag],
    responses={"200": ArticleViewSchema, "404": ErrorSchema},
)
def get_article(path: SingleArticleViewSchema):
    """Busca um artigo específico à partir do id.

    Retorna uma representação do artigo.
    """

    return get_article_by_id(path)


@app.post(
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


@app.put(
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


@app.delete(
    "/article/<string:id>",
    tags=[article_tag],
    responses={"200": ArticleDeletionSchema, "404": ErrorSchema},
)
def delete_article(path: ArticleSearchSchema):
    """Remove um article à partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    return delete_article_by_id(path)


@app.get(
    "/authors",
    tags=[author_tag],
    responses={"200": AuthorListSchema, "404": ErrorSchema},
)
def get_authors():
    """Faz a busca por todos os autores cadastrados.

    Retorna uma representação da listagem de autores.
    """
    return get_all_authors()


@app.post(
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


@app.get(
    "/author/<int:id>",
    tags=[author_tag],
    responses={"200": AuthorViewSchema, "404": ErrorSchema},
)
def get_author(path: AuthorSearchSchema):
    """Busca um autor específico à partir do id.

    Retorna uma representação do autor.
    """
    author_id = path.id

    return return_author_by_id(author_id)


if __name__ == "__main__":
    app.run(debug=True)
