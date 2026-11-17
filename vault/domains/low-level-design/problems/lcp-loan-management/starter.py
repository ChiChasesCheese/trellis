"""LedgerBridge 贷款服务（待修复）。公开 API 与 `solution.py` 一致，可以原样放进真实工作区的 `service.py`。

这份代码能跑，但有几处和下面的规则不符：它就是要你修的东西。

规则（每一条都有测试，金额一律是整数分）：
 1. 金额必须是恰好为 `int` 的正数；布尔、浮点、字符串、`None`、0、负数都抛 `ServiceError(400, "invalid_amount")`。
 2. `create(borrower, amount)`：先验金额，再验借款人存在（`404 user_not_found`）；成功才消耗编号，编号从 1 起；
    创建不动钱；返回 `{id, borrower, lender: None, principal, outstanding, status: "pending"}`。
 3. `get(loan_id)` 返回已存的贷款，编号不存在 `404 loan_not_found`；`balance(user)` 对不存在的用户 `404 user_not_found`。
 4. `fund(loan_id, lender)` 的检查顺序：贷款存在 → 出借人存在 → 贷款是 pending 且出借人不是借款人（否则 `409 invalid_state`）
    → 出借人余额不低于本金（否则 `409 insufficient_balance`，恰好等于本金可以）。
 5. 放款成功：本金从出借人划给借款人，记下出借人，状态变 active，未还金额仍等于本金。
 6. `repay(loan_id, borrower, amount)` 的检查顺序：金额 → 贷款存在 → 借款人对得上（`403 forbidden`）
    → 状态是 active 且金额不超过未还金额（`409 invalid_state`）→ 借款人余额够（`409 insufficient_balance`）。
 7. 还款成功：钱从借款人划给出借人，未还金额减少；减到 0 变 repaid，否则仍是 active。
 8. 失败不留痕迹：贷款、余额、编号计数都和调用前一样。
 9. 同一个实例上的所有方法并发安全；同一笔贷款并发放款恰好一次成功；所有余额之和恒定，没有负数。
10. 返回值是独立的快照；构造时复制传入的余额；多个实例互不相干。

Python 3.11，只用标准库。
"""

from __future__ import annotations

import threading


class ServiceError(Exception):
    """对外的服务错误：status 是 HTTP 状态码，code 是稳定的错误码字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


def _bad_amount() -> ServiceError:
    return ServiceError(400, "invalid_amount")


class LoanService:
    def __init__(self, balances: dict[str, int]) -> None:
        self._cents = dict(balances)  # 已经做对：构造时复制，外面再改也不影响
        self._book: dict[int, dict] = {}
        self._serial = 1
        self._mutex = threading.RLock()

    def _lookup(self, user: str) -> int:
        if user in self._cents:
            return self._cents[user]
        raise ServiceError(404, "user_not_found")

    def balance(self, user: str) -> int:
        with self._mutex:
            return self._lookup(user)

    def total_balance(self) -> int:
        with self._mutex:
            return sum(self._cents.values())

    def create(self, borrower: str, amount: int) -> dict:
        with self._mutex:
            # 已经做对：先验金额、再验借款人，全部通过才消耗编号
            if type(amount) is not int or amount < 1:
                raise _bad_amount()
            self._lookup(borrower)
            number = self._serial
            self._serial += 1
            row = {"id": number, "borrower": borrower, "lender": None, "principal": amount,
                   "outstanding": amount, "status": "pending"}
            # 缺陷：存进了编号加一的位置，用返回的 id 查不到
            self._book[number + 1] = row
            return dict(row)

    def get(self, loan_id: int) -> dict:
        with self._mutex:
            row = self._book.get(loan_id)
            if row is None:
                raise ServiceError(404, "loan_not_found")
            # 缺陷：把内部字典本体交了出去，调用方一改，服务里的贷款跟着变
            return row

    def fund(self, loan_id: int, lender: str) -> dict:
        with self._mutex:
            row = self.get(loan_id)
            funds = self._lookup(lender)
            # 缺陷：只拦了自己借给自己，没看贷款是不是 pending，同一笔贷款可以被放款多次
            if row["borrower"] == lender:
                raise ServiceError(409, "invalid_state")
            # 缺陷：比较方向反了，余额充足的人被拒，余额不够的人反而放行（余额还会变成负数）
            if funds > row["principal"]:
                raise ServiceError(409, "insufficient_balance")
            self._cents[lender] -= row["principal"]
            self._cents[row["borrower"]] += row["principal"]
            row.update(lender=lender, status="active")
            return dict(row)

    def repay(self, loan_id: int, borrower: str, amount: int) -> dict:
        """还款；按规则 6 的顺序检查后，划转并扣减未还金额。"""
        with self._mutex:
            if type(amount) is not int or amount < 1:
                raise _bad_amount()
            row = self.get(loan_id)
            if row["borrower"] != borrower:
                raise ServiceError(403, "forbidden")
            if row["status"] != "active" or amount > row["outstanding"]:
                raise ServiceError(409, "invalid_state")
            # 缺陷：比较方向反了，余额够还的人被拒，余额不够的人反而放行（余额还会变成负数）
            if self._cents[borrower] > amount:
                raise ServiceError(409, "insufficient_balance")
            self._cents[borrower] -= amount
            self._cents[row["lender"]] += amount
            row["outstanding"] -= amount
            if row["outstanding"] == 0:  # 已经做对：还清变 repaid，没还清仍是 active
                row["status"] = "repaid"
            return dict(row)
