import boto3
import uuid

# Create SQS client
sqs = boto3.client('sqs')

# update your queue Url as needed
queue_url = 'https://sqs.us-east-1.amazonaws.com/xxx/demo-queue-standard'
#queue_url = 'https://sqs.us-east-1.amazonaws.com/xxx/demo-queue-fifo.fifo'

# Send message to SQS queue
response = sqs.send_message(
    QueueUrl= queue_url,
    # un-comment below lines for FIFO queue
    #MessageGroupId= "G3",
    #MessageDeduplicationId= str(uuid.uuid4()),
    MessageAttributes= {
        'Title': {
            'DataType': 'String',
            'StringValue': 'Mr'
        }
    },
    MessageBody=(f'700')
)

print(response['MessageId'])