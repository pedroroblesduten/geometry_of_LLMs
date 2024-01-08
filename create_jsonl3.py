import json

# Conteúdo de exemplo a ser salvo no arquivo JSONL
example_content = [
    {
        "author": "elizabeth bowen",
        "prompt_type": 1,
        "prompt": "write a paragraph to continue the story that follows.: \n",
        "begin_original": "'MR AND MRS TOTTENHAM had come home. The moist brown gravel of the drive and sweep bore impress of their fly wheels. Lydia Broadbent listened from the doorstep to the receding gritty rumble of the empty fly, and the click and rattle as the gate swung to. Behind her, in the dusky hall, Mr Tottenham shouted directions for the disposal of the luggage, flustered servants bumped against each other and recoiled, and Porloch the gardener shouldered the heavy trunks with gasps and lurches, clutching at the banisters until they creaked.'",
        "complete_original": "'MR AND MRS TOTTENHAM had come home. The moist brown gravel of the drive and sweep bore impress of their fly wheels. Lydia Broadbent listened from the doorstep to the receding gritty rumble of the empty fly, and the click and rattle as the gate swung to. Behind her, in the dusky hall, Mr Tottenham shouted directions for the disposal of the luggage, flustered servants bumped against each other and recoiled, and Porloch the gardener shouldered the heavy trunks with gasps and lurches, clutching at the banisters until they creaked. Lydia heard Mrs Tottenham burst open the drawing-room door and cross the threshold with her little customary pounce, as though she hoped to catch somebody unawares. She pictured her looking resentfully round her, and knew that presently she would hear her tweaking at the curtains. During her six weeks of solitude the house had grown very human to Lydia. She felt now as if it were drawing itself together into a nervous rigor, as a man draws himself together in suffering irritation at the entrance of a fussy wife.'"
    }
    # Você pode adicionar mais entradas aqui se necessário
]

# Definindo o caminho do arquivo onde o conteúdo será salvo
file_path = './data/inputs.jsonl'

# Abrindo o arquivo para escrita e salvando o conteúdo no formato JSONL
with open(file_path, 'w', encoding='utf-8') as file:
    for entry in example_content:
        file.write(json.dumps(entry) + '\n')  # Escrevendo cada entrada como uma linha JSON


