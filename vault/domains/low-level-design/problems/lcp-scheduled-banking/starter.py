"""带定时付款的银行账本练习骨架。公开 API 与 `solution.py` 一致，可以原样放进真实工作区的 `service.py`。

产品规则（逐条都有测试）：
 1. 所有调用按严格递增的非负整数 `timestamp` 顺序发生；金额、延迟都是正整数，余额是整数，没有透支；
    各个 `Bank` 互相独立；账户 ID 是非空、区分大小写的字符串。
 2. `create_account` 新建零余额账户并返回 True；曾经用过的 ID（包括被合并掉的）返回 False。
 3. `deposit` 返回新余额；账户不存在（含已并掉）返回 None。
 4. `transfer` 返回转出账户转出后的余额；账户不存在、两端相同、余额不足都返回 None 且什么都不变；恰好花光是合法的。
 5. 每个公开方法执行之前，先处理所有到期时间不晚于本次 `timestamp` 的待付款项——查询和会失败的调用也一样。
    先按到期时间、再按创建序号的数值（payment10 在 payment9 之后）排队。
 6. 一笔付款到期时：当前归属账户余额够就扣一次并计入支出，不够就永久失败，不留任何痕迹；
    扣款的余额变化记在它的到期时刻，哪怕是后来某次调用才触发的结算。
    同一时刻的存款发生在到期付款之后，救不了已经失败的付款。
 7. `schedule_payment` 账户不存在返回 None，且不消耗编号；成功返回 `payment1`、`payment2`……（整个银行内全局递增）；
    到期时间是 `timestamp + delay`；安排付款不冻结资金。
 8. `cancel_payment` 只在"待付款、且归属于传入的活跃账户"时返回 True 并取消；
    未知编号、别人的付款、已取消或已处理的付款返回 False。到期那一刻再取消已经太晚。
 9. `merge_accounts(timestamp, id1, id2)`：先结算到期付款；任一账户不存在或 ID 相同返回 False；
    成功时 id2 的余额、累计支出、待付款项（编号、到期时间、创建序号不变）并入 id1，id2 退役，返回 True；支持连环合并。
10. `top_spenders(timestamp, n)`：最多 n 个活跃账户，含支出为 0 的；格式 `"账户(累计转出)"`；
    先按累计转出降序，再按 ID 的 Python 字符串顺序升序；n=0 返回 []。累计转出只含成功的转账和成功的定时付款；
    存款、收到的转入、失败的付款、合并本身都不算；合并把两个账户的累计相加。
11. `get_balance(timestamp, account_id, time_at)`：返回 `time_at` 时刻所有事件之后的余额，或此前最近的余额；
    账户当前不活跃、`time_at` 时账户还不存在、`time_at > timestamp` 都返回 None；
    存活账户在合并之前保留自己原来的余额，合并后的总额从合并时刻起算，不追溯；已并掉的账户查任何时刻都是 None。
12. `transfer_batch(timestamp, transfers)`：先结算到期付款（空批次、失败批次也是）；
    再按列表顺序在暂存余额上演算，后面的转账可以花前面刚收到的钱；
    任何一笔的端点不存在、两端相同或余额不足，整批返回 None，批内的余额、支出、历史一概不留（已结算的付款保留）；
    成功则整批提交，返回每笔转出后转出账户的余额（按输入顺序）；每笔成功转账都计入支出（净额为零也算）；
    同一时间戳上的历史查询只看到批次结束后的余额；空批次返回 []；不修改传入的列表，返回的列表是新对象。
13. 失败一律用返回值表示，不抛异常。

下面两个只读属性不属于工作区的接口，只是让测试能断言"已取消的付款不会让内部队列无限增长"：
`pending_count`（待付款项数）和 `queue_size`（到期队列里存着的条目数）。
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any


class Bank:
    def __init__(self) -> None:
        raise NotImplementedError

    @property
    def pending_count(self) -> int:
        raise NotImplementedError

    @property
    def queue_size(self) -> int:
        raise NotImplementedError

    def create_account(self, timestamp: int, account_id: str) -> bool:
        raise NotImplementedError

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        raise NotImplementedError

    def transfer(self, timestamp: int, source: str, target: str, amount: int) -> int | None:
        raise NotImplementedError

    def transfer_batch(
        self, timestamp: int, transfers: Iterable[Sequence[Any]]
    ) -> list[int] | None:
        raise NotImplementedError

    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        raise NotImplementedError

    def schedule_payment(
        self, timestamp: int, account_id: str, amount: int, delay: int
    ) -> str | None:
        raise NotImplementedError

    def cancel_payment(self, timestamp: int, account_id: str, payment_id: str) -> bool:
        raise NotImplementedError

    def merge_accounts(self, timestamp: int, id1: str, id2: str) -> bool:
        raise NotImplementedError

    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        raise NotImplementedError
