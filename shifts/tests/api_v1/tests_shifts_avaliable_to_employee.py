import pytest

pytestmark = [
    pytest.mark.django_db,
]


def test_get_shifts_list_by_employee_available(tz, employee_api, shift, make_shift):
    employee_api.employee.occupancy_schedule = [
        {"weekday": 1, "start_time": "00:00:00", "end_time": "1 00:00:00"},
    ]

    make_shift(
        organization=employee_api.employee.organization,
        start="2021-03-08T09:00:00+03:00",
        end="2021-03-08T18:00:00+03:00",
    )
    shift_3 = make_shift(
        organization=employee_api.employee.organization,
        start="2021-03-09T09:00:00+03:00",
        end="2021-03-09T18:00:00+03:00",
    )

    assert employee_api.get("/api/v1/shifts/available/") == [
        {
            "id": shift_3.id,
            "start": shift_3.start.astimezone(tz).isoformat(),
            "end": shift_3.end.astimezone(tz).isoformat(),
            "organization": shift_3.organization_id,
            "employee": shift_3.employee_id,
            "state": "open",
        },
    ]
