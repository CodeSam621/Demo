## Lambda: test-hellow-lambda ( GET USER end point)

```python
import json

def lambda_handler(event, context):
    
    print(f'event: {event}');
    
    # this users object can be fetched from database  etc.
    users =  [
                {"id": 1, "name": "john dove"}, 
                {"id": 2, "name": "michel wats"}
             ]
        
    return {
        'statusCode': 200,
        'body': users
    }

```

## Lambda: demo-post-users ( POST USER end point)

```python
import json

def lambda_handler(event, context):
    
    print(f'event: {event}')
    print(f'Posting user details')
    # save the information database
    
    user_name = event['name']

    
    return {
        'statusCode': 200,
        'body': { "message": f'{user_name} added'}
    }


```