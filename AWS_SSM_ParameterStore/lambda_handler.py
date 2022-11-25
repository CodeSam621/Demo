import boto3
import os

client = boto3.client('ssm')

def lambda_handler(event, context):
    parameter = client.get_parameter(Name= os.environ['ENV_DB_CONNECTION_STRING'], WithDecryption=True)
    print(f'parameter: {parameter}')
    
    print(f" Password:  { parameter ['Parameter']['Value']}");