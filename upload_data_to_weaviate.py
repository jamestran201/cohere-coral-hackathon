import weaviate
import os
from langchain.document_loaders import JSONLoader

def metadata_func(record, metadata):
    metadata["title"] = record.get("title")
    metadata["url"] = record.get("url")

    return metadata

loader = JSONLoader(
    file_path="dataset/dataset.jsonl",
    jq_schema=".",
    content_key="snippet",
    text_content=False,
    json_lines=True,
    metadata_func=metadata_func)

data = loader.load()

client = weaviate.Client(
  url=os.environ.get("WEAVIATE_INSTANCE_URL"),
  auth_client_secret=weaviate.AuthApiKey(api_key=os.environ.get("WEAVIATE_API_KEY")),
  additional_headers={
    "X-Cohere-Api-Key": os.environ.get("COHERE_API_KEY")
  }
)
with client.batch as batch:
    batch.batch_size=100

    for i, d in enumerate(data):
        print(f"Importing snippet #{i+1}")

        properties = {
            "title": d.metadata["title"],
            "snippet": d.page_content,
            "url": d.metadata["url"]
        }

        client.batch.add_data_object(properties, "IncidentReview")