import os

# Muda o local do banco de dados para memória
os.environ["DB_URL"] = "sqlite:///:memory:"
