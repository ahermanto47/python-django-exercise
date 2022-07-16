import pytest
from .marketo_identity_client import MarketoIdentityClient

@pytest.fixture
def client():
    return MarketoIdentityClient()

def test_authenticate(client):
    response = client.login()
    assert response != None
    response_data = response.json()
    print('Access token is %s\n' % response_data['access_token'])
    assert response_data['access_token'] != None
    