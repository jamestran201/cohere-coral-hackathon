import os
import weaviate
from pydantic import BaseModel
from fastapi import Depends, FastAPI, Request, HTTPException

API_KEY = os.environ.get("FASTAPI_KEY")

weaviate_client = weaviate.Client(
  url=os.environ.get("WEAVIATE_INSTANCE_URL"),
  auth_client_secret=weaviate.AuthApiKey(api_key=os.environ.get("WEAVIATE_API_KEY")),
  additional_headers={
    "X-Cohere-Api-Key": os.environ.get("COHERE_API_KEY")
  }
)

app = FastAPI()

class SearchParameter(BaseModel):
    query: str

@app.post("/search")
def search(param: SearchParameter, request: Request):
    token = request.headers.get("Authorization").split()[-1]
    if token != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid bearer token")

    weaviate_response = (
        weaviate_client.query
        .get("IncidentReview", ["title", "snippet", "url"])
        .with_near_text({
            "concepts": [param.query]
        })
        .with_limit(10)
        .do()
    )

    response = { "results": [] }
    for document in weaviate_response["data"]["Get"]["IncidentReview"]:
        response["results"].append({
            "title": document["title"],
            "snippet": document["snippet"],
            "url": document["url"]
        })

    return response