# Blog em Flask

Este pequeno projeto do backend de um blog desenvolvido em flask para a Disciplina **Desenvolvimento Full Stack Básico** do programa de pós graduação em Desenvolvimento Full Stack da [PUC-Rio](https://www.puc-rio.br/index.html)

<p align="center">
  <img src="./static/screenshot.png" alt="My Project GIF">
</p>

---

## Como executar

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenpython -m venv .v.pypa.io/en/latest/).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5002
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte.

```
(env)$ flask run --host 0.0.0.0 --port 5002 --reload
```

Abra o [http://localhost:5002/#/](http://localhost:5002/#/) no navegador para verificar o status da API em execução.
