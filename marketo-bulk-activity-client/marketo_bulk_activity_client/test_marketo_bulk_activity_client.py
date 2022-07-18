import pytest
from marketo_bulk_activity_client import MarketoBulkActivityClient
from marketo_identity_client import MarketoIdentityClient
import os
import csv
import time

@pytest.fixture
def security_client():
    os.environ['SECURITY_ENDPOINT'] = 'http://127.0.0.1:4010'
    os.environ['CLIENT_ID'] = 'fqYxsb4BU5OMG1fDO2h5kDU2Le/V6yYF1Om+kLOqdmc='
    os.environ['CLIENT_ID'] = 'SL5J28zkQQm67kO0mKHQOJht2u5Zfsq+adPFhp0kJxT9PymqzdGbLDyzOGQEot9R+s0LUySoMafnfMrFiU3WWg=='   
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
        

def test_full_job_lifecycle(client):

    global lifecycle_client
    
    lifecycle_client = client

    """ set all response to use full-lifecycle example"""
    print('\n')
    print('starting job''s full lifecycle test......!\n')

    lifecycle_client.set_additional_params(additional_params={'__example':'full-lifecycle'})

    """ create a job, save the exportId """

    payload = {
        'fields': ['marketoGUID','leadId','activityDate','activityTypeId','campaignId','primaryAttributeValueId','primaryAttributeValue','attributes'],
        'filter': {
            'createdAt': {
                'startAt': '2022-07-01T00:00:00Z',
                'endAt': '2022-07-31T00:00:00Z'
            }
        }
    }
    response = lifecycle_client.create_export_job(data=payload)
    response_data = response.json()
    assert response_data['requestId'] == 'e42b#14272d07d78'
    assert response_data['success'] == True
    export_id = response_data['result'][0]['exportId']
    assert export_id == 'ce45a7a1-f19d-4ce2-882c-a3c795940a7d'
    
    """ get job status, lets make sure job is created """

    response = lifecycle_client.get_export_job_status(export_id=export_id)
    response_data = response.json()
    assert response_data['result'][0]['status'] == 'Created'
    print('successfully created job with export_id = %s\n' % export_id)

    """ queue the job """
    response = lifecycle_client.enqueue_export_job(export_id=export_id)
    response_data = response.json()
    #print(response_data)
    assert response_data['result'][0]['status'] == 'Queued'
    print('successfully enqueue job with export_id = %s\n' % export_id)

    """ poll job status until its status is completed """
    lifecycle_client.set_additional_params(additional_params={'__example':'full-lifecycle-processing'})
    print('polling job with export_id = %s\n' % export_id)
    for x in range(10):
        time.sleep(2)
        if x == 5:
            lifecycle_client.set_additional_params(additional_params={'__example':'full-lifecycle-completed'})
        response = lifecycle_client.get_export_job_status(export_id=export_id)
        response_data = response.json()
        poll_status = response_data['result'][0]['status']
        if poll_status == 'Completed':
            assert poll_status == 'Completed'
            print('poll iteration %s, received status %s\n' % (str(x),poll_status))
            break
        assert poll_status == 'Processing'
        print('poll iteration %s, received status %s\n' % (str(x),poll_status))

    print('successfully complete job with export_id = %s\n' % export_id)
    
    """ download the file from the job """
    lifecycle_client.set_additional_params(additional_params=None)
    lifecycle_client.set_additional_headers(additional_headers={'Accept': 'text/plain'})
    lifecycle_client.set_additional_headers(additional_headers={'Content-Type': 'text/plain'})
    response = lifecycle_client.get_export_file(export_id=export_id)
    assert response.status_code == 200
    lines = response.text.splitlines()
    # remove its headers
    lines.pop(0)
    # Parse as CSV object
    reader = csv.reader(lines)
    # View Result
    for row in reader:
        print(row)

    print('successfully complete job with export_id = %s\n' % export_id)
    
