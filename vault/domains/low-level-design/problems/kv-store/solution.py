"""内存键值存储（In-Memory Key-Value Store）——分关递进机考题的参考实现。

五行设计：每个 key 下面是一张字段表（field -> Slot），`Slot` 带着自己的绝对过期时刻，key
自己另外可以有一份整体过期时间，两者都是惰性检查、只在被访问到时才物理清除；一切事务能力
建在同一根"撤销日志"上——每一次真正改动物理存储之前，先把"怎么把它变回去"记成一个闭包，
`begin` 开一层新的日志，`commit` 把这一层日志整体并进上一层（数据已经生效，只是还能被
外层撤销），`rollback` 把这一层日志按逆序重放；不在任何事务里时日志根本不会被记录，读写
路径因此和没有事务功能时完全等价，没有为"可能用得上"的分支付出任何代价。
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


class KVStoreError(Exception):
    """本设计所有失败路径的公共基类。"""


class KeyNotFoundError(KVStoreError):
    """key 不存在，或者它的字段已经全部过期/被删空了。"""


class FieldNotFoundError(KVStoreError):
    """字段不存在，或者已经过期——对调用方来说这两者没有区别。"""


class InvalidTTLError(KVStoreError):
    """存活时间不是正数。"""


class NoActiveTransactionError(KVStoreError):
    """在没有对应 `begin` 的情况下调用了 `commit` 或 `rollback`。"""


@dataclass(frozen=True, slots=True)
class Slot:
    """一个字段的当前取值：值本身，加上它自己的绝对过期时刻（`None` 表示不会单独过期，
    但仍然可能随所属的 key 一起过期）。
    """

    value: str
    expires_at: int | None


class KVStore:
    """字段表加撤销日志：`set`/`get`/`delete`/`count_by_field_value` 是第 1 关，
    `scan_prefix`/`fields` 是第 2 关，`expire_key` 和 `set` 的 `ttl` 参数是第 3 关，
    `begin`/`commit`/`rollback` 是第 4 关。除了两个只读的 `*_count` 之外，每个改动或
    读取数据的方法第一个参数都是 `timestamp: int`——这个类内部没有任何地方读墙上时钟；
    事务控制三个方法反而**不带** `timestamp`，理由见题解"关键设计决策"。
    """

    def __init__(self) -> None:
        self._fields: dict[str, dict[str, Slot]] = {}
        self._key_expiry: dict[str, int] = {}
        self._frames: list[list[Callable[[], None]]] = []

    # ---------- 只读视图 ----------

    @property
    def transaction_depth(self) -> int:
        """当前嵌套了多少层未提交的事务；0 表示不在任何事务里。"""
        return len(self._frames)

    @property
    def expiring_key_count(self) -> int:
        """挂着"整体过期时间"的 key 有多少个。一个 key 的所有字段被逐个 `delete` 删空后，
        这个数必须跟着降下来——否则这张表会随着"先设 key 级 TTL、再手动删光字段"这种用法
        无限增长，是一个真实存在过的缺陷，见 `_write_field` 的最后两行。
        """
        return len(self._key_expiry)

    def key_count(self, timestamp: int) -> int:
        """还至少有一个存活字段的 key 有多少个；顺带清掉所有到期的 key 和字段，因此也是
        证明"过期的数据真的从存储里消失了、不是只是查不到"最直接的方式。
        """
        return sum(1 for key in list(self._fields) if self._touch(key, timestamp))

    # ---------- 撤销日志 ----------

    def _log(self, undo: Callable[[], None]) -> None:
        """不在任何事务里时没有人会调用 `rollback`，记录撤销动作没有意义，也没有代价。"""
        if self._frames:
            self._frames[-1].append(undo)

    def _apply_field(self, key: str, field: str, slot: Slot | None) -> None:
        """把 `key.field` 直接改写成 `slot`（`None` 表示删除）。这个方法既是"正向写入"的
        实现，也是"撤销时变回去"的实现——两者是同一个操作，撤销不需要另一套代码，只需要
        知道"变回去的目标状态是什么"。
        """
        if slot is None:
            bucket = self._fields.get(key)
            if bucket is not None:
                bucket.pop(field, None)
                if not bucket:
                    del self._fields[key]
        else:
            self._fields.setdefault(key, {})[field] = slot

    def _write_field(self, key: str, field: str, slot: Slot | None) -> None:
        prior = self._fields.get(key, {}).get(field)
        self._log(lambda prior=prior: self._apply_field(key, field, prior))
        self._apply_field(key, field, slot)
        if key not in self._fields and key in self._key_expiry:
            self._write_key_expiry(key, None)  # 字段删空了，孤立的整体过期时间没有意义

    def _apply_key_expiry(self, key: str, expires_at: int | None) -> None:
        if expires_at is None:
            self._key_expiry.pop(key, None)
        else:
            self._key_expiry[key] = expires_at

    def _write_key_expiry(self, key: str, expires_at: int | None) -> None:
        prior = self._key_expiry.get(key)
        self._log(lambda prior=prior: self._apply_key_expiry(key, prior))
        self._apply_key_expiry(key, expires_at)

    # ---------- 惰性过期 ----------

    def _touch(self, key: str, now: int) -> bool:
        """访问 `key` 之前先把到期的东西清掉，返回清理之后这个 key 是否还有存活字段。
        整个 key 到期时它名下所有字段一起消失；否则只清理单独到期的字段。清理动作本身
        照样走 `_write_field`/`_write_key_expiry`，所以即使发生在事务内部也一样可撤销——
        但撤销回去的是同一份 `(value, expires_at)`，过没过期永远由调用时的 `now` 重新
        判断，所以撤销一次惰性清理绝不会让一条本该过期的数据复活。
        """
        deadline = self._key_expiry.get(key)
        if deadline is not None and now >= deadline:
            for field in list(self._fields.get(key, {})):
                self._write_field(key, field, None)
            self._write_key_expiry(key, None)
            return False
        bucket = self._fields.get(key)
        if bucket:
            for field, slot in list(bucket.items()):
                if slot.expires_at is not None and now >= slot.expires_at:
                    self._write_field(key, field, None)
        return key in self._fields

    # ---------- 第 1 关：基本读写 ----------

    def set(self, timestamp: int, key: str, field: str, value: str, ttl: int | None = None) -> None:
        """写入一个字段，覆盖已有的值（包括它的过期时间）。`ttl` 省略表示这个字段不会
        单独过期——但 key 级的整体过期时间仍然可能连它一起杀死。
        """
        if ttl is not None and ttl <= 0:
            raise InvalidTTLError(f"ttl 必须为正数，收到 {ttl}")
        self._touch(key, timestamp)
        expires_at = None if ttl is None else timestamp + ttl
        self._write_field(key, field, Slot(value, expires_at))

    def get(self, timestamp: int, key: str, field: str) -> str:
        """读取一个字段的值；字段不存在或已经过期都抛 `FieldNotFoundError`。"""
        self._touch(key, timestamp)
        slot = self._fields.get(key, {}).get(field)
        if slot is None:
            raise FieldNotFoundError(f"{key}.{field} 不存在")
        return slot.value

    def delete(self, timestamp: int, key: str, field: str) -> None:
        """删除一个字段；字段不存在（或已经过期）同样抛 `FieldNotFoundError`——删除一样
        东西之前必须先证明它还在，而不是悄悄地什么都不做。
        """
        self._touch(key, timestamp)
        if field not in self._fields.get(key, {}):
            raise FieldNotFoundError(f"{key}.{field} 不存在")
        self._write_field(key, field, None)

    def count_by_field_value(self, timestamp: int, field: str, value: str) -> int:
        """有多少个 key 的这个字段当前恰好等于 `value`。每次调用都会先清一遍所有 key
        到期的字段——这道题的规模决定了线性扫描足够，索引化的取舍见"扩展与追问"。
        """
        count = 0
        for key in list(self._fields):
            self._touch(key, timestamp)
            slot = self._fields.get(key, {}).get(field)
            if slot is not None and slot.value == value:
                count += 1
        return count

    # ---------- 第 2 关：扫描 ----------

    def scan_prefix(self, timestamp: int, prefix: str) -> list[str]:
        """所有以 `prefix` 开头、至少还有一个存活字段的 key，按字典序升序排列。"""
        return sorted(key for key in list(self._fields)
                       if self._touch(key, timestamp) and key.startswith(prefix))

    def fields(self, timestamp: int, key: str) -> list[str]:
        """`key` 当前存活的字段名，按字典序升序排列；key 不存在时返回空列表而不是报错——
        "问一个不存在的东西有哪些字段"和"读一个不存在的字段"是两件不同的事。
        """
        self._touch(key, timestamp)
        return sorted(self._fields.get(key, {}))

    # ---------- 第 3 关：key 级 TTL ----------

    def expire_key(self, timestamp: int, key: str, ttl: int) -> None:
        """给整个 key 设置一个从 `timestamp` 起 `ttl` 之后到期的存活期，到期时它名下所有
        字段一起消失；覆盖它之前的 key 级过期时间，不影响单个字段各自的过期时间——两条
        时间线各自独立，谁先到谁先让相关的数据消失。
        """
        if ttl <= 0:
            raise InvalidTTLError(f"ttl 必须为正数，收到 {ttl}")
        if not self._touch(key, timestamp):
            raise KeyNotFoundError(f"key 不存在：{key}")
        self._write_key_expiry(key, timestamp + ttl)

    # ---------- 第 4 关：嵌套事务 ----------

    def begin(self) -> None:
        """开启一层新的事务，可以在已经开着的事务里再嵌套，深度没有上限。"""
        self._frames.append([])

    def commit(self) -> None:
        """结束当前这一层事务，把它的改动**保留**下来。如果外面还套着一层事务，这些
        改动只是折叠进外层的撤销日志——对存储本身来说它们已经生效，但外层的 `rollback`
        依然能把它们连同外层自己的改动一起撤销；只有最外层的 `commit` 才真正意味着
        "这些改动再也不会被撤销"。
        """
        if not self._frames:
            raise NoActiveTransactionError("没有正在进行的事务")
        finished = self._frames.pop()
        if self._frames:
            self._frames[-1].extend(finished)

    def rollback(self) -> None:
        """撤销当前这一层事务里发生的所有改动，恢复到进入这一层之前的状态；只影响这一层，
        外层（如果有）在这一层开始之前的改动不受影响，因为它们记在另一份日志里。
        """
        if not self._frames:
            raise NoActiveTransactionError("没有正在进行的事务")
        undo_ops = self._frames.pop()
        for undo in reversed(undo_ops):
            undo()


def _demo() -> None:
    store = KVStore()
    store.set(0, "user:1", "name", "Ada")
    store.set(0, "user:1", "session", "abc123", ttl=10)
    store.set(0, "user:2", "name", "Ada")
    print("同名用户数:", store.count_by_field_value(0, "name", "Ada"))

    store.begin()
    store.set(0, "user:1", "name", "Ada Lovelace")
    store.begin()
    store.delete(0, "user:1", "session")
    store.rollback()  # 只撤销内层：session 恢复，改名保留
    store.commit()    # 外层提交：改名落地
    print("回滚内层、提交外层之后:", store.get(0, "user:1", "name"))

    try:
        store.get(15, "user:1", "session")
    except FieldNotFoundError:
        print("session 在 t=15 已过期")


if __name__ == "__main__":
    _demo()
