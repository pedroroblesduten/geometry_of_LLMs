import subprocess
import json
import os
import shlex

def process_text_files(model, parser_url, input_path, output_path):
    files = [filename for filename in os.listdir(input_path) if filename.endswith('.json')]
    for filename in files:
        input_file = os.path.join(input_path, filename)
        print(f"Opening {filename}")
        generated_texts = []

        with open(input_file, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)

            author = json_data["author"]
            begin_original = json_data["begin_original"]
            for text_data in json_data["generated"]:
                for c in text_data["generated_text"]:
                    if c.isalpha():
                        generated_texts.append(text_data["generated_text"])
                        break
                    
            try:
                escaped_begin_original = shlex.quote(begin_original)

                command_begin = f"echo {escaped_begin_original} | curl -X POST -F 'data=<-' -F model={model} -F tokenizer= -F tagger= -F parser= {parser_url} | PYTHONIOENCODING=utf-8 python3 -c \"import sys,json; sys.stdout.write(json.load(sys.stdin)['result'])\""

                begin_output_filename = os.path.splitext(filename)[0] + "_original"
                begin_output_file_path = os.path.join(output_path, f"{begin_output_filename}.conllu")
            
                output = subprocess.check_output(command_begin, shell=True, text=True)
                with open(begin_output_file_path, "w", encoding="utf-8") as output_file:
                    output_file.write(output)
                print(f"Original text from {filename} processed and saved as {begin_output_filename}.conllu")

                for index, generated_text in enumerate(generated_texts, start=1):
                    escaped_generated_text = shlex.quote(generated_text)

                    command_generated = f"echo {escaped_generated_text} | curl -X POST -F 'data=<-' -F model={model} -F tokenizer= -F tagger= -F parser= {parser_url} | PYTHONIOENCODING=utf-8 python3 -c \"import sys,json; sys.stdout.write(json.load(sys.stdin)['result'])\""
                    
                    generated_output_filename = os.path.splitext(filename)[0] + f"_generated_{index}"
                    generated_output_file_path = os.path.join(output_path, f"{generated_output_filename}.conllu")

                    output_generated = subprocess.check_output(command_generated, shell=True, text=True)
                    
                    with open(generated_output_file_path, "w", encoding="utf-8") as output_generated_file:
                        output_generated_file.write(output_generated)

                    print(f"Generated text {index} from {filename} processed and saved as {generated_output_filename}.conllu")
                    
            except subprocess.CalledProcessError as e:
                print(f"Error processing {author}'s data from {filename}: {e}")

def json_format(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    def processa_arvore(arvore_atual):
        arvore_json = {
            "sent_id": arvore_atual["sent_id"],
            "text": arvore_atual["text"],
            "palavras": arvore_atual["palavras"]
        }
        return arvore_json

    for arquivo in os.listdir(input_folder):
        if os.path.isfile(os.path.join(input_folder, arquivo)):
            print(arquivo)
            arvores_sentencas = []
            arvore_atual = {}

            with open(os.path.join(input_folder, arquivo), 'r', encoding='utf-8') as arquivo_leitura:
                conteudo = arquivo_leitura.readlines()

                for linha in conteudo:
                    linha = linha.strip()
                    if linha.startswith('# sent_id ='):
                        if arvore_atual:
                            arvores_sentencas.append(processa_arvore(arvore_atual))
                        arvore_atual = {'sent_id': linha.split('=')[1].strip()}
                    elif linha.startswith('# text ='):
                        arvore_atual['text'] = linha.split('=')[1].strip()
                    elif linha and not linha.startswith('#'):
                        campos = linha.split('\t')
                        palavra = {
                            'ID': campos[0],
                            'FORM': campos[1],
                            'LEMMA': campos[2],
                            'UPOS': campos[3],
                            'XPOS': campos[4],
                            'FEATS': campos[5],
                            'HEAD': campos[6],
                            'DEPREL': campos[7],
                            'DEPS': campos[8],
                            'MISC': campos[9]
                        }
                        arvore_atual.setdefault('palavras', []).append(palavra)
                    else:
                        print(linha)

            if arvore_atual:
                arvores_sentencas.append(processa_arvore(arvore_atual))

            nome_arquivo_json = os.path.join(output_folder, arquivo.split('.')[0] + '.json')
            with open(nome_arquivo_json, 'w', encoding='utf-8') as json_file:
                json.dump(arvores_sentencas, json_file, ensure_ascii=False, indent=2)

    print(f"Treated conllu files finished.")