import subprocess
import os
import signal

def run_command(command, timeout=300):
    """Run a command with a timeout."""
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the process to complete or timeout
        stdout, stderr = process.communicate(timeout=timeout)

        if process.returncode != 0:
            print(f"Error: {stderr.decode('utf-8')}")
            exit()
        else:
            print(stdout.decode('utf-8'))
    except subprocess.TimeoutExpired:
        print(f"Command '{command}' timed out after {timeout} seconds")
        process.send_signal(signal.SIGINT)  # Send interrupt signal
        process.communicate()

def main():
    if 'CONDA_DEFAULT_ENV' not in os.environ:
        print("Please run this script in a Conda environment with PyTorch and CUDA.")
        return

    print("Cloning the Llama 2 repository...")
    repo_url = "https://github.com/facebookresearch/llama.git"
    run_command(f"git clone {repo_url}")

    print("Installing the repository...")
    os.chdir("llama")
    run_command("pip install -e .")

    download_url = input("Enter the signed URL you received for the model download: ")

    print("Checking for necessary commands...")
    run_command("command -v wget")
    run_command("command -v md5sum")

    print("Downloading the model...")
    run_command(f"chmod +x download.sh")
    run_command(f"./download.sh '{download_url}'")

    model_path = input("Enter the path to your checkpoint directory (e.g., llama-2-7b-chat/): ")
    tokenizer_path = input("Enter the path to your tokenizer model (e.g., tokenizer.model): ")
    model_size = input("Enter the model size (7B, 13B, 70B): ")

    mp_value = {"7B": "1", "13B": "2", "70B": "8"}[model_size]

    print(f"Running the model with size {model_size}...")
    run_command(f"torchrun --nproc_per_node {mp_value} example_chat_completion.py "
                f"--ckpt_dir {model_path} --tokenizer_path {tokenizer_path} "
                f"--max_seq_len 512 --max_batch_size 6")

if __name__ == "__main__":
    main()
