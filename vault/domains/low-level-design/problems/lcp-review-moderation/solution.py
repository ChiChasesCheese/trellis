"""评论审核服务（ReviewDesk）修复版：评论的创建、编辑与读取都要先过一个外部审核器，累计三次被拒的用户永久封禁。

产品规则（编号即测试编号，每一条都有测试）：

1. 输入：`user` 与 `content` 必须是字符串，且去掉空白后非空（空白按 `str.strip` 的口径，含 U+001C 到 U+001F）；
   否则抛 `ServiceError(400, "invalid_input")`。`user_state` 的参数同样处理。保存与交给审核器的都是原值，首尾空白也不动。
2. 新建：成功返回 `{id, user, content, version: 1}`，id 从 1 开始连续递增；被拒、被封、审核器出错的写入都不占 id。
   `get` 找不到评论抛 `(404, "review_not_found")`。`get`、`user_state` 与写入的返回值都是独立快照，改它们不影响服务。
3. 审核器返回 `False`：抛 `(422, "content_rejected")`，该用户的违规数恰好加一，不保存任何新内容；被拒的编辑不改内容与版本；
   成功的写入永远不清零违规数。`user_state` 恰好返回 `{strikes, flagged}`，没见过的用户是 `0` 与 `False`。
4. 封禁：第三次被拒的那一次仍然抛 `content_rejected`，结果是 `strikes=3`、`flagged=True`；之后该用户每一次通过校验的写入都抛
   `(403, "user_blocked")`，哪怕内容干净，也不调用审核器、不加违规数。没有解封操作；状态与实例同寿。
5. 校验顺序：`create` 是 输入 → 封禁 → 审核器；`edit` 是 输入 → 评论存在（404）→ 归属（403 `forbidden`）→ 封禁 → 审核器。
6. 编辑成功：id 与作者不变，内容换成新的，版本加一；内容与原来相同也加一。
7. 审核器抛 `Exception`：抛 `(503, "checker_unavailable")`，评论、违规数、id 都不变，也不算违规；`BaseException` 不拦截。
   每一次合格的写入恰好调用审核器一次，参数就是原内容。
8. 并发：同一实例上的调用像一个接一个执行；第三次拒绝记下之后，该用户的其他写入到不了审核器，所以并发的被拒写入恰好产生
   三个 `content_rejected` 与三次审核器调用。不同实例、不同用户互不影响。

设计五句话：
1. 一个 `RLock` 罩住每一次写入，审核器在锁里被调用：规则 8 的"第三次之后到不了审核器"只有"查封禁、问审核器、记违规"不被打断才成立。
2. 违规数只存在 `StrikeBook` 里，`flagged` 永远从计数算出（`>= 3`），没有第二份状态可以和计数对不上。
3. 评论是冻结的 `Review`；编辑造一个新的再换进字典，所以被拒或出错的编辑根本没有碰过旧值。
4. 所有检查都在写入之前，id 在审核通过之后才取：失败路径没有任何需要回滚的东西。
5. 对外只交 `snapshot()` 新建的字典，内部对象不出门。
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from dataclasses import dataclass, replace
from typing import Any

BLOCK_AT = 3  # 累计被拒到这个次数，用户永久封禁


# ---- errors:begin（真实工作区里 ServiceError 在 models.py，放进去时换成 `from models import ServiceError`）----
class ServiceError(Exception):
    """对外的服务错误：整数 `status` 加稳定的字符串 `code`。"""

    def __init__(self, status: int, code: str) -> None:
        super().__init__(code)
        self.status = status
        self.code = code


# ---- errors:end ----


def _require_text(value: object) -> None:
    """必须是字符串且去空白后非空；`strip` 只用来判空，不改值。"""
    if not isinstance(value, str) or not value.strip():
        raise ServiceError(400, "invalid_input")


@dataclass(frozen=True, slots=True)
class Review:
    """一条已发布的评论。冻结：编辑是造新值再替换，旧值从不被改写。"""

    id: int
    user: str
    content: str
    version: int = 1

    def edited(self, content: str) -> Review:
        return replace(self, content=content, version=self.version + 1)

    def snapshot(self) -> dict[str, Any]:
        return {"id": self.id, "user": self.user, "content": self.content, "version": self.version}


class StrikeBook:
    """每个用户一个永久的违规计数。是否封禁由计数现算，不另存标志位。"""

    def __init__(self) -> None:
        self._count: dict[str, int] = {}

    def add(self, user: str) -> int:
        self._count[user] = self._count.get(user, 0) + 1
        return self._count[user]

    def is_blocked(self, user: str) -> bool:
        return self._count.get(user, 0) >= BLOCK_AT

    def state(self, user: str) -> dict[str, Any]:
        return {"strikes": self._count.get(user, 0), "flagged": self.is_blocked(user)}


class ReviewService:
    """评论服务：状态是评论字典、违规本、下一个 id；一把可重入锁保护全部写入。"""

    def __init__(self, checker: Callable[[str], bool]) -> None:
        self._checker = checker
        self._reviews: dict[int, Review] = {}
        self._strikes = StrikeBook()
        self._next_id = 1
        # 审核器在锁里运行；可重入，是为了让审核器回头读本服务（get、user_state）时不把自己锁死
        self._lock = threading.RLock()

    def user_state(self, user: str) -> dict:
        _require_text(user)
        with self._lock:
            return self._strikes.state(user)

    def get(self, review_id: int) -> dict:
        with self._lock:
            return self._find(review_id).snapshot()

    def create(self, user: str, content: str) -> dict:
        _require_text(user)
        _require_text(content)
        with self._lock:
            self._moderate(user, content)
            review = Review(self._next_id, user, content)  # 通过审核之后才取 id
            self._reviews[review.id] = review
            self._next_id += 1
            return review.snapshot()

    def edit(self, review_id: int, user: str, content: str) -> dict:
        _require_text(user)
        _require_text(content)
        with self._lock:
            current = self._find(review_id)
            if current.user != user:
                raise ServiceError(403, "forbidden")
            self._moderate(user, content)
            updated = current.edited(content)
            self._reviews[review_id] = updated
            return updated.snapshot()

    def _find(self, review_id: int) -> Review:
        review = self._reviews.get(review_id)
        if review is None:
            raise ServiceError(404, "review_not_found")
        return review

    def _moderate(self, user: str, content: str) -> None:
        """封禁检查 → 问审核器 → 被拒就记一次违规。调用者必须已经持锁。"""
        if self._strikes.is_blocked(user):
            raise ServiceError(403, "user_blocked")
        try:
            allowed = self._checker(content)
        except Exception as exc:  # 审核器坏了不等于内容违规：不记违规，也不放行
            raise ServiceError(503, "checker_unavailable") from exc
        if not allowed:
            self._strikes.add(user)
            raise ServiceError(422, "content_rejected")


if __name__ == "__main__":
    desk = ReviewService(lambda text: "scam" not in text)
    first = desk.create("mira", "Solid battery life")
    print(desk.edit(first["id"], "mira", "Solid battery, loud fan"))
    for _ in range(BLOCK_AT):
        try:
            desk.create("mira", "total scam")
        except ServiceError as error:
            print(error.status, error.code, desk.user_state("mira"))
    try:
        desk.create("mira", "perfectly fine")
    except ServiceError as error:
        print(error.status, error.code)
