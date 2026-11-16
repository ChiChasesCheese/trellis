"""关键词与用户拦截（ContentGate）练习骨架。公开 API 与 `solution.py` 一致，把 `BlocklistService`
放进真实工作区的 `service.py`（`ServiceError` 用工作区 `models.py` 里的那个）即可运行公开测试。

产品规则（逐条都有测试）：
 1. 配置（关键词、手动封禁名单）是“有限的字符串可迭代对象”。裸 `str` / `bytes`、任何非字符串条目、
    任何空白条目（`strip()` 之后为空），都抛 `ServiceError(400, "invalid_keywords")` 或 `(400, "invalid_users")`。
 2. 全部条目校验通过后才替换；构造函数走同一条校验路径；校验失败或迭代中抛异常，旧配置完全不变。
    迭代过程中抛出的异常原样传出，不换成 400。输入只遍历一次（一次性迭代器可用），并且先复制成快照。
 3. 关键词规范化是 `strip().casefold()`，然后去重。内容只做 `casefold()`，不做其他 Unicode 规范化。
 4. 匹配是字面子串匹配：不是正则，也不是按词匹配。每个规范化关键词在结果里最多出现一次，
    结果按 Python 字符串顺序排序；重叠的关键词都算命中；空内容合法，什么也匹配不到。
 5. 用户 ID 区分大小写，原样保存（包括两端空白）。`check` 遇到非字符串或空白用户、非字符串内容，
    抛 `ServiceError(400, "invalid_input")`，且发生在任何匹配和记账之前（被封的用户也一样）。
 6. `state(user)` 返回新字典 `{"strikes": int, "blocked": bool}`；没见过的用户是 0 次、未封。
 7. 用户被封 = 在手动名单里，或累计违规 ≥ 3。
 8. 被封用户的 `check` 恰好返回 `{"allowed": False, "reason": "user_blocked", "matches": [], "strikes": 当前次数}`，
    不匹配内容、不加次数，并且优先于关键词拒绝。
 9. 未被封的用户命中任何关键词：返回 `{"allowed": False, "reason": "keyword", "matches": 排序后的命中, "strikes": 原次数 + 1}`。
    一个被拒的请求恰好加一次，不论命中几个词、同一个词出现几次。第三次被拒的 reason 仍是 "keyword"，之后才是 "user_blocked"。
10. 干净请求返回 `{"allowed": True, "reason": None, "matches": [], "strikes": 当前次数}`，不清零次数。
11. `replace_keywords`、`replace_blocked_users` 各自整体替换自己那一份，空的可迭代对象表示清空；
    两者都不清零违规次数，也不解除因违规而被封的用户；从手动名单里移除一个用户，只有在他的次数 < 3 时才真正解封。
12. 状态存在实例里，实例之间互不影响；所有调用和替换都是原子的，并发安全；
    返回的字典和列表都是新的，调用方改它们不影响服务。没有 HTTP、磁盘、定时过期。
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import TypedDict

STRIKE_LIMIT = 3


class ServiceError(Exception):
    """对外的统一错误：status 是 HTTP 状态码，code 是稳定的字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


def _snapshot(values: Iterable[str], code: str) -> list[str]:
    raise NotImplementedError


def _require_user(user: object) -> str:
    raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Keywords:
    words: tuple[str, ...] = ()

    @classmethod
    def compile(cls, raw: Iterable[str]) -> Keywords:
        raise NotImplementedError

    def find(self, content: str) -> list[str]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Verdict:
    allowed: bool
    reason: str | None
    matches: tuple[str, ...]
    strikes: int

    @classmethod
    def clean(cls, strikes: int) -> Verdict:
        raise NotImplementedError

    @classmethod
    def blocked(cls, strikes: int) -> Verdict:
        raise NotImplementedError

    @classmethod
    def keyword(cls, matches: Iterable[str], strikes: int) -> Verdict:
        raise NotImplementedError

    def as_dict(self) -> dict[str, object]:
        raise NotImplementedError


class UserState(TypedDict):
    strikes: int
    blocked: bool


class StrikeLedger:
    def __init__(self, limit: int = STRIKE_LIMIT) -> None:
        raise NotImplementedError

    def count(self, user: str) -> int:
        raise NotImplementedError

    def exhausted(self, user: str) -> bool:
        raise NotImplementedError

    def add(self, user: str) -> int:
        raise NotImplementedError


class BlocklistService:
    def __init__(self, keywords: Iterable[str] = (), blocked_users: Iterable[str] = ()) -> None:
        raise NotImplementedError

    @property
    def keywords(self) -> list[str]:
        raise NotImplementedError

    @property
    def blocked_users(self) -> list[str]:
        raise NotImplementedError

    def replace_keywords(self, keywords: Iterable[str]) -> None:
        raise NotImplementedError

    def replace_blocked_users(self, users: Iterable[str]) -> None:
        raise NotImplementedError

    def state(self, user: str) -> UserState:
        raise NotImplementedError

    def check(self, user: str, content: str) -> dict[str, object]:
        raise NotImplementedError
