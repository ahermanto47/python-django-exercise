import requests
import os

class MarketoIdentityClient:

    """A simple marketo identity client application to authenticate using oauth2 mechanism.
    Configuration items like base_url and credential will be obtained from environment variables.
    As an alternative you can also pass credentials to constructor"""

    def base_url(self):
        return os.getenv('SECURITY_ENDPOINT')

    def credential(self):
        return {
            'client_id': os.environ.get('CLIENT_ID'),
            'client_secret': os.getenv('CLIENT_SECRET'),
            'grant_type': 'client_credentials',
        }

    def __init__(self,credential_param=None) -> None:
        self.baseUrl = self.base_url()
        self.credential_dict = None
        if (credential_param != None):
            self.credential_dict = credential_param
        else:
            self.credential_dict = self.credential()
        response = self.login().json()
        self.token = response['access_token']

    def login(self):
        return requests.get(url=self.baseUrl+'/identity/oauth/token',params=self.credential_dict)

    def get_token(self):
        return self.token