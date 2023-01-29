
## Full video >>> : https://www.youtube.com/watch?v=ExjW3HCFG1U
## Connect to EC2 ssh using certificate
- `ssh -i <path_to_pem_file> ec2-user@<public_ip_address>`
- eg: `ssh -i ./demo-ec2-pair.pem ec2-user@ec2-13-33-204-155.ap-southeast-2.compute.amazonaws.com`
- `chmod 400 ./demo-ec2-pair.pem`
- https://chmodcommand.com/chmod-400/

## Policy evaluation logic
- https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html

## Cross account access 
- `aws sts get-caller-identity`
- `aws sts assume-role --profile john --role-arn "arn:aws:iam::<YOUR_ACCOUNT_B_ID>:role/cross-account-role" --role-session-name AWSCLI-Session --external-id lovetocode-id`
- 
`export AWS_ACCESS_KEY_ID=REPLACE_WITH_YOUR_ACCESS_ID`
`export AWS_SECRET_ACCESS_KEY=REPLACE_WITH_YOUR_SECRET_ACCESS_KEY`
`export AWS_SESSION_TOKEN=REPLACE_WITH_YOUR_SESSION_TOKEN`

- Remove env variables
`unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN`
