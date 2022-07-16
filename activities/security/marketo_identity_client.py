import requests
import os

class MarketoIdentityClient:

    def base_url(self):
        return os.getenv('SECURITY_ENDPOINT')

    def credential(self):
        return {
            'client_id': os.environ.get('CLIENT_ID'),
            'client_secret': os.getenv('CLIENT_SECRET'),
            'grant_type': 'client_credentials',
            '__example': 'success'
        }

    def __init__(self) -> None:
        self.baseUrl = self.base_url()
        print(self.baseUrl)
        print(self.credential())
        response = self.login().json()
        self.token = response['access_token']

    def login(self):
        return requests.get(url=self.baseUrl+'/identity/oauth/token',params=self.credential())

    def get_token(self):
        return self.token