import json

class LoadData:
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            for line in file:
                data = json.loads(line)
                yield data

# Uso da classe
if __name__ == "__main__":
    loader = LoadData("./data/inputs.jsonl")
    for item in loader:
        print(item)
