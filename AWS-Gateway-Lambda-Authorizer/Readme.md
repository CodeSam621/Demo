
## Authorizer response
```json
{ 
"principalId": "any-api-principle-id", 
    "policyDocument": 
    { 
        "Version": "2012-10-17",
            "Statement": 
            [
                {
                    "Action": "execute-api:Invoke", 
                    "Resource": ["arn:aws:execute-api:YOUR_AWS_REGION:YOURACCOUNTNUMBER:YOUR_API_IDENTIFIER/STAGEING_ENV/VERB/RESOURCE"], 
                    "Effect": "Allow" // Allow OR Deny
                }
            ] 
    }
}
```

## Resource format
"Resource": ["arn:aws:execute-api:YOUR_AWS_REGION:YOURACCOUNTNUMBER:YOUR_API_IDENTIFIER/STAGEING_ENV/VERB/RESOURCE"]


## Authorizer Lambda code
```
export const handler = async(event) => {
    console.log('event', event)

    const token = event['authorizationToken']

    console.log('token', token)
    
    
    let permission = "Deny";
    if(token === "my-secret-token") {
    	permission = "Allow"
    }
    const authResponse = { 
        "principalId": "abc123", 
        "policyDocument": 
            { 
                "Version": "2012-10-17", 
                "Statement": 
                        [
                            {
                                "Action": "execute-api:Invoke", 
                                "Resource": ["arn:aws:execute-api:YOUR_AWS_REGION:YOURACCOUNTNUMBER:YOUR_API_IDENTIFIER/STAGEING_ENV/VERB/RESOURCE"], 
                                "Effect": `${permission}`
                            }
                        ]
            }
        
    }
    return authResponse;
};
```


