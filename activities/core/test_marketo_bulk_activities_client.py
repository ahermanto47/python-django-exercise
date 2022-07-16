import pytest
from .marketo_bulk_activities_client import GetBulkExportActivitiesClient
from ..security.marketo_identity_client import MarketoIdentityClient

@pytest.fixture
def credential():
    return {
        'client_id': 'fqYxsb4BU5OMG1fDO2h5kDU2Le/V6yYF1Om+kLOqdmc=',
        'client_secret': 'SL5J28zkQQm67kO0mKHQOJht2u5Zfsq+adPFhp0kJxT9PymqzdGbLDyzOGQEot9R+s0LUySoMafnfMrFiU3WWg==',
        'grant_type': 'client_credentials',
        '__example': 'success'
    }

@pytest.fixture
def securityClient():
    return MarketoIdentityClient(baseUrl="http://127.0.0.1:4010")

@pytest.fixture
def client(securityClient, credential):
    mytoken = securityClient.login(credential).json()['access_token']
    return GetBulkExportActivitiesClient(baseUrl="http://127.0.0.1:4011",token=mytoken)

def test_get_all_export_jobs_gets_response_with_200_code(client):
    response = client.get_all_export_jobs()
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data['result']) >= 0

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
    response = client.get_export_file(export_id='abc123')
    assert response.status_code == 200

