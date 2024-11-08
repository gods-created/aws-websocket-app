import json
import boto3
from os import getenv

def lambda_handler(event, context) -> dict:
    try:
        connectionId = event.get('requestContext', {}).get('connectionId', '')
        if not connectionId:
            print('Connection ID is invalid!')
            return {}

        dynamodb_table_name = getenv('DYNAMODB_TABLE_NAME', '')
        if not dynamodb_table_name:
            print('\'DYNAMODB_TABLE_NAME\' value is empty!')
            return {}

        dynamodb_resource = boto3.resource('dynamodb')
        dynamod_table = dynamodb_resource.Table(dynamodb_table_name)
        dynamod_table.delete_item(
            Key={
                'connectionId': connectionId
            }
        )

    except (Exception, ) as e:
        print(str(e))

    finally:
        return {}
