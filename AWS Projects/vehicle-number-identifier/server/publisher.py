import json
import boto3
from botocore.config import Config

callbackUrl = "https://car8br8gbh.execute-api.ap-southeast-2.amazonaws.com/dev"

def publish(connection_id, data):    
    config = Config(
        region_name = 'ap-southeast-2',
        signature_version = 'v4'
    )
    
    try:
        client = boto3.client("apigatewaymanagementapi", endpoint_url=callbackUrl, config=config )
        client.post_to_connection(Data = json.dumps({ "success": True, "message": data}), ConnectionId = connection_id)
    except Exception as error:
        raise Exception(error)




# import boto3

# # callbackUrl = "https://jyqpi0r1y7.execute-api.ap-southeast-2.amazonaws.com/production";
# callbackUrl = "https://car8br8gbh.execute-api.ap-southeast-2.amazonaws.com/dev"
# client = boto3.client('apigatewaymanagementapi', { 'endpoint': callbackUrl })

# def publish(connection_id, data):
    
#     try:
#         command = client.post_to_connection(Data = data, ConnectionId = connection_id)
#         client.send(command)
#     except Exception as error:
#         raise Exception(error)