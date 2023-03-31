from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, BlogPost
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Flask Blog", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
post_tag = Tag(
    name="Blog Post", description="Adição, edição, visualização e remoção de posts à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.get('/posts', tags=[post_tag], responses={"200": BlogPostListSchema, "404": ErrorSchema})
def get_posts():
    """Faz a busca por todos os posts cadastrados

    Retorna uma representação da listagem de posts.
    """
    logger.debug(f"Coletando posts ")

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    posts = session.query(BlogPost).all()

    if not posts:
        # se não há posts cadastrados
        return {"posts": []}, 200
    else:
        logger.debug(f"%d posts encontrados" % len(posts))
        # retorna a representação de posts
        print(posts)
        return apresenta_posts(posts), 200


@app.get('/post/<int:id>', tags=[post_tag], responses={"200": PostViewSchema, "404": ErrorSchema})
def get_post(path: BlogPostSearchSchema):
    """Busca um post específico à partir do id

    Retorna uma representação do post.
    """
    post_id = path.id

    logger.debug(f"Coletando post com ID: {post_id} ")

    # criando conexão com a base
    session = Session()
    # fazendo a busca

    post = session.query(BlogPost).filter(
        BlogPost.id == post_id).one()

    if not post:
        # se o post não foi encontrado
        error_msg = "Post não encontrado na base :/"
        logger.warning(
            f"Erro ao buscar post com ID: #'{post_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"post com ID: #{post_id} encontrado com sucesso")
        # retorna a representação de posts
        print(post)
        return apresenta_post(post), 200


@app.post('/post', tags=[post_tag],
          responses={"200": PostViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_post(form: BlogPostSchema):
    """Adiciona um novo post à base de dados

    Retorna uma representação dos posts.
    """
    post = BlogPost(title=form.title, subtitle=form.subtitle,
                    author=form.author, content=form.content)

    logger.debug(f"Adicionando post de título: '{post.title}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando post
        session.add(post)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado post de nome: '{post.title}'")
        return apresenta_post(post), 200

    except IntegrityError as e:
        # como a duplicidade do título é a provável razão do IntegrityError
        error_msg = "Post de mesmo título já salvo na base :/"
        logger.warning(
            f"Erro ao adicionar post '{post.title}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao adicionar post '{post.title}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.put('/post', tags=[post_tag],
         responses={"200": PostViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def edit_post(query: PostViewSchema):
    """Edita um post já existente na base de dados

    Retorna uma representação dos posts.
    """
    edited_post = BlogPost(title=query.title, subtitle=query.subtitle,
                           author=query.author, content=query.content)

    # criando conexão com a base
    session = Session()

    # fazendo a busca
    post_id = query.id
    post = session.query(BlogPost).filter(BlogPost.id == post_id).first()

    logger.debug(f"Editando post de ID: '{post.id}'")
    try:
        # edita os valores do post
        post.title = edited_post.title
        post.subtitle = edited_post.subtitle
        post.author = edited_post.author
        post.content = edited_post.content

        # efetivando o comando de edição do item na tabela
        session.commit()
        logger.debug(f"Editando post de ID: '{edited_post.title}'")
        return apresenta_post(edited_post), 200

    except IntegrityError as e:
        # como a duplicidade do título é a provável razão do IntegrityError
        error_msg = "Post de mesmo título já salvo na base :/"
        logger.warning(
            f"Erro ao adicionar post '{edited_post.title}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao adicionar post '{edited_post.title}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.delete('/post', tags=[post_tag],
            responses={"200": PostDeletionSchema, "404": ErrorSchema})
def delete_post(query: BlogPostSearchSchema):
    """Deleta um post à partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    post_id = query.id
    print(post_id)
    logger.debug(f"Deletando post com ID: #{post_id}")

    # criando conexão com a base
    session = Session()

    # fazendo a remoção
    count = session.query(BlogPost).filter(
        BlogPost.id == post_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"post com ID: #{post_id} excluído com sucesso")
        return {"message": "Post removido", "id": post_id}
    else:
        # se o post não foi encontrado
        error_msg = "Post não encontrado na base :/"
        logger.warning(
            f"Erro ao deletar post com ID: #'{post_id}', {error_msg}")
        return {"message": error_msg}, 404


if __name__ == '__main__':
    app.run(debug=True)
