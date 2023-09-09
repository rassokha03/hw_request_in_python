import requests
import os
import json
from jsonschema.validators import validate

def test_users_status_code():
    response = requests.get('https://reqres.in/api/users?page=2')
    assert response.status_code == 200

def test_page():
    page = 5
    response = requests.get(
        url = "https://reqres.in/api/users",
        params = {"page":page}
    )
    assert response.json()['page'] == page

def test_users_have_first_name():
    page = 2
    name = 'Michael'
    response = requests.get(
        url = "https://reqres.in/api/users",
        params = {"page":page}
        )
    assert response.json()['data'][0]['first_name'] == name


def load_json_schema(name: str):
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', name)
    with open(schema_path) as schema:
        return json.loads(schema.read())


def test_users_schema():
    schema = load_json_schema('get_users_schema.json')
    response = requests.get('https://reqres.in/api/users?page=2')
    validate(response.json(), schema=schema)

def test_create_user():
    name = 'NEO'
    job = 'The  special'
    response = requests.post(
        url = "https://reqres.in/api/users",
        data ={'name': name, 'job': job}
    )
    assert response.status_code == 201
    assert response.json()['name'] == name
    assert response.json()['job'] == job
    assert 'id' in response.json()
    assert 'createdAt' in response.json()

def load_json_schema_for_create_user(name: str):
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', name)
    with open(schema_path) as schema:
        return json.loads(schema.read())

def test_create_user_schema():
    name = 'NEO'
    job = 'The  special'
    schema = load_json_schema('create_user_schema.json')
    response = requests.post(
        url="https://reqres.in/api/users",
        data={'name': name, 'job': job}
    )
    validate(response.json(),schema=schema)

def test_update_name_user():
    name_new = 'Obi Van Kenobi'
    response = requests.put(
        url = 'https://reqres.in/api/users/2',
        data = {'name': name_new}
    )

    assert response.status_code == 200
    assert response.json()['name'] == name_new

def test_delete_user():
    response = requests.delete('https://reqres.in/api/users/2')
    assert response.status_code == 204

def test_registration_successful_new_user():
    email = 'firstuser@mail.ru'
    password = 'qwerty'
    response = requests.post(
        url = 'https://reqres.in/api/register',
        data = {'email': email,'password': password }
    )
    assert response.status_code == 400

def test_registration_old_user():
    email = 'eve.holt@reqres.in'
    password = 'pistol'
    response = requests.post(
        url='https://reqres.in/api/register',
        data={'email': email, 'password': password}
    )
    assert response.status_code == 200
    assert 'id' in response.json()
    assert 'token' in response.json()

