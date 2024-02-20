import json

# Métricas básicas
def calculo_sentencas(arquivo_json):
    with open(arquivo_json, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    total_sentences = len(json_data)
    total_tokens = 0
    total_words = 0

    for sentence in json_data:
        total_sentences += 1
        for palavra in sentence['palavras']:
            if palavra['ID'].isdigit():
                total_tokens += 1
                if palavra['UPOS'] not in ('PUNCT', 'SYM'):
                    total_words += 1

    average_words_per_sentence = total_words / total_sentences if total_sentences > 0 else 0

    return total_sentences, total_tokens, total_words, average_words_per_sentence

# Métrica MDD
def calculate_dependency_distance(palavras):
    sentence_total_distance = 0
    for palavra in palavras:
        if palavra['HEAD'].isdigit() and palavra['ID'].isdigit():
            distance = abs(int(palavra['ID']) - int(palavra['HEAD']))
            sentence_total_distance += distance
    return sentence_total_distance

def mean_dependency_distance(arquivo_json):
    with open(arquivo_json, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        sample_num_sentences = len(data)
        sample_num_palavras = 0
        sample_total_distance = 0

        for sentenca in data:
            palavras = []
            for palavra in sentenca['palavras']:
                if palavra['ID'].isdigit(): palavras.append(palavra)
            sentence_distance = calculate_dependency_distance(palavras)
            sample_total_distance += sentence_distance
            sample_num_palavras += len(palavras)

        arquivo_mdd = sample_total_distance / (sample_num_palavras - sample_num_sentences) if sample_num_palavras and sample_num_sentences else 0
        return arquivo_mdd