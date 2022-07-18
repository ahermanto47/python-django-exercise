import pytest
from marketo_bulk_activity_client import MarketoBulkActivityClient
from marketo_identity_client import MarketoIdentityClient
import os
import csv
import time

""" This is a sample of contract testing using prism where we mock the responses """

@pytest.fixture
def security_client():
    os.environ['SECURITY_ENDPOINT'] = 'http://127.0.0.1:4010'
    os.environ['CLIENT_ID'] = 'fqYxsb4BU5OMG1fDO2h5kDU2Le/V6yYF1Om+kLOqdmc='
    os.environ['CLIENT_SECRET'] = 'SL5J28zkQQm67kO0mKHQOJht2u5Zfsq+adPFhp0kJxT9PymqzdGbLDyzOGQEot9R+s0LUySoMafnfMrFiU3WWg=='   
    return MarketoIdentityClient()

@pytest.fixture
def client(security_client):
    return MarketoBulkActivityClient(baseUrl="http://127.0.0.1:4011",security_client=security_client)

def test_get_all_export_jobs(client):
    client.set_additional_params(additional_params={'__example':'success'})
    response = client.get_all_export_jobs()
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['success'] == True
    assert response_data['requestId'] == 'abc123'
    assert len(response_data['result']) >= 0
    assert len(response_data['errors']) == 0
    assert len(response_data['warnings']) == 0

def test_create_export_job(client):
    payload = {
        'fields': ['leadId'],
        'filter': {
            'createdAt': {
                'startAt': '2022-07-01T00:00:00Z',
                'endAt': '2022-07-31T00:00:00Z'
            }
        }
    }
    response = client.create_export_job(data=payload)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data['result']) >= 0
    assert response_data['requestId'] != None
    print(response_data)

def test_cancel_export_job(client):
    response = client.cancel_export_job(export_id='abc123')
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['requestId'] != None

def test_enqueue_export_job(client):
    response = client.enqueue_export_job(export_id='abc123')
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['requestId'] != None

def test_get_export_job_status(client):
    response = client.get_export_job_status(export_id='abc123')
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['requestId'] != None

def test_get_export_file(client):
    client.set_additional_headers(additional_headers={'Accept': 'text/plain'})
    client.set_additional_headers(additional_headers={'Content-Type': 'text/plain'})
    response = client.get_export_file(export_id='abc123')
    assert response.status_code == 200
    print('file is \n%s' % response.text)
    # Convert to iterator by splitting on \n chars
    lines = response.text.splitlines()
    # remove its headers
    lines.pop(0)
    # Parse as CSV object
    reader = csv.reader(lines)
    # View Result
    for row in reader:
        print(row)
        