"""关键词与用户拦截（ContentGate）参考解：一个放在讨论区发帖入口前面的准入组件。

设计五句话：
1. 配置先在锁外读成列表并整体校验，通过后在锁内一次换上；中途失败，旧配置一个字节都不变。
2. 关键词在换配置时就规范化、去重、排好序（`Keywords`），判定时只剩一次 `casefold` 加子串查找。
3. 违规次数由 `StrikeLedger` 保管：只记出过违规的用户，到上限（3）就不再增加。
4. 一次 `check` 的“是否被封、匹配、记一次违规”整体放在同一把锁里，所以并发下严格等价于某个串行顺序。
5. 返回值每次新建（`Verdict.as_dict`、`state`），外部改它不影响服务；时间过期、HTTP、磁盘都不在范围内。
"""

from __future__ import annotations

import threading
from collections.abc import Iterable
from dataclasses import dataclass
from typing import TypedDict

STRIKE_LIMIT = 3  # 累计这么多次被拒，就自动封禁


class ServiceError(Exception):
    """对外的统一错误：status 是 HTTP 状态码，code 是稳定的字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


def _snapshot(values: Iterable[str], code: str) -> list[str]:
    """把配置读成一份列表并校验全部条目；任何一条不合格，整批作废。

    迭代过程中自己抛出的异常（比如生成器里的 IOError）原样冒出去，不换成 400。
    """
    if isinstance(values, (str, bytes, bytearray)):  # 裸字符串会被拆成单个字符，必须先拒绝
        raise ServiceError(400, code)
    try:
        iterator = iter(values)
    except TypeError:  # 根本不是可迭代对象
        raise ServiceError(400, code) from None
    items = list(iterator)  # 只遍历一次，一次性迭代器也能用
    if not all(isinstance(item, str) and item.strip() for item in items):
        raise ServiceError(400, code)
    return items


def _require_user(user: object) -> str:
    """用户 ID 必须是非空白字符串；原样返回，不 strip、不改大小写。"""
    if not isinstance(user, str) or not user.strip():
        raise ServiceError(400, "invalid_input")
    return user


@dataclass(frozen=True, slots=True)
class Keywords:
    """一份编译好的关键词表：规范化、去重、按字符串顺序排好，创建后不可变。"""

    words: tuple[str, ...] = ()

    @classmethod
    def compile(cls, raw: Iterable[str]) -> Keywords:
        """校验并规范化：strip 再 casefold，然后去重、排序。"""
        normalized = {word.strip().casefold() for word in _snapshot(raw, "invalid_keywords")}
        return cls(tuple(sorted(normalized)))

    def find(self, content: str) -> list[str]:
        """内容只做 casefold；逐个关键词做字面子串查找，结果已按字符串顺序排好。"""
        folded = content.casefold()
        return [word for word in self.words if word in folded]


@dataclass(frozen=True, slots=True)
class Verdict:
    """一次 `check` 的结果；`as_dict` 每次造新字典，调用方随便改。"""

    allowed: bool
    reason: str | None
    matches: tuple[str, ...]
    strikes: int

    @classmethod
    def clean(cls, strikes: int) -> Verdict:
        return cls(True, None, (), strikes)

    @classmethod
    def blocked(cls, strikes: int) -> Verdict:
        return cls(False, "user_blocked", (), strikes)

    @classmethod
    def keyword(cls, matches: Iterable[str], strikes: int) -> Verdict:
        return cls(False, "keyword", tuple(matches), strikes)

    def as_dict(self) -> dict[str, object]:
        return {
            "allowed": self.allowed,
            "reason": self.reason,
            "matches": list(self.matches),
            "strikes": self.strikes,
        }


class UserState(TypedDict):
    strikes: int
    blocked: bool


class StrikeLedger:
    """每个用户的违规次数。只记出过违规的用户，次数永远不超过上限。

    它自己不加锁：并发由持有它的 `BlocklistService` 用一把锁保证。
    """

    def __init__(self, limit: int = STRIKE_LIMIT) -> None:
        self._limit = limit
        self._counts: dict[str, int] = {}

    def count(self, user: str) -> int:
        return self._counts.get(user, 0)  # 查询不创建条目，没违规过的用户不占内存

    def exhausted(self, user: str) -> bool:
        return self.count(user) >= self._limit

    def add(self, user: str) -> int:
        """记一次违规并返回新的次数；已到上限的用户不该再走到这里。"""
        if self.exhausted(user):
            raise RuntimeError("user already at the strike limit")  # 安全不变量，不用 assert
        self._counts[user] = self.count(user) + 1
        return self._counts[user]


class BlocklistService:
    """关键词匹配、手动封禁与累计违规封禁。"""

    def __init__(self, keywords: Iterable[str] = (), blocked_users: Iterable[str] = ()) -> None:
        # 两份配置都校验通过以后才赋值；构造和替换走同一条校验路径
        compiled = Keywords.compile(keywords)
        manual = frozenset(_snapshot(blocked_users, "invalid_users"))
        self._lock = threading.Lock()
        self._keywords = compiled
        self._manual = manual
        self._ledger = StrikeLedger()

    @property
    def keywords(self) -> list[str]:
        """当前规范化后的关键词（按字符串顺序）的副本。"""
        with self._lock:
            return list(self._keywords.words)

    @property
    def blocked_users(self) -> list[str]:
        """当前手动封禁名单（按字符串顺序）的副本。"""
        with self._lock:
            return sorted(self._manual)

    def replace_keywords(self, keywords: Iterable[str]) -> None:
        compiled = Keywords.compile(keywords)  # 在锁外读用户给的迭代器，慢的或会抛错的迭代器不会占着锁
        with self._lock:
            self._keywords = compiled  # 一次引用替换：并发的 check 看到整份旧表或整份新表

    def replace_blocked_users(self, users: Iterable[str]) -> None:
        manual = frozenset(_snapshot(users, "invalid_users"))
        with self._lock:
            self._manual = manual

    def state(self, user: str) -> UserState:
        _require_user(user)
        with self._lock:
            return {"strikes": self._ledger.count(user), "blocked": self._is_blocked(user)}

    def check(self, user: str, content: str) -> dict[str, object]:
        _require_user(user)
        if not isinstance(content, str):
            raise ServiceError(400, "invalid_input")  # 校验在任何匹配和记账之前
        with self._lock:
            strikes = self._ledger.count(user)
            if self._is_blocked(user):  # 封禁优先于关键词：不匹配、不加次数
                return Verdict.blocked(strikes).as_dict()
            matches = self._keywords.find(content)
            if not matches:  # 干净请求不清零次数
                return Verdict.clean(strikes).as_dict()
            return Verdict.keyword(matches, self._ledger.add(user)).as_dict()  # 不管命中几处，只记一次

    def _is_blocked(self, user: str) -> bool:
        """调用方必须已持有锁。"""
        return user in self._manual or self._ledger.exhausted(user)


if __name__ == "__main__":
    service = BlocklistService([" SPAM "])
    print(service.check("alice", "SPAM offer"))
    print(service.check("alice", "hello"))
    for _ in range(3):
        print(service.check("bob", "spam spam spam"))
    print(service.state("bob"))
