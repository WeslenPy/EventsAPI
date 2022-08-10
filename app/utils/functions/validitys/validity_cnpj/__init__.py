CNPJ_WEIGHTS = ((5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2),
               (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2))

def validityCNPJ(cnpj:str):

    try:

        cnpj = cnpj.translate(str.maketrans({".": None, "-": None, "/": None})).strip()
        if not cnpj.isdigit():return False
        if len(cnpj) != 14 or len(set(cnpj)) == 1:return False

        first_part = cnpj[:12]
        second_part = cnpj[:13]
        first_digit = cnpj[12]
        second_digit = cnpj[13]

        if first_digit == digitValidity(first_part,0
                            ) and second_digit == digitValidity(second_part,1):
            return cnpj

        return False

    except:return False



def digitValidity(number,pos):
    
    sum = 0
    weights = CNPJ_WEIGHTS[pos]

    for i in range(len(number)):
        sum = sum + int(number[i]) * weights[i]
        rest_division = sum % 11

    if rest_division < 2:
        return '0'
    return str(11 - rest_division)
