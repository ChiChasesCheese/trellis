"""付款对账服务（Payment Reconciliation）：发票批量原子登记、三级匹配、幂等重放、全有或全无的付款批次。

设计（五行）：
1. 金额全程是整数分（cent）；`parse_cents` 只收 ASCII 数字，从不经过浮点数。
2. 匹配分三级：备注里的发票号（id）→ 金额完全相等（exact）→ 容差范围内（fuzzy）；
   同一级里按 (到期日, 金额差, 发票号) 取最小，所以结果是确定的。
3. `Ledger` 拥有全部可变状态（发票和幂等回执），并带一本撤销日志：`transaction()` 里出了错，
   就把这一批做过的结算和回执按相反顺序撤销；批次因此全有或全无。
4. `ReconciliationService` 只做两件事：先在锁外校验输入，再在同一把锁里执行；读、写、批次都走这把锁。
5. 所有会抛错的检查都排在该行第一次写之前，所以单行失败不留痕；返回值一律是新字典，和缓存互不相连。
"""

from __future__ import annotations

import re
import threading
from bisect import insort
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Any, NamedTuple

ID_MAX, KEY_MAX = 64, 64
MAX_DIGITS = 4300  # CPython 3.11 的 int() 对超过 4300 位的字符串会抛 ValueError；超过的一律当非法输入
MARKER = re.compile(r"paying (?:for|off):", re.IGNORECASE)  # 大小写按 re 的规则：i、I、İ、ı 等价
ISO_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


# --- errors:begin（真实工作区里 ServiceError 在 models.py，测试比较的是那个类）
class ServiceError(Exception):
    """对外的错误：status 是 HTTP 状态码，code 是稳定的字符串。"""

    def __init__(self, status: int, code: str) -> None:
        self.status, self.code = status, code
        super().__init__(code)


# --- errors:end


def _invalid() -> ServiceError:
    return ServiceError(400, "invalid_input")


def _is_int(value: object) -> bool:
    """`True` 是 int 的子类，但不是合法的宽限额。"""
    return isinstance(value, int) and not isinstance(value, bool)


def parse_cents(text: str) -> int:
    """正整数分：去首尾空白后只允许 ASCII 数字 0-9（前导零可以），零、符号、下划线、别种文字的数字都不行。"""
    text = text.strip()
    digits = text.lstrip("0")
    if not (text.isascii() and text.isdigit()) or not digits or len(digits) > MAX_DIGITS:
        raise _invalid()
    return int(digits)


def parse_label(text: str) -> str:
    """发票号与付款号：去首尾空白后长度 1..64。"""
    text = text.strip()
    if not 1 <= len(text) <= ID_MAX:
        raise _invalid()
    return text


def parse_due_date(text: str) -> str:
    """严格的 YYYY-MM-DD 且是真实存在的日历日；返回原字符串，因为同宽的 ISO 日期按字典序就是时间序。"""
    text = text.strip()
    try:
        if not ISO_DATE.fullmatch(text):
            raise ValueError(text)
        date.fromisoformat(text)
    except ValueError:
        raise _invalid() from None
    return text


class Tier(str, Enum):
    """三级匹配的名字，值就是返回体里的 `tier_used`。"""

    ID = "id"
    EXACT = "exact"
    FUZZY = "fuzzy"


class Invoice:
    """一张发票。状态由 `settled_by` 推出来，所以"已付款当且仅当有结算它的付款号"不可能被写坏。"""

    __slots__ = ("invoice_id", "due_date", "amount", "settled_by")

    def __init__(self, invoice_id: str, due_date: str, amount: int) -> None:
        self.invoice_id, self.due_date, self.amount = invoice_id, due_date, amount
        self.settled_by: str | None = None

    @property
    def unpaid(self) -> bool:
        return self.settled_by is None

    @property
    def order(self) -> tuple[str, str]:
        """列表顺序：到期日升序，再按发票号升序。"""
        return self.due_date, self.invoice_id

    @classmethod
    def parse(cls, entry: object) -> Invoice:
        """"发票号, 到期日, 金额"：按 ", " 切成恰好三段，每段去空白后各自校验。"""
        if not isinstance(entry, str):
            raise _invalid()
        parts = entry.split(", ")
        if len(parts) != 3:
            raise _invalid()
        invoice_id, due_date, amount = parts
        return cls(parse_label(invoice_id), parse_due_date(due_date), parse_cents(amount))

    def snapshot(self) -> dict[str, Any]:
        return {"invoice_id": self.invoice_id, "due_date": self.due_date, "amount_cents": self.amount,
                "status": "UNPAID" if self.unpaid else "PAID", "settled_by_payment_id": self.settled_by}


@dataclass(frozen=True, slots=True)
class PaymentRequest:
    """校验并解析后的一次付款请求。`fingerprint` 就是幂等比较的"同一个请求"。"""

    payment_id: str
    amount: int
    memo: str
    forgiveness: int
    key: str | None
    text: str  # 去首尾空白的整串付款文本

    @property
    def fingerprint(self) -> tuple[str, int]:
        return self.text, self.forgiveness

    @classmethod
    def parse(cls, payment: object, forgiveness: object = 0, key: object = None) -> PaymentRequest:
        if not isinstance(payment, str) or not _is_int(forgiveness) or forgiveness < 0:
            raise _invalid()
        if key is not None and not (isinstance(key, str) and 1 <= len(key) <= KEY_MAX):
            raise _invalid()
        parts = payment.split(", ", 2)  # 第三段是原样的备注：备注里的 ", " 保留
        if len(parts) < 2:
            raise _invalid()
        memo = parts[2] if len(parts) == 3 else ""
        return cls(parse_label(parts[0]), parse_cents(parts[1]), memo, forgiveness, key, payment.strip())

    @classmethod
    def from_row(cls, row: object) -> PaymentRequest:
        """批次里的一行：必须是字典，必须有 payment，只允许 payment、forgiveness、key 三个键。"""
        if not isinstance(row, dict) or "payment" not in row or not row.keys() <= {"payment", "forgiveness", "key"}:
            raise _invalid()
        return cls.parse(row["payment"], row.get("forgiveness", 0), row.get("key"))


class Receipt(NamedTuple):
    """一次已完成请求的回执：当初的指纹，以及当初的状态码和响应体（私有副本）。"""

    fingerprint: tuple[str, int]
    status: int
    body: dict[str, Any]


class Ledger:
    """全部可变状态：按 (到期日, 发票号) 排好序的发票、发票号索引、幂等回执，加一本撤销日志。

    不变量：发票号唯一；一张发票至多被结算一次；一个键至多一份回执。自己不加锁，锁归服务。
    """

    def __init__(self) -> None:
        self._rows: list[Invoice] = []
        self._by_id: dict[str, Invoice] = {}
        self._receipts: dict[str, Receipt] = {}
        self._undo: list[Callable[[], None]] | None = None

    # ---- 发票 ----
    def check_new(self, invoices: list[Invoice]) -> None:
        for invoice in invoices:
            if invoice.invoice_id in self._by_id:
                raise ServiceError(409, "duplicate_invoice")

    def add_all(self, invoices: list[Invoice]) -> None:
        """先检查全部、再写入全部：中途不会抛错，所以批次原子。"""
        self.check_new(invoices)
        for invoice in invoices:
            insort(self._rows, invoice, key=lambda row: row.order)
            self._by_id[invoice.invoice_id] = invoice

    def snapshot(self) -> list[dict[str, Any]]:
        return [invoice.snapshot() for invoice in self._rows]

    # ---- 事务 ----
    @contextmanager
    def transaction(self) -> Iterator[None]:
        """块里抛出任何异常，就把块里做过的结算和回执按相反顺序撤销，然后原样抛出。"""
        self._undo = []
        try:
            yield
        except BaseException:
            for undo in reversed(self._undo):
                undo()
            raise
        finally:
            self._undo = None

    def _journal(self, undo: Callable[[], None]) -> None:
        if self._undo is not None:
            self._undo.append(undo)

    # ---- 匹配 ----
    def _unpaid(self) -> Iterator[Invoice]:
        return (invoice for invoice in self._rows if invoice.unpaid)

    def _explicit(self, memo: str) -> Invoice | None:
        """第一级：从左到右扫每个标记，取标记后到下一个逗号的文字（去空白、保留大小写），第一个指向未付发票的号胜出。"""
        for marker in MARKER.finditer(memo):  # 位置取自原串，不能先 lower()：İ 小写后长度会变
            invoice = self._by_id.get(memo[marker.end():].split(",", 1)[0].strip())
            if invoice is not None and invoice.unpaid:
                return invoice
        return None

    def _closest(self, amount: int, spread: int) -> Invoice | None:
        """金额落在 [amount - spread, amount + spread] 里的未付发票中，按 (到期日, 金额差, 发票号) 取最小。"""
        found = [i for i in self._unpaid() if abs(i.amount - amount) <= spread]
        return min(found, key=lambda i: (i.due_date, abs(i.amount - amount), i.invoice_id), default=None)

    def match(self, request: PaymentRequest) -> tuple[Invoice, Tier] | None:
        explicit = self._explicit(request.memo)
        if explicit is not None:
            return explicit, Tier.ID
        exact = self._closest(request.amount, 0)
        if exact is not None:
            return exact, Tier.EXACT
        if request.forgiveness > 0:
            fuzzy = self._closest(request.amount, request.forgiveness)
            if fuzzy is not None:
                return fuzzy, Tier.FUZZY
        return None

    # ---- 一次付款 ----
    def reconcile(self, request: PaymentRequest) -> tuple[int, dict[str, Any]]:
        """幂等检查 → 匹配 → 结算 → 记回执；会抛错的只有第一步，且在任何写之前。"""
        if request.key is not None and request.key in self._receipts:
            receipt = self._receipts[request.key]
            if receipt.fingerprint != request.fingerprint:
                raise ServiceError(409, "idempotency_conflict")
            return 200, dict(receipt.body)  # 重放：不匹配、不改状态，给一份新拷贝

        hit = self.match(request)
        if hit is None:
            status = 200
            body: dict[str, Any] = {
                "status": "UNMATCHED", "payment_id": request.payment_id, "settled_invoice_id": None,
                "tier_used": None, "message": f"Payment {request.payment_id} could not be matched to any invoice"}
        else:
            invoice, tier = hit
            self._settle(invoice, request.payment_id)
            status = 201
            body = {
                "status": "MATCHED", "payment_id": request.payment_id, "settled_invoice_id": invoice.invoice_id,
                "tier_used": tier.value,
                "message": f"Payment {request.payment_id} paid {request.amount} for invoice "
                           f"{invoice.invoice_id} due on {invoice.due_date}"}
        if request.key is not None:
            self._remember(request.key, Receipt(request.fingerprint, status, dict(body)))
        return status, body

    def _settle(self, invoice: Invoice, payment_id: str) -> None:
        invoice.settled_by = payment_id
        self._journal(lambda: setattr(invoice, "settled_by", None))

    def _remember(self, key: str, receipt: Receipt) -> None:
        self._receipts[key] = receipt
        self._journal(lambda: self._receipts.pop(key, None))


class ReconciliationService:
    """公开接口。输入校验在锁外（纯函数），状态访问在同一把锁里；返回值都是新对象。"""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._ledger = Ledger()

    def register_invoices(self, invoices: list[str]) -> tuple[int, dict[str, Any]]:
        if not isinstance(invoices, list) or not invoices:
            raise _invalid()
        parsed: list[Invoice] = []
        seen: set[str] = set()
        for entry in invoices:  # 按输入顺序：格式错 400，批内重复 409，先遇到的赢
            invoice = Invoice.parse(entry)
            if invoice.invoice_id in seen:
                raise ServiceError(409, "duplicate_invoice")
            seen.add(invoice.invoice_id)
            parsed.append(invoice)
        with self._lock:
            self._ledger.add_all(parsed)  # 全部通过后才查账本里已有的号
        return 201, {"registered_count": len(parsed)}

    def reconcile_payment(self, payment: str, forgiveness: int = 0,
                          key: str | None = None) -> tuple[int, dict[str, Any]]:
        request = PaymentRequest.parse(payment, forgiveness, key)
        with self._lock:
            return self._ledger.reconcile(request)

    def list_invoices(self) -> tuple[int, list[dict[str, Any]]]:
        with self._lock:
            return 200, self._ledger.snapshot()

    def reconcile_batch(self, payments: list[dict[str, Any]]) -> tuple[int, dict[str, Any]]:
        if not isinstance(payments, list) or not payments:
            raise _invalid()
        rows = tuple(payments)  # 快照：调用方之后再改列表，不影响这一批
        with self._lock, self._ledger.transaction():  # 退出时先回滚、再放锁：别人看不到中间状态
            results = []
            for row in rows:  # 逐行：先校验这一行、再处理；第一个错误按行序胜出
                status, body = self._ledger.reconcile(PaymentRequest.from_row(row))
                results.append({"status": status, "body": body})
        return 200, {"results": results}


if __name__ == "__main__":
    service = ReconciliationService()
    print(service.register_invoices(["INV A, 2026-03-01, 100", "INV B, 2026-03-02, 100"]))
    print(service.reconcile_batch([
        {"payment": "p1, 1, paying for:INV A", "key": "retry-1"},
        {"payment": "p1, 1, paying for:INV A", "key": "retry-1"},
        {"payment": "p2, 100"},
    ]))
    print(service.list_invoices())
