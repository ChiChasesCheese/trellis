from datetime import date, datetime, timezone

import pytest

from insiderwatch.errors import InsiderWatchError, RosterError
from insiderwatch.hr import Roster
from insiderwatch.timeutil import daterange, is_business_hours, parse_date, parse_ts


def test_parse_ts_variants_all_land_in_utc():
    expected = datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc)
    assert parse_ts("2026-09-01T12:00:00Z") == expected
    assert parse_ts("2026-09-01T12:00:00") == expected  # naive means UTC
    assert parse_ts("2026-09-01T08:00:00-04:00") == expected
    assert parse_ts(expected.timestamp()) == expected


def test_business_hours_respects_local_zone_and_weekends():
    monday_14utc = datetime(2026, 8, 31, 14, 0, tzinfo=timezone.utc)
    assert is_business_hours(monday_14utc, "America/New_York")  # 10:00 local
    assert not is_business_hours(monday_14utc, "Asia/Tokyo")  # 23:00 local
    assert not is_business_hours(datetime(2026, 9, 5, 14, 0, tzinfo=timezone.utc), "UTC")  # Saturday


def test_daterange_excludes_end():
    assert list(daterange(date(2026, 9, 1), date(2026, 9, 4))) == [date(2026, 9, 1), date(2026, 9, 2), date(2026, 9, 3)]


def test_parse_date_rejects_garbage():
    with pytest.raises(InsiderWatchError):
        parse_date("09/01/2026")


def test_roster_loads_fixture(fixtures_dir):
    roster = Roster.load(fixtures_dir / "hr" / "roster.json")
    carol = roster.get("Carol.Diaz@acme.example")
    assert carol is not None
    assert carol.resignation_submitted == date(2026, 9, 11)
    assert carol.termination_date == date(2026, 9, 26)
    assert roster.get("alice.nguyen@acme.example").termination_date is None
    assert roster.timezone_for("nobody@acme.example", "UTC") == "UTC"


def test_roster_missing_file_is_roster_error(tmp_path):
    with pytest.raises(RosterError):
        Roster.load(tmp_path / "nope.json")
