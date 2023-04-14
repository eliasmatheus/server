from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from sqlalchemy.exc import IntegrityError

from schemas import *
from services import *
from routes import *
from flask_cors import CORS

from services import *

info = Info(title="Code Chronicles API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)


@app.get("/", tags=[home_tag])
def home():
    """
    Redireciona para /openapi.

    Redireciona para a tela do OpenAI que permite a escolha do estilo de
    documentação.
    """
    return redirect("/openapi")


# Registra rotas
app.register_api(author_bp)
app.register_api(article_bp)

if __name__ == "__main__":
    app.run(debug=True)
