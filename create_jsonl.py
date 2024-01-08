import json

# Conteúdo de exemplo a ser salvo no arquivo JSONL
example_content = [
    {
        "author": "clarice lispector",
        "prompt_type": 1,
        "prompt": "without any commentary or instructions before simply continue the story, write a paragraph to continue the story that follows.: \n",
        "begin_original": "'COMING INTO MOHER over the bridge, you may see a terrace of houses by the river. They are to the left of the bridge, below it. Their narrow height and faded air of importance make them seem to mark the approach to some larger town. The six dwellings unite into one frontage, colour-washed apricot years ago. They face north. Their lower sash windows, front steps and fanlit front doors are screened by lime trees, making for privacy. There are area railings. Between them and the water runs a road with a parapet, which comes to its end opposite the last house.'",
        "complete_original": "'COMING INTO MOHER over the bridge, you may see a terrace of houses by the river. They are to the left of the bridge, below it. Their narrow height and faded air of importance make them seem to mark the approach to some larger town. The six dwellings unite into one frontage, colour-washed apricot years ago. They face north. Their lower sash windows, front steps and fanlit front doors are screened by lime trees, making for privacy. There are area railings. Between them and the water runs a road with a parapet, which comes to its end opposite the last house. On the other side of the bridge picturesquely rises a ruined castle – more likely to catch the tourist’s eye. Woods, from which the river emerges, go back deeply behind the ruin: on clear days there is a backdrop of Irish-blue mountains. Otherwise Moher has little to show. The little place prospers – a market town with a square, on a main road. The hotel is ample, cheerful, and does business. Moreover Moher is, and has been for ages, a milling town. Obsolete stone buildings follow you some way along the river valley as, having passed through Moher, you pursue your road. The flour-white modern mills, elsewhere, hum.'"
    }
    # Você pode adicionar mais entradas aqui se necessário
]

# Definindo o caminho do arquivo onde o conteúdo será salvo
file_path = './data/inputs.jsonl'

# Abrindo o arquivo para escrita e salvando o conteúdo no formato JSONL
with open(file_path, 'w', encoding='utf-8') as file:
    for entry in example_content:
        file.write(json.dumps(entry) + '\n')  # Escrevendo cada entrada como uma linha JSON


