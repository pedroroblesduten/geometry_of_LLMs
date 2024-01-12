import json
from termcolor import colored

file1 =  open('resultados/elaizabeth_bowen_9_1_01112024_222437.json', encoding='utf8')
file2 = open('./resultados/elaizabeth_bowen_9_1_01112024_224154.json', encoding='utf8')
example = json.load(file1)
example2 = json.load(file2)
model_input = example["prompt"] + example["begin_original"]

for i, sample in enumerate(example["generated"]):
    print(colored(f"-"*150, "red"))
    print(colored("SAME TEXT? " + str(sample == example2["generated"][i]), "red"))
    print(colored(f"-"*150, "green"))
    print(colored(f"User INPUT:\n{model_input}", "green"))
    print(colored("-"*15, "cyan"))
    print(colored(f"Model OUTPUT:\n{sample['generated_text']}", "cyan"))