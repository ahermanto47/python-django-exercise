import pytest
from .marketo_bulk_custom_object_client import MarketoBulkCustomObjectClient
from marketo_identity_client import MarketoIdentityClient
import os
import csv
import time

""" This is a sample of integration testing against a sandbox """

@pytest.fixture
def security_client():
    return MarketoIdentityClient()

@pytest.fixture
def client(security_client):
    bulk_activity_base_url = os.getenv('SECURITY_ENDPOINT')
    return MarketoBulkCustomObjectClient(baseUrl=bulk_activity_base_url,security_client=security_client)

def test_full_export_job_lifecycle(client):

    global lifecycle_client, export_id
    
    lifecycle_client = client

    print('\n')
    print('starting job''s full lifecycle test......!\n')

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
    response = lifecycle_client.create_export_job(api_name='reservation_c',data=payload)
    response_data = response.json()
    assert response_data['success'] == True
    export_id = response_data['result'][0]['exportId']
    
    """ get job status, lets make sure job is created """

    response = lifecycle_client.get_export_job_status(api_name='reservation_c',export_id=export_id)
    response_data = response.json()
    assert response_data['result'][0]['status'] == 'Created'
    print('successfully created job with export_id = %s\n' % export_id)

    """ queue the job """
    response = lifecycle_client.enqueue_export_job(api_name='reservation_c',export_id=export_id)
    response_data = response.json()
    #print(response_data)
    assert response_data['result'][0]['status'] == 'Queued'
    print('successfully enqueue job with export_id = %s\n' % export_id)

    """ poll job status until its status is completed """
    print('polling job with export_id = %s\n' % export_id)
    for x in range(10):
        time.sleep(60)
        response = lifecycle_client.get_export_job_status(api_name='reservation_c',export_id=export_id)
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
    response = lifecycle_client.get_export_file(api_name='reservation_c',export_id=export_id)
    assert response.status_code == 200
    lines = response.text.splitlines()
    # remove its headers
    lines.pop(0)
    # Parse as CSV object
    reader = csv.reader(lines)
    # View Result
    for row in reader:
        print(row)

    print('successfully download job with export_id = %s\n' % export_id)
    
