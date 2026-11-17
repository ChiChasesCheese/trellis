"""密码重置服务的测试：每条产品规则至少一个用例，边界用时钟精确推进，不依赖真实时间与随机数。"""

import importlib
import os
import time
from datetime import datetime, timedelta, timezone, tzinfo

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

UTC = timezone.utc
T0 = datetime(2026, 1, 1, 12, tzinfo=UTC)
USERS = {
    "acct_mira": {"password_hash": "pw_mira_v1", "email": "mira@example.org"},
    "acct_noel": {"password_hash": "pw_noel_v1", "email": "noel@example.org"},
}


class Clock:
    """可控时钟：每次被读取都计数，测试用它断言"哪些路径不读时钟"。"""

    def __init__(self, start: datetime = T0) -> None:
        self.current = start
        self.calls = 0

    def __call__(self) -> datetime:
        self.calls += 1
        return self.current

    def advance(self, seconds: float) -> None:
        self.current += timedelta(seconds=seconds)


class RecordingDatabase(impl.MockDatabase):
    """记录每次写入调用的顺序，用来断言"一次 update_password、再 clear"与"失败路径零写入"。"""

    def __init__(self, users=None) -> None:
        super().__init__(users)
        self.writes: list[str] = []

    def update_password(self, user_id, new_password_hash):
        self.writes.append("update_password")
        super().update_password(user_id, new_password_hash)

    def save_reset_code(self, user_id, code, timestamp):
        self.writes.append("save_reset_code")
        super().save_reset_code(user_id, code, timestamp)

    def clear_reset_code(self, user_id):
        self.writes.append("clear_reset_code")
        super().clear_reset_code(user_id)


@pytest.fixture(autouse=True)
def database(monkeypatch):
    fresh = RecordingDatabase(USERS)
    monkeypatch.setattr(impl, "db", fresh)
    return fresh


@pytest.fixture
def clock():
    return Clock()


@pytest.fixture
def service(clock):
    return impl.PasswordResetService(clock=clock)


def scripted(*codes):
    """返回一个按顺序给出 codes 的生成器钩子，并记录被调用了几次。"""
    calls = []
    queue = list(codes)

    def generate():
        calls.append(1)
        return queue.pop(0)

    generate.calls = calls
    return generate


def password_of(database, user_id="acct_mira"):
    return database.get_user(user_id)["password_hash"]


# ---------------------------------------------------------------- 1. 配置


def test_missing_variable_uses_default_url():
    assert impl.PasswordResetService(environment={}).auth_service_url == "http://internal.auth.local"


@pytest.mark.parametrize(
    "value",
    ["", "   ", " http://internal.auth.local/ ", "http://internal.auth.local/", "https://u:p@host:8443/a?b=1#c", "HTTP://X"],
)
def test_explicit_url_is_preserved_exactly(value):
    service = impl.PasswordResetService(environment={"INTERNAL_AUTH_URL": value})
    assert service.auth_service_url == value


def test_url_is_a_snapshot_taken_at_construction():
    env = {"INTERNAL_AUTH_URL": "http://one"}
    first = impl.PasswordResetService(environment=env)
    env["INTERNAL_AUTH_URL"] = "http://two"
    second = impl.PasswordResetService(environment=env)
    del env["INTERNAL_AUTH_URL"]
    assert first.auth_service_url == "http://one"
    assert second.auth_service_url == "http://two"
    assert impl.PasswordResetService(environment=env).auth_service_url == "http://internal.auth.local"


def test_process_environment_is_used_when_no_mapping_is_given(monkeypatch):
    monkeypatch.setenv("INTERNAL_AUTH_URL", "http://from-os-environ")
    service = impl.PasswordResetService()
    monkeypatch.setenv("INTERNAL_AUTH_URL", "http://changed-later")
    assert service.auth_service_url == "http://from-os-environ"
    monkeypatch.delenv("INTERNAL_AUTH_URL")
    assert impl.PasswordResetService().auth_service_url == "http://internal.auth.local"


def test_an_empty_mapping_is_a_mapping_not_a_missing_one(monkeypatch):
    monkeypatch.setenv("INTERNAL_AUTH_URL", "http://process-level")
    service = impl.PasswordResetService(environment={})
    assert service.auth_service_url == "http://internal.auth.local"


def test_construction_reads_no_clock_and_changes_no_state(database, clock):
    before = database.snapshot()
    impl.PasswordResetService(clock=clock, environment={})
    assert clock.calls == 0
    assert database.snapshot() == before
    assert database.writes == []


# ---------------------------------------------------------------- 2. 请求重置码


def test_unknown_user_raises_before_any_clock_read_or_write(service, clock, database):
    before = database.snapshot()
    with pytest.raises(ValueError, match="^User not found$"):
        service.request_reset("nobody")
    assert clock.calls == 0
    assert database.writes == []
    assert database.snapshot() == before


def test_request_returns_nonempty_string_and_stores_it_with_the_clock_instant(service, database):
    code = service.request_reset("acct_mira")
    assert isinstance(code, str) and code
    row = database.get_reset_code("acct_mira")
    assert row["code"] == code
    assert row["created_at"] == T0
    assert row["created_at"].utcoffset() == timedelta(0)


def test_stored_time_is_utc_even_when_the_clock_has_another_offset(database):
    plus_five = timezone(timedelta(hours=5, minutes=30))
    service = impl.PasswordResetService(clock=Clock(datetime(2026, 1, 1, 17, 30, tzinfo=plus_five)))
    service.request_reset("acct_mira")
    stored = database.get_reset_code("acct_mira")["created_at"]
    assert stored == T0 and stored.utcoffset() == timedelta(0)


def test_request_reads_the_clock_once(service, clock):
    service.request_reset("acct_mira")
    assert clock.calls == 1


def test_request_changes_no_password_and_no_other_user(service, database):
    before_users, _ = database.snapshot()
    service.request_reset("acct_mira")
    assert database.snapshot()[0] == before_users
    assert database.get_reset_code("acct_noel") is None


def test_second_request_replaces_code_and_restarts_the_window(service, clock):
    first = service.request_reset("acct_mira")
    clock.advance(20)
    second = service.request_reset("acct_mira")
    assert second != first
    clock.advance(20)  # 第一个码已 40 秒，第二个码 20 秒
    assert service.verify_and_reset("acct_mira", first, "pw") is False
    assert service.verify_and_reset("acct_mira", second, "pw") is True


def test_default_generator_never_repeats_within_one_instance(service):
    codes = [service.request_reset("acct_mira") for _ in range(300)]
    assert len(set(codes)) == 300


def test_retries_when_the_hook_returns_a_code_already_issued(clock):
    service = impl.PasswordResetService(clock=clock)
    service.generate_code = scripted("aaa", "aaa", "bbb", "aaa", "ccc")
    assert service.request_reset("acct_mira") == "aaa"
    assert service.request_reset("acct_mira") == "bbb"  # 第二次请求：撞上 aaa，重试一次
    assert service.request_reset("acct_mira") == "ccc"


def test_hook_is_called_once_per_attempt():
    service = impl.PasswordResetService(clock=Clock())
    hook = scripted("a", "a", "a", "b")
    service.generate_code = hook
    service.request_reset("acct_mira")
    assert len(hook.calls) == 1
    service.request_reset("acct_mira")
    assert len(hook.calls) == 4  # a 撞车两次，第四次得到 b


def test_a_used_code_is_not_issued_again_even_after_success(clock, database):
    service = impl.PasswordResetService(clock=clock)
    service.generate_code = scripted("aaa", "aaa", "bbb")
    code = service.request_reset("acct_mira")
    assert service.verify_and_reset("acct_mira", code, "pw") is True
    assert database.get_reset_code("acct_mira") is None
    assert service.request_reset("acct_mira") == "bbb"


def test_new_code_differs_from_the_one_another_instance_stored(clock):
    first = impl.PasswordResetService(clock=clock)
    first.generate_code = scripted("same")
    stored = first.request_reset("acct_mira")
    second = impl.PasswordResetService(clock=clock)
    second.generate_code = scripted(stored, "different")
    assert second.request_reset("acct_mira") == "different"


def test_a_stuck_generator_fails_loudly_and_leaves_state_alone(clock, database):
    service = impl.PasswordResetService(clock=clock)
    service.generate_code = lambda: "stuck"
    assert service.request_reset("acct_mira") == "stuck"
    before = database.snapshot()
    with pytest.raises(RuntimeError):
        service.request_reset("acct_mira")
    assert database.snapshot() == before


# ---------------------------------------------------------------- 3. 校验失败不留痕


@pytest.mark.parametrize(
    "user_id, code",
    [("nobody", "abc"), ("acct_noel", "abc"), ("acct_mira", "WRONG"), ("acct_mira", ""), ("acct_mira", " abc"), ("acct_mira", "ABC")],
)
def test_every_false_leaves_state_untouched(clock, database, user_id, code):
    service = impl.PasswordResetService(clock=clock)
    service.generate_code = scripted("abc")
    service.request_reset("acct_mira")
    database.writes.clear()
    before = database.snapshot()
    assert service.verify_and_reset(user_id, code, "pw") is False
    assert database.snapshot() == before
    assert database.writes == []


def test_unknown_user_verification_reads_no_clock(service, clock):
    assert service.verify_and_reset("nobody", "abc", "pw") is False
    assert clock.calls == 0


def test_user_without_a_record_is_rejected(service, database):
    assert service.verify_and_reset("acct_mira", "abc", "pw") is False
    assert password_of(database) == "pw_mira_v1"


def test_wrong_attempt_does_not_consume_a_valid_code(service, database):
    code = service.request_reset("acct_mira")
    assert service.verify_and_reset("acct_mira", code + "x", "pw") is False
    assert service.verify_and_reset("acct_mira", code, "pw") is True
    assert password_of(database) == "hashed_pw"


# ---------------------------------------------------------------- 4. 有效期


@pytest.mark.parametrize(
    "age, expected",
    [
        (timedelta(0), True),
        (timedelta(seconds=29.9), True),
        (timedelta(seconds=29, microseconds=999999), True),
        (timedelta(seconds=30), False),
        (timedelta(seconds=30, microseconds=1), False),
        (timedelta(hours=2), False),
        (timedelta(microseconds=-1), False),
        (timedelta(seconds=-5), False),
    ],
)
def test_validity_window_is_half_open(service, clock, database, age, expected):
    code = service.request_reset("acct_mira")
    clock.current = T0 + age
    assert service.verify_and_reset("acct_mira", code, "pw") is expected
    assert (password_of(database) == "hashed_pw") is expected


def test_expired_code_stays_stored_and_a_new_request_replaces_it(service, clock, database):
    old = service.request_reset("acct_mira")
    clock.advance(31)
    assert service.verify_and_reset("acct_mira", old, "pw") is False
    assert database.get_reset_code("acct_mira")["code"] == old
    fresh = service.request_reset("acct_mira")
    assert database.get_reset_code("acct_mira") == {"code": fresh, "created_at": clock.current}
    assert service.verify_and_reset("acct_mira", fresh, "pw") is True


def test_a_clock_that_moves_backwards_makes_the_record_invalid_not_consumed(service, clock, database):
    code = service.request_reset("acct_mira")
    clock.advance(-1)
    assert service.verify_and_reset("acct_mira", code, "pw") is False
    assert database.get_reset_code("acct_mira") is not None
    clock.advance(1)
    assert service.verify_and_reset("acct_mira", code, "pw") is True


def test_verify_reads_the_clock_once(service, clock):
    code = service.request_reset("acct_mira")
    clock.calls = 0
    service.verify_and_reset("acct_mira", code, "pw")
    assert clock.calls == 1


@pytest.mark.parametrize("hours", [-8, 0, 5.5, 14])
def test_offsets_compare_instants_not_wall_fields(clock, database, hours):
    zone = timezone(timedelta(hours=hours))
    service = impl.PasswordResetService(clock=clock)
    created = T0.astimezone(zone)  # 同一瞬间，钟面字段不同
    for seconds, expected in [(29.9, True), (30, False)]:
        database.save_reset_code("acct_mira", "abc", created)
        clock.current = T0 + timedelta(seconds=seconds)
        assert service.verify_and_reset("acct_mira", "abc", "pw") is expected


def test_clock_in_another_zone_is_compared_by_instant(database):
    tokyo = timezone(timedelta(hours=9))
    clock = Clock(T0.astimezone(tokyo))
    service = impl.PasswordResetService(clock=clock)
    database.save_reset_code("acct_mira", "abc", T0)
    clock.advance(29.9)
    assert service.verify_and_reset("acct_mira", "abc", "pw") is True
    database.save_reset_code("acct_mira", "abc", T0)
    clock.current = T0.astimezone(tokyo) + timedelta(seconds=30)
    assert service.verify_and_reset("acct_mira", "abc", "pw") is False


class OneHourJumpZone(tzinfo):
    """2026-01-01 02:00 起偏移从 UTC+0 变成 UTC+1，像夏令时开始；用来触发"同一个 tzinfo 对象直接相减"的陷阱。"""

    cutover = datetime(2026, 1, 1, 2)

    def utcoffset(self, dt):
        return timedelta(hours=1) if dt.replace(tzinfo=None) >= self.cutover else timedelta(0)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "JUMP"


def test_same_tzinfo_object_across_an_offset_change_still_measures_real_seconds(database):
    zone = OneHourJumpZone()
    created = datetime(2026, 1, 1, 1, 59, 50, tzinfo=zone)  # 01:59:50Z
    now = datetime(2026, 1, 1, 3, 0, 10, tzinfo=zone)  # 02:00:10Z，真实只过了 20 秒，钟面却差一小时
    database.save_reset_code("acct_mira", "abc", created)
    service = impl.PasswordResetService(clock=lambda: now)
    assert service.verify_and_reset("acct_mira", "abc", "pw") is True


@pytest.fixture
def tokyo_local_time(monkeypatch):
    """把进程的本地时区改成 UTC+9（POSIX 写法，不依赖系统时区库），测完恢复。"""
    monkeypatch.setenv("TZ", "JST-9")
    time.tzset()
    yield
    monkeypatch.undo()
    time.tzset()


def test_legacy_naive_timestamp_is_utc_regardless_of_the_machine_zone(tokyo_local_time, clock, database):
    service = impl.PasswordResetService(clock=clock)
    naive = datetime(2026, 1, 1, 12, 0, 0)
    database.save_reset_code("acct_mira", "abc", naive)
    clock.advance(29.9)
    assert service.verify_and_reset("acct_mira", "abc", "pw") is True
    database.save_reset_code("acct_mira", "abc", naive)
    clock.advance(0.1)
    assert service.verify_and_reset("acct_mira", "abc", "pw") is False
    database.save_reset_code("acct_mira", "abc", datetime(2026, 1, 1, 12, 0, 1))
    clock.current = T0
    assert service.verify_and_reset("acct_mira", "abc", "pw") is False  # 创建时间在"未来"


# ---------------------------------------------------------------- 5. 保存密码

@pytest.mark.parametrize("password", ["new_pass", "", "   ", "  pad  ", "pässwörd-密码-🔑", "hashed_x", "a\nb\t"])
def test_exactly_hashed_prefix_plus_password_is_saved(service, database, password):
    code = service.request_reset("acct_mira")
    assert service.verify_and_reset("acct_mira", code, password) is True
    assert password_of(database) == "hashed_" + password


def test_success_uses_one_update_then_one_clear_and_keeps_profile_fields(service, database):
    code = service.request_reset("acct_mira")
    database.writes.clear()
    assert service.verify_and_reset("acct_mira", code, "pw") is True
    assert database.writes == ["update_password", "clear_reset_code"]
    assert database.get_user("acct_mira") == {"password_hash": "hashed_pw", "email": "mira@example.org"}
    assert database.get_user("acct_noel") == USERS["acct_noel"]


def test_mutating_the_copy_from_get_user_saves_nothing(database):
    copy_of_user = database.get_user("acct_mira")
    copy_of_user["password_hash"] = "hacked"
    assert password_of(database) == "pw_mira_v1"


def test_password_is_not_saved_when_the_code_is_already_expired(service, clock, database):
    code = service.request_reset("acct_mira")
    clock.advance(30)
    database.writes.clear()
    assert service.verify_and_reset("acct_mira", code, "pw") is False
    assert database.writes == []
    assert password_of(database) == "pw_mira_v1"


def test_a_failed_password_write_does_not_consume_the_code(service, monkeypatch, database):
    code = service.request_reset("acct_mira")

    def boom(user_id, new_password_hash):
        raise OSError("database down")

    monkeypatch.setattr(database, "update_password", boom)
    with pytest.raises(OSError):
        service.verify_and_reset("acct_mira", code, "pw")
    assert database.get_reset_code("acct_mira")["code"] == code
    monkeypatch.undo()
    monkeypatch.setattr(impl, "db", database)
    assert service.verify_and_reset("acct_mira", code, "pw") is True


# ---------------------------------------------------------------- 6. 一次性与用户隔离


def test_replay_fails_on_the_same_and_on_another_instance(clock, database):
    first = impl.PasswordResetService(clock=clock)
    second = impl.PasswordResetService(clock=clock)
    code = first.request_reset("acct_mira")
    assert first.verify_and_reset("acct_mira", code, "one") is True
    assert first.verify_and_reset("acct_mira", code, "two") is False
    assert second.verify_and_reset("acct_mira", code, "three") is False
    assert password_of(database) == "hashed_one"
    assert database.get_reset_code("acct_mira") is None


def test_a_later_request_allows_another_change(service, database):
    first = service.request_reset("acct_mira")
    assert service.verify_and_reset("acct_mira", first, "one") is True
    second = service.request_reset("acct_mira")
    assert second != first
    assert service.verify_and_reset("acct_mira", second, "two") is True
    assert password_of(database) == "hashed_two"


def test_instances_share_the_database(clock, database):
    code = impl.PasswordResetService(clock=clock).request_reset("acct_mira")
    assert impl.PasswordResetService(clock=clock).verify_and_reset("acct_mira", code, "pw") is True
    assert password_of(database) == "hashed_pw"


def test_a_code_belongs_to_the_user_whose_record_stores_it(clock, database):
    service = impl.PasswordResetService(clock=clock)
    service.generate_code = scripted("one", "two")
    code_a = service.request_reset("acct_mira")
    code_b = service.request_reset("acct_noel")
    assert service.verify_and_reset("acct_noel", code_a, "pw") is False
    assert service.verify_and_reset("acct_mira", code_b, "pw") is False
    assert service.verify_and_reset("acct_mira", code_a, "pw") is True
    assert database.get_reset_code("acct_noel")["code"] == code_b
    assert password_of(database, "acct_noel") == "pw_noel_v1"


def test_the_same_code_string_for_two_users_clears_only_one(clock, database):
    service = impl.PasswordResetService(clock=clock)
    database.save_reset_code("acct_mira", "dup", T0)
    database.save_reset_code("acct_noel", "dup", T0)
    assert service.verify_and_reset("acct_mira", "dup", "pw") is True
    assert database.get_reset_code("acct_mira") is None
    assert database.get_reset_code("acct_noel")["code"] == "dup"
    assert password_of(database, "acct_noel") == "pw_noel_v1"


def test_leftover_record_of_a_deleted_user_returns_false_and_changes_nothing(clock, database):
    service = impl.PasswordResetService(clock=clock)
    database.save_reset_code("ghost", "abc", T0)
    before = database.snapshot()
    database.writes.clear()
    assert service.verify_and_reset("ghost", "abc", "pw") is False
    assert database.snapshot() == before
    assert database.writes == []
