    hdr = ["COD_PROD", "NOME_PROD", "DESC_PROD", "CP", "CF", "CV", "IV", "ML"]
    from tabulate import tabulate
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