from .get_bulk_export_activities import GetBulkExportActivities

def test_get_all_export_jobs_gets_response_with_200_code():
    response = GetBulkExportActivities.get_all_export_jobs(self=None)
    assert response.status_code == 200
