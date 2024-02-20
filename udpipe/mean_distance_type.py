import json

def carregar_dados(arquivo_json):
    with open(arquivo_json, 'r', encoding='utf-8') as file:
        return json.load(file)

def processa_estatisticas(data):
    contagem_relacoes = {}
    soma_distancias = {}
    total_palavras = 0
    head_id = None 

    for sentenca in data:
        for palavra in sentenca['palavras']:
            if int(palavra['ID'].isdigit()):
                relacao = palavra['DEPREL']
                head_id = int(palavra['HEAD']) if palavra['HEAD'].isdigit() else None
                word_id = int(palavra['ID'])

            if head_id is not None and relacao:
                distancia = abs(head_id - word_id)
                contagem_relacoes[relacao] = contagem_relacoes.get(relacao, 0) + 1
                soma_distancias[relacao] = soma_distancias.get(relacao, 0) + distancia
                total_palavras += 1

    estatisticas = {}
    for relacao, contagem in contagem_relacoes.items():
        proporcao = contagem / total_palavras
        distancia_media = soma_distancias[relacao] / contagem
        estatisticas[relacao] = (proporcao, distancia_media)

    return estatisticas, contagem_relacoes, total_palavras

def calcular_estatisticas(arquivo_json):
    data = carregar_dados(arquivo_json)
    estatisticas, contagem, total_palavras = processa_estatisticas(data)
    # print(f'Total de Palavras no texto: {total_palavras}')
    # print(f"Contagem de relações distintas no texto: {len(contagem.keys())}\n")
    # for relacao in contagem.keys():
    #     print(f"\tRelação {relacao}:\n\tContagem={contagem[relacao]}, Proporção={estatisticas[relacao][0]}, Distância Média={estatisticas[relacao][1]}")
    return estatisticas, contagem