import json

# Conteúdo de exemplo a ser salvo no arquivo JSONL
example_content = [
    {
        "author":"elizabeth bowen",
        "prompt_type":3,
        "prompt":"write another paragraph to continue the story that follows, keeping the style of the story's author, Elizabeth Bowen.: \n",
        "begin_original":"'‘YOU ARE LOSING your imagination,’ cried Maurice. It was a bitter reproach. He stood over her, rumpling up his hair, and the wiry tufts sprang upright, quivering from his scalp.'",
        "complete_original":"'‘YOU ARE LOSING your imagination,’ cried Maurice. It was a bitter reproach. He stood over her, rumpling up his hair, and the wiry tufts sprang upright, quivering from his scalp. Penelope gulped, then sat for a moment in a silence full of the consciousness of her brutality. She had never dreamed that her secret preoccupation would be so perceptible to Maurice. Unconsciously she had been drawing her imaginations in upon herself like the petals of a flower, and her emotions buzzed and throbbed within them like a pent-up bee.'"
    },
    {
        "author":"elizabeth bowen",
        "prompt_type":1,
        "prompt":"write a paragraph to continue the story that follows.: \n",
        "begin_original":"'‘YOU ARE LOSING your imagination,’ cried Maurice. It was a bitter reproach. He stood over her, rumpling up his hair, and the wiry tufts sprang upright, quivering from his scalp.'",
        "complete_original":"'‘YOU ARE LOSING your imagination,’ cried Maurice. It was a bitter reproach. He stood over her, rumpling up his hair, and the wiry tufts sprang upright, quivering from his scalp. Penelope gulped, then sat for a moment in a silence full of the consciousness of her brutality. She had never dreamed that her secret preoccupation would be so perceptible to Maurice. Unconsciously she had been drawing her imaginations in upon herself like the petals of a flower, and her emotions buzzed and throbbed within them like a pent-up bee.'"
    },
    {
        "author":"elizabeth bowen",
        "prompt_type":3,
        "prompt":"write another paragraph to continue the story that follows, keeping the style of the story's author, Elizabeth Bowen.: \n",
        "begin_original":"'MR AND MRS TOTTENHAM had come home. The moist brown gravel of the drive and sweep bore impress of their fly wheels. Lydia Broadbent listened from the doorstep to the receding gritty rumble of the empty fly, and the click and rattle as the gate swung to. Behind her, in the dusky hall, Mr Tottenham shouted directions for the disposal of the luggage, flustered servants bumped against each other and recoiled, and Porloch the gardener shouldered the heavy trunks with gasps and lurches, clutching at the banisters until they creaked.'",
        "complete_original":"'MR AND MRS TOTTENHAM had come home. The moist brown gravel of the drive and sweep bore impress of their fly wheels. Lydia Broadbent listened from the doorstep to the receding gritty rumble of the empty fly, and the click and rattle as the gate swung to. Behind her, in the dusky hall, Mr Tottenham shouted directions for the disposal of the luggage, flustered servants bumped against each other and recoiled, and Porloch the gardener shouldered the heavy trunks with gasps and lurches, clutching at the banisters until they creaked. Lydia heard Mrs Tottenham burst open the drawing-room door and cross the threshold with her little customary pounce, as though she hoped to catch somebody unawares. She pictured her looking resentfully round her, and knew that presently she would hear her tweaking at the curtains. During her six weeks of solitude the house had grown very human to Lydia. She felt now as if it were drawing itself together into a nervous rigor, as a man draws himself together in suffering irritation at the entrance of a fussy wife.'"
    },
    {
        "author":"elizabeth bowen",
        "prompt_type":1,
        "prompt":"write a paragraph to continue the story that follows.: \n",
        "begin_original":"'MR AND MRS TOTTENHAM had come home. The moist brown gravel of the drive and sweep bore impress of their fly wheels. Lydia Broadbent listened from the doorstep to the receding gritty rumble of the empty fly, and the click and rattle as the gate swung to. Behind her, in the dusky hall, Mr Tottenham shouted directions for the disposal of the luggage, flustered servants bumped against each other and recoiled, and Porloch the gardener shouldered the heavy trunks with gasps and lurches, clutching at the banisters until they creaked.'",
        "complete_original":"'MR AND MRS TOTTENHAM had come home. The moist brown gravel of the drive and sweep bore impress of their fly wheels. Lydia Broadbent listened from the doorstep to the receding gritty rumble of the empty fly, and the click and rattle as the gate swung to. Behind her, in the dusky hall, Mr Tottenham shouted directions for the disposal of the luggage, flustered servants bumped against each other and recoiled, and Porloch the gardener shouldered the heavy trunks with gasps and lurches, clutching at the banisters until they creaked. Lydia heard Mrs Tottenham burst open the drawing-room door and cross the threshold with her little customary pounce, as though she hoped to catch somebody unawares. She pictured her looking resentfully round her, and knew that presently she would hear her tweaking at the curtains. During her six weeks of solitude the house had grown very human to Lydia. She felt now as if it were drawing itself together into a nervous rigor, as a man draws himself together in suffering irritation at the entrance of a fussy wife.'"
    },
    {
        "author":"elizabeth bowen",
        "prompt_type":3,
        "prompt":"write another paragraph to continue the story that follows, keeping the style of the story's author, Elizabeth Bowen.: \n",
        "begin_original":"'MISS MURCHESON STOPPED AT the corner of the High Street to buy a bunch of daffodils from the flower-man. She counted out her money very carefully, pouring a little stream of coppers from her purse into the palm of her hand. ‘— ninepence – ten – eleven – pence halfpenny – a shilling! Thank you very much. Good afternoon.’'",
        "complete_original":"'MISS MURCHESON STOPPED AT the corner of the High Street to buy a bunch of daffodils from the flower-man. She counted out her money very carefully, pouring a little stream of coppers from her purse into the palm of her hand. ‘— ninepence – ten – eleven – pence halfpenny – a shilling! Thank you very much. Good afternoon.’ A gust of wind rushed up the street, whirling her skirts up round her like a ballet-dancer’s, and rustling the Reckitts-blue paper round the daffodils. The slender gold trumpets tapped and quivered against her face as she held them up with one hand and pressed her skirts down hastily with the other. She felt as though she had been enticed into a harlequinade by a company of Columbines who were quivering with laughter at her discomfiture; and looked round to see if anyone had witnessed her display of chequered moirette petticoat and the inches of black stocking above her boots. But the world remained unembarrassed.'"
    },
    {
        "author":"elizabeth bowen",
        "prompt_type":1,
        "prompt":"write a paragraph to continue the story that follows.: \n",
        "begin_original":"'MISS MURCHESON STOPPED AT the corner of the High Street to buy a bunch of daffodils from the flower-man. She counted out her money very carefully, pouring a little stream of coppers from her purse into the palm of her hand. ‘— ninepence – ten – eleven – pence halfpenny – a shilling! Thank you very much. Good afternoon.’'",
        "complete_original":"'MISS MURCHESON STOPPED AT the corner of the High Street to buy a bunch of daffodils from the flower-man. She counted out her money very carefully, pouring a little stream of coppers from her purse into the palm of her hand. ‘— ninepence – ten – eleven – pence halfpenny – a shilling! Thank you very much. Good afternoon.’ A gust of wind rushed up the street, whirling her skirts up round her like a ballet-dancer’s, and rustling the Reckitts-blue paper round the daffodils. The slender gold trumpets tapped and quivered against her face as she held them up with one hand and pressed her skirts down hastily with the other. She felt as though she had been enticed into a harlequinade by a company of Columbines who were quivering with laughter at her discomfiture; and looked round to see if anyone had witnessed her display of chequered moirette petticoat and the inches of black stocking above her boots. But the world remained unembarrassed.'"
    },
    {
        "author":"elizabeth bowen",
        "prompt_type":3,
        "prompt":"write another paragraph to continue the story that follows, keeping the style of the story's author, Elizabeth Bowen.: \n",
        "begin_original":"'‘BEHOLD, I DIE daily,’ thought Mr Rossiter, entering the breakfast-room. He saw the family in silhouette against the windows; the windows looked out into a garden closed darkly in upon by walls. There were so many of the family it seemed as though they must have multiplied during the night; their flesh gleamed pinkly in the cold northern light and they were always moving. Often, like the weary shepherd, he could have prayed them to keep still that he might count them.'",
        "complete_original":"'‘BEHOLD, I DIE daily,’ thought Mr Rossiter, entering the breakfast-room. He saw the family in silhouette against the windows; the windows looked out into a garden closed darkly in upon by walls. There were so many of the family it seemed as though they must have multiplied during the night; their flesh gleamed pinkly in the cold northern light and they were always moving. Often, like the weary shepherd, he could have prayed them to keep still that he might count them. They turned at his entrance profiles and three-quarter faces towards him. There was a silence of suspended munching and little bulges of food were thrust into their cheeks that they might wish him perfunctory good- mornings.'"
    },
    {
        "author":"elizabeth bowen",
        "prompt_type":1,
        "prompt":"write a paragraph to continue the story that follows.: \n",
        "begin_original":"'‘BEHOLD, I DIE daily,’ thought Mr Rossiter, entering the breakfast-room. He saw the family in silhouette against the windows; the windows looked out into a garden closed darkly in upon by walls. There were so many of the family it seemed as though they must have multiplied during the night; their flesh gleamed pinkly in the cold northern light and they were always moving. Often, like the weary shepherd, he could have prayed them to keep still that he might count them.'",
        "complete_original":"'‘BEHOLD, I DIE daily,’ thought Mr Rossiter, entering the breakfast-room. He saw the family in silhouette against the windows; the windows looked out into a garden closed darkly in upon by walls. There were so many of the family it seemed as though they must have multiplied during the night; their flesh gleamed pinkly in the cold northern light and they were always moving. Often, like the weary shepherd, he could have prayed them to keep still that he might count them. They turned at his entrance profiles and three-quarter faces towards him. There was a silence of suspended munching and little bulges of food were thrust into their cheeks that they might wish him perfunctory good- mornings.'"
    }
]
    
# Definindo o caminho do arquivo onde o conteúdo será salvo
file_path = './data/inputs.jsonl'

# Abrindo o arquivo para escrita e salvando o conteúdo no formato JSONL
with open(file_path, 'w', encoding='utf-8') as file:
    for entry in example_content:
        file.write(json.dumps(entry) + '\n')  # Escrevendo cada entrada como uma linha JSON


