"""t2 -- search and filters. Only the query parameters on GET /files are new; response shape is the existing one."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cb06_support import build_env  # noqa: E402

pytestmark = pytest.mark.t2

PDF, TXT, PNG = "application/pdf", "text/plain", "image/png"
INJECTION = "x' OR '1'='1.pdf"


@pytest.fixture
def env(tmp_path):
    e = build_env(tmp_path)
    yield e
    e.app.close()


@pytest.fixture
def seeded(env):
    """alice: one file per day starting 2026-09-01T12:00Z; bob: two files."""
    rows = [
        ("q3-report.pdf", 100, PDF),
        ("Q3-Report-FINAL.PDF", 300, PDF),
        ("notes.txt", 10, TXT),
        ("logo.png", 2000, PNG),
        (INJECTION, 50, PDF),
        ("100%_done.txt", 20, TXT),
    ]
    for name, size, ctype in rows:
        env.upload_ok("alice", name, (name[:1] * size).encode(), ctype)
        env.clock.tick(days=1)
    env.upload_ok("bob", "q3-report.pdf", b"b" * 70, PDF)
    env.upload_ok("bob", "bob-private.txt", b"p" * 5, TXT)
    return env


def error_text(resp) -> str:
    return str(resp.json).lower()


@pytest.mark.regression
def test_unfiltered_listing_is_newest_first_and_paginates(seeded):
    page1 = seeded.client("alice").get("/files", {"limit": 4}).json
    assert [i["filename"] for i in page1["items"]][0] == "100%_done.txt"
    assert len(page1["items"]) == 4 and page1["next_cursor"]
    page2 = seeded.client("alice").get("/files", {"limit": 4, "cursor": page1["next_cursor"]}).json
    assert len(page2["items"]) == 2 and page2["next_cursor"] is None


@pytest.mark.regression
def test_users_still_only_see_their_own_files(seeded):
    assert seeded.names("bob") == ["bob-private.txt", "q3-report.pdf"]


@pytest.mark.core
def test_q_matches_substring_case_insensitively(seeded):
    assert seeded.names("alice", q="REPORT") == ["Q3-Report-FINAL.PDF", "q3-report.pdf"]
    assert seeded.names("alice", q="notes") == ["notes.txt"]
    assert seeded.names("alice", q="nothing-like-this") == []


@pytest.mark.core
def test_type_filter(seeded):
    assert seeded.names("alice", type=TXT) == ["100%_done.txt", "notes.txt"]
    assert seeded.names("alice", type=PNG) == ["logo.png"]


@pytest.mark.core
def test_size_range_is_inclusive(seeded):
    assert seeded.names("alice", min_size=50, max_size=100) == sorted([INJECTION, "q3-report.pdf"])
    assert seeded.names("alice", min_size=2000) == ["logo.png"]
    assert seeded.names("alice", max_size=10) == ["notes.txt"]


@pytest.mark.core
def test_date_range(seeded):
    # alice's uploads: 09-01 q3-report, 09-02 FINAL, 09-03 notes, 09-04 logo, 09-05 injection, 09-06 100%
    got = seeded.names("alice", **{"from": "2026-09-02T00:00:00Z", "to": "2026-09-03T23:59:59Z"})
    assert got == ["Q3-Report-FINAL.PDF", "notes.txt"]
    assert seeded.names("alice", **{"from": "2026-09-06T00:00:00Z"}) == ["100%_done.txt"]
    assert seeded.names("alice", to="2026-09-01T23:00:00Z") == ["q3-report.pdf"]


@pytest.mark.core
def test_filters_combine(seeded):
    assert seeded.names("alice", q="report", type=PDF, min_size=200) == ["Q3-Report-FINAL.PDF"]
    assert seeded.names("alice", type=PDF, **{"from": "2026-09-02T00:00:00Z"}) == sorted([INJECTION, "Q3-Report-FINAL.PDF"])


@pytest.mark.core
def test_injection_filename_is_an_ordinary_string(seeded):
    assert seeded.names("alice", q="' OR '1'='1") == [INJECTION]
    assert seeded.names("alice", q="'; DROP TABLE files; --") == []
    assert len(seeded.listing("alice", limit=200)) == 6  # nothing was damaged or leaked


@pytest.mark.core
def test_search_is_scoped_to_the_caller(seeded):
    assert seeded.names("bob", q="report") == ["q3-report.pdf"]
    assert seeded.names("bob", type=PDF) == ["q3-report.pdf"]
    assert seeded.names("bob", min_size=60) == ["q3-report.pdf"]


@pytest.mark.core
def test_invalid_numbers_are_400_naming_the_parameter(seeded):
    for params, name in [({"min_size": "abc"}, "min_size"), ({"max_size": "-5"}, "max_size")]:
        resp = seeded.client("alice").get("/files", params)
        assert resp.status_code == 400, params
        assert resp.json["error"]
        assert name in error_text(resp)


@pytest.mark.core
def test_invalid_dates_are_400_naming_the_parameter(seeded):
    for params, name in [({"from": "last tuesday"}, "from"), ({"to": "2026-99-99"}, "to")]:
        resp = seeded.client("alice").get("/files", params)
        assert resp.status_code == 400, params
        assert name in error_text(resp)


@pytest.mark.core
def test_filtered_pagination_with_identical_timestamps_loses_nothing(env):
    for i in range(7):  # the frozen clock gives all of these the same created_at
        env.upload_ok("alice", f"match-{i}.pdf", f"m{i}".encode(), PDF)
    for i in range(3):
        env.upload_ok("alice", f"other-{i}.txt", f"o{i}".encode(), TXT)
    seen, cursor = [], None
    for _ in range(10):
        params = {"type": PDF, "limit": 3}
        if cursor:
            params["cursor"] = cursor
        page = env.client("alice").get("/files", params).json
        seen += [i["filename"] for i in page["items"]]
        cursor = page["next_cursor"]
        if cursor is None:
            break
    assert sorted(seen) == [f"match-{i}.pdf" for i in range(7)]


@pytest.mark.stretch
def test_percent_and_underscore_are_literal(seeded):
    assert seeded.names("alice", q="%") == ["100%_done.txt"]
    assert seeded.names("alice", q="_") == ["100%_done.txt"]


@pytest.mark.stretch
def test_inverted_ranges_are_400(seeded):
    assert seeded.client("alice").get("/files", {"min_size": 10, "max_size": 5}).status_code == 400
    resp = seeded.client("alice").get("/files", {"from": "2026-09-03T00:00:00Z", "to": "2026-09-01T00:00:00Z"})
    assert resp.status_code == 400


@pytest.mark.stretch
def test_date_only_values_are_accepted(seeded):
    assert "notes.txt" in seeded.names("alice", **{"from": "2026-09-03", "to": "2026-09-04"})
