import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import h5py
import numpy as np
from typing import *


class ModelLLM:
    def __init__(self,
                 model_name_or_path,
                 results_path,
                 device,
                 use_auth_token=True,
                 torch_dtype=torch.float16
        ):

        self.device = device
        self.torch_dtype = torch_dtype
        self.model_name_or_path = model_name_or_path
        self.use_auth_token=use_auth_token
        self.results_path = results_path
        self.__load_checkpoint()
        


    def __load_checkpoint(self) -> None:

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path)
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name_or_path, 
            device_map=self.device, 
            torch_dtype=self.torch_dtype,
        )
        
        self.model.eval()

    def generate(self, input_prompt, max_new_tokens=30, return_embbdings=True)-> Tuple[Any, Any]:
        model_input = self.tokenizer(input_prompt, return_tensors="pt").to("cuda")
        input_length = model_input.input_ids.size(1)

        with torch.no_grad():
            generated_output = self.model.generate(
                **model_input, max_new_tokens=max_new_tokens)

            generated_text = self.tokenizer.decode(
                generated_output[0][input_length:], skip_special_tokens=True)
        
        return generated_text, generated_output if return_embbdings else generated_text

    def generate_tokens(self, text)-> torch.Tensor:
        tokens = self.tokenizer(text, return_tensors="pt")
        return tokens

    def get_embeddings_from_input(self, input_text)-> torch.Tensor:
        model_input = self.tokenizer(input_text, return_tensors="pt").to("cuda")
        with torch.no_grad():
            outputs = self.model(**model_input, output_hidden_states=True)
            input_embeddings = outputs.hidden_states[-1].cpu()
        
        return input_embeddings


    def save_results(self, file_name, generated_text, generated_tokens, generated_embeddings):
        raise NotImplementedError("")

