import torch
from transformers import LlamaForCausalLM, LlamaTokenizer

def save_prompt_and_response(input_file, output_file, model_id):
    # Load model and tokenizer
    tokenizer = LlamaTokenizer.from_pretrained(model_id)
    model = LlamaForCausalLM.from_pretrained(model_id, device_map='auto', torch_dtype=torch.float16)
    model.eval()

    # Read the prompt from the input file
    with open(input_file, 'r') as file:
        eval_prompt = file.read()

    # Tokenize the input prompt
    model_input = tokenizer(eval_prompt, return_tensors="pt").to("cuda")
    input_length = model_input.input_ids.size(1)

    # Generate response
    with torch.no_grad():
        generated_output = model.generate(**model_input, max_new_tokens=100)
        generated_text = tokenizer.decode(generated_output[0][input_length:], skip_special_tokens=True)

    # Get embeddings for input, output, and complete sequence
    with torch.no_grad():
        outputs = model(**model_input, output_hidden_states=True)
        input_embeddings = outputs.hidden_states[-1][:, :input_length, :]
        output_embeddings = outputs.hidden_states[-1][:, input_length:, :]
        complete_embeddings = outputs.hidden_states[-1]

    # Save to output file
    with open(output_file, 'w') as file:
        # Input prompt and embeddings
        file.write("Input Prompt:\n" + eval_prompt + "\n\nInput Prompt Embeddings:\n")
        for emb in input_embeddings[0]:
            file.write(' '.join(map(str, emb.cpu().numpy())) + '\n')

        # Output prompt and embeddings
        file.write("\nOutput Prompt:\n" + generated_text + "\n\nOutput Prompt Embeddings:\n")
        for emb in output_embeddings[0]:
            file.write(' '.join(map(str, emb.cpu().numpy())) + '\n')

        # Complete sequence and embeddings
        file.write("\nComplete Sequence:\n" + eval_prompt + generated_text + "\n\nComplete Embeddings:\n")
        for emb in complete_embeddings[0]:
            file.write(' '.join(map(str, emb.cpu().numpy())) + '\n')

# Example usage
model_id = "meta-llama/Llama-2-7b-chat-hf"
save_prompt_and_response('input_prompt.txt', 'output_data.txt', model_id)


def load_prompt_and_embeddings(file_path):
    with open(file_path, 'r') as file:
        data = file.read()

    # Split the data into sections
    sections = data.split('\n\n')

    # Extract and print data from each section
    for section in sections:
        title, content = section.split('\n', 1)
        print(title)
        print(content.shape)
        print("\n")

# Example usage
load_prompt_and_embeddings('output_data.txt')

