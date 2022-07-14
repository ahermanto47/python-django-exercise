import requests

url="http://127.0.0.1:4010/bulk/v1/activities/export.json"

class GetBulkExportActivities:
    def __init__(self) -> None:
        pass

    def get_all_export_jobs(self):
        response = requests.get(url)
        return response