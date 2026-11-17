"""贷款服务（LedgerBridge）参考解：账本管余额，贷款管状态，服务用一把锁把两者的联动包成原子操作。

产品规则（编号即测试编号，金额一律是整数分，Python 的 int 没有上限）：

1. 金额：必须是恰好为 `int` 的正数；`bool`、浮点、字符串、`None`、0 和负数都是 400 invalid_amount。
2. 创建：先验金额，再验借款人存在（404 user_not_found）；成功才消耗编号，编号从 1 起；创建不动钱。
   返回 `{id, borrower, lender: None, principal, outstanding, status: "pending"}`。
3. 查询：`get` 返回已存的贷款；编号不存在 404 loan_not_found；`balance` 对不存在的用户 404 user_not_found。
4. 放款检查顺序：贷款存在 → 出借人存在 → 状态与身份（只有 pending 且出借人不是借款人，否则 409 invalid_state）
   → 余额（低于本金 409 insufficient_balance，恰好等于本金可以）。
5. 放款成功：本金从出借人划给借款人，贷款记下出借人、变为 active，未还金额等于本金。
6. 还款检查顺序：金额 → 贷款存在 → 借款人对得上（403 forbidden）→ 状态为 active 且不超额（409 invalid_state）
   → 借款人余额（409 insufficient_balance）。
7. 还款成功：钱从借款人划给出借人，未还金额减少；减到 0 变 repaid，否则仍是 active。
8. 任何一次失败都不留痕迹：贷款、余额、编号计数都和调用前一样。
9. 并发：同一实例上的所有方法互斥；同一笔贷款并发放款恰好一次成功；所有余额之和恒定且没有负数。
10. 隔离：返回值都是独立的快照，改它不影响服务；构造时复制传入的余额；多个实例互不相干。

放进真实工作区时，把下面的 `ServiceError` 换成 `from models import ServiceError`，其余原样使用。
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from enum import Enum


class ServiceError(Exception):
    """对外的服务错误：status 是 HTTP 状态码，code 是稳定的错误码字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


def require_amount(amount: object) -> int:
    """金额合格就原样返回。用 `type(...) is int` 而不是 isinstance：True 也是 int，必须挡在外面。"""
    if type(amount) is int and amount > 0:
        return amount
    raise ServiceError(400, "invalid_amount")


class LoanStatus(Enum):
    """贷款的三个状态；只允许 PENDING → ACTIVE → REPAID 单向前进。"""

    PENDING = "pending"
    ACTIVE = "active"
    REPAID = "repaid"


@dataclass
class Loan:
    """一笔贷款。状态转移的前提都写在这里，调用方不能绕过检查直接改字段。

    不变量：0 <= outstanding <= principal；status 为 PENDING 时 lender 是 None；
    status 为 REPAID 当且仅当 outstanding == 0。
    """

    id: int
    borrower: str
    principal: int
    outstanding: int
    lender: str | None = None
    status: LoanStatus = LoanStatus.PENDING

    def snapshot(self) -> dict:
        """对外的快照：每次现建一个新字典，全是不可变的值，调用方怎么改都碰不到贷款本身。"""
        return {
            "id": self.id,
            "borrower": self.borrower,
            "lender": self.lender,
            "principal": self.principal,
            "outstanding": self.outstanding,
            "status": self.status.value,
        }

    def ensure_fundable(self, lender: str) -> None:
        """放款的状态与身份检查；只读，不改任何字段。"""
        if self.status is not LoanStatus.PENDING or lender == self.borrower:
            raise ServiceError(409, "invalid_state")

    def ensure_repayable(self, borrower: str, amount: int) -> None:
        """还款的归属、状态与超额检查，顺序固定：先 403，再 409；只读。"""
        if borrower != self.borrower:
            raise ServiceError(403, "forbidden")
        if self.status is not LoanStatus.ACTIVE or amount > self.outstanding:
            raise ServiceError(409, "invalid_state")

    def activate(self, lender: str) -> None:
        """放款成功后的状态转移；调用前必须已通过 ensure_fundable。"""
        self.lender = lender
        self.status = LoanStatus.ACTIVE

    def reduce(self, amount: int) -> None:
        """还款成功后扣减未还金额；扣到 0 就结清。调用前必须已通过 ensure_repayable。"""
        self.outstanding -= amount
        if self.outstanding == 0:
            self.status = LoanStatus.REPAID


class Ledger:
    """账本：只管余额。唯一能改余额的入口是 `transfer`，它先查后改，所以余额守恒且不会出现负数。"""

    def __init__(self, balances: dict[str, int]) -> None:
        self._cents = dict(balances)  # 复制一份：之后调用方改它的字典，账本不受影响

    def balance(self, user: str) -> int:
        """用户必须存在；非字符串（含不可哈希的值）也按"不存在"处理，而不是抛 TypeError。"""
        if type(user) is str and user in self._cents:
            return self._cents[user]
        raise ServiceError(404, "user_not_found")

    def total(self) -> int:
        """所有人的余额之和：守恒的那个量，测试与对账都读它。"""
        return sum(self._cents.values())

    def transfer(self, source: str, target: str, amount: int) -> None:
        """从 source 划 amount 给 target。余额不够就抛错且什么都不改；两次写之间没有可能失败的步骤。"""
        if self.balance(source) < amount:
            raise ServiceError(409, "insufficient_balance")
        self.balance(target)
        self._cents[source] -= amount
        self._cents[target] += amount


class LoanService:
    """对外的服务。一把锁罩住"贷款状态 + 账本"这一对：它们之间的联动才是需要原子的东西。"""

    def __init__(self, balances: dict[str, int]) -> None:
        self._ledger = Ledger(balances)
        self._book: dict[int, Loan] = {}
        self._serial = 1
        self._mutex = threading.Lock()  # 公开方法之间不互相调用，用不着可重入锁

    def balance(self, user: str) -> int:
        with self._mutex:
            return self._ledger.balance(user)

    def total_balance(self) -> int:
        """全部余额之和；放款与还款只在人与人之间搬钱，所以它在任何时刻都等于构造时的总和。"""
        with self._mutex:
            return self._ledger.total()

    def create(self, borrower: str, amount: int) -> dict:
        with self._mutex:
            require_amount(amount)
            self._ledger.balance(borrower)  # 只为确认借款人存在
            loan = Loan(self._serial, borrower, amount, amount)
            self._book[loan.id] = loan
            self._serial += 1  # 全部检查通过、贷款已入表之后才消耗编号
            return loan.snapshot()

    def get(self, loan_id: int) -> dict:
        with self._mutex:
            return self._find(loan_id).snapshot()

    def fund(self, loan_id: int, lender: str) -> dict:
        with self._mutex:
            loan = self._find(loan_id)
            self._ledger.balance(lender)  # 出借人存在
            loan.ensure_fundable(lender)  # 状态与身份，先于余额
            self._ledger.transfer(lender, loan.borrower, loan.principal)  # 最后一道检查，也是第一个写
            loan.activate(lender)  # 转账成功后状态才变，之间没有失败点
            return loan.snapshot()

    def repay(self, loan_id: int, borrower: str, amount: int) -> dict:
        """还款：先过五道检查（金额、贷款、归属、状态与超额、余额），再划转并扣减。"""
        with self._mutex:
            require_amount(amount)
            loan = self._find(loan_id)
            loan.ensure_repayable(borrower, amount)
            assert loan.lender is not None  # 仅为类型检查：active 的贷款一定有出借人
            self._ledger.transfer(borrower, loan.lender, amount)
            loan.reduce(amount)
            return loan.snapshot()

    def _find(self, loan_id: int) -> Loan:
        """调用方已持锁。编号不是 int（含 True、字符串）都按"不存在"处理：True 与 1 哈希相同，会误中第一笔贷款。"""
        loan = self._book.get(loan_id) if type(loan_id) is int else None
        if loan is None:
            raise ServiceError(404, "loan_not_found")
        return loan


if __name__ == "__main__":
    service = LoanService({"mia": 5, "noah": 500})
    loan = service.create("mia", 120)
    print(service.fund(loan["id"], "noah"))
    print(service.repay(loan["id"], "mia", 50))
    print(service.repay(loan["id"], "mia", 70)["status"])  # 还清：repaid
    print({user: service.balance(user) for user in ("mia", "noah")}, service.total_balance())
    for attempt in (lambda: service.fund(loan["id"], "noah"), lambda: service.repay(loan["id"], "mia", 71)):
        try:
            attempt()
        except ServiceError as error:  # 失败的调用：状态码、错误码，余额一分没动
            print(error.status, error.code, service.total_balance())
