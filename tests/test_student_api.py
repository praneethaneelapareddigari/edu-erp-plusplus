import os
os.environ['DATABASE_URL'] = 'sqlite:///./test_api.db'  # use sqlite for tests
from fastapi.testclient import TestClient
from fastapi_app.main import app
from fastapi_app.db import init_db

client = TestClient(app)

def get_token():
    resp = client.post('/auth/token', data={'username':'admin@example.com','password':'admin123'})
    assert resp.status_code == 200, resp.text
    return resp.json()['access_token']

def setup_module():
    init_db()

def test_student_crud():
    token = get_token()
    r = client.post('/api/students', json={'name':'Alice','roll_no':'CS001','email':'alice@example.com'},
                    headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 200, r.text
    sid = r.json()['id']
    g = client.get(f'/api/students/{sid}', headers={'Authorization': f'Bearer {token}'})
    assert g.status_code == 200
    assert g.json()['roll_no'] == 'CS001'
