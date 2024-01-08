import json

# Conteúdo de exemplo a ser salvo no arquivo JSONL
example_content = [
    {
        "author": "elizabeth bowen",
        "prompt_type": 3,
        "prompt": "write another paragraph to continue the story that follows, keeping the style of the story's author, Elizabeth Bowen.: \n",
        "begin_original": "'MISS MURCHESON STOPPED AT the corner of the High Street to buy a bunch of daffodils from the flower-man. She counted out her money very carefully, pouring a little stream of coppers from her purse into the palm of her hand. ‘— ninepence – ten – eleven – pence halfpenny – a shilling! Thank you very much. Good afternoon.’'",
        "complete_original": "'MISS MURCHESON STOPPED AT the corner of the High Street to buy a bunch of daffodils from the flower-man. She counted out her money very carefully, pouring a little stream of coppers from her purse into the palm of her hand. ‘— ninepence – ten – eleven – pence halfpenny – a shilling! Thank you very much. Good afternoon.’ A gust of wind rushed up the street, whirling her skirts up round her like a ballet-dancer’s, and rustling the Reckitts-blue paper round the daffodils. The slender gold trumpets tapped and quivered against her face as she held them up with one hand and pressed her skirts down hastily with the other. She felt as though she had been enticed into a harlequinade by a company of Columbines who were quivering with laughter at her discomfiture; and looked round to see if anyone had witnessed her display of chequered moirette petticoat and the inches of black stocking above her boots. But the world remained unembarrassed.'"
    }
    # Você pode adicionar mais entradas aqui se necessário
]

# Definindo o caminho do arquivo onde o conteúdo será salvo
file_path = './data/inputs.jsonl'

# Abrindo o arquivo para escrita e salvando o conteúdo no formato JSONL
with open(file_path, 'w', encoding='utf-8') as file:
    for entry in example_content:
        file.write(json.dumps(entry) + '\n')  # Escrevendo cada entrada como uma linha JSON


