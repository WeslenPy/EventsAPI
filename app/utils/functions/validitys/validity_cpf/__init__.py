from marshmallow import ValidationError

def validityCPF(cpf:str):

    if not cpf.isdigit():raise ValidationError('CPF field only requires numbers.','cpf')
    elif len(cpf) < 11 or len(cpf)>11:raise ValidationError('CPF is invalid .','cpf')

    novo_cpf = cpf[:-2]
    total = 0
    reverso = 10
    for i in range(19):
        if i > 8: i -= 9
        total += int(novo_cpf[i]) * reverso
        reverso -= 1
        if reverso < 2:
            reverso = 11
            d = 11 - (total % 11)
            if d > 9:d = 0
            total = 0
            novo_cpf += str(d)

    if cpf == novo_cpf and not len(set(maskcpf(cpf)))==1:return cpf

    raise ValidationError('CPF is invalid','cpf')

def maskcpf(doc):
    return [i for i in doc]

