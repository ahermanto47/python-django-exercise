import requests
from enum import Enum
from marketo_identity_client import MarketoIdentityClient

class Operation(Enum):
    get_all_export_job = f'/bulk/v1/customobjects/{{api_name}}/export.json'
    get_export_job_status = f'/bulk/v1/customobjects/{{api_name}}/export/{{export_id}}/status.json'
    get_export_file = f'/bulk/v1/customobjects/{{api_name}}/export/{{export_id}}/file.json'
    create_export_job = f'/bulk/v1/customobjects/{{api_name}}/export/create.json'
    cancel_export_job = f'/bulk/v1/customobjects/{{api_name}}/export/{{export_id}}/cancel.json'
    enqueue_export_job = f'/bulk/v1/customobjects/{{api_name}}/export/{{export_id}}/enqueue.json'
    create_import_job = f'/bulk/v1/customobjects/{{api_name}}/import.json'

class MarketoBulkCustomObjectClient:

    """A simple application to create a bulk activity job, 
       poll its status, and retrieve the file when status completed"""

    def __init__(self,api_name,security_client: MarketoIdentityClient,baseUrl,additional_params=None,additional_headers=None) -> None:
        self.api_name = api_name
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
        return requests.post(url=self.baseUrl+path,headers=self.headers,json=data,params=self.additional_params) 

    def do_post_file(self,path,files=None):
        return requests.post(url=self.baseUrl+path,headers=self.headers,files=files,params=self.additional_params) 

    """Add additional headers"""

    def set_additional_headers(self,additional_headers):
        if additional_headers != None:
            self.headers.update(additional_headers)

    """Add additional query parameters"""

    def set_additional_params(self,additional_params):
        self.additional_params = additional_params

    """Pull all export jobs"""

    def get_all_export_jobs(self):
        return self.do_get(path=Operation.get_all_export_job.value.format(api_name=self.api_name))

    """Get status of an export job"""

    def get_export_job_status(self,export_id):
        return self.do_get(path=Operation.get_export_job_status.value.format(api_name=self.api_name,export_id=export_id))

    """Get file of an export job"""

    def get_export_file(self,export_id):
        return self.do_get(path=Operation.get_export_file.value.format(api_name=self.api_name,export_id=export_id))

    """Create an export job"""

    def create_export_job(self,data):
        return self.do_post(path=Operation.create_export_job.value.format(api_name=self.api_name),data=data)

    """Cancel an export job"""

    def cancel_export_job(self,export_id):
        return self.do_post(path=Operation.cancel_export_job.value.format(api_name=self.api_name,export_id=export_id))

    """Enqueue an export job"""

    def enqueue_export_job(self,export_id):
        return self.do_post(path=Operation.enqueue_export_job.value.format(api_name=self.api_name,export_id=export_id))

    """Create an import job"""

    def create_import_job(self,files):
        return self.do_post_file(path=Operation.create_import_job.value.format(api_name=self.api_name),files=files)
