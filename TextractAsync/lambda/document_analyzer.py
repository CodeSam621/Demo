import os
import json
from time import sleep
import logging
from boto3 import client

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.INFO)

textract_client = client('textract')

WAIT_TIME_FOR_RESULTS = os.environ.get("WAIT_TIME_FOR_RESULTS", 2)

def analyze_document(bucket, key):
 
    blocks = trigger_analysis(bucket, key)

    # for debuging
    text_file = open(f'./responses/test_block.json', "w")
    text_file.write(json.dumps(blocks))
    text_file.close()

    key_map = {}
    value_map = {}
    block_map = {}
    table_blocks = []
    for block in blocks:
        block_id = block['Id']
        block_map[block_id] = block
        if block['BlockType'] == "KEY_VALUE_SET":
            if 'KEY' in block['EntityTypes']:
                key_map[block_id] = block
            else:
                value_map[block_id] = block
        elif block['BlockType'] == "TABLE":
            table_blocks.append(block)

    return key_map, value_map, block_map, table_blocks

def trigger_analysis(bucket, key):
    response = textract_client.start_document_analysis(
        DocumentLocation={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        FeatureTypes=["FORMS", "TABLES"]
    )
    job_id = response['JobId']
    logger.info(f"\t\t\t\t -----------Job_id: {job_id} --------------\n\n")

    block_list = []
    get_analysis_result(job_id, next_token = None, block_list = block_list)
    return block_list

def get_analysis_result(job_id, next_token, block_list):
    if(next_token == None):
        result = textract_client.get_document_analysis(JobId=job_id)
    else:
        result = textract_client.get_document_analysis(JobId=job_id, NextToken=next_token)
        
    blocks = result.get("Blocks")

    if(blocks != None):
        # logger.info(f'Analysis blocks: {blocks}')
        block_list.extend(blocks)
        if(result.get("NextToken") != None):
            get_analysis_result(job_id, result["NextToken"], block_list )      

    else:
        logger.info(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Waiting to finish the analysis >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        logger.info(f'Analysis result: {result}')
        sleep(int(WAIT_TIME_FOR_RESULTS))
        get_analysis_result(job_id, None, block_list)