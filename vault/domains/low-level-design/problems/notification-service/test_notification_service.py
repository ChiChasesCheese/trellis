"""通知服务的验收测试：四关的行为、失败路径，以及并发下"同一幂等键只发一次"的不变量。

所有断言只看公开 API（`sent_count`、`pending_count`、`dead_letters`、`history`、`tracked_keys`、
`size`、`queue_depth`），不碰任何下划线属性。渠道一律是注入的假实现，从不发真网络请求；
时钟是注入的固定时钟，退避与限流窗口靠推时钟验证，测试里没有一个 `sleep` 参与断言。
"""

from __future__ import annotations

import importlib
import os
import threading
import time
from datetime import datetime, timedelta, timezone

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


class FrozenClock:
    """固定时钟，测试自己推进。"""

    def __init__(self, hour: int = 12) -> None:
        self._now = datetime(2026, 1, 1, hour, tzinfo=timezone.utc)

    def __call__(self) -> datetime:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += timedelta(seconds=seconds)


class FakeProvider:
    """注入的假渠道：记录收到的信封，可以被编排成前 N 次瞬时失败、或永久失败。"""

    def __init__(self, channel: str, fail_times: int = 0, permanent: bool = False,
                 always_fail: bool = False) -> None:
        self.channel = channel
        self.sent: list = []
        self.calls = 0
        self._fail_times = fail_times
        self._permanent = permanent
        self._always_fail = always_fail
        self._lock = threading.Lock()

    def send(self, envelope) -> str:
        with self._lock:
            self.calls += 1
            failing = self._always_fail or self.calls <= self._fail_times
            if failing and self._permanent:
                raise impl.PermanentDeliveryError(f"{self.channel}: bad address")
            if failing:
                raise impl.TransientDeliveryError(f"{self.channel}: timeout")
            self.sent.append(envelope)
            return f"{self.channel}-{self.calls}"

    @property
    def titles(self) -> list:
        with self._lock:
            return [e.title for e in self.sent]


def make_service(clock=None, **kwargs):
    """一个注册好模板的服务。模板是数据，注册它不碰任何一行派发逻辑。"""
    service = impl.NotificationService(clock=clock or FrozenClock(), **kwargs)
    service.templates.register("alert", "{tag}", "正文 {tag}")
    return service


def make_user(user_id: str = "u1", channels=("email", "sms"), **kwargs):
    return impl.UserPreferences(
        user_id,
        addresses={c: f"{user_id}@{c}" for c in channels},
        enabled_channels=frozenset(channels),
        **kwargs)


def status_by_channel(results) -> dict:
    return {r.channel: r.status for r in results}


# ---------------------------------------------------------------------------
# 第 1 关：渠道抽象、寻址到人、可能失败的投递
# ---------------------------------------------------------------------------


def test_one_request_fans_out_to_every_enabled_channel() -> None:
    service = make_service()
    email, sms = FakeProvider("email"), FakeProvider("sms")
    service.register_provider(email)
    service.register_provider(sms)
    service.set_preferences(make_user())
    results = service.submit(impl.Notification("n1", "u1", "alert", {"tag": "A"}))
    assert set(status_by_channel(results)) == {"email", "sms"}
    service.drain()
    assert email.titles == ["A"] and sms.titles == ["A"]
    assert service.sent_count == 2
    assert service.pending_count == 0


def test_a_channel_specific_template_overrides_the_default() -> None:
    service = make_service()
    service.templates.register("alert", "短", "短信只有 {tag}", channel="sms")
    email, sms = FakeProvider("email"), FakeProvider("sms")
    service.register_provider(email)
    service.register_provider(sms)
    service.set_preferences(make_user())
    service.submit(impl.Notification("n1", "u1", "alert", {"tag": "A"}))
    service.drain()
    assert email.sent[0].body == "正文 A"
    assert sms.sent[0].body == "短信只有 A"


def test_an_unregistered_template_is_refused_before_any_side_effect() -> None:
    service = make_service()
    email, sms = FakeProvider("email"), FakeProvider("sms")
    service.register_provider(email)
    service.register_provider(sms)
    service.set_preferences(make_user())
    with pytest.raises(impl.UnknownTemplateError):
        service.submit(impl.Notification("n1", "u1", "nope", {}))
    assert service.pending_count == 0            # 第一个渠道不许已经入队
    assert service.history == ()                 # 幂等键也不许已经被占掉
    service.templates.register("nope", "{tag}", "{tag}")
    service.submit(impl.Notification("n1", "u1", "nope", {"tag": "A"}))
    service.drain()
    assert email.titles == ["A"] and sms.titles == ["A"]


def test_one_channel_failing_does_not_stop_the_other() -> None:
    service = make_service(retry=impl.RetryPolicy(max_attempts=1))
    email = FakeProvider("email", always_fail=True, permanent=True)
    sms = FakeProvider("sms")
    service.register_provider(email)
    service.register_provider(sms)
    service.set_preferences(make_user())
    service.submit(impl.Notification("n1", "u1", "alert", {"tag": "A"}))
    service.drain()
    assert sms.titles == ["A"]                       # 邮件炸了，短信照发
    assert service.sent_count == 1
    assert [d.channel for d in service.dead_letters] == ["email"]


def test_a_channel_without_a_provider_is_reported_not_crashed() -> None:
    service = make_service()
    service.register_provider(FakeProvider("email"))
    service.set_preferences(make_user())             # 偏好里有 sms，但没注册 provider
    results = status_by_channel(service.submit(impl.Notification("n1", "u1", "alert", {"tag": "A"})))
    assert results["sms"] is impl.DeliveryStatus.SUPPRESSED_NO_PROVIDER
    assert results["email"] is impl.DeliveryStatus.QUEUED


# ---------------------------------------------------------------------------
# 第 2 关：偏好、静默时段、频次上限、优先级车道
# ---------------------------------------------------------------------------


def test_a_disabled_channel_is_suppressed_with_its_own_reason() -> None:
    service = make_service()
    service.register_provider(FakeProvider("email"))
    service.register_provider(FakeProvider("sms"))
    service.set_preferences(make_user(channels=("email",)))
    results = status_by_channel(service.submit(
        impl.Notification("n1", "u1", "alert", {"tag": "A"}, channels=("email", "sms"))))
    assert results["sms"] is impl.DeliveryStatus.SUPPRESSED_CHANNEL_OFF
    assert results["email"] is impl.DeliveryStatus.QUEUED


def test_min_priority_per_channel_keeps_marketing_off_sms() -> None:
    service = make_service()
    email, sms = FakeProvider("email"), FakeProvider("sms")
    service.register_provider(email)
    service.register_provider(sms)
    service.set_preferences(make_user(min_priority={"sms": impl.Priority.URGENT}))
    marketing = status_by_channel(service.submit(
        impl.Notification("n1", "u1", "alert", {"tag": "M"}, impl.Priority.MARKETING)))
    urgent = status_by_channel(service.submit(
        impl.Notification("n2", "u1", "alert", {"tag": "U"}, impl.Priority.URGENT)))
    assert marketing["sms"] is impl.DeliveryStatus.SUPPRESSED_PRIORITY
    assert urgent["sms"] is impl.DeliveryStatus.QUEUED
    service.drain()
    assert sms.titles == ["U"] and email.titles == ["U", "M"]   # 邮件两条都发，但紧急的先走


def test_quiet_hours_stop_marketing_but_never_a_one_time_password() -> None:
    clock = FrozenClock(hour=23)
    service = make_service(clock)
    email = FakeProvider("email")
    service.register_provider(email)
    service.set_preferences(make_user(channels=("email",), quiet_hours=(22, 7)))
    marketing = service.submit(
        impl.Notification("n1", "u1", "alert", {"tag": "M"}, impl.Priority.MARKETING))
    otp = service.submit(impl.Notification("n2", "u1", "alert", {"tag": "OTP"}, impl.Priority.URGENT))
    assert marketing[0].status is impl.DeliveryStatus.SUPPRESSED_QUIET_HOURS
    assert otp[0].status is impl.DeliveryStatus.QUEUED
    service.drain()
    assert email.titles == ["OTP"]                   # 免打扰挡不住验证码


def test_quiet_hours_wrap_around_midnight_in_the_users_timezone() -> None:
    prefs = make_user(channels=("email",), quiet_hours=(22, 7), utc_offset_minutes=480)
    assert prefs.in_quiet_hours(datetime(2026, 1, 1, 15, tzinfo=timezone.utc))   # 本地 23:00
    assert prefs.in_quiet_hours(datetime(2026, 1, 1, 21, tzinfo=timezone.utc))   # 本地 05:00
    assert not prefs.in_quiet_hours(datetime(2026, 1, 1, 6, tzinfo=timezone.utc))  # 本地 14:00
    assert not make_user(channels=("email",)).in_quiet_hours(datetime(2026, 1, 1, 3, tzinfo=timezone.utc))


def test_the_rate_cap_is_per_user_and_per_channel() -> None:
    service = make_service(rate_limit=(2, 60.0))
    email, sms = FakeProvider("email"), FakeProvider("sms")
    service.register_provider(email)
    service.register_provider(sms)
    service.set_preferences(make_user("u1"))
    service.set_preferences(make_user("u2"))
    statuses = [status_by_channel(service.submit(impl.Notification(f"n{i}", "u1", "alert", {"tag": i})))
                for i in range(3)]
    assert statuses[0]["email"] is impl.DeliveryStatus.QUEUED
    assert statuses[2]["email"] is impl.DeliveryStatus.SUPPRESSED_RATE_LIMIT
    assert statuses[2]["sms"] is impl.DeliveryStatus.SUPPRESSED_RATE_LIMIT
    other = status_by_channel(service.submit(impl.Notification("n9", "u2", "alert", {"tag": 9})))
    assert other["email"] is impl.DeliveryStatus.QUEUED    # 别的用户不受牵连
    service.drain()
    assert len(email.sent) == 3


def test_the_rate_limiter_forgets_a_key_once_its_window_empties() -> None:
    clock = FrozenClock()
    limiter = impl.RateLimiter(2, 60.0, clock)
    assert limiter.allow("u1|email") and limiter.allow("u1|email")
    assert not limiter.allow("u1|email")
    assert limiter.tracked_keys == 1
    clock.advance(61)
    assert limiter.allow("u1|email")                 # 窗口滑过去了
    clock.advance(61)
    assert limiter.purge() == 1
    assert limiter.tracked_keys == 0                 # 只涨不落的字典就是一个内存事故


def test_urgent_is_drained_before_marketing() -> None:
    service = make_service()
    email = FakeProvider("email")
    service.register_provider(email)
    service.set_preferences(make_user(channels=("email",)))
    for i in range(2):
        service.submit(impl.Notification(f"m{i}", "u1", "alert", {"tag": f"M{i}"}, impl.Priority.MARKETING))
    for i in range(2):
        service.submit(impl.Notification(f"u{i}", "u1", "alert", {"tag": f"U{i}"}, impl.Priority.URGENT))
    assert service.queue_depth(impl.Priority.URGENT) == 2
    assert service.queue_depth(impl.Priority.MARKETING) == 2
    service.drain()
    assert email.titles == ["U0", "U1", "M0", "M1"]  # 营销先入队也排在后面


def test_a_lane_quota_keeps_a_flood_of_urgent_from_starving_marketing() -> None:
    service = make_service(lane_quota={impl.Priority.URGENT: 2})
    email = FakeProvider("email")
    service.register_provider(email)
    service.set_preferences(make_user(channels=("email",)))
    for i in range(2):
        service.submit(impl.Notification(f"m{i}", "u1", "alert", {"tag": f"M{i}"}, impl.Priority.MARKETING))
    for i in range(5):
        service.submit(impl.Notification(f"u{i}", "u1", "alert", {"tag": f"U{i}"}, impl.Priority.URGENT))
    service.drain()
    assert email.titles == ["U0", "U1", "M0", "U2", "U3", "M1", "U4"]


# ---------------------------------------------------------------------------
# 第 3 关：重试与退避、死信、调用方提供的幂等键
# ---------------------------------------------------------------------------


def test_backoff_is_exponential_and_capped() -> None:
    policy = impl.RetryPolicy(max_attempts=5, base_delay=2.0, multiplier=3.0, max_delay=20.0)
    assert [policy.delay_for(a) for a in (1, 2, 3, 4)] == [2.0, 6.0, 18.0, 20.0]


def test_a_transient_failure_is_retried_only_after_its_backoff_elapses() -> None:
    clock = FrozenClock()
    service = make_service(clock, retry=impl.RetryPolicy(max_attempts=3, base_delay=10.0))
    email = FakeProvider("email", fail_times=1)
    service.register_provider(email)
    service.set_preferences(make_user(channels=("email",)))
    service.submit(impl.Notification("n1", "u1", "alert", {"tag": "A"}))
    service.drain()
    assert email.calls == 1 and service.sent_count == 0
    assert service.pending_count == 1                # 排到未来了，还没到点
    service.drain()
    assert email.calls == 1                          # 时间没走，重试就不该发生
    clock.advance(10)
    service.drain()
    assert email.calls == 2 and service.sent_count == 1
    assert service.pending_count == 0


def test_retries_run_out_and_the_message_lands_in_the_dead_letter() -> None:
    clock = FrozenClock()
    service = make_service(clock, retry=impl.RetryPolicy(max_attempts=3, base_delay=1.0, multiplier=2.0))
    email = FakeProvider("email", always_fail=True)
    service.register_provider(email)
    service.set_preferences(make_user(channels=("email",)))
    service.submit(impl.Notification("n1", "u1", "alert", {"tag": "A"}))
    for _ in range(4):
        service.drain()
        clock.advance(60)
    assert email.calls == 3                          # 正好 max_attempts 次，不多不少
    assert service.sent_count == 0
    dead = service.dead_letters
    assert len(dead) == 1 and dead[0].channel == "email"
    assert dead[0].status is impl.DeliveryStatus.DEAD_LETTERED
    assert dead[0].attempts == 3
    assert service.pending_count == 0


def test_a_permanent_failure_is_not_retried_at_all() -> None:
    clock = FrozenClock()
    service = make_service(clock, retry=impl.RetryPolicy(max_attempts=5, base_delay=1.0))
    email = FakeProvider("email", always_fail=True, permanent=True)
    service.register_provider(email)
    service.set_preferences(make_user(channels=("email",)))
    service.submit(impl.Notification("n1", "u1", "alert", {"tag": "A"}))
    service.drain()
    clock.advance(600)
    service.drain()
    assert email.calls == 1                          # 地址非法，重试一百次也是同一个结果
    assert len(service.dead_letters) == 1


def test_resubmitting_the_same_caller_supplied_id_is_a_no_op() -> None:
    service = make_service()
    email = FakeProvider("email")
    service.register_provider(email)
    service.set_preferences(make_user(channels=("email",)))
    notification = impl.Notification("order-42", "u1", "alert", {"tag": "A"})
    first = service.submit(notification)
    service.drain()
    second = service.submit(notification)            # 调用方超时重发
    service.drain()
    assert first[0].status is impl.DeliveryStatus.QUEUED
    assert second[0].status is impl.DeliveryStatus.DUPLICATE
    assert email.calls == 1 and service.sent_count == 1


def test_idempotency_is_scoped_to_one_request_times_one_channel() -> None:
    clock = FrozenClock()
    service = make_service(clock, retry=impl.RetryPolicy(max_attempts=2, base_delay=1.0))
    email = FakeProvider("email", fail_times=1)
    sms = FakeProvider("sms")
    service.register_provider(email)
    service.register_provider(sms)
    service.set_preferences(make_user())
    service.submit(impl.Notification("n1", "u1", "alert", {"tag": "A"}))
    service.drain()
    clock.advance(5)
    service.drain()
    assert sms.calls == 1                            # 短信一次就成了，没被邮件的重试牵连
    assert email.calls == 2 and service.sent_count == 2


def test_the_idempotency_store_expires_and_purges() -> None:
    clock = FrozenClock()
    store = impl.IdempotencyStore(ttl_seconds=10.0, clock=clock)
    assert store.claim("k") is None
    assert store.claim("k") is not None              # 占坑成功之后再来就是重复
    assert store.size == 1
    clock.advance(11)
    assert store.purge() == 1
    assert store.size == 0
    assert store.claim("k") is None                  # 过期之后同一个键可以重新用


def test_concurrent_submits_of_the_same_id_deliver_exactly_once() -> None:
    service = make_service()
    email = FakeProvider("email")
    service.register_provider(email)
    service.set_preferences(make_user(channels=("email",)))
    threads_count = 8
    barrier = threading.Barrier(threads_count)
    outcomes: list = []
    lock = threading.Lock()

    def submit_once() -> None:
        barrier.wait()
        results = service.submit(impl.Notification("same-id", "u1", "alert", {"tag": "A"}))
        with lock:
            outcomes.extend(results)

    workers = [threading.Thread(target=submit_once) for _ in range(threads_count)]
    for w in workers:
        w.start()
    for w in workers:
        w.join(10.0)
    service.drain()
    queued = [r for r in outcomes if r.status is impl.DeliveryStatus.QUEUED]
    assert len(queued) == 1                          # 检查—然后—行动的竞态必须被锁住
    assert len(outcomes) == threads_count
    assert email.calls == 1 and service.sent_count == 1


def test_worker_threads_deliver_every_distinct_request_exactly_once() -> None:
    service = make_service(clock=impl.utc_now)
    email = FakeProvider("email")
    service.register_provider(email)
    service.set_preferences(make_user(channels=("email",)))
    service.start(workers=3)
    try:
        for i in range(100):
            service.submit(impl.Notification(f"n{i}", "u1", "alert", {"tag": i}))
        deadline = time.monotonic() + 10.0
        while service.sent_count < 100 and time.monotonic() < deadline:
            time.sleep(0.005)
    finally:
        service.stop()
    assert service.sent_count == 100
    assert len({e.notification_id for e in email.sent}) == 100
    assert email.calls == 100                        # 不多发，也不少发
    assert service.pending_count == 0


# ---------------------------------------------------------------------------
# 第 4 关：加一个渠道、加一个模板，派发器一行不改
# ---------------------------------------------------------------------------


def test_a_brand_new_channel_needs_only_a_provider_and_a_preference() -> None:
    service = make_service()
    email = FakeProvider("email")
    webhook = FakeProvider("webhook")                # 派发器从没听说过这个名字
    service.register_provider(email)
    service.register_provider(webhook)
    service.set_preferences(make_user(channels=("email", "webhook")))
    assert service.channels == ("email", "webhook")
    service.submit(impl.Notification("n1", "u1", "alert", {"tag": "A"}))
    service.drain()
    assert webhook.titles == ["A"] and email.titles == ["A"]


def test_registering_a_template_is_data_not_code() -> None:
    service = make_service()
    before = service.templates.template_count
    service.templates.register("welcome", "欢迎 {name}", "你好 {name}")
    service.templates.register("welcome", "欢迎", "你好 {name}（短）", channel="sms")
    assert service.templates.template_count == before + 2
    title, body = service.templates.render("welcome", "email", {"name": "Chi"})
    assert (title, body) == ("欢迎 Chi", "你好 Chi")
    assert service.templates.render("welcome", "sms", {"name": "Chi"})[1] == "你好 Chi（短）"


def test_history_and_dead_letters_are_snapshots_not_internal_containers() -> None:
    service = make_service(retry=impl.RetryPolicy(max_attempts=1))
    service.register_provider(FakeProvider("email", always_fail=True, permanent=True))
    service.set_preferences(make_user(channels=("email",)))
    service.submit(impl.Notification("n1", "u1", "alert", {"tag": "A"}))
    service.drain()
    assert isinstance(service.dead_letters, tuple)
    assert isinstance(service.history, tuple)
    snapshot = service.dead_letters
    service.submit(impl.Notification("n2", "u1", "alert", {"tag": "B"}))
    service.drain()
    assert len(snapshot) == 1 and len(service.dead_letters) == 2


def test_a_delivery_result_says_exactly_why_nothing_was_sent() -> None:
    service = make_service(FrozenClock(hour=23), rate_limit=(1, 60.0))
    service.register_provider(FakeProvider("email"))
    service.register_provider(FakeProvider("sms"))
    service.set_preferences(make_user(quiet_hours=(22, 7), min_priority={"sms": impl.Priority.URGENT}))
    reasons = {r.status for r in service.submit(
        impl.Notification("n1", "u1", "alert", {"tag": "A"}, impl.Priority.MARKETING))}
    assert impl.DeliveryStatus.SUPPRESSED_QUIET_HOURS in reasons
    assert impl.DeliveryStatus.SUPPRESSED_PRIORITY in reasons     # 两个渠道两个不同的原因
    assert all(not r.delivered for r in service.history)
