import boto3, json
from publisher import publish

is_local = False
s3_client = boto3.client('s3', "ap-southeast-2")

def lambda_handler(event, context):
    
    try:
        bucket = "vehicle-image-bucket"
        key = "audi2.png"

        print(f'event: {event}')
        if(event == None):
            return {
                    'statusCode': 200,
                    'body': "empty event"
            } 
            
        message_body = json.loads(event["body"])        
        message =  message_body['message']        
        bucket = message["bucket"]
        key = message["key"]
        connection_id = event["requestContext"].get("connectionId")
        
        print(f'bucket: {bucket}, key: {key}, connection_id: {connection_id} ')

        number_plate = extract_number_plate( bucket, key)
        if(connection_id != None):
            publish(connection_id, number_plate)
        
        return {
            'statusCode': 200,
            'body': json.dumps({"success": True, "message": number_plate})
        }
    except Exception as error:
        print(f'Error occurrred. {error}')
        return {
            'statusCode': 200,
            'body': json.dumps({"success": False, "message": "Failed"})
        }

def get_connection_id(bucket, key):
    try:
        result = s3_client.get_object_tagging( Bucket=bucket,Key= key)
        for tag in result["TagSet"]:
            if(tag["Key"]== "connection_id"):
                return tag["Value"]
        return None
    except Exception as error:
        print('Error while getting connection Id. {error}')
        return None

def write_to_file(response):
    text_file = open("./sample_responses/audi2.json", "w")
    text_file.write(str(response['TextDetections']))    
    text_file.close()

def get_existing_response():
    with open('./sample_responses/audi1.json') as json_file:
        contents = json.load(json_file)
    return contents

def extract_number_plate(bucket, key):
   list = get_detected_text_list(bucket, key)
   print('List', list)
   if(list != None):
       return list[0]
   return "Unable to find number"
   

def get_detected_text_list( bucket, key):
    response = {}
    if(is_local is False):
        client = boto3.client('rekognition', "ap-southeast-2")
        response = client.detect_text(Image= {
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        })
        # write_to_file(response)
        print('Response:', response)
    else:
        print('Reading from local file')
        response = get_existing_response()
    list_of_detected_object = response["TextDetections"]
    
    list_of_detected_text = []
    if(list_of_detected_object != None):
        for item in list_of_detected_object:
            validated_text = validate_detected_text(item["DetectedText"])
            if(validated_text != None):
                list_of_detected_text.append(validated_text)

    return list_of_detected_text

###########
## Custom logic to validate the number plate.
###########
def validate_detected_text(text):
    ## validate length
    text = text.strip()
    if(len(text) != 8):
        return None
    return text

# testing
lambda_handler(None, None)