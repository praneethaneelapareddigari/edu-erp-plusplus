import os
os.environ['DATABASE_URL'] = 'sqlite:///./test_api3.db'
from fastapi.testclient import TestClient
from fastapi_app.main import app
from fastapi_app.db import init_db

client = TestClient(app)

def token():
    r = client.post('/auth/token', data={'username':'admin@example.com','password':'admin123'})
    assert r.status_code == 200
    return r.json()['access_token']

def setup_module():
    init_db()

def test_listing_and_enroll_assign():
    t = token()
    # Seed courses/students/faculty
    for i in range(1, 6):
        client.post('/api/courses', json={'code':f'CS10{i}','name':f'Course {i}','credits':3},
                    headers={'Authorization': f'Bearer {t}'})
    for i in range(1, 6):
        client.post('/api/students', json={'name':f'User{i}','roll_no':f'R{i:03d}','email':f'u{i}@ex.com'},
                    headers={'Authorization': f'Bearer {t}'})
    rf = client.post('/api/faculties', json={'name':'Dr. Rao','dept':'CSE','email':'rao@example.com'},
                     headers={'Authorization': f'Bearer {t}'})
    fid = rf.json()['id']

    # List with pagination
    rlist = client.get('/api/students?limit=2&offset=0', headers={'Authorization': f'Bearer {t}'})
    assert rlist.status_code == 200 and rlist.json()['total'] >= 5

    # Enroll student 1 to course 1
    sid = 1
    cid = 1
    re = client.post(f'/api/students/{sid}/enroll/{cid}', headers={'Authorization': f'Bearer {t}'})
    assert re.status_code == 200

    # Assign faculty to course
    ra = client.post(f'/api/courses/{cid}/assign-faculty/{fid}', headers={'Authorization': f'Bearer {t}'})
    assert ra.status_code == 200

    # List course students/faculties
    lstu = client.get(f'/api/courses/{cid}/students', headers={'Authorization': f'Bearer {t}'})
    lfac = client.get(f'/api/courses/{cid}/faculties', headers={'Authorization': f'Bearer {t}'})
    assert len(lstu.json()['items']) >= 1
    assert len(lfac.json()['items']) >= 1
