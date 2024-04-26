#ANTES DE TUDO EXECUTAR O COMANDO "python -m pip install oracledb" no CMD

import getpass
import oracledb

try:
    conexao = oracledb.connect(
    user = "BD150224315",
    password = 'Fsqad8',
    dsn="BD-ACD/xe")
except Exception as erro:
    print('Erro de conexão', erro)
else:
    print("Conectado", conexao.version)

cursor = conexao.cursor()

cursor.execute("select * from estoque")
resultado = cursor.fetchall()
cursor.close()
conexao.close()

hdr = ["COD_PROD", "NOME_PROD", "DESC_PROD", "CP", "CF", "CV", "IV", "ML"]
from tabulate import tabulate
print(tabulate(resultado, headers= hdr, tablefmt='psql'))