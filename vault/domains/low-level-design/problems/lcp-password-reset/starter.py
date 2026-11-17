"""密码重置服务（待修复）。公开 API 与 `solution.py` 一致，去掉存储边界那一段后可以原样放进真实工作区的 `auth_service.py`。

这份代码能跑，但有几处和下面的规则不符：它就是要你修的东西。

产品规则（逐条都有测试）：
 1. 配置：构造实例时读一次环境变量 `INTERNAL_AUTH_URL`，保存在 `auth_service_url`；没有这个变量就是
    `http://internal.auth.local`；有就原样保留（空字符串、首尾空白也不动），不改写、不校验、不访问；
    之后环境变化只影响新实例；构造不读时钟、不改存储。`environment` 映射缺省时用 `os.environ`（空映射也算"给了"）。
 2. `request_reset(user_id)`：先查用户，不存在就抛 `ValueError("User not found")`，此时不读时钟、不写任何状态。
 3. 已知用户：生成并返回非空字符串码；同一个服务实例生成的值不重复（成功用过之后也不重复），也不能等于该用户
    当前存着的码（哪怕是另一个实例签发的）。`generate_code()` 是可覆盖的钩子，每次尝试调用一次，撞上就重试。
 4. 码与"当前时间"通过 `db.save_reset_code` 保存；时间存成有时区的 UTC 时刻，与时钟值是同一瞬间。
 5. 再次请求替换该用户的码与时间，重新开始 30 秒；请求不改任何密码，也不动别的用户。
 6. `verify_and_reset(user_id, code, new_password)` 返回布尔值：用户不存在、没有记录、码不精确相等（不去空白）都是 `False`。
 7. 年龄 = 当前时钟 − 记录创建时间，按时刻比较而不是按钟面字段；有效当且仅当 0 <= 年龄 < 30 秒：
    0 秒与 29.9 秒有效，30 秒过期，负年龄（记录在"未来"）无效。时钟可能倒退。
 8. 记录里没有时区的旧时间戳按 UTC 解释；有时区的时间戳可以是任意 UTC 偏移。
 9. 任何返回 `False` 的校验都不改任何密码和重置记录：错误的码不消耗有效的码；过期记录可以留在库里直到被新请求替换。
10. 成功：用一次 `db.update_password` 把 `"hashed_" + new_password` 原样存下（空串、空白、Unicode 都允许），
    保留邮箱等其他字段；`db.get_user` 返回副本，改副本不会保存。
11. 成功之后用 `db.clear_reset_code` 清掉该用户的记录，再返回 `True`；同一个码重放（哪怕换一个服务实例）得到 `False`；
    之后再请求会得到新码，可以再改一次密码。
12. 用户隔离：码属于存着它的那个用户，不能用 A 的码重置 B，也不清 B 的记录；用户在校验时才检查是否存在，
    被删用户的残留记录返回 `False` 且不改状态。
13. 所有读写都走共享的 `db`（不同实例共享它），不要换成实例自己的存储，也不要碰它的私有字典。
14. 调用是串行的；并发校验、事务、尝试次数限制、码的哈希、持久化是书面问题，不需要实现。

Python 3.11，标准库。
"""

from __future__ import annotations

import copy
import os
import random
from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from typing import Any


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


class PasswordResetService:
    def __init__(
        self,
        *,
        clock: Callable[[], datetime] | None = None,
        environment: Mapping[str, str] | None = None,
    ) -> None:
        self._environment = environment or os.environ
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._clock()  # 先读一次，"确认时钟可用"

    @property
    def auth_service_url(self) -> str:
        url = self._environment.get("INTERNAL_AUTH_URL") or "http://internal.auth.local"
        return url.strip().rstrip("/")

    def generate_code(self) -> str:
        return str(random.randint(1000, 9999))

    def request_reset(self, user_id: str) -> str:
        issued_at = self._clock()
        if db.get_user(user_id) is None:
            raise ValueError("User not found")
        token = self.generate_code()
        db.save_reset_code(user_id, token, issued_at)
        return token

    def verify_and_reset(self, user_id: str, code: str, new_password: str) -> bool:
        row = db.get_reset_code(user_id)
        if not row or row["code"] != code.strip():
            return False
        created = row["created_at"]
        if created.tzinfo is None:
            created = created.astimezone(timezone.utc)
        age = self._clock().replace(tzinfo=None) - created.replace(tzinfo=None)
        if age.total_seconds() > 30:
            return False
        user = db.get_user(user_id)
        if user is not None:
            user["password_hash"] = "hashed_" + new_password
        return True
