#instalar no cmd : tabulate, oracledb e numpy
import getpass
import oracledb
from tabulate import tabulate
import numpy as np
from unidecode import unidecode

def ins_produto():
        codp = (input("Digite o codigo do produto"))
        nomep = (input("Digite o nome do produto: "))
        descp =  (input("Digite o descricao do produto: "))
        descp = criptografar(descp)
        cp = (input("Digite o custo do produto: "))
        if cp == "0":
            print("digite um valor diferente de 0: ")
            cp = (input("Digite o codigo do produto: "))
        cfp = (input("Digite a porcentagem do custo fixo do produto: "))
        cvp = (input("Digite a porcentagem do comissao de venda do produto: "))
        ivp = (input("Digite a porcentagem do imposto de venda do produto: "))
        mlp = (input("Digite a porcentagem do margem de lucro de venda do produto: "))
        cursor.execute(f"insert into estoque (COD_PROD, NOME_PROD, DESC_PROD, CP, CF, CV, IV, ML) values ({codp}, '{nomep}', '{descp}', {cp}, {cfp}, {cvp}, {ivp}, {mlp})")
        print("Produto Adicionado!")

    
def alt_produto():
        cursor.execute(f"select * from estoque")
        resultados = cursor.fetchall()
        hdr = ["COD_PROD", "NOME_PROD", "DESC_PROD", "CP", "CF", "CV", "IV", "ML"]
        from tabulate import tabulate
        print(tabulate(resultados, headers=hdr, tablefmt='psql'))
        coda = int(input("Digite o codigo do produto que deseja alterar: "))
        alt = input("O que deseja alterar?")
        alt2 = input("Para que deseja alterar: ")
        cursor.execute(f"update estoque set {alt} = {alt2} where COD_PROD = {coda}")
        print("Alteracao concluida!")
        cursor.execute(f"select * from estoque where COD_PROD = {coda}")
        conexao.commit()

def sel_apg_prod():
    cursor.execute(f"select * from estoque")
    resultados = cursor.fetchall()
    hdr = ["COD_PROD", "NOME_PROD", "DESC_PROD", "CP", "CF", "CV", "IV", "ML"]
    from tabulate import tabulate
    print(tabulate(resultados, headers=hdr, tablefmt='psql'))
    apgp = int(input("Digite o codigo do produto que desejar apagar: "))
    cursor.execute(f"select * from estoque where COD_PROD = {apgp}")
    rapg = cursor.fetchall()
    hdr = ["COD_PROD", "NOME_PROD", "DESC_PROD", "CP", "CF", "CV", "IV", "ML"]
    from tabulate import tabulate
    print(tabulate(rapg, headers= hdr, tablefmt='psql'))
    conf_apg(apgp)
    
def conf_apg(apgp):
    print("\n1. Confirmar e apagar produto\n2. Voltar para o menu")
    opt_dlt = int(input("O que deseja fazer: "))
    if opt_dlt == 1:
        cursor.execute(f"delete from estoque where COD_PROD = {apgp} ")
        print("Produto Apagado!")
    elif opt_dlt == 2:
        print("ok")
        menu()
    conexao.commit()


alfabeto = {' ': 0,'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26}

def criptografar(descricao):
    palavra = f'{unidecode(descricao)}'.upper()
    palavra_impar = False
    if len(palavra) % 2 != 0:
        palavra += "A"
        palavra_impar = True

    matriz_palavra_em_num = palavra_em_matriz(palavra)

    chaveMatriz = np.array([[4, 3], [1, 2]])
    criptografada = np.dot(chaveMatriz, matriz_palavra_em_num) % 26
    palavra_criptografada = monta_palavra(criptografada, palavra_impar)

    return palavra_criptografada

def palavra_em_matriz(palavra):
    letras = []
    for letra in palavra:
        letras.append(alfabeto[letra])
    matriz_palavra_em_num = np.array(letras)

    if len(matriz_palavra_em_num) % 2 != 0:
        matriz_palavra_em_num = np.append(matriz_palavra_em_num, [0]) 

    matriz_palavra_em_num = matriz_palavra_em_num.reshape(2, -1, order='F')
    return matriz_palavra_em_num

def monta_palavra(matriz, palavra_impar):
    palavra_formada = ''
    for coluna in matriz.T:
        for num in coluna:
            if num == 0:
                palavra_formada += ' '
            else:
                palavra_formada += list(alfabeto.keys())[list(alfabeto.values()).index(num)]
    if palavra_impar:
        palavra_formada = palavra_formada[:-1]
    return palavra_formada

def decifrar(descricao):
    palavra_criptografada = descricao.upper()

    matriz_palavra_em_num = palavra_em_matriz(palavra_criptografada)
    a, b, c, d = 4, 3, 1, 2
    chaveMatrizInversa = np.array([[d, -b], [-c, a]])
    det = (a * d) - (b * c)
    det_inversas = {1: 1, 3: 9, 5: 21, 7: 15, 9: 3, 11: 19, 15: 7, 17: 23, 19: 11, 21: 5, 23: 17, 25: 25}
    det_inv = det_inversas[det % 26]
    chaveMatrizInversa = (chaveMatrizInversa * det_inv) % 26
    matriz_palavra_em_num = np.dot(chaveMatrizInversa, matriz_palavra_em_num) % 26
    palavra_decifrada = monta_palavra(matriz_palavra_em_num, len(palavra_criptografada) % 2 != 0)

    return palavra_decifrada


def listar_produtos():
    cursor.execute("SELECT * FROM estoque")
    resultados = cursor.fetchall()

    hdr = ["COD_PROD", "NOME_PROD", "DESC_PROD", "CP", "CF", "CV", "IV", "ML"]
    print(tabulate(resultados, headers=hdr, tablefmt='psql'))

    for resultado in resultados:
        descricao_criptografada = resultado[2]
        descricao_descriptografada = descriptografar(descricao_criptografada)
        resultado_com_descricao_descriptografada = resultado[:2] + (descricao_descriptografada,) + resultado[3:]
        print(resultado_com_descricao_descriptografada)
        # Continue com o restante do processamento, se necessário



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
        sel_apg_prod()
        conexao.commit()

    elif opt == 4:  # Listar produtos
        cursor.execute("SELECT * FROM estoque")
        resultados = cursor.fetchall()

        hdr = ["COD_PROD", "NOME_PROD", "DESC_PROD", "CP", "CF", "CV", "IV", "ML"]
        print(tabulate(resultados, headers=hdr, tablefmt='psql'))

        for resultado in resultados:
            descricao_criptografada = resultado[2]
            descricao_decifrada = decifrar(descricao_criptografada)
            resultado_com_descricao_decifrada = resultado[:2] + (descricao_decifrada,) + resultado[3:]
            print(tabulate([resultado_com_descricao_decifrada], headers=hdr, tablefmt='psql'))

            cp, cf, cv, iv, ml = resultado_com_descricao_decifrada[3:8]
            cfp = cf / 100
            cvp = cv / 100
            ivp = iv / 100
            mlp = ml / 100

            if cfp + cvp + ivp + mlp >= 1:
                print("Erro: A soma das porcentagens de custo fixo, comissão de venda, imposto de venda e margem de lucro é igual ou maior que 100%.")
                continue

            pv = cp / (1 - (cfp + cvp + ivp + mlp))

            if pv == 0:
                print("Erro: O preço de venda não pode ser zero.")
                continue

            ivr = ivp * pv
            cvr = cvp * pv
            cfr = cfp * pv

            A = (pv / pv) * 100
            B = (cp / pv) * 100
            C = pv - cp
            CP = (C / pv) * 100
            D = cfp * pv
            E = cvp * pv
            F = ivp * pv
            G = (cfp + cvp + ivp) * pv
            GP = cf + cv + iv
            H = C - G
            HP = (H / pv) * 100
            I = cp * (cfp + cvp + ivp)

            pcp = (cp / pv) * 100

            preco_de_venda = ["preço de venda", round(pv, 2), A]
            custo_de_aquisicao = ["custo de aquisição", round(cp, 2), B]
            receita_bruta = ["receita bruta", round(C, 2), CP]
            custo_fixo = ["custo fixo", round(cfr, 2), cf]
            valor_de_comissao = ["valor de comissão", round(cvr, 2), cv]
            imposto_de_venda = ["imposto de venda", round(ivr, 2), iv]
            outros_custos = ["outros custos", round(G, 2), GP]
            rentabilidade = ["rentabilidade", round(H, 2), HP]

            lista = [preco_de_venda, custo_de_aquisicao, receita_bruta, custo_fixo, valor_de_comissao, imposto_de_venda,
                    outros_custos, rentabilidade]

            hdr2 = ["DESCRIÇÃO", "VALOR", "%"]
            
            print(tabulate(lista, headers=hdr2, tablefmt='psql'))


    elif opt == 5: #Fechar programa

        cursor.close()
        conexao.close()
        print("Programa encerrando")
        break       