import pytest
import os
from .marketo_identity_client import MarketoIdentityClient

@pytest.fixture
def client():
    os.environ['SECURITY_ENDPOINT'] = 'http://127.0.0.1:4010'
    os.environ['CLIENT_ID'] = 'fqYxsb4BU5OMG1fDO2h5kDU2Le/V6yYF1Om+kLOqdmc='
    os.environ['CLIENT_ID'] = 'SL5J28zkQQm67kO0mKHQOJht2u5Zfsq+adPFhp0kJxT9PymqzdGbLDyzOGQEot9R+s0LUySoMafnfMrFiU3WWg=='   
    return MarketoIdentityClient()

def test_authenticate(client):
    response = client.login()
    assert response != None
    response_data = response.json()
    print('Access token is %s\n' % response_data['access_token'])
    assert response_data['access_token'] != None
    