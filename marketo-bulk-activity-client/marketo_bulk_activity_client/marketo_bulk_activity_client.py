import requests
from enum import Enum
from marketo_identity_client import MarketoIdentityClient

class Operation(Enum):
    get_all_job = '/bulk/v1/activities/export.json'
    get_job_status = f'/bulk/v1/activities/export/{{export_id}}/status.json'
    get_export_file = f'/bulk/v1/activities/export/{{export_id}}/file.json'
    create_job = '/bulk/v1/activities/export/create.json'
    cancel_job = f'/bulk/v1/activities/export/{{export_id}}/cancel.json'
    enqueue_job = f'/bulk/v1/activities/export/{{export_id}}/enqueue.json'

class MarketoBulkActivityClient:

    """A simple application to create a bulk activity job, 
       poll its status, and retrieve the file when status completed"""

    def __init__(self,security_client: MarketoIdentityClient,baseUrl,additional_params=None,additional_headers=None) -> None:
        self.baseUrl=baseUrl
        self.security_client = security_client
        self.token = security_client.get_token()
        self.headers = {'Authorization': 'Bearer ' + self.token}
        if additional_headers != None:
            self.headers.update(additional_headers)
        self.additional_params = additional_params

    def do_get(self,path):
        return requests.get(url=self.baseUrl+path,headers=self.headers,params=self.additional_params)
    
    def do_post(self,path,data=None):
        if data != None :
            return requests.post(url=self.baseUrl+path,headers=self.headers,json=data,params=self.additional_params) 
        else:
            return requests.post(url=self.baseUrl+path,headers=self.headers,params=self.additional_params)

    """Add additional headers"""

    def set_additional_headers(self,additional_headers):
        if additional_headers != None:
            self.headers.update(additional_headers)

    """Add additional query parameters"""

    def set_additional_params(self,additional_params):
        self.additional_params = additional_params

    """Pull all export jobs"""

    def get_all_export_jobs(self):
        return self.do_get(path=Operation.get_all_job.value)

    """Get status of an export job"""

    def get_export_job_status(self,export_id):
        return self.do_get(path=Operation.get_job_status.value.format(export_id=export_id))

    """Get file of an export job"""

    def get_export_file(self,export_id):
        return self.do_get(path=Operation.get_export_file.value.format(export_id=export_id))

    """Create an export jobs"""

    def create_export_job(self,data):
        return self.do_post(path=Operation.create_job.value,data=data)

    """Cancel an export jobs"""

    def cancel_export_job(self,export_id):
        return self.do_post(path=Operation.cancel_job.value.format(export_id=export_id))

    """Enqueue an export jobs"""

    def enqueue_export_job(self,export_id):
        return self.do_post(path=Operation.enqueue_job.value.format(export_id=export_id))


