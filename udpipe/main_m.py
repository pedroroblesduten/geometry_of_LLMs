import os
import csv
import re
import shutil
import mdd
import mean_distance_type as mdt
import rank_distance as rkd
import ud_pipe_api as ud
# import plots as pl

# NÃO ALTERAR
model = 'english-gum-ud-2.12-230717'
parser_url = "http://lindat.mff.cuni.cz/services/udpipe/api/process"
input_folder = '../resultados_mistral/'
output_folder = 'ud_pipe_output/'
# NÃO ALTERAR

TREE_PATH = "ud_pipe_output"
JSON_FOLDER_PATH = "tratados_json"
RESULTADOS_METRICAS_FOLDER = "resultados_metricas_udpipe"

# Coleta árvores do UdPipe e trata em arquivos json para manipulação
ud.process_text_files(model, parser_url, input_folder, output_folder)
ud.json_format(TREE_PATH, JSON_FOLDER_PATH)

pasta_arquivos = os.listdir(JSON_FOLDER_PATH)
arquivos_correspondentes = {}
arquivos_autores = []
data_by_file = {}
all_relations = set()

if pasta_arquivos:
    if not os.path.exists(RESULTADOS_METRICAS_FOLDER):
        os.makedirs(RESULTADOS_METRICAS_FOLDER)

    # Métricas individuais
    with open(os.path.join(RESULTADOS_METRICAS_FOLDER, "udpipe_metrics_mistral.csv"), mode="w", newline="") as output_csv:
        csv_writer = csv.writer(output_csv)
        headers = ["File", "Total Sentences", "Total Tokens", "Total Words", "Average Words per Sentence", "Mean Dependency Distance"]
        csv_writer.writerow(headers)

        for arquivo_json in pasta_arquivos:
            if arquivo_json.endswith('.json'):
                arquivo_json_path = os.path.join(JSON_FOLDER_PATH, arquivo_json)
                total_sentences, total_tokens, total_words, average_words_per_sentence = mdd.calculo_sentencas(arquivo_json_path)
                mdd_value = mdd.mean_dependency_distance(arquivo_json_path)
                csv_writer.writerow([arquivo_json, total_sentences, total_tokens, total_words, average_words_per_sentence, mdd_value])

    # Métricas Mean Distance Type
    for arquivo_json in pasta_arquivos:
        if arquivo_json.endswith('.json'):
            arquivo_json_path = os.path.join(JSON_FOLDER_PATH, arquivo_json)
            estatisticas, contagem = mdt.calcular_estatisticas(arquivo_json_path)
            data_by_file[arquivo_json] = (estatisticas, contagem)
            
    all_relations.update(estatisticas.keys())                

    with open(os.path.join(RESULTADOS_METRICAS_FOLDER, "udpipe_mean_distance_type_mistral.csv"), mode="w", newline="") as mdt_output_csv:
        csv_writer = csv.writer(mdt_output_csv)
        headers = ["File"] + [f"{relacao} Proporção" for relacao in all_relations] + [f"{relacao} Distância Média" for relacao in all_relations] + [f"{relacao} Contagem" for relacao in all_relations]
        csv_writer.writerow(headers)

        for arquivo_json, (estatisticas, contagem) in data_by_file.items():
            row_data = [arquivo_json]
            for relacao in all_relations:
                proporcao, distancia_media = estatisticas.get(relacao, (None, None))
                contagem_relacao = contagem.get(relacao, None)
                row_data.append(proporcao)
                row_data.append(distancia_media)
                row_data.append(contagem_relacao)
            csv_writer.writerow(row_data)

    # Métrica de Rank Distance entre Original e Gerado                
    with open(os.path.join(RESULTADOS_METRICAS_FOLDER, "udpipe_rank_distance_mistral.csv"), mode="w", newline="") as rd_output_csv:
        csv_writer = csv.writer(rd_output_csv)
        headers = ["Original File", "Generated File", "Rank Distance"]
        csv_writer.writerow(headers)

        pattern = r'_generated_\d+\.json'
        for arquivo in pasta_arquivos:
            if '_generated_' in arquivo:
                aux = re.sub(pattern, '', arquivo)
                arquivos_correspondentes[arquivo] = aux + '_original.json'

        for gerado, original in arquivos_correspondentes.items():
            valor_rkd = rkd.calcular_rank_distance(original, gerado)
            csv_writer.writerow([original, gerado, valor_rkd])

        pares_comparados = set()
        for arquivo in pasta_arquivos:
            if '_original' in arquivo:
                arquivos_autores.append(arquivo)
            for i in range(len(arquivos_autores)):
                for j in range(i+1, len(arquivos_autores)):
                    autor_1 = arquivos_autores[i]
                    autor_2 = arquivos_autores[j]
                    par = tuple(sorted((autor_1, autor_2)))
                    if par not in pares_comparados:
                        valor_rkd = rkd.calcular_rank_distance(autor_1, autor_2)
                        pares_comparados.add(par)
                        csv_writer.writerow([autor_1, autor_2, valor_rkd])

    # Plotagem de Gráficos
    # output_plot_path = 'resultados_metricas_udpipe/plots'
    # pl.plot_metrics_udpipe('resultados_metricas_udpipe/udpipe_metrics.csv', output_plot_path)

else:
    print(f"The folder {JSON_FOLDER_PATH} is empty.")