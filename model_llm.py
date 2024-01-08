import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import h5py
import numpy as np
from load_data import LoadData
from termcolor import colored

class ModelLLM:
    def __init__(self,
                 model_name,
                 save_results_path
                 ):

        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map='auto', torch_dtype=torch.float16)
        self.model.eval()
        self.save_results_path = save_results_path

    def generate_text(self, input_prompt, max_new_tokens=500):
        print('\n')
        print(colored("───────────────────────────────────────────────────", "cyan"))
        print(colored(" --- USER INPUT ---", "green"))
        print(input_prompt)
        print(colored("───────────────────────────────────────────────────", "cyan"))

        model_input = self.tokenizer(input_prompt, return_tensors="pt").to("cuda")
        input_length = model_input.input_ids.size(1)

        with torch.no_grad():
            generated_output = self.model.generate(**model_input, max_new_tokens=max_new_tokens)
            generated_text = self.tokenizer.decode(generated_output[0][input_length:], skip_special_tokens=True)

        print(colored("───────────────────────────────────────────────────", "cyan"))
        print(colored(f" --- LLM OUTPUT: model {self.model_name} ---", "yellow"))
        print(generated_text)
        print(colored("───────────────────────────────────────────────────", "cyan"))
        print('\n')

        return generated_text

    def generate(self, input_prompt, max_new_tokens=500):
        model_input = self.tokenizer(input_prompt, return_tensors="pt").to("cuda")
        input_length = model_input.input_ids.size(1)
        with torch.no_grad():
            generated_tokens = self.model.generate(**model_input, max_new_tokens=max_new_tokens)
            generated_text = self.tokenizer.decode(generated_tokens[0][input_length:], skip_special_tokens=True)

        return generated_text

    def get_tokens(self, text):
        tokens = self.tokenizer(text, return_tensors='pt').input_ids.to("cuda")
        return tokens

    def get_embeddings(self, tokens, layer=None):
        if layer is None:
            layer = -1

        with torch.no_grad():
            outputs = self.model(input_ids=tokens, output_hidden_states=True)
            embeddings = outputs.hidden_states[layer]

        return embeddings


    def get_result_dict(self, data):
        model_input = data['prompt'] + data['begin_original']

        # generating text
        generated_text = self.generate(model_input)

        # get tokens
        tokens_original = self.get_tokens(data['complete_original'])
        tokens_generated = self.get_tokens(data['begin_original'] + generated_text)

        # get embeddings
        embeddings_original = self.get_embeddings(tokens_original)
        embeddings_generated = self.get_embeddings(tokens_generated)

        return_dict = {
                'autor': data['author'],
                'prompt': data['prompt'],
                'prompt_type': data['prompt_type'],
                'begin_original': data['begin_original'],
                'complete_original': data['complete_original'],
                'embeddings_original': embeddings_original,
                'embeddings_generated': embeddings_generated,
                'tokens_original': tokens_original,
                'tokens_generated': tokens_generated,
                }

        return return_dict


# Example usage
model_llm = ModelLLM("meta-llama/Llama-2-7b-chat-hf", "./results/")

# Create an empty list to store result dictionaries
results_list = []

# load data
loader = LoadData('./data/inputs.jsonl')

for example in loader:
    out = model_llm.generate_text(example['prompt'] + example['begin_original'])
    result_dict = model_llm.get_result_dict(example)

    # Append the result dictionary to the list
    results_list.append(result_dict)

    for chave, valor in result_dict.items():
        print(colored(f" -- {chave}: --", 'green'))
        print(valor)
        print('\n')

# Define the path for the JSON file
json_file_path = "./resultados/results.json"

# Write the list of result dictionaries to the JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(results_list, json_file, indent=4)

print(f"Results saved to {json_file_path}")