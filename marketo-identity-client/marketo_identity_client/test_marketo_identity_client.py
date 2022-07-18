import pytest
import os
from marketo_identity_client import MarketoIdentityClient

@pytest.fixture
def test_credential():
    return {
        'client_id': 'fqYxsb4BU5OMG1fDO2h5kDU2Le/V6yYF1Om+kLOqdmc=',
        'client_secret': 'SL5J28zkQQm67kO0mKHQOJht2u5Zfsq+adPFhp0kJxT9PymqzdGbLDyzOGQEot9R+s0LUySoMafnfMrFiU3WWg==',
        'grant_type': 'client_credentials',
        '__example': 'success'
    }
    
@pytest.fixture
def client(test_credential):
    os.environ['SECURITY_ENDPOINT'] = 'http://127.0.0.1:4010'

    """ You can specify credential in environment variables"""
    # os.environ['CLIENT_ID'] = 'fqYxsb4BU5OMG1fDO2h5kDU2Le/V6yYF1Om+kLOqdmc='
    # os.environ['CLIENT_ID'] = 'SL5J28zkQQm67kO0mKHQOJht2u5Zfsq+adPFhp0kJxT9PymqzdGbLDyzOGQEot9R+s0LUySoMafnfMrFiU3WWg=='
    # return MarketoIdentityClient()

    """ Or you can pass it in on constructor"""

    return MarketoIdentityClient(credential_param=test_credential)

def test_authenticate(client):
    response = client.login()
    assert response != None
    assert response['access_token'] == 'OTqizIIO53cgpWDOCgwIzw=='
    
def test_expired_token(client):
    expired_token_credential = {
        'client_id': 'fqYxsb4BU5OMG1fDO2h5kDU2Le/V6yYF1Om+kLOqdmc=',
        'client_secret': 'SL5J28zkQQm67kO0mKHQOJht2u5Zfsq+adPFhp0kJxT9PymqzdGbLDyzOGQEot9R+s0LUySoMafnfMrFiU3WWg==',
        'grant_type': 'client_credentials',
        '__example': 'expired_token'
    }

    client.set_credential(credential_param=expired_token_credential)
    response = client.login()
    assert response != None
    assert response['access_token'] == 'UZmYzNDFiZmI4MjQ4MDVhNg=='
    assert client.is_token_expired() == True

def test_expired_token_then_refresh(client):
    """ Start with mocking token expiration situation """

    expired_token_credential = {
        'client_id': 'fqYxsb4BU5OMG1fDO2h5kDU2Le/V6yYF1Om+kLOqdmc=',
        'client_secret': 'SL5J28zkQQm67kO0mKHQOJht2u5Zfsq+adPFhp0kJxT9PymqzdGbLDyzOGQEot9R+s0LUySoMafnfMrFiU3WWg==',
        'grant_type': 'client_credentials',
        '__example': 'expired_token'
    }

    client.set_credential(credential_param=expired_token_credential)
    response = client.login()
    assert response != None
    assert response['access_token'] == 'UZmYzNDFiZmI4MjQ4MDVhNg=='
    assert client.is_token_expired() == True

    """ call refresh_token to get new token """

    normal_token_credential = {
        'client_id': 'fqYxsb4BU5OMG1fDO2h5kDU2Le/V6yYF1Om+kLOqdmc=',
        'client_secret': 'SL5J28zkQQm67kO0mKHQOJht2u5Zfsq+adPFhp0kJxT9PymqzdGbLDyzOGQEot9R+s0LUySoMafnfMrFiU3WWg==',
        'grant_type': 'client_credentials',
        '__example': 'success'
    }

    client.set_credential(credential_param=normal_token_credential)
    client.refresh_token()
    assert client.get_token() == 'OTqizIIO53cgpWDOCgwIzw=='
    assert client.is_token_expired() == False
