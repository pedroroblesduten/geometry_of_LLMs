import json

def calcular_frequencias(data):
    frequencias = {}
    for sentenca in data:
        for palavra in sentenca['palavras']:
            forma = palavra['UPOS'].lower()
            frequencias[forma] = frequencias.get(forma, 0) + 1
    return frequencias

def calcular_rankings(frequencias):
    ordenado = sorted(frequencias.items(), key=lambda x: x[1], reverse=True)
    rankings = {}
    rank_atual = 1
    i = 0

    while i < len(ordenado):
        if i < len(ordenado) - 1 and ordenado[i][1] == ordenado[i + 1][1]:
            soma_ranks = rank_atual
            contagem_empates = 1
            j = i + 1
            while j < len(ordenado) and ordenado[j][1] == ordenado[i][1]:
                soma_ranks += rank_atual + contagem_empates
                contagem_empates += 1
                j += 1

            rank_medio = soma_ranks / contagem_empates
            for k in range(i, j):
                rankings[ordenado[k][0]] = rank_medio

            rank_atual += contagem_empates
            i = j
        else:
            rankings[ordenado[i][0]] = rank_atual
            rank_atual += 1
            i += 1

    return rankings

def calcular_rank_distance(arquivo_json1, arquivo_json2):
    with open(f'tratados_json/{arquivo_json1}', 'r', encoding='utf-8') as json_file:
        data1 = json.load(json_file)
    with open(f'tratados_json/{arquivo_json2}', 'r', encoding='utf-8') as json_file:
        data2 = json.load(json_file)

    freq1 = calcular_frequencias(data1)
    freq2 = calcular_frequencias(data2)

    rankings1 = calcular_rankings(freq1)
    rankings2 = calcular_rankings(freq2)

    rank_distance = 0
    for palavra in set(rankings1.keys()).intersection(rankings2.keys()):
        rank_distance += abs(rankings1[palavra] - rankings2[palavra])

    return rank_distance