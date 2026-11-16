"""销售报表（Sales Reporting）参考解：校验请求，再用参数化 SQL 在 SQLite 里算出一份报表。

设计（五行）：
1. `parse_report_request` 在碰数据库之前把请求体校验成冻结的 `ReportRequest`；任何不合规的字段都是 400 `invalid_request`。
2. 资格条件与请求筛选只写一次（`MATCHING`），四条查询共用同一段 WHERE，所以总数与三个排行永远看同一批文档。
3. 过滤、去重计数、分组、求和、排序、限量全在数据库里做；Python 只把结果行映射成响应字段。
4. 请求里的值一律是 `$name` 绑定参数，SQL 文本里只有表名（来自上下文）和固定的列名；连 `sale`、`active`、`termed` 这些常量也绑定，
   所以任何请求能带来的值（包括 `status` 的 "active"）都不会以字面量出现在语句里。
5. 排行的平局顺序写进 `ORDER BY`（数值降序，再按键升序），先排序再 `LIMIT`；四条查询共返回至多 `1 + 3k` 行。

`ServiceError`、`fail`、`reply`、`integer` 在真实工作区里由 `support.py` 提供；这里复制一份，让参考解可以独立运行。
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from typing import Any, NoReturn

# ---- 导入面开始：真实工作区里这一段换成 from support import ServiceError, fail, reply, integer ----


class ServiceError(Exception):
    """带状态码与错误代码的业务错误；适配器把它翻成 `{"error": code}`。"""

    def __init__(self, status: int, code: str) -> None:
        super().__init__(code)
        self.status, self.code = status, code


def fail(status: int, code: str) -> NoReturn:
    raise ServiceError(status, code)


def reply(status: int, value: Any, content_type: str = "application/json") -> tuple[int, str, bytes]:
    return status, content_type, json.dumps(value, ensure_ascii=False).encode()


def integer(value: Any) -> bool:
    """布尔在 Python 里是 int 的子类，必须显式排除。"""
    return isinstance(value, int) and not isinstance(value, bool)


# ---- 导入面结束 ----

DATE_SHAPE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")  # 先卡形状：3.11 的 fromisoformat 还收 20260101 和 2026-W01-1
FIRST_YEAR, LAST_YEAR = 2020, 2099
END_ONLY_SENTINEL = "2100-01-01"  # 只能做 end：让 2099-12-31 的销售也能被报表覆盖
DEFAULT_K, MAX_K = 10, 20
MAX_TEXT_LENGTH = 100
ROW_BUDGET_BASE = 32  # 一次请求所有查询返回的行数合计不得超过 32 + 3k
FIELDS = frozenset({"start", "end", "k", "status", "region", "item"})
STATUSES = ("active", "termed")
CONSTANTS = {"kind": "sale", "live": "active", "gone": "termed"}  # 语句里的常量，作为绑定参数传入；参数名不能含常量本身的字样

# 资格（type、日期、状态）与请求筛选：所有查询共用这一段。
# 日期或状态为 NULL 时比较结果是 NULL，行自然被过滤掉；`$x IS NULL OR …` 让"不筛选"也走同一条语句。
# `$kind`、`$live`、`$gone` 是常量 sale、active、termed，也走绑定：请求能带来的任何值都不会以字面量出现在语句里（参数名与列别名也不拼成这些词）。
MATCHING = """
    type = $kind
    AND saleDate >= $start AND saleDate < $end
    AND customerStatus IN ($live, $gone)
    AND ($status IS NULL OR customerStatus = $status)
    AND ($region IS NULL OR region = $region)
    AND ($item IS NULL OR itemName = $item)
"""


@dataclass(frozen=True, slots=True)
class ReportRequest:
    """校验之后的请求：日期是 YYYY-MM-DD 文本（定宽，文本顺序就是日期顺序）。"""

    start: str
    end: str
    k: int
    status: str | None
    region: str | None
    item: str | None

    def bindings(self) -> dict[str, Any]:
        """SQL 的命名参数；没用到的参数允许存在，所以四条查询共用一份。"""
        return {"start": self.start, "end": self.end, "k": self.k,
                "status": self.status, "region": self.region, "item": self.item}


@dataclass(frozen=True, slots=True)
class SalesReport:
    """一份报表：三个标量，三个排行（每项是 (键, 数值)，已经排好序并截到 k）。"""

    active_customers: int
    total_quantity: int
    total_spend_cents: int
    quantity_leaders: tuple[tuple[str, int], ...]
    spend_leaders: tuple[tuple[str, int], ...]
    item_leaders: tuple[tuple[str, int], ...]

    def as_response(self) -> dict[str, Any]:
        return {
            "active_customers": self.active_customers,
            "total_quantity": self.total_quantity,
            "total_spend_cents": self.total_spend_cents,
            "quantity_leaders": [{"customer_id": c, "quantity": n} for c, n in self.quantity_leaders],
            "spend_leaders": [{"customer_id": c, "spend_cents": n} for c, n in self.spend_leaders],
            "item_leaders": [{"item": i, "quantity": n} for i, n in self.item_leaders],
        }


def _invalid() -> NoReturn:
    fail(400, "invalid_request")


def _parse_date(value: Any, *, allow_sentinel: bool = False) -> str:
    if not isinstance(value, str) or not DATE_SHAPE.fullmatch(value):  # 形状不对（连空白、换行）一律 400
        _invalid()
    if allow_sentinel and value == END_ONLY_SENTINEL:
        return value
    try:
        parsed = date.fromisoformat(value)  # 2026-02-30 在这里抛 ValueError
    except ValueError:
        _invalid()
    if not FIRST_YEAR <= parsed.year <= LAST_YEAR:
        _invalid()
    return value


def _parse_text(value: Any) -> str | None:
    """可选的非空文本，至多 100 个码点；None 表示不筛选。"""
    if value is None:
        return None
    if not isinstance(value, str) or not 1 <= len(value) <= MAX_TEXT_LENGTH:
        _invalid()
    try:
        value.encode("utf-8")  # 孤立代理码点存不进 UTF-8 数据库，也就匹配不到任何行：当作非法
    except UnicodeEncodeError:
        _invalid()
    return value


def parse_report_request(body: Any) -> ReportRequest:
    """请求体 → `ReportRequest`；先于一切数据库访问。"""
    if not isinstance(body, dict) or not FIELDS.issuperset(body):
        _invalid()
    if "start" not in body or "end" not in body:
        _invalid()
    start = _parse_date(body["start"])
    end = _parse_date(body["end"], allow_sentinel=True)
    if end <= start:
        _invalid()
    k = body["k"] if "k" in body else DEFAULT_K  # 显式 null 不是缺省：下一行会拒绝它
    if not integer(k) or not 1 <= k <= MAX_K:
        _invalid()
    status = body.get("status")
    if status is not None and status not in STATUSES:
        _invalid()
    return ReportRequest(start, end, k, status, _parse_text(body.get("region")), _parse_text(body.get("item")))


class ReportQueries:
    """把一个 `ReportRequest` 变成四条参数化查询，并把结果行映射成 `SalesReport`。"""

    def __init__(self, context: Any) -> None:
        self._query = context.query
        self._table = context.keyspace  # 受信任的带引号表名，可以拼进语句

    def run(self, request: ReportRequest) -> SalesReport:
        scalars = self._rows(f"""
            SELECT COUNT(DISTINCT CASE WHEN customerStatus = $live THEN customerId END) AS live_customers,
                   COALESCE(SUM(itemQuantity), 0) AS total_quantity,
                   COALESCE(SUM(totalPrice), 0) AS total_spend_cents
            FROM {self._table} WHERE {MATCHING}""", request)[0]
        return SalesReport(
            scalars["live_customers"], scalars["total_quantity"], scalars["total_spend_cents"],
            self._leaders(request, "customerId", "itemQuantity"),
            self._leaders(request, "customerId", "totalPrice"),
            self._leaders(request, "itemName", "itemQuantity"),
        )

    def _leaders(self, request: ReportRequest, key: str, measure: str) -> tuple[tuple[str, int], ...]:
        """按 key 分组求和；数值降序、再按 key 升序（BINARY 排序规则 = UTF-8 字节序），之后才 LIMIT。"""
        rows = self._rows(f"""
            SELECT {key} AS leader, SUM({measure}) AS total
            FROM {self._table} WHERE {MATCHING}
            GROUP BY {key} ORDER BY total DESC, {key} ASC LIMIT $k""", request)
        return tuple((row["leader"], row["total"]) for row in rows)

    def _rows(self, statement: str, request: ReportRequest) -> list[dict[str, Any]]:
        return self._query(statement, {**request.bindings(), **CONSTANTS})


def handle(request: dict[str, Any], context: Any) -> tuple[int, str, bytes]:
    """`POST /report`；其余方法与路径都是 404。数据库异常原样上抛，由适配器翻成 500。"""
    if request["method"] != "POST" or request["path"] != "/report":
        fail(404, "not_found")
    parsed = parse_report_request(request.get("json"))
    return reply(200, ReportQueries(context).run(parsed).as_response())


if __name__ == "__main__":  # 演示：内存库里放五行销售，打印一份 k=2 的报表
    import sqlite3
    from types import SimpleNamespace

    demo = sqlite3.connect(":memory:")
    demo.row_factory = sqlite3.Row
    demo.execute("CREATE TABLE sales (type TEXT, customerId TEXT, customerName TEXT, customerStatus TEXT, itemName TEXT,"
                 " itemQuantity INTEGER, totalPrice INTEGER, saleDate TEXT, region TEXT)")
    demo.executemany("INSERT INTO sales VALUES ('sale', ?, NULL, ?, ?, ?, ?, ?, ?)", [
        ("u1", "active", "tea", 4, 800, "2026-03-02", "east"), ("u1", "termed", "tea", 1, 150, "2026-03-09", "east"),
        ("u2", "termed", "cake", 6, 1200, "2026-03-10", "west"), ("u3", "active", "cake", 6, 900, "2026-03-15", None),
        ("u3", "active", "tea", 2, 300, "2026-03-31", "east")])
    demo_context = SimpleNamespace(keyspace='"sales"', query=lambda sql, params: [dict(r) for r in demo.execute(sql, params)])
    print(handle({"method": "POST", "path": "/report", "json": {"start": "2026-03-01", "end": "2026-04-01", "k": 2}},
                 demo_context)[2].decode())
