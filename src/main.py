from typing import Dict
from boto3.dynamodb.conditions import Key
from datetime import datetime
import json
import boto3

def get_data(event_raw: Dict) -> Dict:
    return json.loads(event_raw["body"])


def get_prefix_data(data: Dict) -> str:
    return data.get("id").split('.', 1)[0]


def enrich_data(data: Dict, prefix: str, metadata) -> Dict:
    if prefix == "07PI":
        id = data.get("id")
        response = metadata.query(
            KeyConditionExpression=Key('id').eq(id)
        )
        item = response['Items'][0]
        data.update(item)
    else:
        data["description"] = "N/A"
        data["metric"] = "N/A"
    return data


def persist_dynamodb(data, sensor):
    sensor.put_item(Item=data)


def persist_s3(data, s3_client):
    now = datetime.now().utcnow()
    timestamp = now.strftime("%Y%m%dT%H%M%S")
    s3_data = json.dumps(data).encode()
    s3_client.put_object(Body=s3_data, Bucket='sensor', Key=timestamp+'.txt')


def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        metadata = dynamodb.Table('metadata')
        sensor = dynamodb.Table('sensor')
        s3_client = boto3.client('s3')
        # Pipeline
        data = get_data(event)
        prefix = get_prefix_data(data)
        data = enrich_data(data, prefix, metadata)
        persist_dynamodb(data, sensor)
        persist_s3(data, s3_client)
        print("Pipiline Finish!")
        print(f'Result: {data}')
        return data
    except Exception as e:
        print("ERROR: " + str(e))


event = {"body": '{"ts": "2019-09-24T15:07:23.6290000Z", "value": 19.23, "id": "07PI.S-TRC-1255BPV", "state": 0}'}
lambda_handler(event, None)
