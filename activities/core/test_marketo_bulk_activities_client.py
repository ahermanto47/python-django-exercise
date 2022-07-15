from .marketo_bulk_activities_client import GetBulkExportActivitiesClient

def test_get_all_export_jobs_gets_response_with_200_code():
    client = GetBulkExportActivitiesClient()
    response = client.get_all_export_jobs()
    assert response.status_code == 200

def test_create_export_job():
    client = GetBulkExportActivitiesClient()
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