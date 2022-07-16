from .marketo_bulk_activities_client import GetBulkExportActivitiesClient
import pytest

@pytest.fixture
def client():
    return GetBulkExportActivitiesClient()

def test_get_all_export_jobs_gets_response_with_200_code(client):
    response = client.get_all_export_jobs()
    assert response.status_code == 200

def test_create_export_job(client):
    payload = {
        'fields': ['leadId'],
        'filter': {
            'createdAt': {
                'startAt': '2017-01-01T00:00:00Z',
                'endAt': '2017-01-31T00:00:00Z'
            }
        }
    }
    response = client.create_export_job(data=payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['requestId'] != None

def test_cancel_export_job(client):
    response = client.cancel_export_job(export_id='abc123')
    assert response.status_code == 200

def test_enqueue_export_job(client):
    response = client.enqueue_export_job(export_id='abc123')
    assert response.status_code == 200

def test_get_export_job_status(client):
    response = client.get_export_job_status(export_id='abc123')
    assert response.status_code == 200

def test_get_export_file(client):
    response = client.get_export_file(export_id='abc123')
    assert response.status_code == 200
    
