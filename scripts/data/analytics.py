# Função para categorizar os preços com base na moda
def cr_val_alert(preco, moda):
    limite_inferior = moda * 0.7
    limite_superior = moda * 1.3

    if preco > limite_superior:
        return r"30% acima da moda"
    elif preco < limite_inferior:
        return r"30% abaixo da moda"
    return r"Dentro da faixa"