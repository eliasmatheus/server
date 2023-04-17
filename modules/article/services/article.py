from sqlalchemy.exc import IntegrityError
from logger import logger

from models import Article, Author, Session
from ..schemas import *


def get_all_articles():
    """Faz a busca por todos os artigos cadastrados.

    Retorna uma representação da listagem de artigos.
    """
    logger.debug(f"Coletando artigos ")

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    articles = session.query(Article).all()

    if not articles:
        # se não há artigos cadastrados
        return {"articles": []}, 200
    else:
        logger.debug(f"%d artigos encontrados" % len(articles))
        # retorna a representação de artigos
        print(articles)
        return show_articles(articles), 200


def get_article_by_id(path: ArticleSearchSchema):
    """Busca um artigo específico à partir do id.

    Retorna uma representação do artigo.
    """
    article_id = path.id

    logger.debug(f"Coletando artigo com ID: {article_id} ")

    # criando conexão com a base
    session = Session()

    # fazendo a busca
    article = (
        session.query(Article)
        .join(Author)
        .filter(Article.id == article_id)
        .one_or_none()
    )

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
        return show_article_details(article), 200


def add_article(form: ArticleSchema):
    """Adiciona um novo artigo à base de dados.

    Retorna uma representação dos artigos.
    """
    article = Article(**form.dict())

    logger.debug(f"Adicionando artigo com título: '{article.title}'")

    try:
        # criando conexão com a base
        session = Session()
        # adicionando artigo
        session.add(article)
        # efetivando o comando de adição de novo artigo na tabela
        session.commit()

        logger.debug(f"Adicionado artigo com título: '{article.title}'")

        return show_article_details(article), 200

    except IntegrityError as e:
        invalid_author = (
            "(sqlite3.IntegrityError) FOREIGN KEY constraint failed"
        )

        # caso o autor não exista, teremos um erro de FOREIGN KEY constraint
        if e.args[0] == invalid_author:
            error_msg = "Autor não encontrado :/"
            log_error_msg = (
                f"Erro ao adicionar artigo '{article.title}', {error_msg}"
            )
            logger.warning(log_error_msg)

            return {"message": error_msg}, 409

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

    print(old_article)

    logger.debug(f"Editando artigo de ID: '{old_article.id}'")

    try:
        # edita os valores do artigo
        old_article.title = article.title
        old_article.subtitle = article.subtitle
        old_article.author_id = article.author_id
        old_article.content = article.content

        # efetivando o comando de edição do artigo na tabela
        session.commit()
        logger.debug(f"Editado artigo de ID: '{article.title}'")

        # fazendo a busca
        article = (
            session.query(Article)
            .join(Author)
            .filter(Article.id == article_id)
            .one_or_none()
        )

        return show_article_details(article), 200

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


def delete_article_by_id(path: ArticleSearchSchema):
    """Remove um article à partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    article_id = path.id

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
