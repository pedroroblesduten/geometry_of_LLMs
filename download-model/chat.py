import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def load_model(model_directory='./llama_model'):
    """
    Load the model and tokenizer from the specified directory.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_directory)
    model = AutoModelForCausalLM.from_pretrained(model_directory)
    return model, tokenizer

def generate_text(input_text, model, tokenizer):
    """
    Generate text using the model based on the input text.
    """
    # Tokenize the input text
    input_ids = tokenizer.encode(input_text, return_tensors='pt')

    # Generate a response from the model
    output = model.generate(input_ids, max_length=50)

    # Decode the output to human-readable text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Load the model and tokenizer
model, tokenizer = load_model('./llama_model')

# Input text (can be modified)
input_text = "Hello, how are you today?"

# Generate and print the model's response
response = generate_text(input_text, model, tokenizer)
print(response)
