from src.nali import Nali, School, Notice

import os
import pytest

target_schools = os.getenv("TARGET_SCHOOLS")

if target_schools:
    target_schools = target_schools.split(",")
else:
    target_schools = [school.value for school in School]


@pytest.mark.parametrize("school", list(School))
def test_scraper_for_school(school):
    if school.value not in target_schools:
        pytest.skip(f"No scraper implemented for {school}")

    n = Nali(school)
    notices = n.get_notices(page=1)
    assert isinstance(notices, list)
    assert all(isinstance(n, Notice) for n in notices)
