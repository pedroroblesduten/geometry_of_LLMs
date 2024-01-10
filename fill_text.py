from termcolor import colored
import argparse
import torch
from  model_llm import ModelLLM
from load_data import LoadData
from tqdm import tqdm
import os
import json
import datetime

def main(input_paths, model_name_or_path, device, output_path):
    
    print(f"Loading {model_name_or_path} on {device}")
    model_llm = ModelLLM(model_name_or_path, output_path, device)
    loader = LoadData(input_paths)

    print("Creating files")
    for example in tqdm(loader, unit="inputs"):
        model_input = example['prompt'] + example['begin_original']
        generated_text, _ = model_llm.generate(model_input)

        # get tokens
        tokens_original = model_llm.get_tokens(example['complete_original'])
        tokens_generated = model_llm.get_tokens(
            example['begin_original'] + generated_text)

        
        embeddings_original = model_llm.get_embeddings(tokens_original)
        embeddings_generated = model_llm.get_embeddings(tokens_generated)

        print(colored(
            f"-->Info: autor: {example['author']}, prompt_type: {example['prompt_type']}", "yellow"))
        
        print(colored(f"User INPUT: {model_input}", "green"))
        print(colored(f"Model OUTPUT: {generated_text}", "cyan"))

        result =  {
            'author': example['author'],
            'prompt': example['prompt'],
            'prompt_type': example['prompt_type'],
            'begin_original': example['begin_original'],
            'complete_original': example['complete_original'],
            'embeddings_original': embeddings_original.cpu().tolist(),
            'embeddings_generated': embeddings_generated.cpu().tolist(),
            'tokens_original': tokens_original.cpu().tolist(),
            'tokens_generated': tokens_generated.cpu().tolist(),
            }
        
        timemark = datetime.now().strftime("%m%d%Y_%H%M%S")
        json_filename = os.path.join(output_path, f"{result['prompt_type']}_{result['author']}_{timemark}.json")
        with open(json_filename, 'w') as json_file:
            json.dump(result, json_file, indent=4)





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='input_paths')
    parser.add_argument(
        'input_paths', 
        nargs='+', 
        help='Paths to input files')
    
    parser.add_argument(
         '--model-name-or-path',
         "-m",
         default="meta-llama/Llama-2-7b-chat-hf"
    )

    parser.add_argument(
         "--device",
         "-d",
         default="cuda" if torch.cuda.is_available() else "cpu"
    )
    
    parser.add_argument(
         "--output-path",
         "-o",
         default="./resultados"
    )

    args = parser.parse_args()
    main(**vars(args))