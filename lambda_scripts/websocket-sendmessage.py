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
        items = dynamod_table.scan().get('Items', [])
        if not items:
            print('No connection right now!')
            return {}

        connectionIds = [item.get('connectionId') for item in items]

        domainName = event.get('requestContext', {}).get('domainName', '')
        stage = event.get('requestContext', {}).get('stage', '')
        api = boto3.client('apigatewaymanagementapi', endpoint_url=f'https://{domainName}/{stage}')

        message = json.loads(event.get('body', '{}')).get('message', 'Hello everyone!')

        if connectionIds:
            for connectionId in connectionIds:
                api.post_to_connection(
                    Data=message,
                    ConnectionId=connectionId
                )

    except (Exception, ) as e:
        print(str(e))

    return {}
