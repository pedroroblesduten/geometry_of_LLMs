import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

class ModelLLM:
    def __init__(self,
                 model_name,
                 save_results_path,
                 device
                 ):

        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.save_results_path = save_results_path
        self.device = device
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, device_map=device, torch_dtype=torch.float16)
        
        self.model.eval()
        

        # Create the "resultados" folder if it doesn't exist
        if not os.path.exists(save_results_path):
            os.makedirs(save_results_path)

    def generate(self, input_prompt, max_new_tokens=500, return_embeddings=True):
        model_input = self.tokenizer(input_prompt, return_tensors="pt").to(self.device)
        input_length = model_input.input_ids.size(1)

        with torch.no_grad():
            output = self.model.generate(
                **model_input, 
                max_new_tokens=max_new_tokens)
            
            output_text = self.tokenizer.decode(
                output[0][input_length:], 
                skip_special_tokens=True)
        
        if return_embeddings:
            return output_text, output
        else:
            return output_text
        
    def get_tokens(self, text):
        tokens = self.tokenizer(text, return_tensors='pt') \
            .input_ids.to(self.device)
        
        return tokens

    def get_embeddings(self, tokens, layer=-1):
        with torch.no_grad():
            outputs = self.model(input_ids=tokens, output_hidden_states=True)
            embeddings = outputs.hidden_states[layer]

        return embeddings
    