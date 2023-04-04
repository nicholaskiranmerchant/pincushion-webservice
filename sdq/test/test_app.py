from src.wsgi import app

def hateoas_compliance(json):
    return 'data', 'links' in json

def test_root_resource():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert hateoas_compliance(response.json)
    assert 'message' in response.json['data']
    assert response.json['data']['message'] == 'Yo what\'s popping kings and kingesses'