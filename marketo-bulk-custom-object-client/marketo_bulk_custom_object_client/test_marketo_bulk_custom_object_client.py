import pytest
from .marketo_bulk_custom_object_client import MarketoBulkCustomObjectClient
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
    return MarketoBulkCustomObjectClient(api_name='reservation_c',baseUrl="http://127.0.0.1:4012",security_client=security_client)

def test_get_all_export_jobs(client):
    client.set_additional_params(additional_params={'__example':'success'})
    response = client.get_all_export_jobs()
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200
    assert response_data['success'] == True
    assert response_data['requestId'] == 'abc123'
    assert len(response_data['result']) >= 0

def test_create_export_job(client):
    payload = {
        'fields': ['leadId'],
        'filter': {
            'updatedAt': {
                'startAt': '2022-07-01T00:00:00Z',
                'endAt': '2022-07-31T00:00:00Z'
            },
            "smartListId": 1,
            "smartListName": 'test smart list',
            "staticListId": 2,
            "staticListName": 'test static list'
        }
    }
    response = client.create_export_job(data=payload)
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200
    assert len(response_data['result']) >= 0
    assert response_data['requestId'] != None


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

"""

@pytest.mark.skip(reason="need to figure out how to mock 602 response in prism")
def test_get_all_export_jobs_with_expired_tokens(client):
    client.set_additional_params(additional_params={'__example':'expired_token'})
    response = client.get_all_export_jobs()
    print(response.json())
    assert response.status_code == 602

"""

def test_create_import_job_for_reservation(client):
    client.set_additional_params(additional_params={'__example':'create_reservation_import_job'})
    client.set_additional_params(additional_params={'format':'csv'})
    multipart_form_data = {
       ('reservation-data.csv', open('input/reservation.csv', 'rb')) 
    }
    response = client.create_import_job(files=multipart_form_data)
    print(response.json())
    assert response.status_code == 200
