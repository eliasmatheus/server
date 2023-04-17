from flask import Flask
from flask_testing import TestCase
import os

from modules.author import author_bp
from models import Author, Session

# from modules.author.schemas import AuthorSchema


class TestAuthor(TestCase):
    def create_app(self):
        app = Flask(__name__)

        app.register_blueprint(author_bp)

        return app

    def setUp(self):
        self.app.config["TESTING"] = True

        # cria sessão
        self.session = Session()

        # cria autor para ser utilizado nos testes
        self.author_data = {
            "first_name": "Teste",
            "last_name": "Autor",
            "email": "teste.autor@teste.com.br",
            "twitter_username": "twitter_username",
            "avatar_url": "avatar_url",
        }
        self.author = Author(**self.author_data)

        # adiciona autor na sessão
        self.session.add(self.author)

        # efetiva a inserção na base de dados
        self.session.commit()

    def tearDown(self):
        # verifica se o autor ainda existe na base de dados
        author = (
            self.session.query(Author).filter_by(id=self.author.id).first()
        )

        if author:
            # remove autor inserido nos testes da sessão
            self.session.delete(self.author)

            # efetiva a exclusão na base de dados
            self.session.commit()

    def test_get_all_authors(self):
        response = self.client.get("/authors")

        assert response.status_code == 200
        assert response.content_type == "application/json"
        assert isinstance(response.json, dict)
        assert "authors" in response.json

    def test_add_author(self):
        with self.client:
            # define dados do autor a ser adicionado
            new_author_data = {
                "first_name": "Novo",
                "last_name": "Autor",
                "email": "novo.autor@teste.com.br",
                "twitter_username": "novo.autor@teste.com.br",
                "avatar_url": "novo.autor@teste.com.br",
            }
            # author_schema = Author().load(new_author_data)

            # faz requisição POST
            response = self.client.post("/author", data=new_author_data)

            # verifica se a resposta é 200
            self.assertEqual(response.status_code, 200)

            # verifica se o novo autor foi adicionado na base
            author_id = response.json["id"]
            authors = self.session.query(Author).all()

            # TODO: verificar se o autor foi adicionado na base de dados
            # self.assertEqual(len(authors), 2)

            # verifica se os dados do autor adicionado são os mesmos que foram
            # enviados
            # added_author = authors[1]
            # self.assertEqual(added_author.first_name, "Novo")
            # self.assertEqual(added_author.last_name, "Autor")
            # self.assertEqual(added_author.email, "novo.autor@teste.com.br")

    def test_add_author_with_duplicate_email(self):
        with self.client:
            # define dados do autor a ser adicionado
            new_author_data = {
                "first_name": "Novo",
                "last_name": "Autor",
                "email": "teste.autor@teste.com.br",
                "twitter_username": "novo.autor@teste.com.br",
                "avatar_url": "novo.autor@teste.com.br",
            }
            # author_schema = AuthorSchema().load(new_author_data)

            # faz requisição POST
            response = self.client.post("/author", data=new_author_data)

            # verifica se a resposta é 409 (conflito)
            self.assertEqual(response.status_code, 409)

            # verifica se a mensagem de erro foi retornada corretamente
            expected_error_message = {
                "message": "Autor com mesmo email já salvo na base :/"
            }
            self.assertEqual(response.json, expected_error_message)

            # TODO: verificar se o autor foi adicionado na base de dados
            # verifica se não foi adicionado um novo autor com o mesmo email
            authors = self.session.query(Author).all()
            # self.assertEqual(len(authors), 2)

    def test_return_author_by_id(self):
        with self.client:
            # faz requisição GET para um id válido
            response = self.client.get("/author/{}".format(self.author.id))

            # verifica se a resposta é 200
            self.assertEqual(response.status_code, 200)

            # verifica se os dados do autor retornado são os mesmos que foram
            # adicionados
            self.assertEqual(response.json["id"], self.author.id)
            self.assertEqual(
                response.json["first_name"], self.author.first_name
            )
            self.assertEqual(response.json["last_name"], self.author.last_name)
            self.assertEqual(response.json["email"], self.author.email)
            self.assertEqual(
                response.json["twitter_username"], self.author.twitter_username
            )
            self.assertEqual(
                response.json["avatar_url"], self.author.avatar_url
            )

            # faz requisição GET para um id inválido
            response = self.client.get("/author/{}".format(4564645))

            # verifica se a resposta é 404
            self.assertEqual(response.status_code, 404)

            # verifica se a mensagem de erro foi retornada corretamente
            expected_error_message = {
                "message": "Autor não encontrado na base :/"
            }
            self.assertEqual(response.json, expected_error_message)

    def test_edit_author(self):
        with self.client:
            # define dados do autor a ser atualizado
            author_data = {
                "id": self.author.id,
                "first_name": "Novo",
                "last_name": "Autor",
                "email": "teste.autor@teste.com.br",
                "twitter_username": "novo.autor@teste.com.br",
                "avatar_url": "novo.autor@teste.com.br",
            }

            # faz requisição PUT
            response = self.client.put("/author", data=author_data)

            # verifica se a resposta é 200
            self.assertEqual(response.status_code, 200)

            self.assertEqual(response.json["id"], self.author.id)
            self.assertEqual(
                response.json["first_name"], author_data["first_name"]
            )
            self.assertEqual(response.json["email"], author_data["email"])
            self.assertEqual(
                response.json["twitter_username"],
                author_data["twitter_username"],
            )
            self.assertEqual(
                response.json["avatar_url"], author_data["avatar_url"]
            )

    def test_delete_author_by_id(self):
        with self.client:
            # faz requisição DELETE para um id válido
            response = self.client.delete("/author/{}".format(self.author.id))

            # verifica se a resposta é 200
            self.assertEqual(response.status_code, 200)

            # verifica se a mensagem de confirmação foi retornada corretamente
            expected_response = {
                "message": "Autor e seus artigos excluídos com sucesso",
                "id": self.author.id,
            }
            self.assertEqual(
                response.json["message"], expected_response["message"]
            )
            self.assertEqual(response.json["id"], self.author.id)

            # TODO: verifica se o autor foi removido da base
            # verifica se o autor foi removido da base
            # authors = self.session.query(Author).all()
            # self.assertEqual(len(authors), 0)

            # faz requisição DELETE para um id inválido
            response = self.client.delete("/author/{}".format(4564645))

            # verifica se a resposta é 404
            self.assertEqual(response.status_code, 404)

            # verifica se a mensagem de erro foi retornada corretamente
            expected_error_message = {
                "message": "Autor não encontrado na base :/"
            }
            self.assertEqual(response.json, expected_error_message)
