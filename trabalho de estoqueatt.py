

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

print(f"--------------------------------------------")
print(f"DESCRIÇÕES |  VALORES |  PORCENTAGEM")
print(f"preço de venda | {pv} | {A}")
print(f"custo de aquisição | {cp} | {B}")
print(f"receita bruta | {C} | {CP}")
print(f"custo fixo | {D} | {cf}")
print(f"valor de comissão | {E} | {cv}")
print(f"imposto de venda | {F} | {iv}")
print(f"outros custos são | {G} | {GP}")
print(f"rentabilidade | {H} | {HP}")
print(f"--------------------------------------------")

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
