import os
os.environ['DATABASE_URL'] = 'sqlite:///./test_api2.db'
from fastapi.testclient import TestClient
from fastapi_app.main import app
from fastapi_app.db import init_db

client = TestClient(app)

def setup_module():
    init_db()

def token():
    r = client.post('/auth/token', data={'username':'admin@example.com','password':'admin123'})
    assert r.status_code == 200
    return r.json()['access_token']

def test_exam_flow():
    t = token()
    # Create course to reference in exam
    client.post('/api/courses', json={'code':'CS101','name':'Intro','credits':3,'faculty':'Dr. Rao'},
                headers={'Authorization': f'Bearer {t}'})
    # Create exam
    r = client.post('/api/exams', json={'name':'Midterm','date':'2025-09-25','course_code':'CS101'},
                    headers={'Authorization': f'Bearer {t}'})
    assert r.status_code == 200, r.text
    # Upload results
    r2 = client.post('/api/exams/results', json={'results': {'CS001': 92, 'CS002': 84}},
                    headers={'Authorization': f'Bearer {t}'})
    assert r2.status_code == 200
    # Timetable (cached result)
    r3 = client.get('/api/timetable/CS001', headers={'Authorization': f'Bearer {t}'})
    assert r3.status_code == 200
    assert 'data' in r3.json()
