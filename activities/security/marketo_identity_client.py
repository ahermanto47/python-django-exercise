import requests

class MarketoIdentityClient:

    def base_url(self):
        return "http://127.0.0.1:4010"

    def credential(self):
        return {
            'client_id': 'fqYxsb4BU5OMG1fDO2h5kDU2Le/V6yYF1Om+kLOqdmc=',
            'client_secret': 'SL5J28zkQQm67kO0mKHQOJht2u5Zfsq+adPFhp0kJxT9PymqzdGbLDyzOGQEot9R+s0LUySoMafnfMrFiU3WWg==',
            'grant_type': 'client_credentials',
            '__example': 'success'
        }

    def __init__(self) -> None:
        self.baseUrl = self.base_url()
        response = self.login().json()
        self.token = response['access_token']

    def login(self):
        return requests.get(url=self.baseUrl+'/identity/oauth/token',params=self.credential())

    def get_token(self):
        return self.token