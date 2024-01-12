from termcolor import colored
import argparse
import torch
from  model_llm import ModelLLM
from load_data import LoadData
from tqdm import tqdm
import os
import json
from datetime import datetime
from transformers import set_seed


def main(input_path, model_name_or_path, device, output_path, seed, num_samples, max_new_tokens, verbose):
    set_seed(seed)
    print(f"Loading {model_name_or_path} on {device}")
    model_llm = ModelLLM(model_name_or_path, output_path, device)
    
    if verbose:
        print("Inputs path:", input_path)
    
    loader = LoadData(input_path)

    print("Begin experiment...")
    result = {}
    i = 0 # contador dos trechos  lidos de um autor
    author = ""
    timemark = datetime.now().strftime("%m%d%Y_%H%M%S")    
    for example in tqdm(loader, unit="input", desc="text inputs"):
        prompt_type = example['prompt_type']
        
        # Mudou de autor? reniciar contador, senao incrementa
        if author != example['author']:
            author = example['author']
            i=0 
        else:
            i+=1 
        
        if verbose:
            print(colored(
                f"-->Info: autor: {example['author']}, prompt_type: {example['prompt_type']}", "yellow"))
            
        tokens_original = model_llm.get_tokens(example['complete_original'])
        embeddings_original = model_llm.get_embeddings(tokens_original)
        result = {
            'author': author,
            'prompt': example['prompt'],
            'prompt_type': prompt_type,
            'begin_original': example['begin_original'],
            'complete_original': example['complete_original'],
            'embeddings_original': embeddings_original.cpu().tolist()
        }

        model_input = example['prompt'] + example['begin_original']
        generated = []
        for i in tqdm(range(num_samples), desc="Genereting", unit="sample", leave=False):
            generated_text = model_llm.generate(
                model_input, 
                max_new_tokens=max_new_tokens, 
                return_embeddings=False)

            
            if verbose:
                print(colored(f"User INPUT: {model_input}", "green"))
                print(colored("-"*100, "cyan"))
                print(colored(f"Model OUTPUT: {generated_text}", "cyan"))
            
            tokens_generated = model_llm.get_tokens(example['begin_original'] + generated_text)
            embeddings_generated = model_llm.get_embeddings(tokens_generated)
            generated.append({
                 "generated_text": generated_text,
                 "tokens_generated": tokens_generated.cpu().tolist(),
                 "embeddings_generated": embeddings_generated.cpu().tolist()
             })
        
        result["generated"] = generated
        json_filename = os.path.join(output_path, f"{author.lower().replace(' ', '_')}_{i}_{prompt_type}_{timemark}.json")
        print(f"Saving file", end="...\t")
        with open(json_filename, 'w') as json_file:
            json.dump(result, json_file, indent=2)
        print(json_filename, "created")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='input_paths')
    parser.add_argument(
        'input_path',
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
    
    parser.add_argument(
        "--seed",
        "-s",
        default=42,
        type=int
    )

    parser.add_argument(
        "--num-samples",
        "-n",
        default=10,
        type=int
    )

    parser.add_argument(
        "--max-new-tokens",
        "-t",
        default=5000,
        type=int
    )

    parser.add_argument(
        "--verbose",
        "-v",
        default=False,
        type=bool
    )

    args = parser.parse_args()
    main(**vars(args))
