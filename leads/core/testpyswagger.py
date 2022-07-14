from pyswagger import App, Security
from pyswagger.contrib.client.requests import Client
from pyswagger.utils import jp_compose

# load Swagger resource file into App object
app = App._create_('http://petstore.swagger.io/v2/swagger.json')

auth = Security(app)
auth.update_with('api_key', '12312312312312312313q') # api key
auth.update_with('petstore_auth', '12334546556521123fsfss') # oauth2

# init swagger client
client = Client(auth)

# a dict is enough for representing a Model in Swagger
pet_Tom=dict(id=1, name='Tom', photoUrls=['http://test']) 
# a request to create a new pet
client.request(app.op['addPet'](body=pet_Tom))

# - access an Operation object via App.op when operationId is defined
# - a request to get the pet back
req, resp = app.op['getPetById'](petId=1)
# prefer json as response
req.produce('application/json')
pet = client.request((req, resp)).data
assert pet.id == 1
assert pet.name == 'Tom'

# new ways to get Operation object corresponding to 'getPetById'.
# 'jp_compose' stands for JSON-Pointer composition
req, resp = app.resolve(jp_compose('/pet/{petId}', base='#/paths')).get(petId=1)
req.produce('application/json')
pet = client.request((req, resp)).data
assert pet.id == 1