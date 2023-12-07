from transformers import AutoModelForCausalLM, AutoTokenizer
import os

def download_llama_model(model_name='meta-llama/Llama-2-7b-chat-hf', save_directory='./llama_model'):
    # Set your Hugging Face token
    token = 'Your hf token here'

    # Authenticate with Hugging Face
    os.environ['HF_HOME'] = save_directory
    os.environ['HUGGINGFACE_HUB_TOKEN'] = token

    try:
        # Download the model and tokenizer
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Save the model and tokenizer
        model.save_pretrained(save_directory)
        tokenizer.save_pretrained(save_directory)

        print(f'Model downloaded and saved to {save_directory}')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    download_llama_model()
