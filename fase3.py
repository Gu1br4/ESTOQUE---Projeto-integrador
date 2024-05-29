import getpass
import oracledb
def ins_produto():
        codp = (input("Digite o codigo do produto: "))
        nomep = (input("Digite o nome do produto: "))
        descp =  (input("Digite o descricao do produto: "))
        cpp = (input("Digite a porcentagem do custo do produto: "))
        cfp = (input("Digite a porcentagem do custo fixo do produto: "))
        cvp = (input("Digite a porcentagem do comissao de venda do produto: "))
        ivp = (input("Digite a porcentagem do imposto de venda do produto: "))
        mlp = (input("Digite a porcentagem do margem de lucro de venda do produto: "))
        cursor.execute(f"insert into estoque (COD_PROD) values {codp}, '{nomep}', '{descp}', {cpp}, {cfp}, {cvp}, {ivp}, {mlp}")
        print("Produto Adicionado!")

    
def alt_produto():
        coda = int(input("Digite o codigo do produto que deseja alterar: "))
        alt = input("O que deseja alterar?")
        alt2 = input("Para que deseja alterar: ")
        cursor.execute(f"update estoque set {alt} = {alt2} where COD_PROD = {coda}")
        print("Alteracao concluida!")
        cursor.execute(f"select * where COD_PROD = {coda}")
        conexao.commit()



while True:
    print("-"*25)
    print("1. Inserir produto\n2. Alterar produtos \n3. Apagar produto \n4. Listar produtos\n5. Sair do sistema ")
    print("-"*25)
    opt = int(input("O que deseja fazer: "))
  

    try:
        conexao = oracledb.connect(
        user = "GUI",
        password = 'Br@z2005',
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

    elif opt =="4": #Listar produtos 
        
        cursor.execute(f"select * from estoque")
        resultado = cursor.fetchall()
        from tabulate import tabulate
        hdr = ["COD_PROD", "NOME_PROD", "DESC_PROD", "CP", "CF", "CV", "IV", "ML"]
        print(tabulate(resultado, headers= hdr, tablefmt='psql'))

        x = input("digite o codigo do produto: ")

        lista2 = []

        cursor.execute(f"select cp from estoque where COD_PROD = {x}")
        resultado2 = cursor.fetchone()
        lista2.append(resultado2)
        cursor.execute(f"select cf from estoque where COD_PROD = {x}")
        resultado2 = cursor.fetchone()
        lista2.append(resultado2)
        cursor.execute(f"select cv from estoque where COD_PROD = {x}")
        resultado2 = cursor.fetchone()
        lista2.append(resultado2)
        cursor.execute(f"select iv from estoque where COD_PROD = {x}")
        resultado2 = cursor.fetchone()
        lista2.append(resultado2)
        cursor.execute(f"select ml from estoque where COD_PROD = {x}")
        resultado2 = cursor.fetchone()
        lista2.append(resultado2)

        cp =  lista2[0][0]
        cf =  lista2[1][0]
        cv =  lista2[2][0]
        iv =  lista2[3][0]
        ml =  lista2[4][0]
        
        cfp = cf / 100
        cvp = cv / 100
        ivp = iv / 100
        mlp = ml / 100

        pv = cp / (1 - (cfp + cvp + ivp + mlp))
        ivr = ivp*pv
        cvr = cvp*pv
        cfr = cfp*pv

        A=(pv/pv)*100
        B = (cp/pv) * 100
        C = pv - cp
        CP = (C/pv) * 100
        D = cfp * pv
        E = cvp * pv
        F = ivp * pv
        G = (cfp+cvp+ivp) * pv
        GP = cf+cv+iv
        H = C - G
        HP = (H/pv) * 100
        I = cp * (cfp + cvp + ivp)

        pcp=(cp/pv)*100

        preco_de_venda = ["preço de venda", round(pv,2), A]
        custo_de_aquisicao = ["custo de aquisição", round(cp,2), B]
        receita_bruta = ["receita bruta", round(C,2), CP]
        custo_fixo = ["custo fixo", round(cfr,2), cf]
        valor_de_comissao = ["valor de comissão", round(cvr,2), cv]
        imposto_de_venda = ["imposto de venda", round(ivr,2), iv]
        outros_custos = ["outros custos", round(G,2), GP]
        rentabilidade = ["rentabilidade", round(H,2), HP]

        lista =[preco_de_venda, custo_de_aquisicao, receita_bruta, custo_fixo, valor_de_comissao, imposto_de_venda, outros_custos, rentabilidade]

        hdr2 = ["DESCRIÇÃO", "VALOR", "%"]
        print(tabulate(lista ,headers = hdr2, tablefmt='psql'))

        if H > 0.2 * pv:
            print("O lucro é alto")
        elif 0.1 * pv <= H <= 0.2 * pv:
            print("O lucro é médio")
        elif 0 < H < 0.1 * pv:
            print("O lucro é baixo")
        elif H == 0:
            print("Não há lucro nem prejuízo")
        else:
            print("Prejuízo")

    elif opt == 5: #Fechar programa

        cursor.close()
        conexao.close()
        print("Programa encerrando")
        break