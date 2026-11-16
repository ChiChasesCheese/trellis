"""销售报表练习骨架。公开 API 与 `solution.py` 一致：`handle(request, context)` 就是真实工作区 `service.py` 里要补全的函数。
`ServiceError`、`fail`、`reply`、`integer` 在真实工作区里来自 `support.py`，这里复制一份让骨架可以独立导入。

数据：一张 `sales` 表，每行是一次购买（一个客户可以有很多行）。列：`type`、`customerId`、`customerName`、`customerStatus`
（`active` 或 `termed`，记在这一笔销售上）、`itemName`、`itemQuantity`（整数）、`totalPrice`（这一笔的总价，整数分，不是单价）、
`saleDate`（`YYYY-MM-DD` 文本）、`region`（可为空）。文本列按 BINARY 排序规则比较，数量与金额是 INTEGER。

上下文：`context.query(statement, parameters)` 返回字典行的列表；语句用 `$name` 占位符，参数字典的键不带 `$`，没用到的参数可以留着；
`context.keyspace` 是受信任的带引号表名（`"sales"`），可以拼进语句；请求里的值一律走绑定参数。数据库出错时 `query` 抛异常。

产品规则（逐条都有测试）：
 1. 只有 `POST /report` 有效；其余方法与路径（含 `/report/`）返回 404 `{"error": "not_found"}`，先于任何请求体检查。
 2. 请求体必须是 JSON 对象（`request["json"]`）；出现未知字段、或体不是对象，一律 400 `{"error": "invalid_request"}`。
 3. `start` 必填：形如 `YYYY-MM-DD`（定宽、ASCII 数字）、真实存在的日期、年份 2020–2099；含起点。
 4. `end` 必填：同上，或者恰好是 `2100-01-01`（只能做 end，让 2099-12-31 的销售也能被覆盖）；不含终点；必须晚于 `start`。
 5. `k`：整数 1–20，缺省为 10。显式 null、布尔、小数（如 1.5）、字符串都是 400；`1`、`1.0`、`1e0` 解码后都是整数 1，合法。
 6. `status`：缺省或 null 表示两种资格状态都要；否则必须恰好是 `"active"` 或 `"termed"`（区分大小写）。
 7. `region`、`item`：缺省或 null 表示不筛选；否则必须是非空文本、至多 100 个码点，按字面精确匹配，区分大小写，不去空白，
    `%`、`_`、引号、SQL 语法都只是普通字符。给了具体 `region` 就不匹配缺失或 null 的地区。
 8. 资格：只有 `type` 为 `sale`、日期非空、状态是 `active` 或 `termed` 的行参与；缺日期、缺状态或未知状态的行永远不算。
 9. 所有筛选（日期区间、状态、地区、商品）对报表的每个部分生效。
10. `active_customers`：匹配行里状态为 `active` 的不同 `customerId` 个数；一个客户多条 active 销售只算一次；
    状态筛选为 `termed` 时是 0。按销售行的状态算，不推断客户"最新状态"。
11. `total_quantity` 与 `total_spend_cents` 是匹配行的 `itemQuantity`、`totalPrice` 各自的和；两者独立，绝不把价格乘以数量。
12. `quantity_leaders`：按 `customerId` 分组，数量降序、再按 `customerId` 升序，取前 k 个，每项 `{"customer_id", "quantity"}`。
13. `spend_leaders`：按 `customerId` 分组，金额降序、再按 `customerId` 升序，取前 k 个，每项 `{"customer_id", "spend_cents"}`。
14. `item_leaders`：按 `itemName` 分组，数量降序、再按商品名升序，取前 k 个，每项 `{"item", "quantity"}`。
15. 升序指 UTF-8 字节序，不做区域或大小写折叠；先按平局顺序排序，再截断到 k。
16. 没有匹配行时三个标量是 0，三个数组是空数组。
17. 过滤、去重计数、分组、求和、排序、限量都在数据库里做，不把销售文档拉回 Python 里算。
    请求里的值，连同语句里的常量 `sale`、`active`、`termed`，都用绑定参数传入；任何请求能带来的值都不以字面量出现在语句文本里。
18. 一次请求所有查询返回的行数合计至多 `32 + 3 * k`。
19. 响应是 HTTP 200，字段如上；校验失败在访问数据库之前；数据库异常不要吞掉，也不要把内部细节写进响应。
"""

from __future__ import annotations

import json
from dataclasses import dataclass
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


@dataclass(frozen=True, slots=True)
class ReportRequest:
    """校验之后的请求。"""

    start: str
    end: str
    k: int
    status: str | None
    region: str | None
    item: str | None

    def bindings(self) -> dict[str, Any]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class SalesReport:
    """一份报表：三个标量，三个排行。"""

    active_customers: int
    total_quantity: int
    total_spend_cents: int
    quantity_leaders: tuple[tuple[str, int], ...]
    spend_leaders: tuple[tuple[str, int], ...]
    item_leaders: tuple[tuple[str, int], ...]

    def as_response(self) -> dict[str, Any]:
        raise NotImplementedError


def parse_report_request(body: Any) -> ReportRequest:
    """请求体 → `ReportRequest`；非法就 `fail(400, "invalid_request")`。"""
    raise NotImplementedError


class ReportQueries:
    """把一个 `ReportRequest` 变成参数化查询，并把结果行映射成 `SalesReport`。"""

    def __init__(self, context: Any) -> None:
        raise NotImplementedError

    def run(self, request: ReportRequest) -> SalesReport:
        raise NotImplementedError


def handle(request: dict[str, Any], context: Any) -> tuple[int, str, bytes]:
    """`POST /report`；其余方法与路径都是 404。"""
    raise NotImplementedError
