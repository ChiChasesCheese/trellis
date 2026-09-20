"""职业社交的测试：分关覆盖档案、连接请求与度数、职位与申请、背书与推荐、并发。"""

from __future__ import annotations

import importlib
import os
import threading
from datetime import UTC, datetime, timedelta

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

START = datetime(2026, 9, 1, 10, 0, tzinfo=UTC)


class FakeClock:
    """注入的时钟：测试里绝不 `sleep`。"""

    def __init__(self, now: datetime = START) -> None:
        self.now = now

    def __call__(self) -> datetime:
        return self.now

    def advance(self, **kwargs: float) -> None:
        self.now = self.now + timedelta(**kwargs)


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def service(clock: FakeClock):
    svc = impl.LinkedInService(clock=clock)
    for member_id, name in [("alice", "Alice"), ("bob", "Bob"), ("carol", "Carol"),
                            ("dave", "Dave"), ("erin", "Erin")]:
        svc.create_profile(member_id, name, headline=f"{name} @ somewhere")
    return svc


def connect(service, clock, a: str, b: str) -> None:
    request = service.send_request(a, b)
    service.accept_request(request.id, by=b)


def test_the_whole_flow_runs_end_to_end():
    """不借助 fixture 的完整走一遍：档案 → 连接 → 度数 → 技能搜索 → 职位申请。"""
    clock = FakeClock()
    svc = impl.LinkedInService(clock=clock)
    svc.create_profile("alice", "Alice", "工程师")
    svc.create_profile("bob", "Bob", "工程师")
    svc.create_profile("carol", "Carol", "招聘")
    svc.add_skill("alice", "python")
    request = svc.send_request("alice", "bob")
    svc.accept_request(request.id, by="bob")
    assert svc.degrees_of_separation("alice", "bob") == 1
    job = svc.post_job("carol", "Acme", "工程师", required_skills=("python",))
    application = svc.apply("alice", job.id)
    svc.advance_application("carol", application.id, impl.ApplicationStatus.UNDER_REVIEW)
    svc.advance_application("carol", application.id, impl.ApplicationStatus.OFFERED)
    assert svc.applications_of(job.id)[0].status is impl.ApplicationStatus.OFFERED
    assert svc.search_candidates_by_skill("python") == (svc.profile("alice"),)


# --- 第 1 关：档案是结构化的值对象，不是自由格式的 dict ------------------------


def test_experience_is_ordered_by_start_date_not_insertion_order(service, clock):
    service.add_experience("alice", impl.ExperienceEntry(
        "初级工程师", "Acme", datetime(2018, 1, 1, tzinfo=UTC), datetime(2020, 1, 1, tzinfo=UTC)))
    service.add_experience("alice", impl.ExperienceEntry(
        "高级工程师", "Acme", datetime(2020, 1, 1, tzinfo=UTC)))
    titles = [e.title for e in service.profile("alice").experience]
    assert titles == ["高级工程师", "初级工程师"]
    assert service.profile("alice").current_position.title == "高级工程师"


def test_skills_cannot_be_added_twice(service, clock):
    service.add_skill("alice", "python")
    with pytest.raises(impl.DuplicateSkillError):
        service.add_skill("alice", "python")
    assert service.profile("alice").skills == ("python",)


# --- 第 2 关：连接请求与度数（无向图，不是关注） -------------------------------


def test_accepting_a_request_makes_the_connection_mutual(service, clock):
    request = service.send_request("alice", "bob")
    assert request.status is impl.ConnectionStatus.PENDING
    service.accept_request(request.id, by="bob")
    assert service.degrees_of_separation("alice", "bob") == 1
    assert service.degrees_of_separation("bob", "alice") == 1  # 无向：反过来查同样成立


def test_only_the_recipient_can_accept_or_ignore(service, clock):
    request = service.send_request("alice", "bob")
    with pytest.raises(impl.NotRecipientError):
        service.accept_request(request.id, by="alice")
    with pytest.raises(impl.NotRecipientError):
        service.ignore_request(request.id, by="alice")


def test_only_the_sender_can_withdraw(service, clock):
    request = service.send_request("alice", "bob")
    with pytest.raises(impl.NotSenderError):
        service.withdraw_request(request.id, by="bob")
    service.withdraw_request(request.id, by="alice")
    assert service.request(request.id).status is impl.ConnectionStatus.WITHDRAWN


def test_a_processed_request_cannot_be_processed_again(service, clock):
    request = service.send_request("alice", "bob")
    service.ignore_request(request.id, by="bob")
    with pytest.raises(impl.RequestNotPendingError):
        service.accept_request(request.id, by="bob")


def test_duplicate_pending_requests_are_refused_in_either_direction(service, clock):
    service.send_request("alice", "bob")
    with pytest.raises(impl.DuplicateRequestError):
        service.send_request("bob", "alice")


def test_already_connected_members_cannot_request_again(service, clock):
    connect(service, clock, "alice", "bob")
    with pytest.raises(impl.AlreadyConnectedError):
        service.send_request("alice", "bob")


def test_self_connection_is_refused(service, clock):
    with pytest.raises(impl.SelfConnectionError):
        service.send_request("alice", "alice")


def test_degrees_of_separation_up_to_three_then_none(service, clock):
    connect(service, clock, "alice", "bob")
    connect(service, clock, "bob", "carol")
    connect(service, clock, "carol", "dave")
    connect(service, clock, "dave", "erin")
    assert service.degrees_of_separation("alice", "bob") == 1
    assert service.degrees_of_separation("alice", "carol") == 2
    assert service.degrees_of_separation("alice", "dave") == 3
    assert service.degrees_of_separation("alice", "erin") is None  # 第四度：超出 limit


def test_degrees_of_separation_finds_the_shortest_path(service, clock):
    """alice 到 dave 有两条路：经 bob/carol 长度 3，经 erin 长度 2——必须找到更短的那条。"""
    connect(service, clock, "alice", "bob")
    connect(service, clock, "bob", "carol")
    connect(service, clock, "carol", "dave")
    connect(service, clock, "alice", "erin")
    connect(service, clock, "erin", "dave")
    assert service.degrees_of_separation("alice", "dave") == 2


# --- 第 3 关：职位与申请、按技能反查候选人 --------------------------------------


def test_search_candidates_by_skill_uses_the_reverse_index(service, clock):
    service.add_skill("alice", "python")
    service.add_skill("bob", "python")
    service.add_skill("carol", "java")
    found = service.search_candidates_by_skill("python")
    assert {p.id for p in found} == {"alice", "bob"}
    assert service.search_candidates_by_skill("rust") == ()


def test_applying_to_a_closed_job_is_refused(service, clock):
    job = service.post_job("carol", "Acme", "工程师", required_skills=("python",))
    service.close_job("carol", job.id)
    with pytest.raises(impl.JobClosedError):
        service.apply("alice", job.id)


def test_applying_twice_to_the_same_job_is_refused(service, clock):
    job = service.post_job("carol", "Acme", "工程师", required_skills=("python",))
    service.apply("alice", job.id)
    with pytest.raises(impl.DuplicateApplicationError):
        service.apply("alice", job.id)


def test_application_transitions_follow_the_table(service, clock):
    job = service.post_job("carol", "Acme", "工程师", required_skills=("python",))
    application = service.apply("alice", job.id)
    with pytest.raises(impl.InvalidTransitionError):
        service.advance_application("carol", application.id, impl.ApplicationStatus.OFFERED)
    service.advance_application("carol", application.id, impl.ApplicationStatus.UNDER_REVIEW)
    service.advance_application("carol", application.id, impl.ApplicationStatus.OFFERED)
    with pytest.raises(impl.InvalidTransitionError):
        service.advance_application("carol", application.id, impl.ApplicationStatus.REJECTED)


def test_only_the_posting_recruiter_can_advance_an_application(service, clock):
    job = service.post_job("carol", "Acme", "工程师", required_skills=("python",))
    application = service.apply("alice", job.id)
    with pytest.raises(impl.NotRecruiterError):
        service.advance_application("dave", application.id, impl.ApplicationStatus.UNDER_REVIEW)


def test_applicant_can_withdraw_their_own_application(service, clock):
    job = service.post_job("carol", "Acme", "工程师", required_skills=("python",))
    application = service.apply("alice", job.id)
    service.withdraw_application("alice", application.id)
    assert service.applications_of(job.id)[0].status is impl.ApplicationStatus.WITHDRAWN


# --- 第 4 关：背书与推荐——不碰连接图 ------------------------------------------


def test_endorsement_requires_a_connection_and_an_existing_skill(service, clock):
    service.add_skill("alice", "python")
    with pytest.raises(impl.NotConnectedError):
        service.endorse_skill("bob", "alice", "python")
    connect(service, clock, "alice", "bob")
    with pytest.raises(impl.UnknownSkillError):
        service.endorse_skill("bob", "alice", "java")
    service.endorse_skill("bob", "alice", "python")
    assert service.profile("alice").endorsement_count("python") == 1
    with pytest.raises(impl.DuplicateEndorsementError):
        service.endorse_skill("bob", "alice", "python")


def test_recommendation_requires_a_connection(service, clock):
    with pytest.raises(impl.NotConnectedError):
        service.recommend("bob", "alice", "共事两年，非常靠谱。")
    connect(service, clock, "alice", "bob")
    rec = service.recommend("bob", "alice", "共事两年，非常靠谱。")
    assert service.profile("alice").recommendations == (rec,)


# --- 并发：多人同时申请同一个职位，申请记录不重不漏 ----------------------------


def test_concurrent_applications_to_the_same_job_are_all_recorded_once(service, clock):
    """十个候选人同时申请同一个职位，无论线程怎么交错，最终必须恰好十份申请、
    每人一份，`applications_of` 不能漏记也不能重复计入同一个人两次。
    """
    for n in range(10):
        service.create_profile(f"cand{n}", f"Cand{n}", "求职者")
    job = service.post_job("carol", "Acme", "工程师", required_skills=("python",))
    barrier = threading.Barrier(10)
    errors: list[Exception] = []
    lock = threading.Lock()

    def do_apply(candidate_id: str) -> None:
        barrier.wait()
        try:
            service.apply(candidate_id, job.id)
        except Exception as exc:  # pragma: no cover - 失败即测试失败
            with lock:
                errors.append(exc)

    threads = [threading.Thread(target=do_apply, args=(f"cand{n}",)) for n in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    applications = service.applications_of(job.id)
    assert len(applications) == 10
    assert len({a.applicant_id for a in applications}) == 10
