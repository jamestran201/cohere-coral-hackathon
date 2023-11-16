import weaviate
import json
import os


client = weaviate.Client(
  url=os.environ.get("WEAVIATE_INSTANCE_URL"),
  auth_client_secret=weaviate.AuthApiKey(api_key=os.environ.get("WEAVIATE_API_KEY")),
  additional_headers={
    "X-Cohere-Api-Key": os.environ.get("COHERE_API_KEY")
  }
)

schema = {
   "classes": [
       {
           "class": "IncidentReview",
           "description": "Incident reviews from SaaS companies",
           "vectorizer": "text2vec-cohere",
           "moduleConfig": {
               "generative-cohere": { 
                    "model": "command-xlarge-nightly"
                },
                "reranker-cohere": {
                    "model": "rerank-english-v2.0",
                },
           },
           "properties": [
               {
                  "name": "title",
                  "dataType": ["text"],
                  "description": "Title of the incident review",
               },
               {
                  "name": "snippet",
                  "dataType": ["text"],
                  "description": "A snippet from the incident review",
               },
               {
                  "name": "url",
                  "dataType": ["text"],
                  "description": "The url to the original review",
                }
            ]
        }
    ]
}

client.schema.create(schema)

print("Successfully created the schema.")