#!/bin/bash

curl --request POST \
    --url 'https://api.cohere.ai/v1/connectors' \
    --header "Authorization: Bearer $COHERE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data "{
    \"name\":\"electric_lime_connector\",
    \"url\":\"$CONNECTOR_URL\",
    \"service_auth\": {
        \"type\": \"bearer\",
        \"token\": \"$FASTAPI_KEY\"
        }
    }"