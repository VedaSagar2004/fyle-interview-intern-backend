from core.models.assignments import AssignmentStateEnum, GradeEnum
from core.models.principals import Principal
import json


def test_check_ready(client, h_principal):
    response = client.get(
        '/',
        headers=h_principal
    )
    assert response.status_code == 200
    assert response.json['status'] == 'ready'


def test_no_principal_header(client):
    response = client.get(
        '/principal/assignments'
    )

    assert response.status_code == 401


def test_no_principal_id(client):
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
    principal = Principal(id=1)
    assert repr(principal) ==  '<Principal 1>'

    principal = Principal(id=100)
    assert repr(principal) == '<Principal 100>'

   

def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )
    
    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_get_teachers(client, h_principal):
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )
    assert response.status_code == 200

    data = response.json['data']
    for teacher in data:
        assert teacher['user_id'] in [3, 4]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 2,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 1,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 1,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B
