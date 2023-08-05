import json
from boto3 import resource
import logging
from processor.document_processor import process_forms_data, process_table_data
from document_analyzer import analyze_document

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f' \n\n\t ---------------------------------- STARTED ----------------------------------\n\n')
    logger.info(f'event: { event }')
    try:
        if(event.get("bucket") == None or event.get("file_key") == None):
            return {'status_code': 400, 'message': 'Both bucket and file_key should included in the request'}

        bucket = event["bucket"]
        key = event["file_key"]

        key_map, value_map, block_map, table_blocks = analyze_document(bucket, key)
        
        # process key-value
        key_value_maps = process_forms_data(key_map, value_map, block_map)
        for key in key_value_maps:
            logger.info(f'\t\tForm key: {key}, value: {key_value_maps[key]}')

        # process tables
        table_data = process_table_data(block_map, table_blocks)
        logger.info(f'\n\n\nTables: {table_data}')         
    
    except Exception as exp:
        logger.info(f'Failed extraction. Exception: {str(exp)}')
        return {'status_code': 500, 'message': 'Failed extraction'}



# tigger lambda locally
event = {}
event["file_key"] = "sample3.pdf"
event["bucket"] = "sam-textract-test-bucket-new"
lambda_handler(event, None)
