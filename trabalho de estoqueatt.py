item = str(input("Item que deseja vender: "))
cod  = int(input("Coloque o código do produto:"))
desc = str(input("Descrição do produto:"))
cp = float(input("Custo do produto: "))
cf = float(input("Porcentagem de custo fixo: "))
cv = float(input("Porcentagem de comissão de vendas: "))
iv = float(input("Porcentagem de imposto de venda: "))
ml = float(input("Porcentagem de margem de lucro: "))



cfp = cf / 100
cvp = cv / 100
ivp = iv / 100
mlp = ml / 100



pv = cp / (1 - (cfp + cvp + ivp + mlp))
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

preco_de_venda = "preço de venda"
custo_de_aquisicao = "custo de aquisição"
receita_bruta = "receita bruta"
custo_fixo = "custo fixo"
valor_de_comissao = "valor de comissão"
imposto_de_venda = "imposto de venda"
outros_custos = "outros custos"
rentabilidade = "rentabilidade"
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
print("\n")
def criartabela():
    print("Descrição\t\tvalor\t\t%")
    print(f"{preco_de_venda:<20}\t{pv:.2f}\t\t{A:.2f}")
    print(f"{custo_de_aquisicao:<20}\t{cp:.2f}\t\t{cp/pv*100:.2f}")
    print(f"{receita_bruta:<20}\t{pv:.2f}\t\t{100:.2f}")
    print(f"{custo_fixo:<20}\t{cf:.2f}\t\t{cf:.2f}")
    print(f"{valor_de_comissao:<20}\t{cv:.2f}\t\t{cv:.2f}")
    print(f"{imposto_de_venda:<20}\t{iv:.2f}\t\t{iv:.2f}")
    print(f"{outros_custos:<20}\t{cfp+cvp+ivp:.2f}\t\t{cf+cv+iv:.2f}")
    print(f"{rentabilidade:<20}\t{pv - (cf+cv+iv):.2f}\t\t{(pv - (cf+cv+iv))/pv*100:.2f}")
criartabela()



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
