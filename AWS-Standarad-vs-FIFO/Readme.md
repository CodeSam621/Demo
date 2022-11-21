## SQS quotas
- https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html

 ## Long polling and short polling
 - https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html


## Lambda code

```
import json

def lambda_handler(event, context):
  
    for item in event["Records"]:
        body =  item["body"]
        print(f'message: ', body)

        # throw error to simulate the an error in the Lambda
        myvalue = float(body)        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```