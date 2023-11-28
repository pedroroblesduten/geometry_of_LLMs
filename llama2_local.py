from transformers import AutoTokenizer, pipeline
import torch

# Local model directory (assuming 'model' is the directory where you have saved the model)
local_model_dir = "model"

tokenizer = AutoTokenizer.from_pretrained(local_model_dir)
pipeline = transformers.pipeline(
    "text-generation",
    model=local_model_dir,
    torch_dtype=torch.float16,
    device_map="auto"
)

sequences = pipeline(
    'voce acha que fazer teste de hipoteses é importante?\n',
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    max_length=200,
)

print('\n\n')
print("\033[92m" + "-- LLAMA 2 --" + "\033[0m")
for seq in sequences:
    print(f"Result: {seq['generated_text']}")

