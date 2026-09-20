"""问答社区（Stack Overflow）——问题、回答与文章共享同一套评论与投票机制的参考实现。

五行设计：`Question`、`Answer`、`Article` 都是 `Post` 的子类，评论**长在帖子对象自己身上**
（组合），所以没有任何代码需要一个 `parent_type` 字符串去分派——谁的评论就调用谁的
`add_comment`。声望从不是一个可以被直接改写的字段：每一次投票或采纳都在
`ReputationLedger` 里追加一条不可变事件，声望是这些事件的**折叠**（fold），增量缓存和
从事件日志重新折叠两条算路必须永远相等，测试钉住这一条。评论、投票降级、编辑三种权限
门槛收在一张表里查，不是散落的 `if 声望 > 数字`。加一种帖子类型（文章）只是加一个
`Post` 子类和政策表里一行数据，投票与声望的代码一行不动。
"""

from __future__ import annotations

import itertools
import threading
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Mapping


# --------------------------------------------------------------------------
# 失败路径。

class QAError(Exception):
    """本设计里所有失败路径的公共基类。"""


class UnknownPostError(QAError):
    """这个帖子 id 不存在。"""


class UnknownQuestionError(QAError):
    """这个 id 存在，但不是一个问题（比如传了一个回答 id 进来）。"""


class SelfVoteError(QAError):
    """不能给自己的帖子投票。"""


class DuplicateVoteError(QAError):
    """已经投过同一个方向的票——改票请传另一个方向，撤票请调用 retract。"""


class NoVoteToRetractError(QAError):
    """这个人在这个帖子上没有票可撤。"""


class InsufficientReputationError(QAError):
    """声望没到这项操作要求的门槛。"""


class NotAskerError(QAError):
    """只有提问者本人能采纳或改变采纳的回答。"""


class AnswerMismatchError(QAError):
    """这个回答不属于这个问题，不能被采纳。"""


class QuestionClosedError(QAError):
    """问题已关闭或已删除，不再接受新回答。"""


# --------------------------------------------------------------------------
# 枚举。

class PostKind(Enum):
    """三种独立的发帖类型；只影响声望表怎么查，不影响任何流程代码。"""

    QUESTION = "question"
    ANSWER = "answer"
    ARTICLE = "article"


class QuestionStatus(Enum):
    """问题的三态。关闭与删除是两件不同的事，见 `QAService.delete_question` 的文档。"""

    OPEN = "open"
    CLOSED = "closed"
    DELETED = "deleted"


class VoteDirection(Enum):
    """投票只有两个方向；"没投票"用 `None` 表达，不是第三个枚举成员。"""

    UP = 1
    DOWN = -1


class Privilege(Enum):
    """按声望解锁的三项权限。"""

    COMMENT = "comment"
    VOTE_DOWN = "vote_down"
    EDIT = "edit"


# --------------------------------------------------------------------------
# 值对象：编辑记录与评论。

@dataclass(frozen=True, slots=True)
class EditEntry:
    """一次编辑：谁改的、改之前是什么样、什么时候。"""

    edited_at: datetime
    editor_id: str
    previous_body: str


@dataclass(frozen=True, slots=True)
class Comment:
    """一条评论。`post_id` 只是给读者显示用的回指，存取从不靠它去分派——评论天生就长在
    它所属的那个 `Post` 对象上（见下面 `Post.add_comment`）。
    """

    id: str
    post_id: str
    author_id: str
    body: str
    at: datetime


# --------------------------------------------------------------------------
# Post 层级：Question / Answer / Article 共享身份、正文、编辑历史与评论。

class Post:
    """问题、回答、文章的公共基类：一个可以被评论、被投票、被编辑的帖子。

    评论**没有 `parent_type` 字段**：每个具体帖子对象自己持有一份评论列表（组合），
    调用方已经拿到了那个具体对象（一个 `Question` 或一个 `Answer`），直接调
    `post.add_comment(...)` 就够了，不需要任何代码去问"这是问题还是回答"。
    """

    def __init__(self, post_id: str, author_id: str, body: str, created_at: datetime) -> None:
        self.id = post_id
        self.author_id = author_id
        self.body = body
        self.created_at = created_at
        self._edits: list[EditEntry] = []
        self._comments: list[Comment] = []

    @property
    def kind(self) -> PostKind:
        """具体帖子类型，只用于查声望表——每个子类必须覆盖它。"""
        raise NotImplementedError

    @property
    def is_edited(self) -> bool:
        """这个帖子被编辑过，用于在界面上打一个"已编辑"标记。"""
        return bool(self._edits)

    @property
    def edit_count(self) -> int:
        """被编辑过几次。"""
        return len(self._edits)

    def record_edit(self, editor_id: str, new_body: str, at: datetime) -> None:
        """记一条编辑历史，再把正文换成新的。"""
        self._edits.append(EditEntry(at, editor_id, self.body))
        self.body = new_body

    def add_comment(self, comment: Comment) -> None:
        """挂一条评论到这个帖子上。"""
        self._comments.append(comment)

    @property
    def comments(self) -> tuple[Comment, ...]:
        """这个帖子下面全部评论的快照，内部列表不外借。"""
        return tuple(self._comments)


class Question(Post):
    """一个问题：标题、标签、状态，以及此刻被采纳的那个回答（至多一个）。"""

    def __init__(self, post_id: str, author_id: str, title: str, body: str,
                tags: tuple[str, ...], created_at: datetime) -> None:
        super().__init__(post_id, author_id, body, created_at)
        self.title = title
        self.tags = frozenset(tags)
        self.status = QuestionStatus.OPEN
        self.accepted_answer_id: str | None = None

    @property
    def kind(self) -> PostKind:
        return PostKind.QUESTION


class Answer(Post):
    """一个回答，挂在某个问题下面。`deleted` 由问题被删除时级联置位（见
    `QAService.delete_question`），回答本身没有独立的删除入口。
    """

    def __init__(self, post_id: str, author_id: str, question_id: str, body: str,
                created_at: datetime) -> None:
        super().__init__(post_id, author_id, body, created_at)
        self.question_id = question_id
        self.deleted = False

    @property
    def kind(self) -> PostKind:
        return PostKind.ANSWER


class Article(Post):
    """第 4 关新增的第二种独立发帖类型：不属于任何问题，标题与正文都是自己的。

    它不需要修改 `ReputationLedger`、`cast_vote` 或 `retract_vote` 里的任何一行——那些代码
    只认 `Post.kind` 和 `Post.author_id`，`Article` 继承了两者。真正的"新增"只有两处：这个
    子类本身，和 `ReputationRules.vote_delta` 表里一行 `(ARTICLE, ...)` 的数据。
    """

    def __init__(self, post_id: str, author_id: str, title: str, body: str,
                created_at: datetime) -> None:
        super().__init__(post_id, author_id, body, created_at)
        self.title = title

    @property
    def kind(self) -> PostKind:
        return PostKind.ARTICLE


# --------------------------------------------------------------------------
# 声望规则：一张表，不是散落的 if。

@dataclass(frozen=True, slots=True)
class ReputationRules:
    """投票的声望增减、降票的代价、采纳的奖励、权限门槛——全部是数据，不是分支。

    加一种帖子类型（`Article`）只往 `vote_delta` 里加两行；加一项权限只往
    `privilege_threshold` 里加一行；两处都不碰任何调用这张表的代码。
    """

    vote_delta: Mapping[tuple[PostKind, VoteDirection], int] = field(default_factory=lambda: {
        (PostKind.QUESTION, VoteDirection.UP): 5,
        (PostKind.QUESTION, VoteDirection.DOWN): -2,
        (PostKind.ANSWER, VoteDirection.UP): 10,
        (PostKind.ANSWER, VoteDirection.DOWN): -2,
        (PostKind.ARTICLE, VoteDirection.UP): 5,
        (PostKind.ARTICLE, VoteDirection.DOWN): -2,
    })
    downvote_cost: int = -1
    accept_bonus_answer: int = 15
    accept_bonus_asker: int = 2
    privilege_threshold: Mapping[Privilege, int] = field(default_factory=lambda: {
        Privilege.COMMENT: 50, Privilege.VOTE_DOWN: 125, Privilege.EDIT: 2000,
    })

    def can(self, reputation: int, privilege: Privilege) -> bool:
        """这份声望够不够解锁这项权限。"""
        return reputation >= self.privilege_threshold[privilege]


# --------------------------------------------------------------------------
# 声望账本：事件的折叠，不是一个可写字段。

@dataclass(frozen=True, slots=True)
class VoteEvent:
    """一次投票动作（首投 / 改票 / 撤票）造成的净声望变化。`delta_author` 记给帖子作者，
    `delta_voter` 记给投票人自己（降票要扣自己的分）。"""

    id: str
    post_id: str
    post_author_id: str
    voter_id: str
    direction: VoteDirection | None
    delta_author: int
    delta_voter: int
    at: datetime


@dataclass(frozen=True, slots=True)
class AcceptEvent:
    """一次采纳变更：可能同时影响两个人——被换下的回答作者（扣分）和新采纳的回答作者
    （加分），以及提问者自己（有没有回答被采纳过，只影响一次固定奖励）。"""

    id: str
    question_id: str
    asker_id: str
    delta_asker: int
    previous_author_id: str | None
    delta_previous_author: int
    new_author_id: str | None
    delta_new_author: int
    at: datetime


class ReputationLedger:
    """声望永远是事件日志的折叠（fold），从来不是一个被到处 `+=` 的计数器。

    `_totals` 是这份折叠结果的增量缓存：每追加一条事件，按事件自带的 delta 更新它，
    图的是 O(1) 查询。`recompute` 是完全独立的第二条算路——只读 `_votes` 与 `_accepts`
    两份事件日志，从零把它们重新加一遍。这两条路径算出来的数字必须永远相等：一旦
    `cast_vote` 未来被改出一个只更新其中一处的 bug，`recompute` 的结果会立刻和 `_totals`
    对不上，测试就会失败——这正是"声望不能是一个会漂移的计数器"的证明方式。
    """

    def __init__(self, rules: ReputationRules) -> None:
        self._rules = rules
        self._votes: list[VoteEvent] = []
        self._accepts: list[AcceptEvent] = []
        self._current: dict[tuple[str, str], VoteDirection] = {}
        self._totals: dict[str, int] = {}
        self._ids = (f"E{n}" for n in itertools.count(1))

    def reputation(self, user_id: str) -> int:
        """当前声望：增量缓存的读取。"""
        return self._totals.get(user_id, 0)

    def current_vote(self, voter_id: str, post_id: str) -> VoteDirection | None:
        """这个人在这个帖子上此刻投的是哪个方向，没投过是 `None`。"""
        return self._current.get((voter_id, post_id))

    def cast_vote(self, voter_id: str, post: Post, direction: VoteDirection,
                 at: datetime) -> VoteEvent:
        """投票，或者改票（同一个人对同一个帖子再投一次，换成不同方向）。"""
        key = (voter_id, post.id)
        old = self._current.get(key)
        if old is direction:
            raise DuplicateVoteError(f"{voter_id} already voted {direction.name} on {post.id}")
        old_a, old_v = self._effect(post.kind, old)
        new_a, new_v = self._effect(post.kind, direction)
        event = VoteEvent(next(self._ids), post.id, post.author_id, voter_id, direction,
                          new_a - old_a, new_v - old_v, at)
        self._record(event)
        self._current[key] = direction
        return event

    def retract_vote(self, voter_id: str, post: Post, at: datetime) -> VoteEvent:
        """撤票：把已投的那一票的效果原样减掉。"""
        key = (voter_id, post.id)
        old = self._current.get(key)
        if old is None:
            raise NoVoteToRetractError(f"{voter_id} has no vote on {post.id} to retract")
        old_a, old_v = self._effect(post.kind, old)
        event = VoteEvent(next(self._ids), post.id, post.author_id, voter_id, None,
                          -old_a, -old_v, at)
        self._record(event)
        del self._current[key]
        return event

    def apply_accept(self, question_id: str, asker_id: str, previous: Answer | None,
                     new: Answer | None, at: datetime) -> AcceptEvent:
        """把"这个问题的采纳从 previous 变成 new"记成一条事件；两者之一可以是 `None`。"""
        delta_prev = -self._rules.accept_bonus_answer if previous is not None else 0
        delta_new = self._rules.accept_bonus_answer if new is not None else 0
        asker_before = self._rules.accept_bonus_asker if previous is not None else 0
        asker_after = self._rules.accept_bonus_asker if new is not None else 0
        event = AcceptEvent(next(self._ids), question_id, asker_id, asker_after - asker_before,
                            previous.author_id if previous is not None else None, delta_prev,
                            new.author_id if new is not None else None, delta_new, at)
        if previous is not None:
            self._apply(previous.author_id, delta_prev)
        if new is not None:
            self._apply(new.author_id, delta_new)
        self._apply(asker_id, event.delta_asker)
        self._accepts.append(event)
        return event

    def recompute(self, user_id: str) -> int:
        """独立于 `_totals` 的第二条算路：把两份事件日志为这个人重新折叠一遍。"""
        total = sum(e.delta_author for e in self._votes if e.post_author_id == user_id)
        total += sum(e.delta_voter for e in self._votes if e.voter_id == user_id)
        for e in self._accepts:
            if e.asker_id == user_id:
                total += e.delta_asker
            if e.previous_author_id == user_id:
                total += e.delta_previous_author
            if e.new_author_id == user_id:
                total += e.delta_new_author
        return total

    def _effect(self, kind: PostKind, direction: VoteDirection | None) -> tuple[int, int]:
        """一个投票方向对(帖子作者, 投票人)各自造成多少声望变化；没投过是 (0, 0)。"""
        if direction is None:
            return 0, 0
        delta_author = self._rules.vote_delta[(kind, direction)]
        delta_voter = self._rules.downvote_cost if direction is VoteDirection.DOWN else 0
        return delta_author, delta_voter

    def _record(self, event: VoteEvent) -> None:
        self._apply(event.post_author_id, event.delta_author)
        self._apply(event.voter_id, event.delta_voter)
        self._votes.append(event)

    def _apply(self, user_id: str, delta: int) -> None:
        if delta:
            self._totals[user_id] = self._totals.get(user_id, 0) + delta


# --------------------------------------------------------------------------
# QAService：问答社区的总控。

class QAService:
    """问答社区：发帖、评论、投票、采纳、关闭与删除、按标签检索，以及声望查询。

    锁纪律：一把锁保护帖子索引、标签倒排表与声望账本。这道题的每个复合操作（比如投票
    要先查当前票、再算声望增量、再落账本）本身只有几十次字典操作，拆锁换不到并发度，
    反而会在"改声望"和"改票据"之间开一条竞态窗口。
    """

    def __init__(self, clock, rules: ReputationRules = ReputationRules()) -> None:
        self._clock = clock
        self._rules = rules
        self._posts: dict[str, Post] = {}
        self._answers_of: dict[str, list[str]] = {}
        self._tag_index: dict[str, set[str]] = {}
        self._ledger = ReputationLedger(rules)
        self._lock = threading.Lock()
        self._q_ids = (f"Q{n}" for n in itertools.count(1))
        self._a_ids = (f"A{n}" for n in itertools.count(1))
        self._c_ids = (f"C{n}" for n in itertools.count(1))
        self._t_ids = (f"T{n}" for n in itertools.count(1))

    # ---- 发帖与编辑 --------------------------------------------------------

    def ask_question(self, author_id: str, title: str, body: str,
                     tags: tuple[str, ...] = ()) -> Question:
        """开一个新问题。"""
        now = self._clock()
        with self._lock:
            question = Question(next(self._q_ids), author_id, title, body, tags, now)
            self._posts[question.id] = question
            self._answers_of[question.id] = []
            for tag in question.tags:
                self._tag_index.setdefault(tag, set()).add(question.id)
            return question

    def post_answer(self, author_id: str, question_id: str, body: str) -> Answer:
        """在一个未关闭的问题下面回答。"""
        now = self._clock()
        with self._lock:
            question = self._question_locked(question_id)
            if question.status is not QuestionStatus.OPEN:
                raise QuestionClosedError(f"{question_id} is {question.status.value}")
            answer = Answer(next(self._a_ids), author_id, question_id, body, now)
            self._posts[answer.id] = answer
            self._answers_of[question_id].append(answer.id)
            return answer

    def post_article(self, author_id: str, title: str, body: str) -> Article:
        """发一篇独立文章——不隶属任何问题。"""
        now = self._clock()
        with self._lock:
            article = Article(next(self._t_ids), author_id, title, body, now)
            self._posts[article.id] = article
            return article

    def add_comment(self, author_id: str, post_id: str, body: str) -> Comment:
        """给任意一种帖子（问题、回答或文章）加一条评论，需要够门槛的声望。"""
        now = self._clock()
        with self._lock:
            post = self._post_locked(post_id)
            if not self._rules.can(self._ledger.reputation(author_id), Privilege.COMMENT):
                raise InsufficientReputationError(f"{author_id} needs more reputation to comment")
            comment = Comment(next(self._c_ids), post_id, author_id, body, now)
            post.add_comment(comment)
            return comment

    def edit_post(self, editor_id: str, post_id: str, new_body: str) -> Post:
        """编辑正文：作者本人随时可以，别人需要够门槛的声望。"""
        now = self._clock()
        with self._lock:
            post = self._post_locked(post_id)
            if editor_id != post.author_id and not self._rules.can(
                    self._ledger.reputation(editor_id), Privilege.EDIT):
                raise InsufficientReputationError(f"{editor_id} cannot edit someone else's post")
            post.record_edit(editor_id, new_body, now)
            return post

    # ---- 投票 --------------------------------------------------------------

    def cast_vote(self, voter_id: str, post_id: str, direction: VoteDirection) -> None:
        """投票或改票；自己不能投自己，降票需要够门槛的声望。"""
        now = self._clock()
        with self._lock:
            post = self._post_locked(post_id)
            if voter_id == post.author_id:
                raise SelfVoteError(f"{voter_id} cannot vote on their own post")
            if direction is VoteDirection.DOWN and not self._rules.can(
                    self._ledger.reputation(voter_id), Privilege.VOTE_DOWN):
                raise InsufficientReputationError(f"{voter_id} needs more reputation to downvote")
            self._ledger.cast_vote(voter_id, post, direction, now)

    def retract_vote(self, voter_id: str, post_id: str) -> None:
        """撤票。"""
        now = self._clock()
        with self._lock:
            post = self._post_locked(post_id)
            self._ledger.retract_vote(voter_id, post, now)

    def reputation(self, user_id: str) -> int:
        """这个人此刻的声望。"""
        with self._lock:
            return self._ledger.reputation(user_id)

    def reputation_matches_log(self, user_id: str) -> bool:
        """增量缓存和从事件日志重新折叠的结果是否一致——声望"不会漂移"的可验证证据。"""
        with self._lock:
            return self._ledger.reputation(user_id) == self._ledger.recompute(user_id)

    # ---- 采纳、关闭、删除 ----------------------------------------------------

    def accept_answer(self, asker_id: str, question_id: str, answer_id: str) -> None:
        """采纳一个回答；只有提问者本人能做，同一时刻只有一个，可以改指到另一个回答。"""
        now = self._clock()
        with self._lock:
            question = self._question_locked(question_id)
            if asker_id != question.author_id:
                raise NotAskerError(f"only {question.author_id} can accept an answer")
            answer = self._post_locked(answer_id)
            if not isinstance(answer, Answer) or answer.question_id != question_id:
                raise AnswerMismatchError(f"{answer_id} does not answer {question_id}")
            previous = self._posts.get(question.accepted_answer_id) \
                if question.accepted_answer_id else None
            self._ledger.apply_accept(question_id, asker_id,
                                      previous if isinstance(previous, Answer) else None,
                                      answer, now)
            question.accepted_answer_id = answer_id

    def close_question(self, by: str, question_id: str) -> None:
        """关闭问题：不再接受新回答，但已有的回答、评论、投票都原样保留、原样可见。"""
        with self._lock:
            question = self._question_locked(question_id)
            self._require_owner_or_trusted(by, question)
            question.status = QuestionStatus.CLOSED

    def delete_question(self, by: str, question_id: str) -> None:
        """删除问题：问题本身和它名下每一个回答一起被标记删除（级联），但对象都还在——
        编辑历史与已经发生的声望变化都不会被这次删除抹掉或撤销。"""
        with self._lock:
            question = self._question_locked(question_id)
            self._require_owner_or_trusted(by, question)
            question.status = QuestionStatus.DELETED
            for answer_id in self._answers_of.get(question_id, ()):
                answer = self._posts[answer_id]
                if isinstance(answer, Answer):
                    answer.deleted = True

    # ---- 查询 --------------------------------------------------------------

    def post(self, post_id: str) -> Post:
        """按 id 取任意类型的帖子。"""
        with self._lock:
            return self._post_locked(post_id)

    def question(self, question_id: str) -> Question:
        """按 id 取问题。"""
        with self._lock:
            return self._question_locked(question_id)

    def answers_of(self, question_id: str) -> tuple[Answer, ...]:
        """一个问题下面还没被级联删除的回答，一份快照。"""
        with self._lock:
            self._question_locked(question_id)
            answers = (self._posts[a] for a in self._answers_of.get(question_id, ()))
            return tuple(a for a in answers if isinstance(a, Answer) and not a.deleted)

    def by_tag(self, tag: str) -> tuple[Question, ...]:
        """按标签查问题的倒排索引：直接查表，不扫描全库。"""
        with self._lock:
            ids = self._tag_index.get(tag, set())
            return tuple(sorted((self._posts[i] for i in ids if isinstance(self._posts[i], Question)),
                                key=lambda q: q.id))

    def _post_locked(self, post_id: str) -> Post:
        found = self._posts.get(post_id)
        if found is None:
            raise UnknownPostError(f"unknown post {post_id!r}")
        return found

    def _question_locked(self, question_id: str) -> Question:
        found = self._post_locked(question_id)
        if not isinstance(found, Question):
            raise UnknownQuestionError(f"{question_id!r} is not a question")
        return found

    def _require_owner_or_trusted(self, by: str, question: Question) -> None:
        if by != question.author_id and not self._rules.can(
                self._ledger.reputation(by), Privilege.EDIT):
            raise InsufficientReputationError(f"{by} cannot close or delete this question")


if __name__ == "__main__":
    from datetime import UTC

    now = datetime(2026, 9, 1, 10, 0, tzinfo=UTC)
    qa = QAService(clock=lambda: now)
    q = qa.ask_question("alice", "如何在 Python 里注入时钟？",
                        "我想让测试不依赖 sleep。", tags=("python", "testing"))
    a1 = qa.post_answer("bob", q.id, "把 now 作为一个 Callable 参数传进去。")
    a2 = qa.post_answer("carol", q.id, "用 freezegun 这类库。")

    for voter in ("carol", "dave", "erin"):
        qa.cast_vote(voter, a1.id, VoteDirection.UP)
    qa.cast_vote("bob", q.id, VoteDirection.UP)
    print(f"bob 声望 {qa.reputation('bob')}，日志重算一致：{qa.reputation_matches_log('bob')}")

    qa.accept_answer("alice", q.id, a1.id)
    print(f"采纳 a1 后，bob 声望 {qa.reputation('bob')}，alice 声望 {qa.reputation('alice')}")
    qa.accept_answer("alice", q.id, a2.id)
    print(f"改采纳 a2 后，bob 声望 {qa.reputation('bob')}，carol 声望 {qa.reputation('carol')}")

    qa.close_question("alice", q.id)
    print("标签 python 命中：", [x.title for x in qa.by_tag("python")])
