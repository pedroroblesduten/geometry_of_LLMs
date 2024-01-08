import json

# Conteúdo de exemplo a ser salvo no arquivo JSONL
example_content = [
    {
        "author": "elizabeth bowen",
        "prompt_type": 1,
        "prompt": "write a paragraph to continue the story that follows.: \n",
        "begin_original": "'‘YOU ARE LOSING your imagination,’ cried Maurice. It was a bitter reproach. He stood over her, rumpling up his hair, and the wiry tufts sprang upright, quivering from his scalp.'",
        "complete_original": "'‘YOU ARE LOSING your imagination,’ cried Maurice. It was a bitter reproach. He stood over her, rumpling up his hair, and the wiry tufts sprang upright, quivering from his scalp. Penelope gulped, then sat for a moment in a silence full of the consciousness of her brutality. She had never dreamed that her secret preoccupation would be so perceptible to Maurice. Unconsciously she had been drawing her imaginations in upon herself like the petals of a flower, and her emotions buzzed and throbbed within them like a pent-up bee.'"
    }
    # Você pode adicionar mais entradas aqui se necessário
]

# Definindo o caminho do arquivo onde o conteúdo será salvo
file_path = './data/inputs.jsonl'

# Abrindo o arquivo para escrita e salvando o conteúdo no formato JSONL
with open(file_path, 'w', encoding='utf-8') as file:
    for entry in example_content:
        file.write(json.dumps(entry) + '\n')  # Escrevendo cada entrada como uma linha JSON


