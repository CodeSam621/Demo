import json
import boto3
from botocore.config import Config

callbackUrl = "YOUR WSS END POINT" # URL like "https://xxxxxxxxx.execute-api.ap-southeast-2.amazonaws.com/<stage>"

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
