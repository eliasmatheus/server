from sqlalchemy.exc import IntegrityError
from logger import logger
from models import Author
from ..schemas import *

from models import Session

# from models import Session


def get_all_authors():
    """Faz a busca por todos os autores cadastrados.

    Retorna uma representação da listagem de autores.
    """
    logger.debug(f"Coletando autores")

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    authors = session.query(Author).all()

    print(authors)

    if not authors:
        # se não há autores cadastrados
        return {"authors": []}, 200
    else:
        logger.debug(f"%d autores encontrados" % len(authors))
        # retorna a representação de autores
        print(authors)
        return show_authors(authors), 200


def return_author_by_id(path: AuthorSearchSchema):
    """Busca um autor específico à partir do id.

    Retorna uma representação do autor.
    """
    author_id = path.id

    logger.debug(f"Coletando autor com ID: {author_id} ")

    # criando conexão com a base
    session = Session()

    # faz a busca pelo autor
    author = session.query(Author).filter(Author.id == author_id).one_or_none()

    if not author:
        # se o autor não foi encontrado
        error_msg = "Autor não encontrado na base :/"
        log_error_msg = (
            f"Erro ao buscar autor com ID: #'{author_id}', {error_msg}"
        )

        logger.warning(log_error_msg)
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Autor com ID: #{author_id} encontrado com sucesso")
        # retorna a representação de autores
        print(author)
        return show_author_details(author), 200


def add_author(form: AuthorSchema):
    """Adiciona um novo autor à base de dados.

    Retorna uma representação dos autores.
    """
    author = Author(**form.dict())

    print(author)

    logger.debug(f"Adicionando autor com título: '{author.first_name}'")

    try:
        # criando conexão com a base
        session = Session()
        # adicionando autor
        session.add(author)
        # efetivando o comando de adição de novo autor na tabela
        session.commit()

        logger.debug(f"Adicionado autor com título: '{author.first_name}'")

        return show_author(author), 200

    except IntegrityError as e:
        # como a duplicidade do email é a provável razão do IntegrityError
        error_msg = "Autor com mesmo email já salvo na base :/"
        log_error_msg = (
            f"Erro ao adicionar autor '{author.first_name}', {error_msg}"
        )
        logger.warning(log_error_msg)

        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo autor :/"
        log_error_msg = (
            f"Erro ao adicionar autor '{author.first_name}', {error_msg}"
        )
        logger.warning(log_error_msg)
        logger.warning(author)

        return {"message": error_msg}, 400


def edit_author(form: AuthorUpdateSchema):
    """Edita um autor já existente na base de dados.

    Retorna uma representação dos autores.
    """
    author = Author(**form.dict())

    # criando conexão com a base
    session = Session()

    author_id = form.id
    # fazendo a busca
    old_author = (
        session.query(Author).filter(Author.id == author_id).one_or_none()
    )

    if not old_author:
        # se o autor não foi encontrado
        error_msg = "Autor não encontrado na base :/"
        log_error_msg = (
            f"Erro ao buscar autor com ID: #'{author_id}', {error_msg}"
        )

        logger.warning(log_error_msg)
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Editando autor de ID: '{old_author.id}'")

        try:
            # edita os valores do autor
            old_author.first_name = author.first_name
            old_author.last_name = author.last_name
            old_author.avatar_url = author.avatar_url
            old_author.twitter_username = author.twitter_username

            # efetivando o comando de edição do autor na tabela
            session.commit()
            logger.debug(f"Editado autor de ID: '{old_author.id}'")

            return show_author(author), 200

        except Exception as e:
            # caso um erro fora do previsto
            error_msg = "Não foi possível salvar autor :/"
            log_error_msg = (
                f"Erro ao editar autor '{old_author.id}', {error_msg}"
            )
            logger.warning(log_error_msg)

            return {"message": error_msg}, 400


def delete_author_by_id(path: AuthorSearchSchema):
    """Remove um author à partir do id informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    author_id = path.id

    print(author_id)
    logger.debug(f"Excluindo autor com ID: #{author_id}")

    # criando conexão com a base
    session = Session()

    # fazendo a remoção
    count = session.query(Author).filter(Author.id == author_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Autor com ID: #{author_id} excluído com sucesso")
        return {"message": "Autor e seus artigos excluídos", "id": author_id}
    else:
        # se o autor não foi encontrado
        error_msg = "Autor não encontrado na base :/"
        log_error_msg = (
            f"Erro ao remover autor com ID: '{author_id}', {error_msg}"
        )
        logger.warning(log_error_msg)

        return {"message": error_msg}, 404
