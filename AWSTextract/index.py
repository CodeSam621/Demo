import boto3
from collections import defaultdict
from urllib.parse import unquote_plus

def get_kv_map(bucket, key):
    # process using image bytes
    client = boto3.client('textract')
    response = client.analyze_document(Document={'S3Object': {'Bucket': bucket, "Name": key}}, FeatureTypes=['FORMS'])

    # Get the text blocks
    blocks = response['Blocks']
    print(f'BLOCKS: {blocks}')

    # get key and value maps
    key_map = {}
    value_map = {}
    block_map = {}
    for block in blocks:
        block_id = block['Id']
        block_map[block_id] = block
        if block['BlockType'] == "KEY_VALUE_SET":
            if 'KEY' in block['EntityTypes']:
                key_map[block_id] = block
            else:
                value_map[block_id] = block

    return key_map, value_map, block_map


def get_kv_relationship(key_map, value_map, block_map):
    kvs = defaultdict(list)
    for block_id, key_block in key_map.items():
        value_block = find_value_block(key_block, value_map)
        key = get_text(key_block, block_map)
        val = get_text(value_block, block_map)
        kvs[key].append(val)
    return kvs


def find_value_block(key_block, value_map):
    for relationship in key_block['Relationships']:
        if relationship['Type'] == 'VALUE':
            for value_id in relationship['Ids']:
                value_block = value_map[value_id]
    return value_block


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X'

    return text

def lambda_handler(event, context):
    file_obj = event["Records"][0]
    bucket = unquote_plus(str(file_obj["s3"]["bucket"]["name"]))
    file_name = unquote_plus(str(file_obj["s3"]["object"]["key"]))
    #file_name ='filled_form.png'
    print(f'Bucket: {bucket}, file: {file_name}')
    key_map, value_map, block_map = get_kv_map( bucket, file_name)

    # Get Key Value relationship
    kvs = get_kv_relationship(key_map, value_map, block_map)
    print("\n\n== FOUND KEY : VALUE pairs ===\n")

    for key, value in kvs.items():
        print(key, ":", value)
