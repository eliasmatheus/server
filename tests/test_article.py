from flask import Flask
from flask_testing import TestCase
import os

from modules.article import article_bp
from modules.author import author_bp

from models import Author, Article, Session


class TestArticle(TestCase):
    def create_app(self):
        app = Flask(__name__)

        app.register_blueprint(article_bp)
        app.register_blueprint(author_bp)

        return app

    def create_author(self):
        # cria autor para ser utilizado nos testes
        self.author_data = {
            "first_name": "Teste",
            "last_name": "Autor",
            "email": "teste.autor.artigos@teste.com.br",
            "twitter_username": "twitter_username",
            "avatar_url": "avatar_url",
        }
        self.author = Author(**self.author_data)

        # adiciona autor na sessão
        self.session.add(self.author)

        # efetiva a inserção na base de dados
        self.session.commit()

    def setUp(self):
        self.app.config["TESTING"] = True
        self.session = Session()

        self.create_author()

        # Adiciona um artigo à sessão
        self.article_data = {
            "title": "Teste",
            "content": "Conteúdo de teste",
            "subtitle": "Subtítulo de teste",
            "author_id": self.author.id,
        }
        self.article = Article(**self.article_data)
        self.session.add(self.article)
        self.session.commit()

    def tearDown(self):
        # Remove o artigo da sessão
        article = (
            self.session.query(Article).filter_by(id=self.article.id).first()
        )

        if article:
            self.session.delete(self.article)
            self.session.commit()

        # verifica se o autor ainda existe na base de dados
        author = (
            self.session.query(Author).filter_by(id=self.author.id).first()
        )

        if author:
            # remove autor inserido nos testes da sessão
            self.session.delete(self.author)

            # efetiva a exclusão na base de dados
            self.session.commit()

    def test_get_articles(self):
        response = self.client.get("/articles")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertIsInstance(response.json, dict)
        self.assertIn("articles", response.json)
        self.assertEqual(response.json["articles"][0]["title"], "Teste")

    def test_get_article(self):
        # cria artigo para ser utilizado nos testes
        article_data = {
            "title": "Artigo Teste",
            "content": "Conteúdo do artigo teste",
            "subtitle": "Subtítulo de teste",
            "author_id": self.author.id,
        }
        article = Article(**article_data)
        self.session.add(article)
        self.session.commit()

        # faz requisição GET para buscar artigo pelo ID
        response = self.client.get(f"/article/{article.id}")

        # verifica se a resposta é 200 e se contém as informações do artigo
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIn("title", response.json)
        self.assertEqual(response.json["title"], article_data["title"])
        self.assertIn("content", response.json)
        self.assertEqual(response.json["content"], article_data["content"])
        self.assertIn("author", response.json)
        self.assertIsInstance(response.json["author"], dict)
        self.assertIn("id", response.json["author"])
        self.assertEqual(response.json["author"]["id"], self.author.id)
        self.assertIn("first_name", response.json["author"])
        self.assertEqual(
            response.json["author"]["first_name"],
            self.author.first_name,
        )

        # remove artigo inserido nos testes da sessão
        self.session.delete(article)
        self.session.commit()

    def test_post_article(self):
        # cria dados do artigo para ser adicionado
        article_data = {
            "title": "Artigo Teste",
            "content": "Conteúdo do artigo teste",
            "subtitle": "Subtítulo de teste",
            "author_id": self.author.id,
        }

        # faz uma requisição POST para adicionar o artigo
        response = self.client.post("/article", data=article_data)

        # verifica se a resposta é 200 e se contém as informações do artigo
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIn("title", response.json)
        self.assertEqual(response.json["title"], article_data["title"])
        self.assertIn("content", response.json)
        self.assertEqual(response.json["content"], article_data["content"])
        self.assertIn("author", response.json)
        self.assertIsInstance(response.json["author"], dict)
        self.assertIn("id", response.json["author"])
        self.assertEqual(response.json["author"]["id"], self.author.id)
        self.assertIn("first_name", response.json["author"])
        self.assertEqual(
            response.json["author"]["first_name"],
            self.author.first_name,
        )

        # verifica se o artigo foi adicionado ao banco de dados
        article = (
            self.session.query(Article)
            .filter_by(title=article_data["title"])
            .first()
        )
        self.assertIsNotNone(article)

        # remove artigo inserido nos testes da sessão
        self.session.delete(article)
        self.session.commit()

    def test_put_article(self):
        # Cria um novo artigo para ser editado
        article_data = {
            "title": "Artigo Teste",
            "content": "Conteúdo do artigo teste",
            "subtitle": "Subtítulo de teste",
            "author_id": self.author.id,
        }
        article = Article(**article_data)
        self.session.add(article)
        self.session.commit()

        # Define os novos dados do artigo
        new_data = {
            "id": self.article.id,
            "title": "Novo título",
            "content": "Novo conteúdo",
            "subtitle": "Novo subtítulo",
            "author_id": self.author.id,
        }

        # Faz a requisição para editar o artigo
        response = self.client.put("/article", data=new_data)

        # Verifica se a resposta é 200 e se o artigo foi editado corretamente
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIn("title", response.json)
        self.assertEqual(response.json["title"], new_data["title"])
        self.assertIn("content", response.json)
        self.assertEqual(response.json["content"], new_data["content"])
        self.assertIn("author", response.json)
        self.assertIsInstance(response.json["author"], dict)
        self.assertIn("id", response.json["author"])
        self.assertEqual(response.json["author"]["id"], self.author.id)
        self.assertIn("first_name", response.json["author"])
        self.assertEqual(
            response.json["author"]["first_name"],
            self.author.first_name,
        )

        # Remove o artigo inserido nos testes da sessão
        self.session.delete(article)
        self.session.commit()

    def test_delete_article(self):
        # faz requisição DELETE para remover o artigo criado no método setUp
        response = self.client.delete(f"/article/{self.article.id}")

        # verifica se a resposta é 200 e se contém a mensagem de confirmação e o id do artigo removido
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertIsInstance(response.json, dict)
        self.assertIn("message", response.json)
        self.assertEqual(response.json["message"], "Artigo removido")
        self.assertIn("id", response.json)
        self.assertEqual(response.json["id"], self.article.id)

        # verifica se o artigo foi removido da base de dados
        deleted_article = (
            self.session.query(Article).filter_by(id=self.article.id).first()
        )
        self.assertIsNone(deleted_article)
