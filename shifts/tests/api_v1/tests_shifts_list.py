import pytest
from rest_framework import status

pytestmark = [
    pytest.mark.django_db,
]


def test_get_shiftss_list_anonymous(anon):
    anon.get(
        "/api/v1/shifts/", expected_status_code=status.HTTP_401_UNAUTHORIZED,
    )


def test_get_shifts_list_empty(basic_api):
    assert basic_api.get("/api/v1/shifts/") == []


def test_get_shifts_list_by_user(tz, basic_api, shift):
    assert basic_api.get("/api/v1/shifts/") == [
        {
            "id": shift.id,
            "start": shift.start.astimezone(tz).isoformat(),
            "end": shift.end.astimezone(tz).isoformat(),
            "organization": shift.organization_id,
            "employee": shift.employee_id,
            "state": "open",
        },
    ]


def test_get_shifts_list_by_employee(tz, employee_api, shift, make_shift):
    shift_2 = make_shift(organization=employee_api.employee.organization)
    assert employee_api.get("/api/v1/shifts/") == [
        {
            "id": shift_2.id,
            "start": shift_2.start.astimezone(tz).isoformat(),
            "end": shift_2.end.astimezone(tz).isoformat(),
            "organization": shift_2.organization_id,
            "employee": shift_2.employee_id,
            "state": "open",
        },
    ]