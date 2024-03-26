# Importações e definições iniciais
from termcolor import colored
import argparse
import torch
from model_llm import ModelLLM
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
    for example in tqdm(loader, unit="input", desc="text inputs"):
        prompt_type = example['prompt_type']
        author = example["author"]
        title = example["title"]
        if verbose:
            print(colored(f"-->Info: author: {author}, prompt_type: {prompt_type}", "yellow"))

        model_input = example['prompt'] + example['begin_original']
        generated = []
        approved_count = 0

        for i in tqdm(range(50), desc="Generating", unit="sample", leave=False):
            if approved_count >= num_samples:
                break

            generated_text = model_llm.generate(
                model_input, 
                max_new_tokens=max_new_tokens, 
                return_embeddings=False)

            # Exibir o texto gerado
            print(colored("Generated Text:", "green"))
            print(generated_text)

            # Solicitar aprovação
            approval = input("Approve this sample? (yes/no): ")
            if approval.lower() == 'yes':
                approved_count += 1
                tokens_generated = model_llm.get_tokens(generated_text)
                embeddings_generated = model_llm.get_embeddings(tokens_generated)
                generated.append({
                    "generated_text": generated_text,
                    "tokens_generated": tokens_generated.cpu().tolist(),
                    "embeddings_generated": embeddings_generated.cpu().tolist()
                })

        result = {
            'author': author,
            'title': title,
            'prompt': example['prompt'],
            'prompt_type': prompt_type,
            'begin_original': example['begin_original'],
            'complete_original': example['complete_original'],
            'generated': generated
        }

        timemark = datetime.now().strftime("%m%d%Y_%H%M%S")
        json_filename = os.path.join(output_path, f"{author.lower().replace(' ', '_')}_{prompt_type}_{timemark}.json")
        print(f"Saving file", end="...\t")
        with open(json_filename, 'w') as json_file:
            json.dump(result, json_file, indent=2)
        print(json_filename, "created")

# Execução condicional
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
         default="./resultados_llama"
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
