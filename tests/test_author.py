from flask import Flask
from flask_testing import TestCase
from database import Session
from modules.author.models.author import Author
from modules.author.routes import author_bp
from modules.author.schemas import AuthorSchema
from logger import logger
import os


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
            "twitter_username": "novo.autor@teste.com.br",
            "avatar_url": "novo.autor@teste.com.br",
        }
        self.author = Author(**self.author_data)

        # adiciona autor na sessão
        self.session.add(self.author)

        # efetiva a inserção na base de dados
        self.session.commit()

    def tearDown(self):
        # remove autor inserido nos testes da sessão
        self.session.delete(self.author)

        # efetiva a exclusão na base de dados
        self.session.commit()

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

            self.assertEqual("PYTEST_CURRENT_TEST" in os.environ, True)
            # verifica se a resposta é 200
            self.assertEqual(response.status_code, 200)

            # verifica se o novo autor foi adicionado na base
            author_id = response.json["id"]
            authors = self.session.query(Author).all()
            self.assertEqual(len(authors), 2)

            # verifica se os dados do autor adicionado são os mesmos que foram
            # enviados
            added_author = authors[1]
            self.assertEqual(added_author.first_name, "Novo")
            self.assertEqual(added_author.last_name, "Autor")
            self.assertEqual(added_author.email, "novo.autor@teste.com.br")

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

            # verifica se não foi adicionado um novo autor com o mesmo email
            authors = self.session.query(Author).all()
            self.assertEqual(len(authors), 2)
