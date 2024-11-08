import json
import boto3
from os import getenv

def lambda_handler(event, context) -> dict:
    try:
        connection_id = event.get('requestContext', {}).get('connectionId')
        if not connection_id:
            print('Connection ID is invalid!')
            return {}

        dynamodb_table_name = getenv('DYNAMODB_TABLE_NAME')
        if not dynamodb_table_name:
            print('\'DYNAMODB_TABLE_NAME\' value is empty!')
            return {}

        dynamodb_resource = boto3.resource('dynamodb')
        dynamodb_table = dynamodb_resource.Table(dynamodb_table_name)

        dynamodb_table.put_item(
            Item={
                'connectionId': connection_id
            }
        )

    except Exception as e:
        print(f'Error: {str(e)}')
        return {}

    finally:
        return {}

