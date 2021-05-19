import pytest
from rest_framework import status

pytestmark = [
    pytest.mark.django_db,
]


def test_get_shift_by_employee(tz, employee_api, make_shift):
    shift = make_shift(organization=employee_api.employee.organization)
    assert employee_api.get(f"/api/v1/shifts/{shift.id}/") == {
            "id": shift.id,
            "start": shift.start.astimezone(tz).isoformat(),
            "end": shift.end.astimezone(tz).isoformat(),
            "organization": shift.organization_id,
            "employee": shift.employee_id,
            "state": "open",
            "change_history": [],
        }


@pytest.mark.freeze_time("2021-03-08T00:00:00.000000+03:00")
def test_get_shift_by_user(tz, basic_api, employee, make_shift):
    shift = make_shift(organization=employee.organization)
    shift.assign_employee(employee, basic_api.user)

    assert basic_api.get(f"/api/v1/shifts/{shift.id}/") == {
        "id": shift.id,
        "start": shift.start.astimezone(tz).isoformat(),
        "end": shift.end.astimezone(tz).isoformat(),
        "organization": shift.organization_id,
        "employee": shift.employee_id,
        "state": "assigned",
        "change_history": [
            {
                "party": "user",
                "user": {
                    "username": basic_api.user.username,
                    "email": basic_api.user.email,
                },
                "action": "assign_employee",
                "state_from": "open",
                "state_to": "assigned",
                "instance_diff": {"employee": {"to": employee.id, "from": None}},
                "dt_created": "2021-03-08T00:00:00.000000+03:00",
            },
        ],
    }


@pytest.mark.freeze_time("2021-03-08T00:00:00.000000+03:00")
def test_book_shift_by_employee(tz, employee_api, make_shift):
    shift = make_shift(organization=employee_api.employee.organization)

    assert employee_api.put(f"/api/v1/shifts/{shift.id}/book/") == {
        "id": shift.id,
        "start": shift.start.astimezone(tz).isoformat(),
        "end": shift.end.astimezone(tz).isoformat(),
        "organization": shift.organization_id,
        "employee": employee_api.employee.id,
        "state": "assigned",
        "change_history": [
            {
                "party": "employee",
                "user": {
                    "username": employee_api.user.username,
                    "email": employee_api.user.email,
                },
                "action": "assign_employee",
                "state_from": "open",
                "state_to": "assigned",
                "instance_diff": {
                    "employee": {"to": employee_api.employee.id, "from": None},
                },
                "dt_created": "2021-03-08T00:00:00.000000+03:00",
            },
        ],
    }


@pytest.mark.freeze_time("2021-03-08T00:00:00.000000+03:00")
def test_refuse_shift_by_employee(tz, employee_api, make_shift):
    shift = make_shift(organization=employee_api.employee.organization)
    shift.assign_employee(employee_api.employee, employee_api.user)

    assert employee_api.put(f"/api/v1/shifts/{shift.id}/refuse/") == {
        "id": shift.id,
        "start": shift.start.astimezone(tz).isoformat(),
        "end": shift.end.astimezone(tz).isoformat(),
        "organization": shift.organization_id,
        "employee": employee_api.employee.id,
        "state": "open",
        "change_history": [
            {
                "party": "employee",
                "user": {
                    "username": employee_api.user.username,
                    "email": employee_api.user.email,
                },
                "action": "reset_employee",
                "state_from": "assigned",
                "state_to": "open",
                "instance_diff": {
                    "employee": {"to": None, "from": employee_api.employee.id},
                },
                "dt_created": "2021-03-08T00:00:00.000000+03:00",
            },
            {
                "party": "employee",
                "user": {
                    "username": employee_api.user.username,
                    "email": employee_api.user.email,
                },
                "action": "assign_employee",
                "state_from": "open",
                "state_to": "assigned",
                "instance_diff": {
                    "employee": {"to": employee_api.employee.id, "from": None},
                },
                "dt_created": "2021-03-08T00:00:00.000000+03:00",
            },
        ],
    }
