"""可重试的工单服务练习骨架。公开 API 与 `solution.py` 一致，可以原样放进真实工作区的 `service.py`
（真实工作区里 `ServiceError` 在 `models.py`，其余相同）。

产品规则（逐条都有测试）：
 1. 授权先于一切：`user` 缺失、不是字符串或全是空白 → `ServiceError(401, "unauthorized")`；
    项目不存在或该用户不是成员 → `(404, "project_not_found")`。四个方法都先授权，再做自己的校验。
 2. 成员表在构造时复制：之后改传入的字典或集合，不影响授权。项目成员可以互相读写对方的工单。
 3. `create(user, project, payload, key=None)`：`payload` 必须是字典，只允许 `title`（必填）和 `description`（可选）；
    `title` 是字符串、去首尾空白后长度 1..120，存的是去空白后的标题；`description` 缺省为 `""`、是字符串、
    至多 2000 个字符、原样保留；`key` 是 `None` 或长度 1..64 的字符串（空白也算内容）。违反 → `(400, "invalid_input")`。
 4. 创建成功返回 `(201, {id, project, creator, title, description, status: "open", version: 1})`；
    id 从 1 开始、整个实例里全局递增；创建失败和幂等重放都不消耗 id；没有 `key` 时每次成功请求都新建一条。
 5. 幂等的范围是 `(user, project, key)`。同一范围内再次用这个键：去空白的标题相同、描述相同（缺省等于空串）
    → `(200, 工单当前的样子)`，即使工单之后改过状态；内容不同 → `(409, "idempotency_conflict")`；
    不同用户或不同项目可以各自独立地用同一个键。
 6. 并发：同一范围内同时发来的相同创建，恰好一个得到 201、只存一条，其余都得到 200。
 7. `get(user, project, issue_id)` 返回独立快照；id 不存在，或属于别的项目 → `(404, "issue_not_found")`。
 8. `transition(user, project, issue_id, status, version)`：先授权、再查工单（404），然后校验 `status ∈ {"open","closed"}`
    和 `version` 是正整数且不是 bool（违反 → 400），最后比较版本。成功时直接返回更新后的工单字典，不是元组。
 9. 版本必须等于当前版本，连"状态没变"的请求也是（否则 `(409, "version_conflict")`）；状态真的变了，版本加一；
    状态没变，版本不变；`open→closed` 与 `closed→open` 都允许；同一版本上的并发写，状态只能被改一次。
10. `list(user, project, status=None, after_id=0, limit=20)`：`status` 是 `None`/`"open"`/`"closed"`，`after_id` 是非负的非 bool 整数，
    `limit` 是 1..100 的非 bool 整数，否则 400；返回本项目里 id 严格大于 `after_id` 且状态匹配的工单，按 id 升序，再截断到 `limit` 条。
11. 所有输入与返回值都互相隔离（改返回的字典不影响存储，改传入的字典不影响已存的工单）；
    失败的操作不留任何痕迹；所有方法在同一个实例上并发调用是安全的。
12. HTTP 适配器（`app.py`，已写好）把 `ServiceError` 翻成 `{"error": code}` 加对应状态码，把 `transition`/`get` 的成功翻成 200。
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


class ServiceError(Exception):
    """对外的错误：status 是 HTTP 状态码，code 是稳定的字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


class IssueService:
    def __init__(self, members: dict[str, Iterable[str]]) -> None:
        self.members = {name: set(people) for name, people in members.items()}

    def create(self, user: str, project: str, payload: object,
               key: str | None = None) -> tuple[int, dict[str, Any]]:
        raise NotImplementedError("Implement authorized, retry-safe creation")

    def get(self, user: str, project: str, issue_id: int) -> dict[str, Any]:
        raise NotImplementedError("Implement issue lookup")

    def transition(self, user: str, project: str, issue_id: int,
                   status: str, version: int) -> dict[str, Any]:
        raise NotImplementedError("Implement versioned lifecycle transitions")

    def list(self, user: str, project: str, status: str | None = None,
             after_id: int = 0, limit: int = 20) -> list[dict[str, Any]]:
        raise NotImplementedError("Implement filtered cursor pagination")
