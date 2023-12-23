import json

# Conteúdo de exemplo a ser salvo no arquivo JSONL
example_content = [
    {
        "autor": "clarice lispector",
        "prompt": "escreva um paragrafo para continuar o texto a seguir: ",
        "begin_original": "o que te direi: te direi os instantes. exorbito-me e só então é que",
        "complete_original": "tenho por dom a paixao, nas queimadas de tronco seco contorço-me as labaredas"
    }
    # Você pode adicionar mais entradas aqui se necessário
]

# Definindo o caminho do arquivo onde o conteúdo será salvo
file_path = './data/inputs.jsonl'

# Abrindo o arquivo para escrita e salvando o conteúdo no formato JSONL
with open(file_path, 'w', encoding='utf-8') as file:
    for entry in example_content:
        file.write(json.dumps(entry) + '\n')  # Escrevendo cada entrada como uma linha JSON


