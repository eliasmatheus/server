from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from sqlalchemy.exc import IntegrityError

from model import Session, Article
from logger import logger
from schemas import *
from flask_cors import CORS

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
    logger.debug(f"Coletando artigos ")

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    articles = session.query(Article).all()

    print(articles)

    if not articles:
        # se não há artigos cadastrados
        return {"articles": []}, 200
    else:
        logger.debug(f"%d artigos encontrados" % len(articles))
        # retorna a representação de artigos
        print(articles)
        return show_articles(articles), 200


@app.get(
    "/article/<string:id>",
    tags=[article_tag],
    responses={"200": ArticleViewSchema, "404": ErrorSchema},
)
def get_article(path: ArticleSearchSchema):
    """Busca um artigo específico à partir do id.

    Retorna uma representação do artigo.
    """
    article_id = path.id

    logger.debug(f"Coletando artigo com ID: {article_id} ")

    # criando conexão com a base
    session = Session()

    # fazendo a busca
    article = session.query(Article).filter(Article.id == article_id).one()

    if not article:
        # se o artigo não foi encontrado
        error_msg = "Artigo não encontrado na base :/"
        log_error_msg = (
            f"Erro ao buscar artigo com ID: #'{article_id}', {error_msg}"
        )

        logger.warning(log_error_msg)
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Artigo com ID: #{article_id} encontrado com sucesso")
        # retorna a representação de artigos
        print(article)
        return show_article(article), 200


@app.post(
    "/article",
    tags=[article_tag],
    responses={
        "200": ArticleViewSchema,
        "409": ErrorSchema,
        "400": ErrorSchema,
    },
)
def add_article(form: ArticleSchema):
    """Adiciona um novo artigo à base de dados.

    Retorna uma representação dos artigos.
    """
    article = Article(**form.dict())

    print(article)

    logger.debug(f"Adicionando artigo com título: '{article.title}'")

    try:
        # criando conexão com a base
        session = Session()
        # adicionando artigo
        session.add(article)
        # efetivando o comando de adição de novo artigo na tabela
        session.commit()

        logger.debug(f"Adicionado artigo com título: '{article.title}'")

        return show_article(article), 200

    except IntegrityError as e:
        # como a duplicidade do título é a provável razão do IntegrityError
        error_msg = "Artigo de mesmo título já salvo na base :/"
        log_error_msg = (
            f"Erro ao adicionar artigo '{article.title}', {error_msg}"
        )
        logger.warning(log_error_msg)

        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo artigo :/"
        log_error_msg = (
            f"Erro ao adicionar artigo '{article.title}', {error_msg}"
        )
        logger.warning(log_error_msg)

        return {"mesage": error_msg}, 400


@app.put(
    "/article",
    tags=[article_tag],
    responses={
        "200": ArticleViewSchema,
        "409": ErrorSchema,
        "400": ErrorSchema,
    },
)
def edit_article(form: ArticleUpdateSchema):
    """Edita um artigo já existente na base de dados.

    Retorna uma representação dos artigos.
    """
    article = Article(**form.dict())

    # criando conexão com a base
    session = Session()

    # fazendo a busca
    article_id = form.id
    old_article = (
        session.query(Article).filter(Article.id == article_id).first()
    )

    logger.debug(f"Editando artigo de ID: '{old_article.id}'")

    try:
        # edita os valores do artigo
        old_article.title = article.title
        old_article.subtitle = article.subtitle
        old_article.author = article.author
        old_article.content = article.content

        # efetivando o comando de edição do artigo na tabela
        session.commit()
        logger.debug(f"Editado artigo de ID: '{article.title}'")

        return show_article(article), 200

    except IntegrityError as e:
        # como a duplicidade do título é a provável razão do IntegrityError
        error_msg = "Artigo de mesmo título já salvo na base :/"
        log_error_msg = (
            f"Erro ao adicionar artigo '{article.title}', {error_msg}"
        )
        logger.warning(log_error_msg)

        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo artigo :/"
        log_error_msg = (
            f"Erro ao adicionar artigo '{article.title}', {error_msg}"
        )
        logger.warning(log_error_msg)

        return {"message": error_msg}, 400


@app.delete(
    "/article",
    tags=[article_tag],
    responses={"200": ArticleDeletionSchema, "404": ErrorSchema},
)
def delete_article(query: ArticleSearchSchema):
    """Remove um article à partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    article_id = query.id
    print(article_id)
    logger.debug(f"Removendo artigo com ID: #{article_id}")

    # criando conexão com a base
    session = Session()

    # fazendo a remoção
    count = session.query(Article).filter(Article.id == article_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Artigo com ID: #{article_id} excluído com sucesso")
        return {"message": "Artigo removido", "id": article_id}
    else:
        # se o artigo não foi encontrado
        error_msg = "Artigo não encontrado na base :/"
        log_error_msg = (
            f"Erro ao remover artigo com ID: '{article_id}', {error_msg}"
        )
        logger.warning(log_error_msg)

        return {"message": error_msg}, 404


if __name__ == "__main__":
    app.run(debug=True)
