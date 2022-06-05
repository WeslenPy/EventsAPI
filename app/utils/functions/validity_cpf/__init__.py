def validatyCPF(cpf):
    if cpf.isdigit(): return False
    if len(cpf) < 11 or len(cpf)>14:
        return False
    novo_cpf = cpf[:-2]
    total = 0
    reverso = 10
    for i in range(19):
        if i > 8:
            i -= 9
        total += int(novo_cpf[i]) * reverso
        reverso -= 1
        if reverso < 2:
            reverso = 11
            d = 11 - (total % 11)
            if d > 9:
                d = 0
            total = 0
            novo_cpf += str(d)

    sequencia = novo_cpf == str(novo_cpf[0]) * len(cpf)
    if cpf == novo_cpf and not sequencia:
        return True
    return False