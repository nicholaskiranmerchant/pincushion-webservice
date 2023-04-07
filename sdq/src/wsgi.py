import requests
import os

## FLASK SETUP ##
from flask import Flask, request

app = Flask(__name__)

## FIRESTORE SETUP ##
import firebase_admin
from firebase_admin import credentials, firestore

fs_cred = credentials.Certificate('sdq/src/credentials/sdq1-382716-94d1796944e2.json')
fs_app = firebase_admin.initialize_app(fs_cred)
fs_db = firestore.client()

## UTILITY FUNCTIONS ##

def hateoas_link(rel, path, method):
    return {
        'rel': rel,
        'href': f'{request.url_root}{path}',
        'method': method,
    }

def hateoas_response(data, path, method, links=[], response_code=200):
    response = {
        'data': data, 
        'links': [
            hateoas_link('root', '', 'GET'),
            hateoas_link('self', path, method),
            *links
        ]
    }

    return response, response_code

## IP LOGGING UTILS ##

fs_collection = fs_db.collection('sdq-pincushion')

def get_fs_remote_addresses():
    documents = fs_collection.list_documents()
    remote_addresses = [document.id for document in documents]

    return remote_addresses

def get_remote_address():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

def query_ip_api(remote_address):
    #TODO: Turn this into a logger
    print(f'Querying http://ip-api.com/json/{remote_address}')
    response = requests.get(f'http://ip-api.com/json/{remote_address}')
    if response.json()['status'] == 'fail':
        raise requests.exceptions.HTTPError(
            f'Failed to retrieve geoinformation from IP {remote_address}')

    return response.json()

def log_remote_ip_as_pin():
    remote_address = get_remote_address()
    ip_geoinformation = query_ip_api(remote_address)
    fs_collection.document(remote_address).set(ip_geoinformation)

    return ip_geoinformation

def query_geoinformation(remote_address):
    fs_collection.document(remote_address).get().to_dict()

## ENDPOINTS ##

PATH_ROOT = ''
@app.get(f'/{PATH_ROOT}')
def get_root():
    data = {'message': 'Welcome to my API! Navigate to services using the below links.'}
    links = [
        hateoas_link('about', PATH_AUTHOR, 'GET'),
        hateoas_link('service', PATH_PINCUSION, 'GET')
    ]

    return hateoas_response(data, PATH_ROOT, 'GET', links)

PATH_AUTHOR = 'author'
@app.get(f'/{PATH_AUTHOR}')
def get_author():
    data = {
        'message': 'Author information',
        'name': 'Nicholas (Kiran) Merchant',
        'location': 'Brooklyn, NY',
        'origin': 'Ketchum, ID'
    }

    return hateoas_response(data, PATH_AUTHOR, 'GET')

PATH_PINCUSION = 'pincushion'
@app.get(f'/{PATH_PINCUSION}')
def get_pincushion():
    data = {'message': 'Add pin to log your IP information, or view logged pins below.'}

    links = [hateoas_link('log', PATH_PIN, 'GET')]
    for remote_address in get_fs_remote_addresses():
        links.append(hateoas_link('item', f'{PATH_PIN}/{remote_address}', 'GET') )

    return hateoas_response(data, PATH_PINCUSION, 'GET', links)

PATH_PIN = f'{PATH_PINCUSION}/pin'
@app.get(f'/{PATH_PIN}')
def log_pin():
    links = [
        hateoas_link('parent', PATH_PINCUSION, 'GET')
    ]

    try:
        ip_geoinformation = log_remote_ip_as_pin()
        data = {
            'message': 'Logged a new pin with the following geoinformation',
            'geoinformation': ip_geoinformation
        }

        return hateoas_response(data, PATH_PIN, 'GET', links)
    except requests.exceptions.HTTPError as e:
        data = {
            'message': 'Failed to log a pin.',
            'exception': str(e)
        }

        return hateoas_response(data, PATH_PIN, 'GET', links, response_code=500)

@app.get(f'/{PATH_PIN}/<string:remote_address>')
def get_pin(remote_address):
    data =  query_geoinformation(remote_address)
    links = [
        hateoas_link('parent', PATH_PINCUSION, 'GET')
    ]

    return hateoas_response(data, f'{PATH_PIN}/{remote_address}', 'GET', links)


if __name__ == '__main__':
    app.run(debug=False)
