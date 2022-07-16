import requests

class MarketoIdentityClient:

    def __init__(self,baseUrl) -> None:
        self.baseUrl=baseUrl

    def login(self,data):
        return requests.get(url=self.baseUrl+'/identity/oauth/token',params=data)