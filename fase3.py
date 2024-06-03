import getpass
import oracledb
from tabulate import tabulate

def ins_produto():
        codp = (input("Digite o codigo do produto: "))
        nomep = (input("Digite o nome do produto: "))
        descp =  (input("Digite o descricao do produto: "))
        cpp = (input("Digite o custo do produto: "))
        cfp = (input("Digite a porcentagem do custo fixo do produto: "))
        cvp = (input("Digite a porcentagem do comissao de venda do produto: "))
        ivp = (input("Digite a porcentagem do imposto de venda do produto: "))
        mlp = (input("Digite a porcentagem do margem de lucro de venda do produto: "))
        cursor.execute(f"insert into estoque (COD_PROD, NOME_PROD, DESC_PROD, CP, CF, CV, IV, ML) values ({codp}, '{nomep}', '{descp}', {cpp}, {cfp}, {cvp}, {ivp}, {mlp})")
        print("Produto Adicionado!")

    
def alt_produto():
        coda = int(input("Digite o codigo do produto que deseja alterar: "))
        alt = input("O que deseja alterar?")
        alt2 = input("Para que deseja alterar: ")
        cursor.execute(f"update estoque set {alt} = {alt2} where COD_PROD = {coda}")
        print("Alteracao concluida!")
        cursor.execute(f"select * from estoque where COD_PROD = {coda}")
        conexao.commit()



while True:
    print("-"*25)
    print("1. Inserir produto\n2. Alterar produtos \n3. Apagar produto \n4. Listar produtos\n5. Sair do sistema ")
    print("-"*25)
    opt = int(input("O que deseja fazer: "))
  

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
    
    if opt == 1: #Inserir produto
        ins_produto()
        conexao.commit()

    elif opt == 2: #Alterar produto
        alt_produto()
        conexao.commit()
        
    elif opt == 3: #Apagar produto
        
        apgp = input("Digite o codigo do produto que desejar apagar: ")
        cursor.execute(f"select * where COD_PROD = {apgp}")
        rapg = cursor.fetchall()

        hdr = ["COD_PROD", "NOME_PROD", "DESC_PROD", "CP", "CF", "CV", "IV", "ML"]
        from tabulate import tabulate
        print(tabulate(rapg, headers= hdr, tablefmt='psql'))
        
        print("1. Confirmar e apagar produto\n2. Voltar para o menu")
        opt2 = input("O que deseja fazer: ")
        if opt2 == 1:
            cursor.execute(f"delete from estoque where COD_PROD = {apgp} ")
            print("Produto Apagado!")
            conexao.commit()
        else:
            continue

    elif opt ==4: #Listar produtos 
        
        cursor = conexao.cursor()
        
        cursor.execute(f"select * from estoque")
        resultado = cursor.fetchall()
    

        hdr = ["COD_PROD", "NOME_PROD", "DESC_PROD", "CP", "CF", "CV", "IV", "ML"]
        from tabulate import tabulate
        print(tabulate(resultado, headers= hdr, tablefmt='psql'))



    elif opt == 5: #Fechar programa

        cursor.close()
        conexao.close()
        print("Programa encerrando")
        break       