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
        self.save_results_path = save_results_path

    def generate_text(self, input_prompt, max_new_tokens=30):
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

    def get_embeddings_from_input(self, input_text):
        model_input = self.tokenizer(input_text, return_tensors="pt").to("cuda")
        with torch.no_grad():
            outputs = self.model(**model_input, output_hidden_states=True)
            input_embeddings = outputs.hidden_states[-1].cpu().numpy()
        return input_embeddings

    def save_results(self, file_name, generated_text, generated_tokens, generated_embeddings):
        with h5py.File(self.save_results_path + file_name, 'w') as f:
            f.create_dataset('generated_text', data=np.string_(generated_text))
            f.create_dataset('tokens', data=generated_tokens.cpu().numpy())
            f.create_dataset('embeddings', data=generated_embeddings)

# Example usage
model_llm = ModelLLM("meta-llama/Llama-2-7b-chat-hf", "./results/")
input_text = "Complete o texto a seguir: tenho por dom a paixao, nas queimadas de tronco seco"
text = model_llm.generate_text(input_text)
print(text)
input_embeddings = model_llm.get_embeddings_from_input(input_text)
print(input_embeddings.shape)


model.generate_text('oi tudo bem')

model.plot_convex_hull(text1=caminho.txt)

