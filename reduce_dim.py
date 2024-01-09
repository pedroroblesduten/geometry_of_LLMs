import argparse
import os
from umap import UMAP
import glob
import json
import numpy as np
from tqdm import tqdm

MODEL_NAMES = ["umap"]
NUM_SETUPS = 2


def main(input_paths, output_path, model_name, n_components, verbose, setup):
    data = []
    for path in input_paths:
        files = (glob.glob(path))
        for file in files:
            with open(file, 'r', encoding="utf8") as fp:
                data_file = json.load(fp)
                data.append(data_file)


    if len(data) == 1 and isinstance(data[0], list):
        data = data[0]

    model = get_projection_model(model_name, n_components, verbose)
    if setup == 1:
        output = setup1(model, data, n_components)
    else:
        raise NotImplementedError("Setup not found")

    
    print('Saving output file', end="...")
    with open(output_path, 'w', encoding="utf8") as fp:
        json.dump(data, fp)
    print("Done")
    print("Execution Finished")
    
    


def setup1(model, data, n_components):
    embeddings = []
    for example in tqdm(data, desc="Joining word emmbdings", unit='texts'):
        embeddings.append(np.array(example['embeddings_original']))
        embeddings.append(np.array(example['embeddings_generated']))
    
    print("Tranning projection model...")
    embeddings = np.concatenate(embeddings, axis=1)
    embeddings = embeddings.reshape(-1, embeddings.shape[-1])
    print("Final set shape:", embeddings.shape)

    model.fit(embeddings)
    del embeddings
    for example in tqdm(data, desc="Genereting reduced embeddings", unit='embeddings'):
        ori = np.array(example['embeddings_original'])
        gen = np.array(example['embeddings_generated'])
        
        example[f"{n_components}d_original"] = model.transform(
            ori.reshape(-1, ori.shape[-1])).tolist()

        example[f"{n_components}d_generated"] = model.transform(
            gen.reshape(-1, gen.shape[-1])).tolist()
        
    return data


def get_projection_model(name, n_components, verbose):
    if name == 'umap':
        return UMAP(n_components=n_components, verbose=verbose)


def is_valid_model_name(name):
    if any([name == n for n in MODEL_NAMES]):
        return name
    
    raise argparse.ArgumentTypeError(f"Projection Model {name} does not implemented")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generete projections and save final file')
    parser.add_argument(
        'input_paths', 
        nargs='+', 
        help='Paths to input files, accepts wilds cards')
    
    parser.add_argument(
        '--output-path', 
        '-o',
        default='./resultados/final_file.json',
        help='Path to output file')
    
    parser.add_argument(
        '--model-name', 
        '-m', 
        default='umap', 
        type=is_valid_model_name,
        help="Projection Model name")
    
    parser.add_argument(
        '--n-components', 
        '-n', 
        type=int,
        default=9,
        help="Number of components of projection")    
    
    parser.add_argument('--verbose','-v', default=True, type=bool, help="Verbose mode")

    parser.add_argument('--setup', '-s', default=1, type=int, help="Setup code")

    args = parser.parse_args()
    main(**vars(args))
