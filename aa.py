from transformers import AutoTokenizer
import transformers
import torch

model = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(model, use_auth_token='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')
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
    use_auth_token='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'
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

