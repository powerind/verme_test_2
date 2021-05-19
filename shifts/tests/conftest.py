"""
Copyright 2020 ООО «Верме»
"""

import pytest

from shifts.models import Shift

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture()
def make_shift(mixer, organization):
    def _shift_generator(**kwargs):
        if "organization" not in kwargs:
            kwargs["organization"] = organization
        return mixer.blend(Shift, **kwargs)

    return _shift_generator


@pytest.fixture()
def shift(make_shift):
    return make_shift()
