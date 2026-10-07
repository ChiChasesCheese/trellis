from datetime import datetime, timedelta, timezone

import pytest

from insiderwatch.alerts import Alert, AlertStore
from insiderwatch.alerts.cases import CaseStore
from insiderwatch.errors import InsiderWatchError

T0 = datetime(2026, 9, 2, 5, 0, tzinfo=timezone.utc)


@pytest.fixture
def stores(conn, config):
    return AlertStore(conn), CaseStore(conn, config)


def file(stores, score, hours=0.0, user="ann@acme.example"):
    alerts, cases = stores
    alert = alerts.add(Alert(user=user, signal="s", score=score, ts=T0 + timedelta(hours=hours), reasons=["r"]))
    return cases.assign(alert)


def test_alerts_in_the_window_share_a_case(stores):
    first = file(stores, 0.2)
    second = file(stores, 0.2, hours=5)
    assert first.created and not second.created
    assert second.case.id == first.case.id and second.case.alert_ids == [1, 2]


def test_gap_beyond_window_or_other_user_opens_a_new_case(stores, config):
    first = file(stores, 0.2)
    assert file(stores, 0.2, hours=config.case_window_hours + 1).case.id != first.case.id
    assert file(stores, 0.2, hours=1, user="lee@acme.example").created


def test_window_is_measured_from_the_latest_alert(stores, config):
    ids = {file(stores, 0.2, hours=h).case.id for h in (0, 40, 80, 120)}
    assert len(ids) == 1  # each step is within 48h of the previous alert


def test_severity_is_the_maximum_and_escalation_is_reported(stores, config):
    file(stores, 0.2)
    assert not file(stores, 0.25, hours=1).escalated
    change = file(stores, 0.9, hours=2)
    assert change.escalated and change.case.score == 0.9
    assert not file(stores, 0.3, hours=3).escalated and stores[1].get(change.case.id).score == 0.9


def test_closed_case_is_not_reopened(stores):
    first = file(stores, 0.2)
    stores[1].close(first.case.id)
    again = file(stores, 0.2, hours=1)
    assert again.created and again.case.id != first.case.id
    assert stores[1].get(first.case.id).status == "closed"


def test_close_errors(stores):
    with pytest.raises(InsiderWatchError):
        stores[1].close(99)
    case = file(stores, 0.2).case
    stores[1].close(case.id)
    with pytest.raises(InsiderWatchError):
        stores[1].close(case.id)
