import json

# Conteúdo de exemplo a ser salvo no arquivo JSONL
example_content = [
    {
        "author": "clarice lispector",
        "prompt_type": 1,
        "prompt": "write a paragraph to continue the story that follows.: \n",
        "begin_original": "'estou procurando, estou procurando. Estou tentando entender. Tentando dar a alguém o que vivi e não sei a quem, mas não quero ficar com o que vivi. Não sei o que fazer com o que vivi, tenho medo dessa desorganização profunda.'",
        "complete_original": "'estou procurando, estou procurando. Estou tentando " +
                             "entender. Tentando dar a alguém o que vivi e não sei a quem, mas " +
                             "não quero ficar com o que vivi. Não sei o que fazer do que vivi, " +
                             "tenho medo dessa desorganização profunda. Não confio no que me " +
                             "aconteceu. Aconteceu-me alguma coisa que eu, pelo fato de não a " +
                             "saber como viver, vivi uma outra? A isso quereria chamar " +
                             "desorganização, e teria a segurança de me aventurar, porque "+
                             "saberia depois para onde voltar: para a organização anterior. A isso "+
                             "prefiro chamar desorganização pois não quero me confirmar no "+
                             "que vivi - na confirmação de mim eu perderia o mundo como eu o tinha, e sei que não tenho capacidade para outro. '"
    }
    # Você pode adicionar mais entradas aqui se necessário
]

# Definindo o caminho do arquivo onde o conteúdo será salvo
file_path = './data/inputs.jsonl'

# Abrindo o arquivo para escrita e salvando o conteúdo no formato JSONL
with open(file_path, 'w', encoding='utf-8') as file:
    for entry in example_content:
        file.write(json.dumps(entry) + '\n')  # Escrevendo cada entrada como uma linha JSON


