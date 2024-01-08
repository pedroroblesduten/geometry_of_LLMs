import json

# Conteúdo de exemplo a ser salvo no arquivo JSONL
example_content = [
    {
        "author": "elizabeth bowen",
        "prompt_type": 1,
        "prompt": "write a paragraph to continue the story that follows.: \n",
        "begin_original": "'‘BEHOLD, I DIE daily,’ thought Mr Rossiter, entering the breakfast-room. He saw the family in silhouette against the windows; the windows looked out into a garden closed darkly in upon by walls. There were so many of the family it seemed as though they must have multiplied during the night; their flesh gleamed pinkly in the cold northern light and they were always moving. Often, like the weary shepherd, he could have prayed them to keep still that he might count them.'",
        "complete_original": "'‘BEHOLD, I DIE daily,’ thought Mr Rossiter, entering the breakfast-room. He saw the family in silhouette against the windows; the windows looked out into a garden closed darkly in upon by walls. There were so many of the family it seemed as though they must have multiplied during the night; their flesh gleamed pinkly in the cold northern light and they were always moving. Often, like the weary shepherd, he could have prayed them to keep still that he might count them. They turned at his entrance profiles and three-quarter faces towards him. There was a silence of suspended munching and little bulges of food were thrust into their cheeks that they might wish him perfunctory good- mornings.'"
    }
    # Você pode adicionar mais entradas aqui se necessário
]

# Definindo o caminho do arquivo onde o conteúdo será salvo
file_path = './data/inputs.jsonl'

# Abrindo o arquivo para escrita e salvando o conteúdo no formato JSONL
with open(file_path, 'w', encoding='utf-8') as file:
    for entry in example_content:
        file.write(json.dumps(entry) + '\n')  # Escrevendo cada entrada como uma linha JSON


