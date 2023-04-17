import os

db_path = "database/"
# Verifica se o diretório não existe
if not os.path.exists(db_path):
    # então cria o diretório
    os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
DATABASE_URI = "sqlite:///%s/db.sqlite3" % db_path

# Para executar os testes em memória, descomente a linha abaixo
# DATABASE_URI = "sqlite:///:memory:"
