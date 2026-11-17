"""评论审核服务 ReviewDesk（待修复）。公开 API 与 `solution.py` 一致，放进真实工作区时把 `ServiceError` 换成 `from models import ServiceError`。

这份代码能跑，却会放过违规内容、永远封不了人、审核器坏了照样发布：它就是要你修的东西。产品规则（每一条都有测试）：

1. 输入：`user` 与 `content` 必须是字符串，且去掉空白后非空，否则抛 `ServiceError(400, "invalid_input")`；`user_state` 的参数同样。
   保存与交给审核器的都是原值，首尾空白也不动。
2. 新建返回 `{id, user, content, version: 1}`，id 从 1 开始连续；被拒、被封、审核器出错的写入不占 id；
   `get` 找不到抛 `(404, "review_not_found")`；所有返回值都是独立快照。
3. 审核器返回 `False`：抛 `(422, "content_rejected")`，该用户违规数恰好加一，不保存新内容；被拒的编辑不改内容与版本；
   成功写入不清零；`user_state` 恰好返回 `{strikes, flagged}`。
4. 第三次被拒仍抛 `content_rejected`，随后 `strikes=3`、`flagged=True`；之后该用户每次通过校验的写入都抛 `(403, "user_blocked")`，
   不调用审核器、不加违规数，哪怕内容干净；没有解封。
5. 顺序：`create` 是 输入 → 封禁 → 审核器；`edit` 是 输入 → 存在 → 归属（403 `forbidden`）→ 封禁 → 审核器。
6. 编辑成功：id 与作者不变，版本加一，内容相同也加。
7. 审核器抛 `Exception`：抛 `(503, "checker_unavailable")`，评论、违规数、id 都不变；`BaseException` 不拦截；
   合格的写入恰好调用审核器一次，参数是原内容。
8. 同一实例上的并发调用像一个接一个执行；不同实例、不同用户互不影响。

Python 3.11，只用标准库。
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from typing import Any

BLOCK_AT = 3


class ServiceError(Exception):
    """对外的服务错误：整数 `status` 加稳定的字符串 `code`。"""

    def __init__(self, status: int, code: str) -> None:
        super().__init__(code)
        self.status = status
        self.code = code


def _require_text(value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ServiceError(400, "invalid_input")


class ReviewService:
    def __init__(self, checker: Callable[[str], bool]) -> None:
        self._checker = checker
        self._rows: dict[int, dict[str, Any]] = {}
        self._strikes: dict[str, int] = {}
        self._next_id = 1
        self._lock = threading.RLock()

    def user_state(self, user: str) -> dict:
        # 已经做对：先校验参数；没见过的用户是零次、未封禁
        _require_text(user)
        with self._lock:
            return {"strikes": self._strikes.get(user, 0), "flagged": self._is_flagged(user)}

    def _is_flagged(self, user: str) -> bool:
        # 缺陷：门槛写成 `> BLOCK_AT`，要第四次违规才算封禁，而规则是第三次
        return self._strikes.get(user, 0) > BLOCK_AT

    def get(self, review_id: int) -> dict:
        # 已经做对：找不到抛 404；返回的是副本
        with self._lock:
            if review_id not in self._rows:
                raise ServiceError(404, "review_not_found")
            return dict(self._rows[review_id])

    def create(self, user: str, content: str) -> dict:
        _require_text(user)
        _require_text(content)
        with self._lock:
            self._moderate(user, content)
            # 已经做对：通过审核之后才取 id，失败的写入不占号
            row = {"id": self._next_id, "user": user, "content": content, "version": 1}
            self._next_id += 1
            self._rows[row["id"]] = row
            return dict(row)

    def edit(self, review_id: int, user: str, content: str) -> dict:
        _require_text(user)
        _require_text(content)
        with self._lock:
            # 已经做对：先看评论在不在，再看归属，最后才审核
            row = self.get(review_id)
            if row["user"] != user:
                raise ServiceError(403, "forbidden")
            self._moderate(user, content)
            # 缺陷：内容换了，版本没有加一
            row["content"] = content
            self._rows[review_id] = row
            return dict(row)

    def _verdict(self, content: str) -> bool:
        try:
            # 缺陷：审核器拿到的是改成小写的内容，大小写敏感的审核器会漏掉违规
            return bool(self._checker(content.lower()))
        except Exception:
            # 缺陷：审核器出错被当成"通过"，评论照样发布
            return True

    def _moderate(self, user: str, content: str) -> None:
        if self._is_flagged(user):
            raise ServiceError(403, "user_blocked")
        if not self._verdict(content):
            # 缺陷：违规数被覆盖成 1，而不是在原来的基础上加一，永远到不了封禁线
            self._strikes[user] = 1
            raise ServiceError(422, "content_rejected")
