#!/bin/bash
set -e
# echo $(pwd)

LAMBDA_NAME="my-lambda-name"
DEPLOY_FILE_PATH=$(pwd)/deploy/$LAMBDA_NAME.zip

rm -f -r ./deploy/*
cd ./lambda
zip -r9 ../deploy/$LAMBDA_NAME.zip * -x \*.pyc responses/* results/* play_ground/* play_ground/temp_data/*

echo "Path: $DEPLOY_FILE_PATH"

echo "Updating lambda with env variable"
aws lambda update-function-configuration --function-name $LAMBDA_NAME  --environment Variables="{ENABLE_DEBUG_LOGS='True'}"
echo "The Lambda updated with env variables"
sleep 3

echo "Updating '$LAMBDA_NAME' with the new package"
aws lambda update-function-code --function-name $LAMBDA_NAME --zip-file fileb://$DEPLOY_FILE_PATH
echo "The Lambda '$LAMBDA_NAME' updated succesfully......"