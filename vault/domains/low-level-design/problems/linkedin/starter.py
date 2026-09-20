"""职业社交（LinkedIn）——起始模板。

公开的类名、方法签名、`Enum`、`dataclass` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/linkedin -q
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class LinkedInError(Exception):
    """本设计里所有失败路径的公共基类。"""


class UnknownMemberError(LinkedInError):
    """这个成员 id 没有档案。"""


class UnknownRequestError(LinkedInError):
    """这个连接请求 id 不存在。"""


class UnknownJobError(LinkedInError):
    """这个职位 id 不存在。"""


class UnknownApplicationError(LinkedInError):
    """这个申请 id 不存在。"""


class SelfConnectionError(LinkedInError):
    """不能给自己发连接请求。"""


class AlreadyConnectedError(LinkedInError):
    """两人已经是一度人脉。"""


class DuplicateRequestError(LinkedInError):
    """两人之间已经有一条待处理的请求。"""


class RequestNotPendingError(LinkedInError):
    """这条请求已经被处理过。"""


class NotRecipientError(LinkedInError):
    """只有请求的接收方能接受或忽略它。"""


class NotSenderError(LinkedInError):
    """只有请求的发起方能撤回它。"""


class DuplicateSkillError(LinkedInError):
    """这项技能已经在档案里了。"""


class UnknownSkillError(LinkedInError):
    """档案上没有这项技能。"""


class DuplicateEndorsementError(LinkedInError):
    """这个人已经为这项技能背书过一次。"""


class NotConnectedError(LinkedInError):
    """背书和推荐都要求双方已经是一度人脉。"""


class JobClosedError(LinkedInError):
    """职位已关闭。"""


class DuplicateApplicationError(LinkedInError):
    """这位候选人已经申请过这个职位。"""


class InvalidTransitionError(LinkedInError):
    """申请状态不允许这样转移。"""


class NotRecruiterError(LinkedInError):
    """只有发布职位的招聘方能操作它的申请或关闭它。"""


class ConnectionStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    IGNORED = "ignored"
    WITHDRAWN = "withdrawn"


class JobStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"


class ApplicationStatus(Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    OFFERED = "offered"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


APPLICATION_TRANSITIONS: dict[ApplicationStatus, frozenset[ApplicationStatus]] = {
    ApplicationStatus.SUBMITTED: frozenset(
        {ApplicationStatus.UNDER_REVIEW, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN}),
    ApplicationStatus.UNDER_REVIEW: frozenset(
        {ApplicationStatus.OFFERED, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN}),
    ApplicationStatus.OFFERED: frozenset(),
    ApplicationStatus.REJECTED: frozenset(),
    ApplicationStatus.WITHDRAWN: frozenset(),
}


@dataclass(frozen=True, slots=True)
class ExperienceEntry:
    """一段工作经历。`end_date` 为 `None` 表示"至今在职"。"""

    title: str
    company: str
    start_date: datetime
    end_date: datetime | None = None
    description: str = ""

    @property
    def is_current(self) -> bool:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class EducationEntry:
    """一段教育经历。"""

    school: str
    degree: str
    field: str
    start_date: datetime
    end_date: datetime | None = None


@dataclass(frozen=True, slots=True)
class Recommendation:
    """一份来自一度人脉的推荐信。"""

    id: str
    author_id: str
    subject_id: str
    body: str
    at: datetime


class Profile:
    """一份职业档案：结构化的工作经历、教育经历、技能，以及技能收到的背书。"""

    def __init__(self, member_id: str, name: str, headline: str, created_at: datetime) -> None:
        raise NotImplementedError

    def add_experience(self, entry: ExperienceEntry) -> None:
        """加一段工作经历。"""
        raise NotImplementedError

    @property
    def experience(self) -> tuple[ExperienceEntry, ...]:
        """按开始时间倒序排列。"""
        raise NotImplementedError

    @property
    def current_position(self) -> ExperienceEntry | None:
        """还在做的那一份工作（如果有）。"""
        raise NotImplementedError

    def add_education(self, entry: EducationEntry) -> None:
        """加一段教育经历。"""
        raise NotImplementedError

    @property
    def education(self) -> tuple[EducationEntry, ...]:
        """按开始时间倒序排列。"""
        raise NotImplementedError

    def add_skill(self, skill: str) -> None:
        """加一项技能，不能重复。"""
        raise NotImplementedError

    @property
    def skills(self) -> tuple[str, ...]:
        """技能列表。"""
        raise NotImplementedError

    def endorse(self, skill: str, endorser_id: str) -> None:
        """给这项技能加一次背书。"""
        raise NotImplementedError

    def endorsement_count(self, skill: str) -> int:
        """这项技能收到过多少次背书。"""
        raise NotImplementedError

    def add_recommendation(self, recommendation: Recommendation) -> None:
        """加一封推荐信。"""
        raise NotImplementedError

    @property
    def recommendations(self) -> tuple[Recommendation, ...]:
        """收到过的推荐信快照。"""
        raise NotImplementedError


@dataclass(slots=True)
class ConnectionRequest:
    """一次连接请求：谁发给谁、什么状态。"""

    id: str
    from_id: str
    to_id: str
    status: ConnectionStatus
    sent_at: datetime
    responded_at: datetime | None = None


class ConnectionGraph:
    """一度人脉的无向图。"""

    def __init__(self) -> None:
        raise NotImplementedError

    def connect(self, a: str, b: str) -> None:
        """建一条无向边。"""
        raise NotImplementedError

    def are_connected(self, a: str, b: str) -> bool:
        """两人是否互为一度人脉。"""
        raise NotImplementedError

    def connections_of(self, member_id: str) -> frozenset[str]:
        """这个人的全部一度人脉。"""
        raise NotImplementedError

    @property
    def edge_count(self) -> int:
        """图里有多少条边。"""
        raise NotImplementedError

    def degrees_of_separation(self, source_id: str, target_id: str, limit: int = 3) -> int | None:
        """有界双向 BFS：1/2/3 度，或者 `None`。"""
        raise NotImplementedError


@dataclass(slots=True)
class JobPosting:
    """一个职位。"""

    id: str
    recruiter_id: str
    company: str
    title: str
    required_skills: frozenset[str]
    posted_at: datetime
    status: JobStatus = JobStatus.OPEN


@dataclass(slots=True)
class Application:
    """一次申请。"""

    id: str
    job_id: str
    applicant_id: str
    status: ApplicationStatus
    submitted_at: datetime
    decided_at: datetime | None = None


class LinkedInService:
    """职业社交总控：档案、连接请求、职位与申请、按技能反查候选人、背书与推荐。"""

    def __init__(self, clock) -> None:
        raise NotImplementedError

    def create_profile(self, member_id: str, name: str, headline: str) -> Profile:
        """开一份档案。"""
        raise NotImplementedError

    def add_experience(self, member_id: str, entry: ExperienceEntry) -> None:
        """加一段工作经历。"""
        raise NotImplementedError

    def add_education(self, member_id: str, entry: EducationEntry) -> None:
        """加一段教育经历。"""
        raise NotImplementedError

    def add_skill(self, member_id: str, skill: str) -> None:
        """加一项技能，并同步维护反向索引。"""
        raise NotImplementedError

    def search_candidates_by_skill(self, skill: str) -> tuple[Profile, ...]:
        """按技能查候选人。"""
        raise NotImplementedError

    def send_request(self, from_id: str, to_id: str) -> ConnectionRequest:
        """发一条连接请求。"""
        raise NotImplementedError

    def accept_request(self, request_id: str, by: str) -> None:
        """接受请求。"""
        raise NotImplementedError

    def ignore_request(self, request_id: str, by: str) -> None:
        """忽略请求。"""
        raise NotImplementedError

    def withdraw_request(self, request_id: str, by: str) -> None:
        """撤回请求。"""
        raise NotImplementedError

    def degrees_of_separation(self, source_id: str, target_id: str) -> int | None:
        """两人之间的度数。"""
        raise NotImplementedError

    def post_job(self, recruiter_id: str, company: str, title: str,
                required_skills: tuple[str, ...]) -> JobPosting:
        """发一个职位。"""
        raise NotImplementedError

    def close_job(self, recruiter_id: str, job_id: str) -> None:
        """关闭职位。"""
        raise NotImplementedError

    def apply(self, applicant_id: str, job_id: str) -> Application:
        """申请一个职位。"""
        raise NotImplementedError

    def advance_application(self, recruiter_id: str, application_id: str,
                            new_status: ApplicationStatus) -> Application:
        """把申请推进到一个新状态。"""
        raise NotImplementedError

    def withdraw_application(self, applicant_id: str, application_id: str) -> Application:
        """候选人主动撤回申请。"""
        raise NotImplementedError

    def applications_of(self, job_id: str) -> tuple[Application, ...]:
        """一个职位收到的全部申请。"""
        raise NotImplementedError

    def endorse_skill(self, endorser_id: str, subject_id: str, skill: str) -> None:
        """给一度人脉的某项技能背书。"""
        raise NotImplementedError

    def recommend(self, author_id: str, subject_id: str, body: str) -> Recommendation:
        """给一度人脉写一封推荐信。"""
        raise NotImplementedError

    def profile(self, member_id: str) -> Profile:
        """按 id 取档案。"""
        raise NotImplementedError

    def request(self, request_id: str) -> ConnectionRequest:
        """按 id 取连接请求。"""
        raise NotImplementedError
