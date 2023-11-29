import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import h5py
import numpy as np

class ModelLLM:
    def __init__(self,
                 model_name,
                 save_results_path
                 ):

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map='auto', torch_dtype=torch.float16)
        self.model.eval()

    def generate_text(self, input_prompt, max_new_tokens=100):
        model_input = self.tokenizer(input_prompt, return_tensors="pt").to("cuda")
        input_length = model_input.input_ids.size(1)

        with torch.no_grad():
            generated_output = self.model.generate(**model_input, max_new_tokens=max_new_tokens)
            generated_text = self.tokenizer.decode(generated_output[0][input_length:], skip_special_tokens=True)
        return generated_text

    def generate_tokens(self, text):
        tokens = self.tokenizer(text, return_tensors="pt").input_ids
        return tokens

    def generate_embeddings(self, text):
        model_input = self.tokenizer(text, return_tensors="pt").to("cuda")
        with torch.no_grad():
            outputs = self.model(**model_input, output_hidden_states=True)
            embeddings = outputs.hidden_states[-1].cpu().numpy()
        return embeddings

    def save_results(self, generated_text, generated_embeddings, generated_tokens):
        with h5py.File(file_name, 'w') as f:
            f.create_dataset('generated_text', data=np.string_(generated_text))
            f.create_dataset('tokens', data=generate_tokens.cpu().numpy())
            f.create_dataset('embeddings', data=generated_embeddings)
