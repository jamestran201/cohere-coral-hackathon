import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

def count_words(text):
    return len(text.split())
    
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 300,
    chunk_overlap = 60,
    length_function = count_words,
)

directory = "raw_data"
for filename in os.listdir(directory):
    if not filename.endswith(".txt"):
        continue

    file_path = os.path.join(directory, filename)
    with open(file_path, "r") as file:
        url = file.readline().strip()
        file.readline()

        title = file.readline().strip()
        file.readline()

        body = file.read().strip()
        chunks = text_splitter.split_text(body)
        for chunk in chunks:
            document = { "title": title, "url": url, "snippet": chunk }
    
            with open("dataset/dataset.jsonl", "a") as f:
                f.write(json.dumps(document) + "\n")