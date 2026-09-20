"""问答社区的测试：分关覆盖发帖/评论、投票与声望、采纳/关闭/删除、文章扩展与并发。"""

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
def qa(clock: FakeClock):
    return impl.QAService(clock=clock)


def high_rep_qa(clock: FakeClock, users: tuple[str, ...]):
    """造一个每个给定用户声望都够用（>=2000）的社区：让很多人给他们的一篇文章点赞。"""
    service = impl.QAService(clock=clock)
    for user in users:
        article = service.post_article(user, "seed", "seed body")
        for n in range(220):
            service.cast_vote(f"voter{user}{n}", article.id, impl.VoteDirection.UP)
    return service


# --- 第 1 关：问题、回答、评论（无 parent_type）、文章检索 -----------------------


def test_the_whole_flow_runs_end_to_end():
    """不借助 fixture 的完整走一遍：提问 → 回答 → 投票涨声望 → 采纳 → 改采纳 → 关闭。"""
    clock = FakeClock()
    service = impl.QAService(clock=clock)
    question = service.ask_question("alice", "如何注入时钟？", "测试不想 sleep。", tags=("python",))
    a1 = service.post_answer("bob", question.id, "把 now 当参数传进去。")
    a2 = service.post_answer("carol", question.id, "用可注入的 Clock 协议。")
    service.cast_vote("dave", a1.id, impl.VoteDirection.UP)
    assert service.reputation("bob") == 10
    service.accept_answer("alice", question.id, a1.id)
    assert (service.reputation("bob"), service.reputation("alice")) == (25, 2)
    service.accept_answer("alice", question.id, a2.id)
    assert (service.reputation("bob"), service.reputation("carol")) == (10, 15)
    service.close_question("alice", question.id)
    assert service.question(question.id).status is impl.QuestionStatus.CLOSED
    assert service.reputation_matches_log("bob") and service.reputation_matches_log("carol")


def test_ask_and_answer_basic_flow(qa, clock):
    question = qa.ask_question("alice", "如何注入时钟？", "测试不想 sleep。", tags=("python",))
    answer = qa.post_answer("bob", question.id, "把 now 当参数传进去。")
    assert answer.question_id == question.id
    assert qa.answers_of(question.id) == (answer,)
    assert qa.question(question.id).status is impl.QuestionStatus.OPEN


def test_comment_attaches_to_question_and_answer_without_a_parent_type_field(qa, clock):
    service = high_rep_qa(clock, ("carol",))
    question = service.ask_question("alice", "标题", "正文")
    answer = service.post_answer("bob", question.id, "回答正文")
    c1 = service.add_comment("carol", question.id, "问题下面的评论")
    c2 = service.add_comment("carol", answer.id, "回答下面的评论")
    assert service.post(question.id).comments == (c1,)
    assert service.post(answer.id).comments == (c2,)
    assert not hasattr(c1, "parent_type")


def test_posting_answer_to_closed_question_is_refused(qa, clock):
    question = qa.ask_question("alice", "标题", "正文")
    qa.close_question("alice", question.id)
    with pytest.raises(impl.QuestionClosedError):
        qa.post_answer("bob", question.id, "太晚了")


def test_by_tag_is_an_index_not_a_scan_result(qa, clock):
    q1 = qa.ask_question("alice", "python 问题", "正文", tags=("python", "testing"))
    qa.ask_question("bob", "java 问题", "正文", tags=("java",))
    assert qa.by_tag("python") == (q1,)
    assert qa.by_tag("nonexistent") == ()


# --- 第 2 关：投票与声望（一张表，事件日志，不漂移） --------------------------


def test_upvote_changes_reputation_by_the_table_amount(qa, clock):
    question = qa.ask_question("alice", "标题", "正文")
    answer = qa.post_answer("bob", question.id, "回答")
    qa.cast_vote("carol", question.id, impl.VoteDirection.UP)
    qa.cast_vote("dave", answer.id, impl.VoteDirection.UP)
    assert qa.reputation("alice") == 5
    assert qa.reputation("bob") == 10


def test_self_vote_is_refused(qa, clock):
    question = qa.ask_question("alice", "标题", "正文")
    with pytest.raises(impl.SelfVoteError):
        qa.cast_vote("alice", question.id, impl.VoteDirection.UP)


def test_voting_the_same_direction_twice_is_refused(qa, clock):
    question = qa.ask_question("alice", "标题", "正文")
    qa.cast_vote("bob", question.id, impl.VoteDirection.UP)
    with pytest.raises(impl.DuplicateVoteError):
        qa.cast_vote("bob", question.id, impl.VoteDirection.UP)


def test_changing_a_vote_applies_only_the_net_difference(qa, clock):
    service = high_rep_qa(clock, ("bob",))
    question = service.ask_question("alice", "标题", "正文")
    service.cast_vote("bob", question.id, impl.VoteDirection.UP)
    assert service.reputation("alice") == 5
    service.cast_vote("bob", question.id, impl.VoteDirection.DOWN)
    assert service.reputation("alice") == -2
    assert service.reputation_matches_log("bob")  # 这次改票没有弄乱 bob 自己的声望账目


def test_retracting_a_vote_reverts_its_effect(qa, clock):
    question = qa.ask_question("alice", "标题", "正文")
    qa.cast_vote("bob", question.id, impl.VoteDirection.UP)
    assert qa.reputation("alice") == 5
    qa.retract_vote("bob", question.id)
    assert qa.reputation("alice") == 0
    with pytest.raises(impl.NoVoteToRetractError):
        qa.retract_vote("bob", question.id)


def test_downvoting_requires_reputation_and_costs_the_voter(qa, clock):
    question = qa.ask_question("alice", "标题", "正文")
    with pytest.raises(impl.InsufficientReputationError):
        qa.cast_vote("bob", question.id, impl.VoteDirection.DOWN)
    service = high_rep_qa(clock, ("bob",))
    question = service.ask_question("alice", "标题", "正文")
    service.cast_vote("bob", question.id, impl.VoteDirection.DOWN)
    assert service.reputation("alice") == -2
    assert service.reputation("bob") == 220 * 5 - 1  # 种子文章的 220 个赞，减去这次降票的代价


def test_commenting_requires_reputation(qa, clock):
    question = qa.ask_question("alice", "标题", "正文")
    with pytest.raises(impl.InsufficientReputationError):
        qa.add_comment("bob", question.id, "路过")
    service = high_rep_qa(clock, ("bob",))
    question = service.ask_question("alice", "标题", "正文")
    service.add_comment("bob", question.id, "现在够格了")
    assert len(service.post(question.id).comments) == 1


def test_reputation_never_drifts_from_its_event_log(qa, clock):
    """随机做一串投票/改票/撤票/采纳，增量缓存必须始终等于对事件日志的重新折叠。"""
    question = qa.ask_question("alice", "标题", "正文")
    answer = qa.post_answer("bob", question.id, "回答")
    ops = [("up", "u1"), ("down_setup", None), ("down", "u1"), ("retract", "u1"),
          ("up", "u2"), ("up", "u1"), ("down_setup", None), ("down", "u2")]
    for kind, voter in ops:
        if kind == "down_setup":
            continue
        target = question.id if voter == "u1" else answer.id
        if kind == "up":
            try:
                qa.cast_vote(voter, target, impl.VoteDirection.UP)
            except impl.DuplicateVoteError:
                pass
        elif kind == "down":
            try:
                qa.cast_vote(f"trusted-{voter}", target, impl.VoteDirection.DOWN)
            except (impl.InsufficientReputationError, impl.DuplicateVoteError):
                pass
        elif kind == "retract":
            try:
                qa.retract_vote(voter, target)
            except impl.NoVoteToRetractError:
                pass
        for user in ("alice", "bob", "u1", "u2"):
            assert qa.reputation_matches_log(user)


# --- 第 3 关：采纳、关闭、删除、编辑历史 --------------------------------------


def test_only_the_asker_can_accept_an_answer(qa, clock):
    question = qa.ask_question("alice", "标题", "正文")
    answer = qa.post_answer("bob", question.id, "回答")
    with pytest.raises(impl.NotAskerError):
        qa.accept_answer("bob", question.id, answer.id)
    qa.accept_answer("alice", question.id, answer.id)
    assert qa.question(question.id).accepted_answer_id == answer.id


def test_accepted_answer_can_be_moved_and_rebalances_reputation(qa, clock):
    question = qa.ask_question("alice", "标题", "正文")
    a1 = qa.post_answer("bob", question.id, "回答一")
    a2 = qa.post_answer("carol", question.id, "回答二")
    qa.accept_answer("alice", question.id, a1.id)
    assert qa.reputation("bob") == 15 and qa.reputation("alice") == 2
    qa.accept_answer("alice", question.id, a2.id)
    assert qa.question(question.id).accepted_answer_id == a2.id
    assert qa.reputation("bob") == 0
    assert qa.reputation("carol") == 15
    assert qa.reputation("alice") == 2  # 提问者的固定奖励不因改指而翻倍
    assert qa.reputation_matches_log("bob") and qa.reputation_matches_log("carol")


def test_accepting_an_answer_from_another_question_is_refused(qa, clock):
    q1 = qa.ask_question("alice", "标题一", "正文")
    q2 = qa.ask_question("dave", "标题二", "正文")
    other_answer = qa.post_answer("bob", q2.id, "答的是另一题")
    with pytest.raises(impl.AnswerMismatchError):
        qa.accept_answer("alice", q1.id, other_answer.id)


def test_closing_a_question_keeps_its_answers_but_blocks_new_ones(qa, clock):
    question = qa.ask_question("alice", "标题", "正文")
    answer = qa.post_answer("bob", question.id, "回答")
    qa.close_question("alice", question.id)
    assert qa.answers_of(question.id) == (answer,)
    assert qa.question(question.id).status is impl.QuestionStatus.CLOSED
    with pytest.raises(impl.QuestionClosedError):
        qa.post_answer("carol", question.id, "太晚了")


def test_deleting_a_question_cascades_to_its_answers(qa, clock):
    question = qa.ask_question("alice", "标题", "正文")
    answer = qa.post_answer("bob", question.id, "回答")
    qa.delete_question("alice", question.id)
    assert qa.question(question.id).status is impl.QuestionStatus.DELETED
    assert qa.answers_of(question.id) == ()
    assert qa.post(answer.id).deleted is True


def test_editing_records_history_and_marks_the_post_edited(qa, clock):
    question = qa.ask_question("alice", "标题", "原始正文")
    assert not question.is_edited
    clock.advance(hours=1)
    qa.edit_post("alice", question.id, "修订后的正文")
    updated = qa.question(question.id)
    assert updated.is_edited and updated.edit_count == 1
    assert updated.body == "修订后的正文"


def test_editing_someone_elses_post_needs_reputation(qa, clock):
    question = qa.ask_question("alice", "标题", "正文")
    with pytest.raises(impl.InsufficientReputationError):
        qa.edit_post("bob", question.id, "越权改")


# --- 第 4 关：文章——不碰投票代码的第二种发帖类型 -----------------------------


def test_articles_reuse_voting_and_comments_untouched(qa, clock):
    article = qa.post_article("alice", "一篇文章", "文章正文")
    qa.cast_vote("bob", article.id, impl.VoteDirection.UP)
    assert qa.reputation("alice") == 5  # 沿用问题同档的声望规则，`cast_vote` 没有为文章特判
    with pytest.raises(impl.InsufficientReputationError):
        qa.add_comment("carol", article.id, "声望不够")
    service = high_rep_qa(clock, ("carol",))
    article = service.post_article("alice", "另一篇", "正文")
    comment = service.add_comment("carol", article.id, "现在够格了")
    assert service.post(article.id).comments == (comment,)


# --- 并发：多人同时投票，声望不漂移，票不重不漏 ------------------------------


def test_concurrent_votes_on_the_same_post_leave_reputation_consistent(qa, clock):
    """二十个人同时给同一个回答投票（一半赞成一半反对），无论线程怎么交错，最终声望都
    必须等于"有效票的净效果"——而且增量缓存必须和从事件日志重新折叠的结果一致。
    """
    service = high_rep_qa(clock, tuple(f"down{n}" for n in range(10)))
    question = service.ask_question("alice", "标题", "正文")
    answer = service.post_answer("bob", question.id, "回答")
    voters = [(f"up{n}", impl.VoteDirection.UP) for n in range(10)] + \
        [(f"down{n}", impl.VoteDirection.DOWN) for n in range(10)]
    barrier = threading.Barrier(len(voters))
    errors: list[Exception] = []
    lock = threading.Lock()

    def vote(voter_id: str, direction) -> None:
        barrier.wait()
        try:
            service.cast_vote(voter_id, answer.id, direction)
        except Exception as exc:  # pragma: no cover - 失败即测试失败
            with lock:
                errors.append(exc)

    threads = [threading.Thread(target=vote, args=(v, d)) for v, d in voters]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    expected = 10 * 10 + 10 * -2  # 十个赞成各 +10，十个反对各 -2
    assert service.reputation("bob") == expected
    assert service.reputation_matches_log("bob")
    for n in range(10):
        assert service.reputation_matches_log(f"down{n}")
