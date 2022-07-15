import requests

baseUrl="http://127.0.0.1:4010"

class GetBulkExportActivitiesClient:

    """A simple console application to create activities job, 
       poll its status, and retrieve the file when status completed"""

    def __init__(self) -> None:
        pass
    
    """Pull all export jobs"""

    def get_all_export_jobs(self):
        path = '/bulk/v1/activities/export.json'
        response = requests.get(url=baseUrl+path)
        return response

    """Create an export jobs"""

    def create_export_job(self,data):
        path = '/bulk/v1/activities/export/create.json'
        response = requests.post(url=baseUrl+path, json=data)
        return response