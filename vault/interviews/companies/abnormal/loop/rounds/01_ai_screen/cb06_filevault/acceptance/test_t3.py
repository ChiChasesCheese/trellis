"""t3 -- quota, stats, rate limit. New: GET /stats, GET /admin/stats, 413/429 behaviour, existing config keys."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cb06_support import build_env, run_together  # noqa: E402

pytestmark = pytest.mark.t3
QUOTA = 1000


def make(tmp_path, **settings):
    return build_env(tmp_path, **settings)


@pytest.fixture
def env(tmp_path):
    e = make(tmp_path, quota_bytes_per_user=QUOTA)
    yield e
    e.app.close()


@pytest.fixture
def plain(tmp_path):
    e = make(tmp_path)
    yield e
    e.app.close()


@pytest.mark.regression
def test_uploads_downloads_and_deletes_still_work_under_defaults(plain):
    fid = plain.upload_ok("alice", "a.txt", b"hello")
    assert plain.download("alice", fid) == b"hello"
    assert plain.client("alice").delete(f"/files/{fid}").status_code == 204


@pytest.mark.regression
def test_reads_are_not_rate_limited(tmp_path):
    e = make(tmp_path, rate_limit_per_sec=1)
    try:
        e.upload_ok("alice", "a", b"1")
        assert all(e.client("alice").get("/files").status_code == 200 for _ in range(10))
    finally:
        e.app.close()


@pytest.mark.regression
def test_oversized_single_upload_is_still_413(plain):
    resp = plain.upload("alice", "huge", b"x" * (10 * 1024 * 1024 + 1))
    assert resp.status_code == 413


@pytest.mark.core
def test_upload_up_to_exactly_the_quota_then_413(env):
    assert env.upload("alice", "a", b"a" * 600).status_code == 201
    assert env.upload("alice", "b", b"b" * 400).status_code == 201  # now exactly QUOTA bytes
    resp = env.upload("alice", "c", b"c")
    assert resp.status_code == 413
    assert resp.json["error"]


@pytest.mark.core
def test_a_single_file_over_the_quota_is_413(env):
    assert env.upload("alice", "big", b"x" * (QUOTA + 1)).status_code == 413
    assert env.listing("alice") == []


@pytest.mark.core
def test_deleting_restores_the_allowance(env):
    first = env.upload_ok("alice", "a", b"a" * QUOTA)
    assert env.upload("alice", "b", b"b").status_code == 413
    assert env.client("alice").delete(f"/files/{first}").status_code == 204
    assert env.upload("alice", "b", b"b" * 500).status_code == 201


@pytest.mark.core
def test_other_users_are_unaffected(env):
    env.upload_ok("alice", "a", b"a" * QUOTA)
    assert env.upload("alice", "more", b"m").status_code == 413
    assert env.upload("bob", "b", b"b" * QUOTA).status_code == 201


@pytest.mark.core
def test_my_stats_report_usage_against_the_free_tier(plain):
    plain.upload_ok("alice", "a", b"x" * 30)
    plain.upload_ok("alice", "b", b"y" * 12)
    stats = plain.client("alice").get("/stats").json
    assert stats["used_bytes"] == 42
    assert stats["quota_bytes"] == 10 * 1024 * 1024
    assert stats["file_count"] == 2
    assert plain.client("bob").get("/stats").json["used_bytes"] == 0


@pytest.mark.core
def test_admin_stats_show_what_dedup_saves(plain):
    plain.upload_ok("alice", "a", b"z" * 1000)
    assert plain.client("admin").get("/admin/stats").json["saved_bytes"] == 0
    plain.upload_ok("alice", "copy", b"z" * 1000)
    stats = plain.client("admin").get("/admin/stats").json
    assert stats["logical_bytes"] == 2000
    assert stats["physical_bytes"] == 1000
    assert stats["saved_bytes"] == 1000


@pytest.mark.core
def test_admin_stats_are_for_admins_only(plain):
    assert plain.client("alice").get("/admin/stats").status_code == 403


@pytest.mark.core
def test_rate_limit_answers_429_with_retry_after(tmp_path):
    e = make(tmp_path, rate_limit_per_sec=1)
    try:
        assert e.upload("alice", "a", b"1").status_code == 201
        resp = e.upload("alice", "b", b"2")
        assert resp.status_code == 429
        assert int(resp.headers["Retry-After"]) >= 1
        assert e.upload("bob", "a", b"1").status_code == 201  # limits are per user
    finally:
        e.app.close()


@pytest.mark.stretch
def test_duplicates_still_count_against_the_users_own_quota(env):
    env.upload_ok("alice", "a", b"d" * 600)
    assert env.upload("alice", "b", b"d" * 600).status_code == 413
    assert env.upload("bob", "a", b"d" * 600).status_code == 201


@pytest.mark.stretch
def test_concurrent_uploads_cannot_overshoot_the_quota(tmp_path):
    e = make(tmp_path, slow_store=True, quota_bytes_per_user=100)
    try:
        for i in range(8):
            user = f"user{i}"
            statuses = []
            errors = run_together(
                lambda: statuses.append(e.upload(user, "a", b"a" * 60).status_code),
                lambda: statuses.append(e.upload(user, "b", b"b" * 60).status_code),
            )
            assert errors == []
            assert sorted(statuses) == [201, 413], statuses
            assert e.client(user).get("/stats").json["used_bytes"] == 60
    finally:
        e.app.close()


@pytest.mark.stretch
def test_over_quota_response_tells_the_user_how_much_room_is_left(env):
    env.upload_ok("alice", "a", b"a" * 900)
    body = str(env.upload("alice", "b", b"b" * 200).json)
    assert "100" in body
