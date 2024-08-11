def normalize_cannon_placements(placements):
    # Dicionário para contar as ocorrências de cada 'row'
    contagem = {}

    # Iterar sobre cada sublista
    for placement in placements:
        # Obtem a 'row'
        row = placement[1]

        # Conta o número de ocorrencias de cada 'row'
        if row in contagem:
            contagem[row] += 1
        else:
            contagem[row] = 1

    # Lista de contagens de 1 a 8
    contagens_frequencia = [0] * 8

    # Preencher a lista de contagens
    for count in contagem.values():
        if count <= 8:
            contagens_frequencia[count - 1] += 1

    # Converter a lista de contagens em uma string
    resultado = "".join(map(str, contagens_frequencia))

    return resultado
