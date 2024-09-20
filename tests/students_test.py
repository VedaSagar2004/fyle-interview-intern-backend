import json
from core.models.students import Student
from core.models.assignments import Assignment

def test_no_api_route(client, h_student_1):
    response = client.get(
        '/testapi',
        headers=h_student_1
    )
    
    assert response.status_code == 404


def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )
    
    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_no_principal_header(client):
    response = client.get(
        '/principal/assignments'
    )

    assert response.status_code == 401


def test_no_student_id(client):
    headers = {
        'X-Principal': json.dumps({
            'user_id': 5
        })
    }
    response = client.get(
        '/principal/assignments',
        headers=headers
    )
    
    assert response.status_code == 403


def test_student_repr():
    student = Student(id=1)
    assert repr(student) ==  '<Student 1>'

    student = Student(id=100)
    assert repr(student) == '<Student 100>'


def test_assignment_repr():
    assignment = Assignment(id=1)
    assert repr(assignment) ==  '<Assignment 1>'

    assignment = Assignment(id=100)
    assert repr(assignment) == '<Assignment 100>'


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_not_in_draft_state(client, h_student_1):
    content = 'ESSAY T1'
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 1,
            'content': content
        })

    assert response.status_code == 400


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400


def test_post_edit_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 2,
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_post_edit_assignment_student_2(client, h_student_2):
    content = 'ABCD TESTPOST 2'

    response = client.post(
        '/student/assignments',
        headers=h_student_2,
        json={
            'id': 5,
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_post_assignment_student_2(client, h_student_2):
    content = 'ABCD TESTPOST 2'

    response = client.post(
        '/student/assignments',
        headers=h_student_2,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'
