
from collections import defaultdict
import logging

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.INFO)

def process_forms_data(key_map, value_map, block_map):
    kvs = defaultdict(list)
    for block_id, key_block in key_map.items():
        value_block = get_value_block(key_block, value_map)
        key, confident_of_key = get_text_form(key_block, block_map)
        value, confident_of_value = get_text_form(value_block, block_map)
        if(value != None):
            value = value.strip()
        data = {'value': value, 'confident_of_key': confident_of_key,
                'confident_of_value': confident_of_value}
        kvs[key].append(data)
    return kvs


def get_value_block(key_block, value_map):
    for relationship in key_block['Relationships']:
        if relationship['Type'] == 'VALUE':
            for value_id in relationship['Ids']:
                value_block = value_map[value_id]
    return value_block


def get_text_form(result, blocks_map):
    text = ''
    confident_level = 0
    number_of_words = 0
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                        confident_level += float(word['Confidence'])
                        number_of_words += 1
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X'
                            confident_level += float(word['Confidence'])
                            number_of_words += 1
    confident_level = confident_level if confident_level == 0 else (confident_level / number_of_words)
    return text, confident_level


def get_text_table(result, blocks_map):
    text = ''
    confident_level = 0
    number_of_words = 0
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                        confident_level += float(word['Confidence'])
                        number_of_words += 1
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X'
                            confident_level += float(word['Confidence'])
                            number_of_words += 1

    confident_level = confident_level if confident_level == 0  else (confident_level / number_of_words)
    return { "value": text, "confident" : confident_level }

# extracting tables data
def process_table_data(blocks_map, table_blocks):
    logger.info('\n\nProcessing table data')
    table_data = []
    for index, table in enumerate(table_blocks):
        logger.info(f'======= TABLE BLOCK ->>: {index} =======')
        data = generate_table(table, blocks_map, index + 1)
        table_data.append(data)
        # logger.info(f'Table text: {data}')
    return table_data


def generate_table(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)
   
    table_data = []
    for row_index, cols in rows.items():
        data = []
        for col_index, text in cols.items():
            data.append(text)        
        table_data.append(data)
    return table_data


def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        rows[row_index] = {}

                    rows[row_index][col_index] = get_text_table(
                        cell, blocks_map)
    return rows
