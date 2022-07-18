import requests
import os
import time

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
        response = self.login()

    def set_credential(self,credential_param):
        self.credential_dict = credential_param

    def login(self):
        global response
        try:
            response = requests.get(url=self.baseUrl+'/identity/oauth/token',params=self.credential_dict).json()
        except:
            print('login - in except')
        else:
            print('login - in else')
            self.token = response['access_token']
            self.token_expiration_time = time.time() + response['expires_in']
        finally:
            print('login - in finally')
            return response

    def get_token(self):
        return self.token

    def is_token_expired(self):
        return time.time() >= self.token_expiration_time

    def refresh_token(self):
        return self.login()
