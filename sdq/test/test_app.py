from src.wsgi import app

def hateoas_compliance(json):
    return 'data', 'links' in json

def test_root_resource():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert hateoas_compliance(response.json)
    assert 'message' in response.json['data']
    assert response.json['data']['message'] == 'Welcome to my API! Navigate to services using the below links.'


def test_query_remote_address():
    response = app.test_client().get('/pincushion/pin/24.46.196.120')
    assert response.json['data']['geoinformation']['city'] == 'Brooklyn'