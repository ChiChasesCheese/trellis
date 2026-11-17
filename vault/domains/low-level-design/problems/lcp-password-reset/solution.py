"""密码重置服务（PasswordResetService）参考解：配置快照、有时限且一次性的重置码、经存储边界保存状态。

设计五句话：
1. 构造时一次性读取 `INTERNAL_AUTH_URL` 并原样保存，之后环境变量再变不影响这个实例；构造不读时钟、不碰存储。
2. 重置码"不重复"由 `UniqueCodes` 负责：它记住本实例生成过的每个码，并把该用户当前存着的码也算作已占用，撞上就重试。
3. 有效期由 `ValidityWindow` 判断，年龄由 `ResetRecord.age` 算：两端先换成 UTC 时刻再相减，没有时区的旧时间当作 UTC，只有 0 <= 年龄 < 30 秒有效。
4. 校验失败一律先返回 `False` 且不写任何东西；成功时先 `update_password` 再 `clear_reset_code`，密码没写成功就不消耗重置码。
5. 所有读写都经过共享的 `db`：`ResetStore` 是服务碰存储的唯一入口，把原始字典变成 `ResetRecord`，并把"先存密码后清记录"固定在一处；每次调用时才取模块里的 `db`。
"""

from __future__ import annotations

import copy
import os
import secrets
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

URL_VARIABLE = "INTERNAL_AUTH_URL"
DEFAULT_AUTH_URL = "http://internal.auth.local"
PASSWORD_PREFIX = "hashed_"  # 题目里的"哈希"只是加前缀的占位，不是真正的密码哈希
MAX_ATTEMPTS = 1000  # 生成器一直撞车时的上限，防止死循环


# ---- 存储边界开始：真实工作区由 database.py 提供同样接口的 `db`；放进去时删掉这一段，改成 `from database import db` ----
class MockDatabase:
    """内存存储：账户（含密码哈希）加上每个账户至多一条待用的重置记录。接口与真实工作区的 `db` 相同，内部结构是我们自己的。"""

    def __init__(self, users: dict[str, dict[str, Any]] | None = None) -> None:
        seed = {"acct_mira": {"password_hash": "pw0", "email": "mira@example.org"}}
        self._accounts: dict[str, dict[str, Any]] = copy.deepcopy(seed if users is None else users)
        self._pending: dict[str, dict[str, Any]] = {}

    def get_user(self, user_id: str) -> dict[str, Any] | None:
        """给调用方一份副本：改副本不会落库，改密码只能走 `update_password`。"""
        account = self._accounts.get(user_id)
        return None if account is None else dict(account)

    def update_password(self, user_id: str, new_password_hash: str) -> None:
        account = self._accounts.get(user_id)
        if account is not None:
            account["password_hash"] = new_password_hash

    def save_reset_code(self, user_id: str, code: str, timestamp: datetime) -> None:
        self._pending[user_id] = {"code": code, "created_at": timestamp}

    def get_reset_code(self, user_id: str) -> dict[str, Any] | None:
        """返回库里那条记录本身而不是副本，所以服务只读它。"""
        return self._pending.get(user_id)

    def clear_reset_code(self, user_id: str) -> None:
        self._pending.pop(user_id, None)

    def snapshot(self) -> tuple[dict[str, Any], dict[str, Any]]:
        """（仅供本仓库的测试）把全部状态深拷贝出来，用来断言失败的调用不留痕迹。"""
        return copy.deepcopy((self._accounts, self._pending))


db = MockDatabase()
# ---- 存储边界结束 ----


def to_utc(moment: datetime) -> datetime:
    """换成 UTC 的有时区时间；没有时区信息的（旧记录）当作本来就是 UTC。"""
    if moment.utcoffset() is None:
        return moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class ResetRecord:
    """存储里一条重置记录的类型化视图：时间在读入这一刻就统一成 UTC，后面不用再想时区。"""

    code: str
    created_at: datetime

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> ResetRecord:
        return cls(row["code"], to_utc(row["created_at"]))

    def age(self, now: datetime) -> timedelta:
        """从创建到 now 过了多久。两端都先换成 UTC 再相减：同一个 tzinfo 对象的两个时间直接相减会忽略偏移变化。"""
        return to_utc(now) - self.created_at


@dataclass(frozen=True)
class ValidityWindow:
    """有效期规则本身：半开区间 [0, length)，下界含、上界不含，全程用 timedelta 精确比较。"""

    length: timedelta = timedelta(seconds=30)

    def accepts(self, age: timedelta) -> bool:
        return timedelta(0) <= age < self.length


class ResetStore:
    """服务与存储之间唯一的接口层：读出来的是类型化的 `ResetRecord`，写入前时间已是 UTC。

    它没有自己的状态，每次调用时才取模块里的 `db`（测试和真实工作区都靠这一点替换存储）。
    """

    def user_exists(self, user_id: str) -> bool:
        return db.get_user(user_id) is not None

    def record_of(self, user_id: str) -> ResetRecord | None:
        row = db.get_reset_code(user_id)
        return None if row is None else ResetRecord.from_row(row)

    def save(self, user_id: str, code: str, now: datetime) -> None:
        db.save_reset_code(user_id, code, to_utc(now))  # 覆盖旧记录，开始新的有效期

    def consume(self, user_id: str, new_password: str) -> None:
        """先存密码、再清记录：存密码抛异常时记录还在，调用方可以重试。"""
        db.update_password(user_id, PASSWORD_PREFIX + new_password)
        db.clear_reset_code(user_id)


class UniqueCodes:
    """一个实例签发的码不重复：已生成过的、该用户当前存着的，都要换一个。"""

    def __init__(self) -> None:
        self._seen: set[str] = set()

    def issue(self, generate: Callable[[], str], stored: str | None) -> str:
        for _ in range(MAX_ATTEMPTS):
            code = generate()
            taken = code in self._seen or code == stored
            self._seen.add(code)  # 被拒绝的值也记下：同一个实例从此不再产生它
            if not taken:
                return code
        raise RuntimeError("code generator keeps returning codes that are already taken")


class PasswordResetService:
    """请求重置码、凭码改密码。本身只持有配置快照、时钟、码的账本和有效期规则，用户数据全在 `db`。"""

    def __init__(
        self,
        *,
        clock: Callable[[], datetime] | None = None,
        environment: Mapping[str, str] | None = None,
    ) -> None:
        env = os.environ if environment is None else environment  # `or` 会把空映射误当成"没给"
        self.auth_service_url: str = env.get(URL_VARIABLE, DEFAULT_AUTH_URL)  # 存在就原样保留，包括空串与空白
        self._clock = clock if clock is not None else utc_now
        self._codes = UniqueCodes()
        self._store = ResetStore()
        self._window = ValidityWindow()

    def generate_code(self) -> str:
        """可覆盖的生成器钩子：每次尝试调用一次。默认用密码学安全的随机数。"""
        return secrets.token_urlsafe(6)

    def request_reset(self, user_id: str) -> str:
        if not self._store.user_exists(user_id):
            raise ValueError("User not found")  # 在读时钟、写存储之前
        current = self._store.record_of(user_id)
        fresh = self._codes.issue(self.generate_code, current.code if current else None)
        issued_at = self._clock()
        self._store.save(user_id, fresh, issued_at)
        return fresh

    def verify_and_reset(self, user_id: str, code: str, new_password: str) -> bool:
        if not self._store.user_exists(user_id):  # 用户被删后残留的记录也不能用
            return False
        record = self._store.record_of(user_id)
        if record is None or record.code != code:  # 精确比较，不去空白、不改大小写
            return False
        if not self._window.accepts(record.age(self._clock())):
            return False
        self._store.consume(user_id, new_password)
        return True


if __name__ == "__main__":
    # 两分钟演示：用手动推进的时钟看窗口边界、重放和旧的无时区记录
    now = [datetime(2026, 1, 1, 12, tzinfo=timezone.utc)]
    service = PasswordResetService(clock=lambda: now[0], environment={})
    print("url        :", service.auth_service_url)
    issued = service.request_reset("acct_mira")
    print("wrong code :", service.verify_and_reset("acct_mira", issued + "x", "pw"))
    now[0] += timedelta(seconds=29.9)
    print("at 29.9 s  :", service.verify_and_reset("acct_mira", issued, "pw"))
    print("replay     :", service.verify_and_reset("acct_mira", issued, "pw2"))
    print("password   :", (db.get_user("acct_mira") or {})["password_hash"])
    db.save_reset_code("acct_mira", "legacy", datetime(2026, 1, 1, 12, 0, 0))  # 旧记录：没有时区信息，按 UTC
    now[0] += timedelta(seconds=0.1)  # 现在正好是 12:00:30.0，旧记录年龄 30 秒
    print("legacy 30 s:", service.verify_and_reset("acct_mira", "legacy", "pw3"))
    print("password   :", (db.get_user("acct_mira") or {})["password_hash"])
