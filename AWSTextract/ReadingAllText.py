import json
import boto3
from urllib.parse import unquote_plus

def lambda_handler(event, context):
    textract = boto3.client("textract")
    print(f'Event: {event}')

    if event:
        file_obj = event["Records"][0]
        bucketname = str(file_obj["s3"]["bucket"]["name"])
        filename = unquote_plus(str(file_obj["s3"]["object"]["key"]))

        print(f"Bucket: {bucketname} ::: Key: {filename}")

        response = textract.detect_document_text(
            Document= {
                "S3Object": {
                    "Bucket": bucketname,
                    "Name": filename,
                }
            }
        )
        print(json.dumps(response))

        raw_text = extract_text(response, extract_by="LINE")
        print(raw_text)

        return {
            "statusCode": 200,
            "body": json.dumps("Document processed successfully!"),
        }

    return {"statusCode": 500, "body": "Event is null."}

def extract_text(response, extract_by="LINE"):
    line_text = []
    for block in response["Blocks"]:
        if block["BlockType"] == extract_by:
            line_text.append(block["Text"])
    return line_text