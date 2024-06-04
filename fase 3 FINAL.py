import getpass
import oracledb
from tabulate import tabulate
import numpy as np
from unidecode import unidecode



alf = {' ': 0, 'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26}

def imp_calc(cp, cfp, cvp, ivp, mlp):
              
            cursor.execute("SELECT * FROM estoque")
            produtos = cursor.fetchall()

            for produto in produtos:
        
                cfpp = cfp / 100
                cvpp = cvp / 100
                ivpp = ivp / 100
                mlpp = mlp / 100

                if cfpp + cvpp + ivpp + mlpp >= 1:
                    print("Erro: A soma das porcentagens de custo fixo, comissão de venda, imposto de venda e margem de lucro é igual ou maior que 100%.")
                

                pv = cp / (1 - (cfpp + cvpp + ivpp + mlpp))

                if pv == 0:
                    print("Erro: O preço de venda não pode ser zero.")
                    
                ivr = ivpp * pv
                cvr = cvpp * pv
                cfr = cfpp * pv

                A = (pv / pv) * 100
                B = (cp / pv) * 100
                C = pv - cp
                CP = (C / pv) * 100
                D = cfpp * pv
                E = cvpp * pv
                F = ivpp * pv
                G = (cfpp + cvpp + ivpp) * pv
                GP = cfp + cvp + ivp
                H = C - G
                HP = (H / pv) * 100
                I = cp * (cfpp + cvpp + ivpp)

                pcp = (cp / pv) * 100

                preco_de_venda = ["preço de venda", round(pv, 2), A]
                custo_de_aquisicao = ["custo de aquisição", round(cp, 2), B]
                receita_bruta = ["receita bruta", round(C, 2), CP]
                custo_fixo = ["custo fixo", round(cfr, 2), cfp]
                valor_de_comissao = ["valor de comissão", round(cvr, 2), cvp]
                imposto_de_venda = ["imposto de venda", round(ivr, 2), ivp]
                outros_custos = ["outros custos", round(G, 2), GP]
                rentabilidade = ["rentabilidade", round(H, 2), HP]

                lista = [preco_de_venda, custo_de_aquisicao, receita_bruta, custo_fixo, valor_de_comissao, imposto_de_venda,
                        outros_custos, rentabilidade]

                hdr2 = ["DESCRIÇÃO", "VALOR", "%"]
                
                print(tabulate(lista, headers=hdr2, tablefmt='psql'))

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

def ins_produto():
    cod_exis = []
    codp = int(input("Digite o código do produto: "))

    cursor.execute("SELECT cod_prod FROM estoque")
    codrpt = cursor.fetchall()

    cod_exis = [item[0] for item in codrpt]

    while codp in cod_exis:
        print("Código de produto já existente, insira outro.")
        codp = int(input("Digite o código do produto: "))

    nomep = input("Digite o nome do produto: ")
    descp = input("Digite a descrição do produto: ")
    descp = criptografar(descp)
    cp = int(input("Digite o custo do produto: "))
    cfp = int(input("Digite a porcentagem do custo fixo do produto: "))
    cvp = int(input("Digite a porcentagem do comissão de venda do produto: "))
    ivp = int(input("Digite a porcentagem do imposto de venda do produto: "))
    mlp = int(input("Digite a porcentagem do margem de lucro de venda do produto: "))
    
    cursor.execute(f"INSERT INTO estoque (cod_prod, nome_prod, desc_prod, cp, cf, cv, iv, ml) VALUES ({codp}, '{nomep}', '{descp}', {cp}, {cfp}, {cvp}, {ivp}, {mlp})")
    print("Produto Adicionado!")
    conexao.commit()

    return cp, cfp, cvp, ivp, mlp
    

def alt_produto():
    coda = int(input("Digite o código do produto que deseja alterar: "))
    alt = input("O que deseja alterar? ")
    
    if alt == 'nome_prod' or alt == 'desc_prod':
        alt2 = input("Para que deseja alterar: ")
        if alt == 'desc_prod':
            alt2 = criptografar(alt2)
        cursor.execute(f"UPDATE estoque SET {alt} = '{alt2}' WHERE cod_prod = {coda}")
        print("Alteração concluída!")
        cursor.execute(f"SELECT * FROM estoque WHERE cod_prod = {coda}")
    else:
        alt2 = input("Para que deseja alterar: ")
        cursor.execute(f"UPDATE estoque SET {alt} = {alt2} WHERE cod_prod = {coda}")
        print("Alteração concluída!")
        cursor.execute(f"SELECT * FROM estoque WHERE cod_prod = {coda}")
    
    conexao.commit()

def sel_apg_prod():
    apgp = int(input("Digite o código do produto que deseja apagar: "))
    cursor.execute(f"SELECT * FROM estoque WHERE cod_prod = {apgp}")
    rapg = cursor.fetchall()

    hdr = ["COD_PROD", "NOME_PROD", "DESC_PROD", "CP", "CF", "CV", "IV", "ML"]
    print(tabulate(rapg, headers=hdr, tablefmt='psql'))
    conf_apg(apgp)
   
def conf_apg(apgp):
    print("\n1. Confirmar e apagar produto\n2. Voltar para o menu")
    opt_dlt = int(input("O que deseja fazer: "))
    if opt_dlt == 1:
        cursor.execute(f"DELETE FROM estoque WHERE cod_prod = {apgp}")
        print("Produto Apagado!")
    elif opt_dlt == 2:
        print("Ok")
        menu()
    
    conexao.commit()

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
        if letra == ' ':
            letras.append(0)
        elif letra == 'Z':
            letras.append(26)
        else:
            letras.append(alf[letra])
    matriz_palavra_em_num = np.array(letras)

    if len(matriz_palavra_em_num) % 2 != 0:
        matriz_palavra_em_num = np.append(matriz_palavra_em_num, [0]) 

    matriz_palavra_em_num = matriz_palavra_em_num.reshape(-1, 2).T
    return matriz_palavra_em_num

def monta_palavra(matriz, palavra_impar):
    palavra_formada = ''
    for coluna in matriz.T:
        for num in coluna:
            if num == 0:
                palavra_formada += ' '
            else:
                for chave, valor in alf.items():
                    if valor == num:
                        palavra_formada += chave

    if palavra_impar:
        palavra_formada = palavra_formada[:-1]
    return palavra_formada

    


def menu():
    print("-" * 25)
    print("1. Inserir produto\n2. Alterar produtos\n3. Apagar produto\n4. Listar produtos\n5. Sair do sistema")
    print("-" * 25)

while True:
    try:
        conexao = oracledb.connect(
            user="123",
            password='gomes',
            dsn="localhost/XEPDB1")
    except Exception as erro:
        print('Erro de conexão', erro)
    else:
        print("Conectado", conexao.version)

    cursor = conexao.cursor()
    break

while True:
    menu()
    opt = int(input("O que deseja fazer: "))

    if opt == 1:  # Inserir produto
      cp, cfp, cvp, ivp, mlp = ins_produto()

    elif opt == 2:  # Alterar produto
        alt_produto()

    elif opt == 3:  # Apagar produto
        sel_apg_prod()

    elif opt == 4:  # Listar produtos
        imp_calc(cp, cfp, cvp, ivp, mlp)
            
    elif opt == 5:  # Fechar programa
        cursor.close()
        conexao.close()
        print("Programa encerrando")
        break
