"""库存 API 修复（Stockroom Inventory）：待修的服务（InventoryService 里有缺陷，集合与辅助函数是固定的）。

产品规则（编号即测试编号；原版跑在 MongoDB 上，这里的存储是标准库 sqlite3，语义对齐，见题解）：

1. 身份：`user` 必须是 trim 之后非空的字符串，否则 401 unauthorized；存进库的 owner 是原样的 user（含首尾空白）。
2. 路由：`/items` 与 `/items/{id}`；其余路径 404 not_found。id 必须恰好 24 个十六进制字符（大小写都行，返回一律小写），
   否则 400 invalid_id；合法路径上不支持的方法 405 method_not_allowed。检查顺序：身份 → 路由 → id → 方法。
3. 错误体恒为 `{"error": 代码}`。
4. 创建：body 恰好是 {sku, name, quantity}；sku 为 1..24 位大写字母、数字、连字符；name 去首尾空白后按 UTF-16 码元数
   计 1..80，存去空白后的名字；quantity 为 0..1000000 的整数（int、整数值的 float、整数值的 Decimal 都行，bool、
   字符串、None 不行）。任何不合格都是 400 invalid_input；成功先写库再返回 201 与库里读出的
   {id, owner, sku, name, quantity, version}，version 为 1；owner、id、version 不由调用方给。
5. 读：`GET /items` 只返回自己的条目，按 sku 升序再按 id 升序，可为空；`GET /items/{id}` 返回一条；
   不存在与别人的条目都是 404 item_not_found。
6. 删：只删自己的，成功 `Response(204, None)`；再删一次 404。
7. 改：body 的键只能是 name、quantity、version，version 必填且为 1..9223372036854775806 的整数，name 与 quantity 至少一个。
   先校验完整个请求（400），再按 owner+id 找条目（404），最后比较版本（409 version_conflict）。
   成功返回更新后的条目，version 加一（值没变也加）；任何失败都不改任何字段。owner、sku、id 永不改变。
8. 唯一：同一个 owner 下 sku 唯一，重复创建 409 sku_conflict 且不新增条目，并发也一样；不同 owner 可用同一个 sku。
9. 存储错误：重复键（code 11000）409 sku_conflict，模式校验失败（code 121）400 invalid_input，其余 503 storage_unavailable；
   不泄露异常细节。
"""


from __future__ import annotations

import math
import re
import secrets
import sqlite3
import threading
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

# 题目规定的"空白"是 ECMAScript 那一套：str.strip() 默认会多剥 0x1c-0x1f 与 0x85，又剥不掉 0xfeff，只能自己列码点
BLANK_CODEPOINTS = (
    *range(0x09, 0x0E), 0x20, 0xA0, 0x1680, *range(0x2000, 0x200B), 0x2028, 0x2029, 0x202F, 0x205F, 0x3000, 0xFEFF,
)
WHITESPACE = "".join(map(chr, BLANK_CODEPOINTS))
SKU = re.compile(r"[A-Z0-9-]{1,24}")  # 与 fullmatch 配用：`$` 会放过结尾的换行
ITEM_ID = re.compile(r"[0-9a-fA-F]{24}")
ITEM_PATH = re.compile(r"/items/([^/]+)")
MAX_VERSION = 9223372036854775806  # 留一位给 +1，仍在 64 位有符号整数之内
FIELDS = ("owner", "sku", "name", "quantity", "version")
COLUMNS = ("id", *FIELDS)
STORE_ERRORS = {11000: (409, "sku_conflict"), 121: (400, "invalid_input")}  # 错误码 → 状态与代码


@dataclass
class Response:
    status: int
    body: Any


def problem(status: int, code: str) -> Response:
    return Response(status, {"error": code})


def trim(value: str) -> str:
    return value.strip(WHITESPACE)


def utf16_length(text: str) -> int:
    return len(text.encode("utf-16-le", errors="surrogatepass")) // 2


def valid_name(value: Any) -> str | None:
    """合格就返回去空白后的名字，否则 None。"""
    name = trim(value) if isinstance(value, str) else ""
    return name if 1 <= utf16_length(name) <= 80 else None


def whole_number(value: Any, minimum: int, maximum: int) -> int | None:
    """只认 int、整数值的 float、整数值的 Decimal；bool、字符串、None 都不是数。落在 [minimum, maximum] 才返回 int。"""
    kind = type(value)  # 用 type() 而不是 isinstance：bool 是 int 的子类，必须挡在外面
    if kind is int:
        integral = True
    elif kind is float:
        integral = math.isfinite(value) and value.is_integer()
    elif kind is Decimal:
        integral = value.is_finite() and value == value.to_integral_value()
    else:
        return None
    if not integral or not minimum <= value <= maximum:
        return None
    return int(value)


class StoreError(Exception):
    """存储层失败；code 对应 MongoDB 的错误码，None 表示未分类。"""

    code: int | None = None


class DuplicateKeyError(StoreError):
    code = 11000


class SchemaViolation(StoreError):
    code = 121


# 集合的模式：写入前逐字段检查，等价于 MongoDB 的 $jsonSchema 验证器
SCHEMA = {
    "owner": lambda v: isinstance(v, str) and len(v) >= 1,
    "sku": lambda v: isinstance(v, str) and SKU.fullmatch(v) is not None,
    "name": lambda v: isinstance(v, str) and 1 <= len(v) <= 80,
    "quantity": lambda v: type(v) is int and 0 <= v <= 1000000,
    "version": lambda v: type(v) is int and v >= 1,
}


class ItemCollection:
    """库存集合：每个方法是一次原子操作，条件与修改在同一条语句里完成。

    查询是 {字段: 值} 的字典，和 MongoDB 一样由调用方负责把 owner 写进去：集合本身不知道"当前用户"。
    """

    def __init__(self, path: str = ":memory:") -> None:
        self._lock = threading.Lock()  # 同一连接上的语句串行；跨连接靠数据库自己的锁
        self._db = sqlite3.connect(path, check_same_thread=False, isolation_level=None, timeout=10)
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS items (id TEXT PRIMARY KEY, owner TEXT NOT NULL, sku TEXT NOT NULL,"
            " name TEXT NOT NULL, quantity INTEGER NOT NULL, version INTEGER NOT NULL, UNIQUE (owner, sku))"
        )

    def _run(self, sql: str, args: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        try:
            with self._lock:
                cursor = self._db.execute(sql, args)
                columns = [c[0] for c in cursor.description or ()]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except sqlite3.IntegrityError as error:
            raise DuplicateKeyError(str(error)) from None
        except UnicodeEncodeError as error:  # 孤立代理项存不进去
            raise SchemaViolation(str(error)) from None
        except sqlite3.Error as error:
            raise StoreError(str(error)) from None

    @staticmethod
    def _where(query: dict[str, Any]) -> tuple[str, tuple[Any, ...]]:
        if not set(query) <= set(COLUMNS):  # 列名只来自白名单，值一律绑定参数
            raise StoreError("unknown field in query")
        return " AND ".join(f"{column} = ?" for column in query) or "1 = 1", tuple(query.values())

    def insert(self, doc: dict[str, Any]) -> None:
        if set(doc) != set(COLUMNS) or not all(SCHEMA[f](doc[f]) for f in FIELDS):
            raise SchemaViolation("document failed validation")
        self._run("INSERT INTO items VALUES (?, ?, ?, ?, ?, ?)", tuple(doc[c] for c in COLUMNS))

    def find_one(self, query: dict[str, Any]) -> dict[str, Any] | None:
        where, args = self._where(query)
        rows = self._run(f"SELECT * FROM items WHERE {where}", args)
        return rows[0] if rows else None

    def find(self, query: dict[str, Any]) -> list[dict[str, Any]]:
        where, args = self._where(query)
        return self._run(f"SELECT * FROM items WHERE {where} ORDER BY sku, id", args)

    def find_one_and_update(self, query: dict[str, Any], changes: dict[str, Any]) -> dict[str, Any] | None:
        """条件与修改在一条语句里：命中就改 changes 并把 version 加一，返回改后的行；没命中返回 None。"""
        if not changes or not set(changes) <= {"name", "quantity"} or not all(SCHEMA[f](v) for f, v in changes.items()):
            raise SchemaViolation("update failed validation")
        where, args = self._where(query)
        assignments = ", ".join(f"{column} = ?" for column in changes)
        rows = self._run(
            f"UPDATE items SET {assignments}, version = version + 1 WHERE {where} RETURNING *",
            (*changes.values(), *args),
        )
        return rows[0] if rows else None

    def delete_one(self, query: dict[str, Any]) -> bool:
        where, args = self._where(query)
        return bool(self._run(f"DELETE FROM items WHERE {where} RETURNING id", args))

    def close(self) -> None:
        self._db.close()


def initialize_items(path: str = ":memory:") -> ItemCollection:
    """建好表与 (owner, sku) 唯一约束再返回集合，对应原版的 initialize_items。"""
    return ItemCollection(path)


def view(row: dict[str, Any]) -> dict[str, Any]:
    return {"id": row["id"], **{field: row[field] for field in FIELDS}}


class InventoryService:
    """待修：这个服务能跑，但有好几处缺陷。"""

    def __init__(self, collection: ItemCollection) -> None:
        self.collection = collection

    def handle(self, method: str, path: str, user: str | None, body: Any = None) -> Response:
        if not isinstance(user, str) or user == "":
            return problem(401, "unauthorized")
        item_id = None
        if path != "/items":
            found = ITEM_PATH.fullmatch(path)
            if found is None:
                return problem(404, "not_found")
            if ITEM_ID.fullmatch(found[1]) is None:
                return problem(400, "invalid_id")
            item_id = found[1]
        try:
            if item_id is None and method == "POST":
                return self._create(user, body)
            if item_id is None and method == "GET":
                return Response(200, [view(row) for row in self.collection.find({})])
            if item_id is not None and method == "GET":
                row = self.collection.find_one({"id": item_id})
                return Response(200, view(row)) if row else problem(404, "item_not_found")
            if item_id is not None and method == "PATCH":
                return self._update(item_id, body)
            if item_id is not None and method == "DELETE":
                gone = self.collection.delete_one({"id": item_id})
                return Response(204, None) if gone else problem(404, "item_not_found")
            return problem(405, "method_not_allowed")
        except StoreError:
            return problem(503, "storage_unavailable")

    def _create(self, user: str, body: Any) -> Response:
        if not isinstance(body, dict) or body.keys() != {"sku", "name", "quantity"}:
            return problem(400, "invalid_input")
        stock = whole_number(body["quantity"], 0, 1000000) or 0  # 数量不合格被悄悄当成 0
        name = valid_name(body["name"])
        sku = body["sku"]
        if name is None or not (isinstance(sku, str) and SKU.fullmatch(sku)):
            return problem(400, "invalid_input")
        draft = {"id": secrets.token_hex(12), "owner": user, "sku": sku, "name": name, "quantity": stock, "version": 1}
        return Response(201, view(draft))

    def _update(self, item_id: str, body: Any) -> Response:
        if not isinstance(body, dict) or not set(body) <= {"name", "quantity", "version"}:
            return problem(400, "invalid_input")
        changes: dict[str, Any] = {}
        if "name" in body:
            new_name = valid_name(body["name"])
            if new_name is None:
                return problem(400, "invalid_input")
            changes["name"] = new_name
        if "quantity" in body:
            new_quantity = whole_number(body["quantity"], 0, 1000000)
            if new_quantity is None:
                return problem(400, "invalid_input")
            changes["quantity"] = new_quantity
        row = self.collection.find_one({"id": item_id})
        if row is None:
            return problem(404, "item_not_found")
        if row["version"] != body.get("version"):
            return problem(409, "version_conflict")
        self.collection.find_one_and_update({"id": item_id}, changes)
        return Response(200, view(row))
