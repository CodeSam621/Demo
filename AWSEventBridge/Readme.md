
## Rule pattern 
```
{
    "detail": {
      "type": ["toy"]
    }
}

```
## Sample payload which can be used in Rule evaluation page

```
{
    "id": "1b8e2e75-b771-e964-f0e6-fbca6a21dad8",
    "detail-type": "test type",
    "source": "test",
    "account": "sasa",
    "resources": [""],
    "time": "2022-10-02T12:47:58Z",
    "region": "ss",
    "detail": {
      "type": "toy"
    }
  }

```

## payload event to test in 'send event' page in AWS console

```
 {
    "name": "lego",
    "price": "10.50",
    "type": "toy"
 } 
```

## Custome payload which can be used to test for Lambda
// payload
```
{
    "name": "lego",
    "price": "10.50",
    "type": "toy"
}
```

## Lambda code to generate events

```
import json
import boto3
import datetime

event_client = boto3.client('events')

def lambda_handler(event, context):    

    # change the 'EventBusName' as per your account and event bus
    response = event_client.put_events(
        Entries= [
                    {
                        'Time': datetime.datetime.now(),
                        'Source': 'Lambda Publish',
                        'Resources': [],
                        'DetailType': 'Demo 1',
                        'Detail': json.dumps(event),
                        'EventBusName': 'arn:aws:events:us-east-1:xxxxxxx:event-bus/test-bus1',
                        'TraceHeader': 'testdemo'
                    },
                ])

```

## Shopify resource URL
https://shopify.dev/apps/webhooks/configuration/eventbridge

## Shopify sample event
```
{
  "version": "0",
  "id": "1b8e2e75-b771-e964-f0e6-fbca6a21dad8",
  "detail-type": ["shopifyWebhook"],
  "source": "aws.partner/shopify.com/shop-event-bus",
  "account": "123456789",
  "resources": [""],
  "time": "2022-10-02T12:47:58Z",
  "region": "ca-central-1",
  "detail": {
    "payload": {
      "product" : {
        "id": 1,
        "title": "Columbia Las Hermosas",
        "body_html": "",
        "vendor": "Reunion Island",
        "product_type": "Coffee",
        "created_at": "2022-10-07T14:55:00-05:00",
        "handle": "columbia-las-hermosas",
        ...
      }
    },
    "metadata": {
      "X-Shopify-Topic": "products/update",
      "X-Shopify-API-Version": "2022-10",
      "X-Shopify-Hmac-SHA256": "rncNozYG6CCjmFJjEgUWowYJ60X+oUtsqul1sTwJMpU=",
      "X-Shopify-Shop-Domain": "{shop}.myshopify.com",
      "X-Shopify-Order-Id": 1
    }
  }
}

```

## Shopify rule pattern

```
{
  "detail-type": ["shopifyWebhook"],
  "detail": {
    "metadata": {
      "X-Shopify-Topic": [{
        "prefix": "products"
      }]
    }
  }
}

```