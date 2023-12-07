from transformers import AutoTokenizer
import transformers
import torch
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer

model_id = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = LlamaTokenizer.from_pretrained(model_id)

model = LlamaForCausalLM.from_pretrained(model_id, device_map='auto', torch_dtype=torch.float16)

print("\033[92m" + "-- INPUT PROMPT --" + "\033[0m")
eval_prompt = """
Fala ai meu mano llama, tudo bem?
"""
print(eval_prompt)

model_input = tokenizer(eval_prompt, return_tensors="pt").to("cuda")

print("\033[92m" + "-- LLAMA 2 --" + "\033[0m")
# Generate text
model_input = tokenizer(eval_prompt, return_tensors="pt").to("cuda")
input_length = model_input.input_ids.size(1)

model.eval()
with torch.no_grad():
    generated_output = model.generate(**model_input, max_new_tokens=100)
    generated_text = tokenizer.decode(generated_output[0][input_length:], skip_special_tokens=True)

# Print the generated text
print(generated_text)
# Get hidden states
with torch.no_grad():
    outputs = model(**model_input, output_hidden_states=True)
    hidden_states = outputs.hidden_states

# Access the embeddings (for example, the last layer)
embeddings = hidden_states[-1]

# Print or process the embeddings
print('\n\n == OUTPUT EMBEDDINGS == ')
print('\n embeddings shape: ', embeddings.shape)
print('\n embeddings vectors: ')
print(embeddings)
