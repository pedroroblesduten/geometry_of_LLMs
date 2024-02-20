from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.util import ngrams
from nltk.stem import WordNetLemmatizer
import sys
import os
import json

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


def metrics_pre_lemmatization(text):
    sentences = nltk.sent_tokenize(text)
    words = []
    num_tokens = []
    for i in range(len(sentences)):
        sentence = nltk.word_tokenize(sentences[i])
        num_tokens.append(len(sentence))
        words.append(nltk.word_tokenize(sentences[i]))

    num_chars = []
    words = [word for sublist in words for word in sublist]
    for word in words:
        num_chars.append(len(word))

    ttr = len(set(words)) / len(words)
    tokens_in_sentence_mean = np.mean(num_tokens)
    chars_in_words_mean = np.mean(num_chars)
    # print(f'TTR: {np.round(ttr, 4)}')
    # print(f'Média de tokens por sentença: {np.round(tokens_in_sentence_mean, 4)}')
    # print(f'Média de caracteres por token: {np.round(chars_in_words_mean, 4)}')
    return [ttr, tokens_in_sentence_mean, chars_in_words_mean]

def metrics_all_texts(orig, gen, prompt):
    mets = []
    # print('----------- Métricas do texto original -----------')
    mets.append(metrics_pre_lemmatization(orig))
    # print('----------- Métricas do texto gerado -----------')
    mets.append(metrics_pre_lemmatization(gen))
    # print('----------- Métricas do texto do prompt -----------')
    mets.append(metrics_pre_lemmatization(prompt))
    mets = [met for sublist in mets for met in sublist]
    return mets

def radical_reduction(text):
    sentences = nltk.sent_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    for i in range(len(sentences)):
        words = nltk.word_tokenize(sentences[i])
        newwords = [lemmatizer.lemmatize(word) for word in words]
        sentences[i] = ' '.join(newwords)
    return ' '.join(sentences)

def reduce_orig_gen_ppt(orig, gen, ppt):
    return (radical_reduction(orig), radical_reduction(gen), radical_reduction(ppt))

def ngram_convertor(sentence, n=3):
    return list(ngrams(sentence.split(), n))

def generate_unigrams_and_compare(orig, gen, ppt):
    orig_unigrams = ngram_convertor(orig, 1)
    gen_unigrams = ngram_convertor(gen, 1)
    ppt_unigrams = ngram_convertor(ppt, 1)

    set_orig = set(orig_unigrams)
    set_gen = set(gen_unigrams)
    set_ppt = set(ppt_unigrams)

    num_unique_unigrams_orig = len(set_orig)
    num_unique_unigrams_gen = len(set_gen)
    num_unique_unigrams_ppt = len(set_ppt)

    common_words_orig_ppt = set_orig.intersection(set_ppt)
    common_words_orig_gen = set_orig.intersection(set_gen)
    common_words_gen_ppt = set_gen.intersection(set_ppt)

    # print(f'Número de tokens únicos para prompt é: {num_unique_unigrams_ppt}')
    # print(f'Número de tokens únicos para texto gerado é: {num_unique_unigrams_gen}')
    # print(f'Número de tokens únicos para texto original é: {num_unique_unigrams_orig}')

    # Coincidência de tokens
    # print(f'Número de tokens em comum entre prompt e texto original é: {len(common_words_orig_ppt)}')
    # print(f'Número de tokens em comum entre prompt e texto gerado é: {len(common_words_gen_ppt)}')
    # print(f'Número de tokens em comum entre texto original e gerado é: {len(common_words_orig_gen)}')

    return [num_unique_unigrams_ppt, num_unique_unigrams_gen, num_unique_unigrams_orig, len(common_words_orig_ppt), len(common_words_gen_ppt), len(common_words_orig_gen)]

def generate_bigrams_and_compare(orig, gen, ppt):
    orig_bigrams = ngram_convertor(orig, 2)
    gen_bigrams = ngram_convertor(gen, 2)
    ppt_bigrams = ngram_convertor(ppt, 2)

    # print(f'Número de bigramas únicos no prompt é: {len(set(ppt_bigrams))}')
    # print(f'Número de bigramas únicos no texto gerado é: {len(set(gen_bigrams))}')
    # print(f'Número de bigramas únicos no texto original é: {len(set(orig_bigrams))}')

    repeated_orig = {}
    cont_orig = 0
    for bigram in orig_bigrams:
        if bigram in repeated_orig:
          cont_orig += 1
          repeated_orig[bigram] += 1
        else:
          repeated_orig[bigram] = 1


    repeated_gen = {}
    cont_gen = 0
    for bigram in gen_bigrams:
        if bigram in repeated_gen:
          cont_gen += 1
          repeated_gen[bigram] += 1
        else:
          repeated_gen[bigram] = 1

    repeated_orig = {bigram: freq for bigram, freq in repeated_orig.items() if freq > 1}
    repeated_gen = {bigram: freq for bigram, freq in repeated_gen.items() if freq > 1}

    # print(f'Número de repetições de bigramas no texto original é: {cont_orig}')
    # print(f'Número de repetições de bigramas no texto gerado é: {cont_gen}')

    common_bigrams_orig_ppt = set(orig_bigrams).intersection(set(ppt_bigrams))
    common_bigrams_orig_gen = set(orig_bigrams).intersection(set(gen_bigrams))
    common_bigrams_gen_ppt = set(gen_bigrams).intersection(set(ppt_bigrams))

    # print(f'Número de bigramas em comum entre prompt e texto original é: {len(common_bigrams_orig_ppt)}')
    # print(f'Número de bigramas em comum entre prompt e texto gerado é: {len(common_bigrams_gen_ppt)}')
    # print(f'Número de bigramas em comum entre texto original e gerado é: {len(common_bigrams_orig_gen)}')

    return [len(set(ppt_bigrams)), len(set(gen_bigrams)), len(set(orig_bigrams)), cont_orig, cont_gen, len(common_bigrams_orig_ppt), len(common_bigrams_gen_ppt), len(common_bigrams_orig_gen)]


def generate_trigrams_and_compare(orig, gen, ppt):
    orig_trigrams = ngram_convertor(orig, 3)
    gen_trigrams = ngram_convertor(gen, 3)
    ppt_trigrams = ngram_convertor(ppt, 3)

    # print(f'Número de trigramas únicos no prompt é: {len(set(ppt_trigrams))}')
    # print(f'Número de trigramas únicos no texto gerado é: {len(set(gen_trigrams))}')
    # print(f'Número de trigramas únicos no texto original é: {len(set(orig_trigrams))}')

    repeated_orig = {}
    cont_orig = 0
    for trigram in orig_trigrams:
        if trigram in repeated_orig:
          cont_orig += 1
          repeated_orig[trigram] += 1
        else:
          repeated_orig[trigram] = 1

    repeated_gen = {}
    cont_gen = 0
    for trigram in gen_trigrams:
        if trigram in repeated_gen:
          cont_gen += 1
          repeated_gen[trigram] += 1
        else:
          repeated_gen[trigram] = 1

    repeated_orig = {trigram: freq for trigram, freq in repeated_orig.items() if freq > 1}
    repeated_gen = {trigram: freq for trigram, freq in repeated_gen.items() if freq > 1}

    # print(f'Número de repetições de trigramas no texto original é: {cont_orig}')
    # print(f'Número de repetições de trigramas no texto gerado é: {cont_gen}')

    common_trigrams_orig_ppt = set(orig_trigrams).intersection(set(ppt_trigrams))
    common_trigrams_orig_gen = set(orig_trigrams).intersection(set(gen_trigrams))
    common_trigrams_gen_ppt = set(gen_trigrams).intersection(set(ppt_trigrams))

    # print(f'Número de trigramas em comum entre prompt e texto original é: {len(common_trigrams_orig_ppt)}')
    # print(f'Número de trigramas em comum entre prompt e texto gerado é: {len(common_trigrams_gen_ppt)}')
    # print(f'Número de trigramas em comum entre texto original e gerado é: {len(common_trigrams_orig_gen)}')

    return [len(set(ppt_trigrams)), len(set(gen_trigrams)), len(set(orig_trigrams)), cont_orig, cont_gen, len(common_trigrams_orig_ppt), len(common_trigrams_gen_ppt), len(common_trigrams_orig_gen)]

def make_path_files(poem_name):
    init_path = ''
    prompt = init_path + poem_name + '_ppt.txt'
    orig = init_path + poem_name + '_orig.txt'
    gen = init_path + poem_name + '_gen.txt'

    return (prompt, orig, gen)

# Checks if there's '\n' at the beggining of a sentence and removes it
def remove_symbol(texts, symbol):
    new_texts = []
    for text in texts:
        while text[0] == symbol:
            text = text[1:]
        new_texts.append(text)

    return new_texts

# Not sure if rest of the code handles unicode
# Also, should I erase the rest of the '\n' the model generates?
def get_and_treat_texts(data, num_samples):
    [ppt, comp] = remove_symbol([data['begin_original'], 
                                 data['complete_original']], '\n')

    gen_texts = remove_symbol([data['generated'][i]['generated_text'] for i in range(num_samples)], '\n')

    ppt = ((ppt)[1:])[:-1]
    comp = ((comp)[1:])[:-1]
    gens = []
    for gen in gen_texts:
        if gen[0] == "'":
            gen = ((gen)[1:])[:-1]
        gens.append(gen)

    orig = comp.replace(ppt, '')
    [orig] = remove_symbol([orig], ' ')
    
    return (ppt, orig, gens)

def analyze_text(data, list_csv, json_file):

    #(prompt_f, orig_f, gen_f) = make_path_files(text_name)
    # with open(orig_f, 'r') as orig_handler:
    #     orig_text = orig_handler.read()
    # with open(gen_f, 'r') as gen_handler:
    #     gen_text = gen_handler.read()
    # with open(prompt_f, 'r') as ppt_handler:
    #     ppt_text = ppt_handler.read()

    ppt_text, orig_text, gen_texts = get_and_treat_texts(data, 10)


    for index, gen_text in enumerate(gen_texts):
        all_metrics = []
        # Metrics with raw text
        basic_metrics = metrics_all_texts(orig_text, gen_text, ppt_text)
        # print('-----------------------------------------------------------------')
        all_metrics.append(basic_metrics)

        (orig, gen, ppt) = reduce_orig_gen_ppt(orig_text, gen_text, ppt_text)
        # Metrics post-lemmatization
        unigram_metrics = generate_unigrams_and_compare(orig, gen, ppt)
        # print('-----------------------------------------------------------------')
        bigram_metrics = generate_bigrams_and_compare(orig, gen, ppt)
        # print('-----------------------------------------------------------------')
        trigram_metrics = generate_trigrams_and_compare(orig, gen, ppt)
        all_metrics.append(unigram_metrics)
        all_metrics.append(bigram_metrics)
        all_metrics.append(trigram_metrics)

        final_list_csv_scores = [score for sublist in all_metrics for score in sublist]

        final_list_csv_scores.insert(0, data['prompt_type'])
        final_list_csv_scores.insert(0, data['title'])
        final_list_csv_scores.insert(0, json_file)
        final_list_csv_scores.insert(0, index)
        list_csv.append(final_list_csv_scores)

    return final_list_csv_scores, list_csv

if __name__ == "__main__":

    json_files = []
    list_csv = []

    for i in range(1, len(sys.argv)):
       json_files.append(sys.argv[i])

    for json_file in json_files:
        with open(json_file, "r") as file:
            data = json.load(file)
        (_, list_csv) = analyze_text(data, list_csv, json_file)

    cols = ['n_gen_text', 'json_file', 'title', 'type_prompt', 'ttr_orig', 'tok_sent_orig', 'char_word_orig', 'ttr_gen', 'tok_sent_gen', 'char_word_gen', 'ttr_ppt', 'tok_sent_ppt', 'char_word_ppt', 
        'n_unique_uni_ppt', 'n_unique_uni_gen', 'n_unique_uni_orig', 'n_uni_comuns_orig_ppt', 'n_uni_comuns_gen_ppt', 'n_uni_comuns_orig_gen', 
        'n_unique_bi_ppt', 'n_unique_bi_gen', 'n_unique_bi_orig', 'bi_repet_orig', 'bi_repet_gen', 'n_bi_comuns_orig_ppt', 'n_bi_comuns_gen_ppt', 'n_bi_comuns_orig_gen', 
        'n_unique_tri_ppt', 'n_unique_tri_gen', 'n_unique_tri_orig', 'tri_repet_orig', 'tri_repet_gen', 'n_tri_comuns_orig_ppt', 'n_tri_comuns_gen_ppt', 'n_tri_comuns_orig_gen']

    data_texts = pd.DataFrame(data=list_csv, columns=cols)
    if os.path.isfile('text_basic_metrics.csv'):
       data_texts.to_csv('text_basic_metrics.csv', mode='a', index=False, header=False)
    else:
       data_texts.to_csv('text_basic_metrics.csv', index=False)

## Como rodar: chamar o script, passando como argumentos os arquivos json dos quais se deseja obter as métricas