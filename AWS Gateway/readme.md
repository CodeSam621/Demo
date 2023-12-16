## Lambda: test-hellow-lambda

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
        'body': json.dumps(users)
    }

```

## Lambda: demo-post-users

```python
import json

def lambda_handler(event, context):
    
    print(f'event: {event}')
    print(f'Posting user details')
    # save the information database
    
    return {
        'statusCode': 200,
        'body': json.dumps('User added')
    }

```