"""问答社区（Stack Overflow）——起始模板。

公开的类名、方法签名、`Enum`、`dataclass` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/stack-overflow -q
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Mapping


class QAError(Exception):
    """本设计里所有失败路径的公共基类。"""


class UnknownPostError(QAError):
    """这个帖子 id 不存在。"""


class UnknownQuestionError(QAError):
    """这个 id 存在，但不是一个问题。"""


class SelfVoteError(QAError):
    """不能给自己的帖子投票。"""


class DuplicateVoteError(QAError):
    """已经投过同一个方向的票。"""


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


class PostKind(Enum):
    QUESTION = "question"
    ANSWER = "answer"
    ARTICLE = "article"


class QuestionStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    DELETED = "deleted"


class VoteDirection(Enum):
    UP = 1
    DOWN = -1


class Privilege(Enum):
    COMMENT = "comment"
    VOTE_DOWN = "vote_down"
    EDIT = "edit"


@dataclass(frozen=True, slots=True)
class EditEntry:
    """一次编辑：谁改的、改之前是什么样、什么时候。"""

    edited_at: datetime
    editor_id: str
    previous_body: str


@dataclass(frozen=True, slots=True)
class Comment:
    """一条评论，挂在它所属的那个 `Post` 对象上，没有 `parent_type` 字段。"""

    id: str
    post_id: str
    author_id: str
    body: str
    at: datetime


class Post:
    """问题、回答、文章的公共基类。"""

    def __init__(self, post_id: str, author_id: str, body: str, created_at: datetime) -> None:
        raise NotImplementedError

    @property
    def kind(self) -> PostKind:
        """具体帖子类型，只用于查声望表。"""
        raise NotImplementedError

    @property
    def is_edited(self) -> bool:
        """这个帖子被编辑过。"""
        raise NotImplementedError

    @property
    def edit_count(self) -> int:
        """被编辑过几次。"""
        raise NotImplementedError

    def record_edit(self, editor_id: str, new_body: str, at: datetime) -> None:
        """记一条编辑历史，再把正文换成新的。"""
        raise NotImplementedError

    def add_comment(self, comment: Comment) -> None:
        """挂一条评论到这个帖子上。"""
        raise NotImplementedError

    @property
    def comments(self) -> tuple[Comment, ...]:
        """这个帖子下面全部评论的快照。"""
        raise NotImplementedError


class Question(Post):
    """一个问题：标题、标签、状态，以及此刻被采纳的回答。"""

    def __init__(self, post_id: str, author_id: str, title: str, body: str,
                tags: tuple[str, ...], created_at: datetime) -> None:
        raise NotImplementedError

    @property
    def kind(self) -> PostKind:
        raise NotImplementedError


class Answer(Post):
    """一个回答，挂在某个问题下面。"""

    def __init__(self, post_id: str, author_id: str, question_id: str, body: str,
                created_at: datetime) -> None:
        raise NotImplementedError

    @property
    def kind(self) -> PostKind:
        raise NotImplementedError


class Article(Post):
    """第 4 关新增的第二种独立发帖类型。"""

    def __init__(self, post_id: str, author_id: str, title: str, body: str,
                created_at: datetime) -> None:
        raise NotImplementedError

    @property
    def kind(self) -> PostKind:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class ReputationRules:
    """投票的声望增减、降票的代价、采纳的奖励、权限门槛。"""

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
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class VoteEvent:
    """一次投票动作造成的净声望变化。"""

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
    """一次采纳变更。"""

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
    """声望永远是事件日志的折叠，不是一个可以直接改写的字段。"""

    def __init__(self, rules: ReputationRules) -> None:
        raise NotImplementedError

    def reputation(self, user_id: str) -> int:
        """当前声望。"""
        raise NotImplementedError

    def current_vote(self, voter_id: str, post_id: str) -> VoteDirection | None:
        """这个人在这个帖子上此刻投的是哪个方向。"""
        raise NotImplementedError

    def cast_vote(self, voter_id: str, post: Post, direction: VoteDirection,
                 at: datetime) -> VoteEvent:
        """投票或改票。"""
        raise NotImplementedError

    def retract_vote(self, voter_id: str, post: Post, at: datetime) -> VoteEvent:
        """撤票。"""
        raise NotImplementedError

    def apply_accept(self, question_id: str, asker_id: str, previous: Answer | None,
                     new: Answer | None, at: datetime) -> AcceptEvent:
        """把一次采纳变更记成一条事件。"""
        raise NotImplementedError

    def recompute(self, user_id: str) -> int:
        """独立于增量缓存的第二条算路：重新折叠事件日志。"""
        raise NotImplementedError


class QAService:
    """问答社区：发帖、评论、投票、采纳、关闭与删除、按标签检索，以及声望查询。"""

    def __init__(self, clock, rules: ReputationRules = ReputationRules()) -> None:
        raise NotImplementedError

    def ask_question(self, author_id: str, title: str, body: str,
                     tags: tuple[str, ...] = ()) -> Question:
        """开一个新问题。"""
        raise NotImplementedError

    def post_answer(self, author_id: str, question_id: str, body: str) -> Answer:
        """在一个未关闭的问题下面回答。"""
        raise NotImplementedError

    def post_article(self, author_id: str, title: str, body: str) -> Article:
        """发一篇独立文章。"""
        raise NotImplementedError

    def add_comment(self, author_id: str, post_id: str, body: str) -> Comment:
        """给任意一种帖子加一条评论。"""
        raise NotImplementedError

    def edit_post(self, editor_id: str, post_id: str, new_body: str) -> Post:
        """编辑正文。"""
        raise NotImplementedError

    def cast_vote(self, voter_id: str, post_id: str, direction: VoteDirection) -> None:
        """投票或改票。"""
        raise NotImplementedError

    def retract_vote(self, voter_id: str, post_id: str) -> None:
        """撤票。"""
        raise NotImplementedError

    def reputation(self, user_id: str) -> int:
        """这个人此刻的声望。"""
        raise NotImplementedError

    def reputation_matches_log(self, user_id: str) -> bool:
        """增量缓存和从事件日志重新折叠的结果是否一致。"""
        raise NotImplementedError

    def accept_answer(self, asker_id: str, question_id: str, answer_id: str) -> None:
        """采纳一个回答。"""
        raise NotImplementedError

    def close_question(self, by: str, question_id: str) -> None:
        """关闭问题。"""
        raise NotImplementedError

    def delete_question(self, by: str, question_id: str) -> None:
        """删除问题，级联删除它名下的回答。"""
        raise NotImplementedError

    def post(self, post_id: str) -> Post:
        """按 id 取任意类型的帖子。"""
        raise NotImplementedError

    def question(self, question_id: str) -> Question:
        """按 id 取问题。"""
        raise NotImplementedError

    def answers_of(self, question_id: str) -> tuple[Answer, ...]:
        """一个问题下面还没被级联删除的回答。"""
        raise NotImplementedError

    def by_tag(self, tag: str) -> tuple[Question, ...]:
        """按标签查问题的倒排索引。"""
        raise NotImplementedError
