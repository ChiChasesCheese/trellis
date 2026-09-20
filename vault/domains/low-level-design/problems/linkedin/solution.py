"""职业社交（LinkedIn）——结构化档案、无向人脉图与有界双向 BFS 度数查询的参考实现。

五行设计：档案的每一栏（工作经历、教育经历、技能）都是**结构化的值对象**，不是
`dict[str, Any]`，因为招聘方要按开始时间排序、按技能反查候选人，自由格式的字典没有
任何一方能校验或查询。人脉连接是**无向图**——`ConnectionGraph` 里一条边同时出现在
两个人的邻接集合里，这和"关注"那种允许单向存在的有向关系是两种不同的东西，绝不共用
一套模型。度数查询是一次**有界双向 BFS**：从两端同时展开、交替扩大较小的一侧，命中
即停，且封顶在三度——超过三度在这道题里不需要精确数字。候选人按技能搜索靠一张**反向
索引**（技能到成员 id 的集合），维护成本摊在"加技能"这个低频操作上，换来搜索的 O(1)
直接命中。背书（endorsement）作为可选的第四关加在最后，一行都没有碰连接图或投票——
它只是调用了连接图已经公开的只读查询。
"""

from __future__ import annotations

import itertools
import threading
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


# --------------------------------------------------------------------------
# 失败路径。

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
    """两人已经是一度人脉，不需要再发请求。"""


class DuplicateRequestError(LinkedInError):
    """两人之间已经有一条待处理的请求（不分方向）。"""


class RequestNotPendingError(LinkedInError):
    """这条请求已经被处理过，不能再次接受/忽略/撤回。"""


class NotRecipientError(LinkedInError):
    """只有请求的接收方能接受或忽略它。"""


class NotSenderError(LinkedInError):
    """只有请求的发起方能撤回它。"""


class DuplicateSkillError(LinkedInError):
    """这项技能已经在档案里了。"""


class UnknownSkillError(LinkedInError):
    """档案上没有这项技能，不能背书。"""


class DuplicateEndorsementError(LinkedInError):
    """这个人已经为这项技能背书过一次。"""


class NotConnectedError(LinkedInError):
    """背书和推荐都要求双方已经是一度人脉。"""


class JobClosedError(LinkedInError):
    """职位已关闭，不再接受新申请。"""


class DuplicateApplicationError(LinkedInError):
    """这位候选人已经申请过这个职位。"""


class InvalidTransitionError(LinkedInError):
    """申请状态不允许这样转移。"""


class NotRecruiterError(LinkedInError):
    """只有发布职位的招聘方能操作它的申请或关闭它。"""


# --------------------------------------------------------------------------
# 枚举。

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


# 申请状态机：一张转移表，而不是散落在各处的 `if 当前状态 == X`。
APPLICATION_TRANSITIONS: dict[ApplicationStatus, frozenset[ApplicationStatus]] = {
    ApplicationStatus.SUBMITTED: frozenset(
        {ApplicationStatus.UNDER_REVIEW, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN}),
    ApplicationStatus.UNDER_REVIEW: frozenset(
        {ApplicationStatus.OFFERED, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN}),
    ApplicationStatus.OFFERED: frozenset(),
    ApplicationStatus.REJECTED: frozenset(),
    ApplicationStatus.WITHDRAWN: frozenset(),
}


# --------------------------------------------------------------------------
# 档案的三栏：结构化的值对象，不是自由格式的字典。

@dataclass(frozen=True, slots=True)
class ExperienceEntry:
    """一段工作经历。`end_date` 为 `None` 表示"至今在职"，不是另外一个布尔字段。"""

    title: str
    company: str
    start_date: datetime
    end_date: datetime | None = None
    description: str = ""

    @property
    def is_current(self) -> bool:
        """这段经历还在继续。"""
        return self.end_date is None


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
    """一份职业档案：结构化的工作经历、教育经历、技能，以及技能收到的背书。

    不变量：`_skills` 里的技能名唯一；`_endorsements` 的键必须是 `_skills` 的子集；
    经历按开始时间排序是查询时算出来的，不是插入顺序碰巧对。
    """

    def __init__(self, member_id: str, name: str, headline: str, created_at: datetime) -> None:
        self.id = member_id
        self.name = name
        self.headline = headline
        self.created_at = created_at
        self._experience: list[ExperienceEntry] = []
        self._education: list[EducationEntry] = []
        self._skills: list[str] = []
        self._endorsements: dict[str, set[str]] = {}
        self._recommendations: list[Recommendation] = []

    def add_experience(self, entry: ExperienceEntry) -> None:
        """加一段工作经历。"""
        self._experience.append(entry)

    @property
    def experience(self) -> tuple[ExperienceEntry, ...]:
        """按开始时间倒序排列——档案的"结构化"直接换来这条查询，`dict` 换不来。"""
        return tuple(sorted(self._experience, key=lambda e: e.start_date, reverse=True))

    @property
    def current_position(self) -> ExperienceEntry | None:
        """还在做的那一份工作（如果有）。"""
        return next((e for e in self._experience if e.is_current), None)

    def add_education(self, entry: EducationEntry) -> None:
        """加一段教育经历。"""
        self._education.append(entry)

    @property
    def education(self) -> tuple[EducationEntry, ...]:
        """按开始时间倒序排列。"""
        return tuple(sorted(self._education, key=lambda e: e.start_date, reverse=True))

    def add_skill(self, skill: str) -> None:
        """加一项技能，不能重复。"""
        if skill in self._skills:
            raise DuplicateSkillError(f"{self.id} already lists {skill!r}")
        self._skills.append(skill)

    @property
    def skills(self) -> tuple[str, ...]:
        """技能列表，按添加顺序。"""
        return tuple(self._skills)

    def endorse(self, skill: str, endorser_id: str) -> None:
        """给这项技能加一次背书；同一个人对同一项技能只能背书一次。"""
        if skill not in self._skills:
            raise UnknownSkillError(f"{self.id} does not list {skill!r}")
        endorsers = self._endorsements.setdefault(skill, set())
        if endorser_id in endorsers:
            raise DuplicateEndorsementError(f"{endorser_id} already endorsed {skill!r}")
        endorsers.add(endorser_id)

    def endorsement_count(self, skill: str) -> int:
        """这项技能收到过多少次背书。"""
        return len(self._endorsements.get(skill, ()))

    def add_recommendation(self, recommendation: Recommendation) -> None:
        """加一封推荐信。"""
        self._recommendations.append(recommendation)

    @property
    def recommendations(self) -> tuple[Recommendation, ...]:
        """收到过的推荐信快照。"""
        return tuple(self._recommendations)


# --------------------------------------------------------------------------
# 人脉：连接请求（有向的生命周期）收敛成一条无向边。

@dataclass(slots=True)
class ConnectionRequest:
    """一次连接请求：谁发给谁、什么状态。状态机单向：PENDING 只能转到其余三态之一。"""

    id: str
    from_id: str
    to_id: str
    status: ConnectionStatus
    sent_at: datetime
    responded_at: datetime | None = None


class ConnectionGraph:
    """一度人脉的无向图：一条边同时出现在两个人的邻接集合里。

    这**不是**关注（follow）图——关注允许 A 关注 B 而 B 不关注 A，这里不允许：接受
    请求的那一刻，两人互为对方的一度人脉，不存在只有一边看得到的连接。
    """

    def __init__(self) -> None:
        self._edges: dict[str, set[str]] = {}

    def connect(self, a: str, b: str) -> None:
        """建一条无向边——两个方向的邻接集合同时更新，缺一不可。"""
        self._edges.setdefault(a, set()).add(b)
        self._edges.setdefault(b, set()).add(a)

    def are_connected(self, a: str, b: str) -> bool:
        """两人是否互为一度人脉。"""
        return b in self._edges.get(a, ())

    def connections_of(self, member_id: str) -> frozenset[str]:
        """这个人的全部一度人脉，一份快照。"""
        return frozenset(self._edges.get(member_id, ()))

    @property
    def edge_count(self) -> int:
        """图里有多少条边（每条边只算一次）。"""
        return sum(len(neighbors) for neighbors in self._edges.values()) // 2

    def degrees_of_separation(self, source_id: str, target_id: str, limit: int = 3) -> int | None:
        """有界双向 BFS：从两端同时展开，交替扩大较小的一侧，命中即停。

        单向 BFS 到深度 `d` 要探索 O(b**d) 个节点（`b` 是平均连接数）；从两端各探索到
        `d/2` 再在中间相遇，是 O(b**(d/2))——底数不变、指数减半，是指数级的节省。
        超过 `limit` 度一律返回 `None`，因为这道题只需要精确的 1/2/3 度，"更远"这个
        事实比"远多少"更重要，继续展开到相遇是纯粹的浪费。
        """
        if source_id == target_id:
            raise LinkedInError("degrees of separation is undefined for the same member")
        if target_id in self._edges.get(source_id, ()):
            return 1
        dist_a: dict[str, int] = {source_id: 0}
        dist_b: dict[str, int] = {target_id: 0}
        frontier_a, frontier_b = {source_id}, {target_id}
        depth = 0
        while depth < limit and frontier_a and frontier_b:
            if len(frontier_a) > len(frontier_b):
                frontier_a, frontier_b = frontier_b, frontier_a
                dist_a, dist_b = dist_b, dist_a
            depth += 1
            grown: set[str] = set()
            for member_id in frontier_a:
                for neighbor in self._edges.get(member_id, ()):
                    if neighbor in dist_a:
                        continue
                    dist_a[neighbor] = dist_a[member_id] + 1
                    if neighbor in dist_b:
                        total = dist_a[neighbor] + dist_b[neighbor]
                        if total <= limit:
                            return total
                    grown.add(neighbor)
            frontier_a = grown
        return None


# --------------------------------------------------------------------------
# 职位与申请：各自的生命周期。

@dataclass(slots=True)
class JobPosting:
    """一个职位：公司、标题、要求的技能集合、状态。"""

    id: str
    recruiter_id: str
    company: str
    title: str
    required_skills: frozenset[str]
    posted_at: datetime
    status: JobStatus = JobStatus.OPEN


@dataclass(slots=True)
class Application:
    """一次申请：候选人、职位、状态，按 `APPLICATION_TRANSITIONS` 单向推进。"""

    id: str
    job_id: str
    applicant_id: str
    status: ApplicationStatus
    submitted_at: datetime
    decided_at: datetime | None = None


# --------------------------------------------------------------------------
# LinkedInService：总控。

class LinkedInService:
    """职业社交总控：档案、连接请求、职位与申请、按技能反查候选人、背书与推荐。

    锁纪律：一把锁保护档案索引、连接图、请求台账、技能反向索引与申请表。这道题的复合
    操作（比如接受请求要同时改请求状态、连接图和"是否还有待处理请求"的索引）本身很短，
    拆锁换不到并发度。
    """

    def __init__(self, clock) -> None:
        self._clock = clock
        self._profiles: dict[str, Profile] = {}
        self._connections = ConnectionGraph()
        self._requests: dict[str, ConnectionRequest] = {}
        self._pending_key: dict[frozenset[str], str] = {}
        self._skill_index: dict[str, set[str]] = {}
        self._jobs: dict[str, JobPosting] = {}
        self._applications: dict[str, Application] = {}
        self._applications_of: dict[str, list[str]] = {}
        self._lock = threading.Lock()
        self._req_ids = (f"R{n}" for n in itertools.count(1))
        self._job_ids = (f"J{n}" for n in itertools.count(1))
        self._app_ids = (f"P{n}" for n in itertools.count(1))
        self._rec_ids = (f"C{n}" for n in itertools.count(1))

    # ---- 档案 --------------------------------------------------------------

    def create_profile(self, member_id: str, name: str, headline: str) -> Profile:
        """开一份档案。"""
        now = self._clock()
        with self._lock:
            profile = Profile(member_id, name, headline, now)
            self._profiles[member_id] = profile
            return profile

    def add_experience(self, member_id: str, entry: ExperienceEntry) -> None:
        """加一段工作经历。"""
        with self._lock:
            self._profile_locked(member_id).add_experience(entry)

    def add_education(self, member_id: str, entry: EducationEntry) -> None:
        """加一段教育经历。"""
        with self._lock:
            self._profile_locked(member_id).add_education(entry)

    def add_skill(self, member_id: str, skill: str) -> None:
        """加一项技能，并同步维护"技能 → 候选人"反向索引。"""
        with self._lock:
            self._profile_locked(member_id).add_skill(skill)
            self._skill_index.setdefault(skill, set()).add(member_id)

    def search_candidates_by_skill(self, skill: str) -> tuple[Profile, ...]:
        """按技能查候选人：直接查反向索引，不扫描全部档案。"""
        with self._lock:
            ids = self._skill_index.get(skill, set())
            return tuple(sorted((self._profiles[i] for i in ids), key=lambda p: p.id))

    # ---- 连接请求 ----------------------------------------------------------

    def send_request(self, from_id: str, to_id: str) -> ConnectionRequest:
        """发一条连接请求；已经是一度人脉、或者已有一条待处理请求都会被拒绝。"""
        now = self._clock()
        with self._lock:
            self._profile_locked(from_id)
            self._profile_locked(to_id)
            if from_id == to_id:
                raise SelfConnectionError("cannot connect to yourself")
            if self._connections.are_connected(from_id, to_id):
                raise AlreadyConnectedError(f"{from_id} and {to_id} are already connected")
            key = frozenset((from_id, to_id))
            if key in self._pending_key:
                raise DuplicateRequestError(f"a pending request already exists between {key}")
            request = ConnectionRequest(next(self._req_ids), from_id, to_id,
                                        ConnectionStatus.PENDING, now)
            self._requests[request.id] = request
            self._pending_key[key] = request.id
            return request

    def accept_request(self, request_id: str, by: str) -> None:
        """接受请求：只有接收方能做，接受之后双方互为一度人脉。"""
        now = self._clock()
        with self._lock:
            request = self._resolve_pending(request_id, expected=by, field="to_id",
                                             error=NotRecipientError)
            self._connections.connect(request.from_id, request.to_id)
            request.status, request.responded_at = ConnectionStatus.ACCEPTED, now

    def ignore_request(self, request_id: str, by: str) -> None:
        """忽略请求：只有接收方能做。"""
        now = self._clock()
        with self._lock:
            request = self._resolve_pending(request_id, expected=by, field="to_id",
                                             error=NotRecipientError)
            request.status, request.responded_at = ConnectionStatus.IGNORED, now

    def withdraw_request(self, request_id: str, by: str) -> None:
        """撤回请求：只有发起方能做。"""
        now = self._clock()
        with self._lock:
            request = self._resolve_pending(request_id, expected=by, field="from_id",
                                             error=NotSenderError)
            request.status, request.responded_at = ConnectionStatus.WITHDRAWN, now

    def degrees_of_separation(self, source_id: str, target_id: str) -> int | None:
        """两人之间的度数：1/2/3，或者 `None`（超过三度或不连通）。"""
        with self._lock:
            self._profile_locked(source_id)
            self._profile_locked(target_id)
            return self._connections.degrees_of_separation(source_id, target_id)

    # ---- 职位与申请 --------------------------------------------------------

    def post_job(self, recruiter_id: str, company: str, title: str,
                required_skills: tuple[str, ...]) -> JobPosting:
        """发一个职位。"""
        now = self._clock()
        with self._lock:
            job = JobPosting(next(self._job_ids), recruiter_id, company, title,
                             frozenset(required_skills), now)
            self._jobs[job.id] = job
            self._applications_of[job.id] = []
            return job

    def close_job(self, recruiter_id: str, job_id: str) -> None:
        """关闭职位：不再接受新申请，已有申请不受影响。"""
        with self._lock:
            job = self._job_locked(job_id, recruiter_id)
            job.status = JobStatus.CLOSED

    def apply(self, applicant_id: str, job_id: str) -> Application:
        """申请一个职位；职位已关闭、或者已经申请过都会被拒绝。"""
        now = self._clock()
        with self._lock:
            self._profile_locked(applicant_id)
            job = self._job_locked_readonly(job_id)
            if job.status is not JobStatus.OPEN:
                raise JobClosedError(f"{job_id} is closed")
            existing = [a for a in self._applications_of[job_id]
                       if self._applications[a].applicant_id == applicant_id]
            if existing:
                raise DuplicateApplicationError(f"{applicant_id} already applied to {job_id}")
            application = Application(next(self._app_ids), job_id, applicant_id,
                                      ApplicationStatus.SUBMITTED, now)
            self._applications[application.id] = application
            self._applications_of[job_id].append(application.id)
            return application

    def advance_application(self, recruiter_id: str, application_id: str,
                            new_status: ApplicationStatus) -> Application:
        """把申请推进到一个新状态，必须是 `APPLICATION_TRANSITIONS` 里允许的那几个之一。"""
        now = self._clock()
        with self._lock:
            application = self._application_locked(application_id)
            self._job_locked(application.job_id, recruiter_id)
            self._transition(application, new_status, now)
            return application

    def withdraw_application(self, applicant_id: str, application_id: str) -> Application:
        """候选人主动撤回申请。"""
        now = self._clock()
        with self._lock:
            application = self._application_locked(application_id)
            if application.applicant_id != applicant_id:
                raise NotRecruiterError(f"{applicant_id} did not submit {application_id}")
            self._transition(application, ApplicationStatus.WITHDRAWN, now)
            return application

    def applications_of(self, job_id: str) -> tuple[Application, ...]:
        """一个职位收到的全部申请，一份快照。"""
        with self._lock:
            self._job_locked_readonly(job_id)
            return tuple(self._applications[a] for a in self._applications_of[job_id])

    # ---- 背书与推荐：第 4 关，不碰连接图的任何一行 ---------------------------

    def endorse_skill(self, endorser_id: str, subject_id: str, skill: str) -> None:
        """给一度人脉的某项技能背书。只读地调用 `ConnectionGraph.are_connected`。"""
        with self._lock:
            if not self._connections.are_connected(endorser_id, subject_id):
                raise NotConnectedError(f"{endorser_id} and {subject_id} are not connected")
            self._profile_locked(subject_id).endorse(skill, endorser_id)

    def recommend(self, author_id: str, subject_id: str, body: str) -> Recommendation:
        """给一度人脉写一封推荐信。"""
        now = self._clock()
        with self._lock:
            if not self._connections.are_connected(author_id, subject_id):
                raise NotConnectedError(f"{author_id} and {subject_id} are not connected")
            recommendation = Recommendation(next(self._rec_ids), author_id, subject_id, body, now)
            self._profile_locked(subject_id).add_recommendation(recommendation)
            return recommendation

    # ---- 查询与内部辅助 ------------------------------------------------------

    def profile(self, member_id: str) -> Profile:
        """按 id 取档案。"""
        with self._lock:
            return self._profile_locked(member_id)

    def request(self, request_id: str) -> ConnectionRequest:
        """按 id 取连接请求。"""
        with self._lock:
            return self._request_locked(request_id)

    def _profile_locked(self, member_id: str) -> Profile:
        found = self._profiles.get(member_id)
        if found is None:
            raise UnknownMemberError(f"unknown member {member_id!r}")
        return found

    def _request_locked(self, request_id: str) -> ConnectionRequest:
        found = self._requests.get(request_id)
        if found is None:
            raise UnknownRequestError(f"unknown request {request_id!r}")
        return found

    def _resolve_pending(self, request_id: str, *, expected: str, field: str,
                         error: type[LinkedInError]) -> ConnectionRequest:
        request = self._request_locked(request_id)
        if request.status is not ConnectionStatus.PENDING:
            raise RequestNotPendingError(f"{request_id} is already {request.status.value}")
        if getattr(request, field) != expected:
            raise error(f"{expected} is not the {field} of {request_id}")
        self._pending_key.pop(frozenset((request.from_id, request.to_id)), None)
        return request

    def _job_locked_readonly(self, job_id: str) -> JobPosting:
        found = self._jobs.get(job_id)
        if found is None:
            raise UnknownJobError(f"unknown job {job_id!r}")
        return found

    def _job_locked(self, job_id: str, recruiter_id: str) -> JobPosting:
        job = self._job_locked_readonly(job_id)
        if job.recruiter_id != recruiter_id:
            raise NotRecruiterError(f"{recruiter_id} did not post {job_id}")
        return job

    def _application_locked(self, application_id: str) -> Application:
        found = self._applications.get(application_id)
        if found is None:
            raise UnknownApplicationError(f"unknown application {application_id!r}")
        return found

    def _transition(self, application: Application, new_status: ApplicationStatus,
                    now: datetime) -> None:
        allowed = APPLICATION_TRANSITIONS[application.status]
        if new_status not in allowed:
            raise InvalidTransitionError(
                f"cannot move {application.id} from {application.status.value} to {new_status.value}")
        application.status, application.decided_at = new_status, now


if __name__ == "__main__":
    from datetime import UTC

    now = datetime(2026, 9, 1, 10, 0, tzinfo=UTC)
    service = LinkedInService(clock=lambda: now)
    for member_id, name in [("alice", "Alice"), ("bob", "Bob"), ("carol", "Carol"),
                            ("dave", "Dave")]:
        service.create_profile(member_id, name, headline=f"{name} @ somewhere")
    service.add_experience("alice", ExperienceEntry("工程师", "Acme", datetime(2020, 1, 1, tzinfo=UTC)))
    service.add_skill("alice", "python")
    service.add_skill("bob", "python")

    for a, b in [("alice", "bob"), ("bob", "carol"), ("carol", "dave")]:
        req = service.send_request(a, b)
        service.accept_request(req.id, by=b)
    print("alice-dave 度数:", service.degrees_of_separation("alice", "dave"))
    print("按 python 搜索候选人:", [p.id for p in service.search_candidates_by_skill("python")])

    service.endorse_skill("bob", "alice", "python")
    print("alice 的 python 背书数:", service.profile("alice").endorsement_count("python"))

    job = service.post_job("carol", "Acme", "Python 工程师", required_skills=("python",))
    application = service.apply("alice", job.id)
    service.advance_application("carol", application.id, ApplicationStatus.UNDER_REVIEW)
    service.advance_application("carol", application.id, ApplicationStatus.OFFERED)
    print("申请状态:", service.applications_of(job.id)[0].status.value)
