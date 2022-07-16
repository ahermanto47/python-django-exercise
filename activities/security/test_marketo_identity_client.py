import pytest
from .marketo_identity_client import MarketoIdentityClient

@pytest.fixture
def client():
    return MarketoIdentityClient(baseUrl="http://127.0.0.1:4010")

def test_authenticate(client):
    credential = {
        'client_id': 'fqYxsb4BU5OMG1fDO2h5kDU2Le/V6yYF1Om+kLOqdmc=',
        'client_secret': 'SL5J28zkQQm67kO0mKHQOJht2u5Zfsq+adPFhp0kJxT9PymqzdGbLDyzOGQEot9R+s0LUySoMafnfMrFiU3WWg==',
        'grant_type': 'client_credentials',
        '__example': 'success'
    }
    response = client.login(credential)
    assert response != None
    response_data = response.json()
    print('Access token is %s\n' % response_data['access_token'])
    assert response_data['access_token'] != None
    

