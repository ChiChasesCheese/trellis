"""可重试的工单服务（Retry-Safe Issue Service）：进程内、按项目隔离、带幂等键与版本号。
设计：`IssueService` 只管两件事——先授权（401 先于 404 先于其他一切），再在同一把锁里执行；
`NewIssue` 把创建请求规范化成一个可比较的值（幂等判断就是比较两个值）；`Board` 是一个项目的全部状态
（按 id 升序的工单、按 id 查找的字典、幂等回执），自己不加锁；`Issue` 是可变记录，对外一律给 `snapshot()` 快照。
所有写操作"先校验、再改状态"：最后一个可能抛错的语句之后才动状态，所以失败不留痕、不消耗 id。
"""

from __future__ import annotations

import threading
from bisect import bisect_right
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import islice
from typing import Any, NamedTuple

STATUSES = frozenset({"open", "closed"})
TITLE_MAX, DESCRIPTION_MAX, KEY_MAX, LIMIT_MAX = 120, 2000, 64, 100


class ServiceError(Exception):
    """对外的错误：status 是 HTTP 状态码，code 是稳定的字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


def _invalid() -> ServiceError:
    return ServiceError(400, "invalid_input")


def _is_int(value: object) -> bool:
    """`True` 是 int 的子类，但不是合法的版本号或游标。"""
    return isinstance(value, int) and not isinstance(value, bool)


@dataclass(frozen=True, slots=True)
class NewIssue:
    """规范化后的创建请求：标题已去首尾空白，描述原样保留，缺省描述就是空串。
    frozen 带来 `==`：幂等键的"同一个请求"就是两个 NewIssue 相等。"""

    title: str
    description: str = ""

    @classmethod
    def parse(cls, payload: object) -> NewIssue:
        if not isinstance(payload, dict) or not payload.keys() <= {"title", "description"}:
            raise _invalid()
        title = payload.get("title")
        description = payload.get("description", "")
        if not isinstance(title, str) or not isinstance(description, str):
            raise _invalid()
        title = title.strip()
        if not 1 <= len(title) <= TITLE_MAX or len(description) > DESCRIPTION_MAX:
            raise _invalid()
        return cls(title, description)


@dataclass(slots=True)
class Issue:
    """一条工单。版本号只在状态真的变了的时候加一。"""

    id: int
    project: str
    creator: str
    title: str
    description: str
    status: str = "open"
    version: int = 1

    def snapshot(self) -> dict[str, Any]:
        """与内部记录脱钩的字典：调用方随便改，不影响存储。"""
        return {"id": self.id, "project": self.project, "creator": self.creator,
                "title": self.title, "description": self.description,
                "status": self.status, "version": self.version}


class Receipt(NamedTuple):
    """幂等回执：当初的规范化请求，和它创建出来的那条工单（引用，所以重放看到的是最新状态）。"""

    request: NewIssue
    issue: Issue


class Board:
    """一个项目的全部状态。不加锁：并发由 `IssueService` 的那把锁负责。"""

    def __init__(self) -> None:
        self._issues: list[Issue] = []  # 按 id 升序：id 全局递增，追加即有序
        self._by_id: dict[int, Issue] = {}
        self._receipts: dict[tuple[str, str], Receipt] = {}  # (用户, 键) → 回执；项目就是这个 Board

    def find(self, issue_id: object) -> Issue:
        issue = self._by_id.get(issue_id) if _is_int(issue_id) else None
        if issue is None:
            raise ServiceError(404, "issue_not_found")
        return issue

    def replay(self, user: str, key: str, request: NewIssue) -> Issue | None:
        """键用过：请求相同就返回原工单，不同就是冲突；键没用过返回 None。"""
        receipt = self._receipts.get((user, key))
        if receipt is None:
            return None
        if receipt.request != request:
            raise ServiceError(409, "idempotency_conflict")
        return receipt.issue

    def add(self, issue: Issue, key: str | None, request: NewIssue) -> None:
        self._issues.append(issue)
        self._by_id[issue.id] = issue
        if key is not None:
            self._receipts[(issue.creator, key)] = Receipt(request, issue)

    def page(self, status: str | None, after_id: int, limit: int) -> list[dict[str, Any]]:
        """二分跳到游标之后，按 id 升序收集，满 limit 条就停。"""
        start = bisect_right(self._issues, after_id, key=lambda issue: issue.id)
        rows: list[dict[str, Any]] = []
        for issue in islice(self._issues, start, None):
            if status is None or issue.status == status:
                rows.append(issue.snapshot())
                if len(rows) == limit:
                    break
        return rows


class IssueService:
    def __init__(self, members: dict[str, Iterable[str]]) -> None:
        # 构造时复制并冻结：之后改传入的集合，不影响授权
        self.members = {project: frozenset(users) for project, users in members.items()}
        self._boards = {project: Board() for project in self.members}
        self._lock = threading.Lock()
        self._next_id = 1

    def _authorize(self, user: object, project: object) -> Board:
        """每个方法的第一步：401 先于 404 先于该方法自己的校验。"""
        if not isinstance(user, str) or not user.strip():
            raise ServiceError(401, "unauthorized")
        if not isinstance(project, str) or user not in self.members.get(project, ()):
            raise ServiceError(404, "project_not_found")
        return self._boards[project]

    def create(self, user: str, project: str, payload: object,
               key: str | None = None) -> tuple[int, dict[str, Any]]:
        board = self._authorize(user, project)
        request = NewIssue.parse(payload)
        if key is not None and not (isinstance(key, str) and 1 <= len(key) <= KEY_MAX):
            raise _invalid()
        with self._lock:
            if key is not None:
                existing = board.replay(user, key, request)
                if existing is not None:
                    return 200, existing.snapshot()
            issue = Issue(self._next_id, project, user, request.title, request.description)
            self._next_id += 1  # 最后一个可能抛错的语句已经过去：只有真的建出来才耗 id
            board.add(issue, key, request)
            return 201, issue.snapshot()

    def get(self, user: str, project: str, issue_id: int) -> dict[str, Any]:
        board = self._authorize(user, project)
        with self._lock:  # 读也要锁：否则可能读到"状态已改、版本未加"的半截
            return board.find(issue_id).snapshot()

    def transition(self, user: str, project: str, issue_id: int,
                   status: str, version: int) -> dict[str, Any]:
        board = self._authorize(user, project)
        with self._lock:  # 比较版本与修改状态必须是同一个临界区
            issue = board.find(issue_id)
            if not isinstance(status, str) or status not in STATUSES or not _is_int(version) or version < 1:
                raise _invalid()
            if version != issue.version:
                raise ServiceError(409, "version_conflict")
            if status != issue.status:
                issue.status = status
                issue.version += 1
            return issue.snapshot()

    def list(self, user: str, project: str, status: str | None = None,
             after_id: int = 0, limit: int = 20) -> list[dict[str, Any]]:
        board = self._authorize(user, project)
        if status is not None and (not isinstance(status, str) or status not in STATUSES):
            raise _invalid()
        if not _is_int(after_id) or after_id < 0 or not _is_int(limit) or not 1 <= limit <= LIMIT_MAX:
            raise _invalid()
        with self._lock:
            return board.page(status, after_id, limit)


if __name__ == "__main__":
    service = IssueService({"demo": ["alice", "bob"]})
    print(service.create("alice", "demo", {"title": " Fix login "}, "retry-1"))
    print(service.create("alice", "demo", {"title": "Fix login"}, "retry-1"))
    print(service.transition("bob", "demo", 1, "closed", 1))
    print(service.list("alice", "demo", status="closed"))
