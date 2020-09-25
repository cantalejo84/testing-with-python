import pytest

EVENT1 = {"body": '{"ts": "2019-09-24T15:07:23.6290000Z", "value": 7, "id": "07PI.S-TRC-1255BPV", "state": 0}'}
EVENT2 = {"body": '{"ts": "2019-09-24T15:07:23.6290000Z", "value": 7, "id": "01PRB.S-TRC-1255BPV", "state": 0}'}
EVENT4 = {"ts": "2019-09-24T15:07:23.6290000Z", "value": 7, "id": "07PI.S-TRC-1255BPV", "state": 0}
EVENT5 = {"ts": "2019-09-24T15:07:23.6290000Z", "value": 7, "id": "01PRB.S-TRC-1255BPV", "state": 0}
EVENT6 = {"Value": 23}
ENRICH_EVENT4 = {"ts": "2019-09-24T15:07:23.6290000Z", "value": 7, "id": "07PI.S-TRC-1255BPV", "state": 0, "description": "valvula laboratorio", "metric": "cm3"}
ENRICH_EVENT5 = {"ts": "2019-09-24T15:07:23.6290000Z", "value": 7, "id": "01PRB.S-TRC-1255BPV", "state": 0, "description": "N/A", "metric": "N/A"}


def test_get_data():
    from src.main import get_data
    event = get_data(EVENT1)
    event_body = {"ts": "2019-09-24T15:07:23.6290000Z", "value": 7, "id": "07PI.S-TRC-1255BPV", "state": 0}
    assert event == event_body


def test_get_prefix_data():
    from src.main import get_data, get_prefix_data
    event = get_data(EVENT1)
    prefix = get_prefix_data(event)
    assert prefix == '07PI'


def test_enrich_data_with_known_prefix(dynamodb_table_metadata):
    from src.main import enrich_data, get_prefix_data
    prefix = get_prefix_data(EVENT4)
    enrich = enrich_data(EVENT4, prefix, dynamodb_table_metadata)
    assert enrich == ENRICH_EVENT4


def test_enrich_data_with_unknown_prefix(dynamodb_table_metadata):
    from src.main import enrich_data, get_prefix_data
    prefix = get_prefix_data(EVENT5)
    assert enrich_data(EVENT5, prefix, dynamodb_table_metadata) == ENRICH_EVENT5


def test_persist_dynamodb(dynamodb_table_sensor):
    from src.main import persist_dynamodb
    persist_dynamodb(ENRICH_EVENT4, dynamodb_table_sensor)
    response = dynamodb_table_sensor.scan()
    item = response['Items'][0]
    assert ENRICH_EVENT4 == item


def test_persist_s3(s3):
    from src.main import persist_s3
    s3.create_bucket(Bucket="sensor")
    persist_s3(ENRICH_EVENT4, s3)
    response = s3.list_objects_v2(Bucket='sensor')
    assert response['KeyCount'] == 1

