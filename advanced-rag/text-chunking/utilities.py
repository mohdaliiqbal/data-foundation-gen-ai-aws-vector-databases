import json
from opensearchpy import OpenSearch, RequestsHttpConnection
import boto3

def embed_phrase( text, model_id, bedrock_client ):
    model_id = model_id # 
    accept = "application/json"
    contentType = "application/json"

    # Prepare the request payload
    request_payload = json.dumps({"inputText": text})

    response = bedrock_client.invoke_model(body=request_payload, modelId=model_id, accept=accept, contentType=contentType)

    # Extract the embedding from the response
    response_body = json.loads(response.get('body').read())

    # Append the embedding to the list
    embedding = response_body.get("embedding")
    return embedding



def opensearch_bulk_load(data, index_name, aos_client):
    
    # Your array of JSON objects

    # Bulk load the data into OpenSearch
    bulk_data = []
    for item in data:
        op_dict = {
            "index": {
                "_index": index_name
            }
        }
        bulk_data.append(json.dumps(op_dict))
        bulk_data.append(json.dumps(item))

    response = aos_client.bulk(bulk_data)

    # Check the response
    if response.errors:
        print(f"Errors occurred: {response.errors}")
        raise Exception(f"Error occurred: {response.errors}")
    else:
        return response