---
tags:
  - lld/lcproject
---

# 库存 API 修复（Inventory API）

**这个项目要做什么。** 修复 MongoDB 后端的库存接口：真正持久化并返回实际存储的数据、每次请求鉴权并按所有者限定读写删、版本号原子校验递增、同一所有者 SKU 唯一、存储错误映射到正确状态码。

## 设计要点

库存 API 修复（Stockroom Inventory）：参考解。

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

## 考点与卡片

- **检查顺序固定：身份 401、路由 404、id 400、方法 405，之后才看请求体**：[[lcp-stockroom-inventory-contract-rules]]
- **身份是去空白后非空的字符串；owner 原样保存，首尾空格也算不同用户**：[[lcp-stockroom-inventory-contract-rules]]
- **错误体恒为 {error: 代码}，不放异常文本和堆栈**：[[lcp-stockroom-inventory-contract-rules]]、[[lcp-stockroom-inventory-reflection-concurrent-uniqueness]]
- **id 恰好 24 位十六进制，大小写都收，返回一律小写**：[[lcp-stockroom-inventory-contract-rules]]
- **畸形 id 的 400 先于 405：方法放在最后分派**：[[lcp-stockroom-inventory-contract-rules]]
- **SKU 用 fullmatch：match 加 $ 会放过结尾的换行**：[[lcp-stockroom-inventory-contract-rules]]
- **名字去 ECMAScript 空白后按 UTF-16 码元数 1 到 80，存去空白后的名字**：[[lcp-stockroom-inventory-contract-rules]]
- **str.strip() 的字符表与 ECMAScript 不同：多剥 0x85、不剥 U+FEFF**：[[lcp-stockroom-inventory-contract-rules]]
- **数字：int、整数值 float、整数值 Decimal 算数；布尔、字符串、None 不算，用 type 不用 isinstance**：[[lcp-stockroom-inventory-contract-rules]]
- **非法数量不能悄悄变成 0：x or 0 把 None 和合法的 0 混为一谈**：[[lcp-stockroom-inventory-contract-rules]]
- **创建的键恰好是 sku、name、quantity；owner、id、version 不由调用方给**：[[lcp-stockroom-inventory-contract-rules]]
- **先写库再回 201，返回库里读出的值，不是自己拼的字典**：[[lcp-stockroom-inventory-contract-rules]]、[[lcp-stockroom-inventory-state-and-invariant]]
- **构造字典、插入、更新是三件事：内存、可能被拒的写入、条件修改**：[[lcp-stockroom-inventory-state-and-invariant]]
- **每个读、改、删的查询都带 owner；别人的与不存在同形，都是 404**：[[lcp-stockroom-inventory-contract-rules]]、[[lcp-stockroom-inventory-state-and-invariant]]
- **别人的条目返回 404 而不是 403，否则泄露 id 是否存在**：[[lcp-stockroom-inventory-contract-rules]]
- **列表只含自己的，按 sku 升序再 id 升序；空列表是 200**：[[lcp-stockroom-inventory-contract-rules]]
- **删除返回 204 且正文是 None，重复删除 404，删后 SKU 可复用**：[[lcp-stockroom-inventory-contract-rules]]
- **更新的键只能是 name、quantity、version；version 必填，至少改一项**：[[lcp-stockroom-inventory-contract-rules]]
- **版本范围 1 到 9223372036854775806：留一位给加一，浮点形式在边界上越界**：[[lcp-stockroom-inventory-contract-rules]]
- **更新顺序：先校验整个请求 400，再找自己的条目 404，最后比版本 409**：[[lcp-stockroom-inventory-contract-rules]]
- **版本检查与加一在同一次库操作里：条件 owner、id、version，修改带 version + 1**：[[lcp-stockroom-inventory-contract-rules]]、[[lcp-stockroom-inventory-state-and-invariant]]、[[lcp-stockroom-inventory-reflection-concurrent-uniqueness]]
- **先读版本再写有窗口：并发两个请求都通过比较，都成功**：[[lcp-stockroom-inventory-state-and-invariant]]、[[lcp-stockroom-inventory-reflection-concurrent-uniqueness]]
- **值没变的更新也要加一版本；失败的更新不改任何字段与版本**：[[lcp-stockroom-inventory-contract-rules]]、[[lcp-stockroom-inventory-state-and-invariant]]
- **更新返回改后的文档，不是读出来的旧文档（RETURNING 或 return_document=AFTER）**：[[lcp-stockroom-inventory-state-and-invariant]]
- **更新没命中后按 owner 再查一次：在是 409，不在是 404**：[[lcp-stockroom-inventory-reflection-concurrent-uniqueness]]
- **唯一性交给 (owner, sku) 唯一索引：直接插入，不先查后插**：[[lcp-stockroom-inventory-contract-rules]]、[[lcp-stockroom-inventory-reflection-concurrent-uniqueness]]
- **不同 owner 可以用同一个 SKU；条目删除后 SKU 可复用**：[[lcp-stockroom-inventory-state-and-invariant]]
- **错误按码映射：11000 是 409，121 是 400，其余是 503；不按消息文本**：[[lcp-stockroom-inventory-contract-rules]]、[[lcp-stockroom-inventory-reflection-concurrent-uniqueness]]
- **库的模式校验只是最后一道网：放过结尾换行、按字符数名字、拒绝整数值浮点**：[[lcp-stockroom-inventory-contract-rules]]
- **进程内的锁和 GIL 管不到多进程：裁决放在数据库里**：[[lcp-stockroom-inventory-state-and-invariant]]、[[lcp-stockroom-inventory-reflection-concurrent-uniqueness]]
- **先把请求解析成合格的值再碰库：解析不过返回 None，失败不留痕**：[[lcp-stockroom-inventory-contract-rules]]
- **孤立代理项不能编码成 UTF-8：当作 400 而不是让异常逃出去**：[[lcp-stockroom-inventory-contract-rules]]
- **增量调整不幂等：操作号加唯一约束，流水与改数量同一个事务**：[[lcp-stockroom-inventory-reflection-retry-safe-adjustments]]
- **设置绝对值天然安全：重发得同一结果，配合版本重发得 409**：[[lcp-stockroom-inventory-reflection-retry-safe-adjustments]]
- **扣减的下限写进更新条件：quantity 不小于扣减量，不先读后判断**：[[lcp-stockroom-inventory-reflection-retry-safe-adjustments]]
- **屏障并发测试：十六个线程同版本更新，恰好一个 200，断言不变量而不是时间**：[[lcp-stockroom-inventory-reflection-concurrent-uniqueness]]
- **多个服务实例连同一个数据库的测试，证明裁决在库里而不在进程里**：[[lcp-stockroom-inventory-reflection-concurrent-uniqueness]]
- **故障注入：让某个库操作抛出指定错误码，断言状态码与错误体**：[[lcp-stockroom-inventory-contract-rules]]
- **指挥智能体：先让它只列规则与代码的差异，一类缺陷一个失败测试，不接受改测试迁就代码**：[[lcp-stockroom-inventory-contract-rules]]
- **测试只连临时库并只删自己建的库：别让智能体把测试指向真实数据**

## 参考解

```python
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


@dataclass(frozen=True)
class NewItem:
    """通过校验的创建请求。"""

    sku: str
    name: str
    quantity: int

    @classmethod
    def parse(cls, body: Any) -> NewItem | None:
        if not isinstance(body, dict) or body.keys() != {"sku", "name", "quantity"}:
            return None
        sku, name = body["sku"], valid_name(body["name"])
        quantity = whole_number(body["quantity"], 0, 1000000)
        if not isinstance(sku, str) or not SKU.fullmatch(sku) or name is None or quantity is None:
            return None
        return cls(sku, name, quantity)


@dataclass(frozen=True)
class ItemPatch:
    """通过校验的更新请求：版本必填，名字与数量至少一个。"""

    version: int
    name: str | None = None
    quantity: int | None = None

    @classmethod
    def parse(cls, body: Any) -> ItemPatch | None:
        if not isinstance(body, dict) or set(body) - {"name", "quantity", "version"}:
            return None
        if not {"name", "quantity"} & body.keys():
            return None
        version = whole_number(body.get("version"), 1, MAX_VERSION)
        name = valid_name(body["name"]) if "name" in body else None
        quantity = whole_number(body["quantity"], 0, 1000000) if "quantity" in body else None
        if version is None or ("name" in body and name is None) or ("quantity" in body and quantity is None):
            return None
        return cls(version, name, quantity)

    def changes(self) -> dict[str, Any]:
        """要写的字段：只含请求里给了的。"""
        given = {"name": self.name, "quantity": self.quantity}
        return {field: value for field, value in given.items() if value is not None}


def view(row: dict[str, Any]) -> dict[str, Any]:
    return {"id": row["id"], **{field: row[field] for field in FIELDS}}


class InventoryService:
    def __init__(self, collection: ItemCollection) -> None:
        self.collection = collection

    def handle(self, method: str, path: str, user: str | None, body: Any = None) -> Response:
        signed_in = isinstance(user, str) and bool(trim(user))
        if not signed_in:
            return problem(401, "unauthorized")
        item_id = None
        if path != "/items":
            match = ITEM_PATH.fullmatch(path)
            if match is None:
                return problem(404, "not_found")
            if ITEM_ID.fullmatch(match[1]) is None:
                return problem(400, "invalid_id")
            item_id = match[1].lower()
        handler = {
            (False, "POST"): self._create,
            (False, "GET"): self._list,
            (True, "GET"): self._get,
            (True, "PATCH"): self._update,
            (True, "DELETE"): self._delete,
        }.get((item_id is not None, method))
        if handler is None:
            return problem(405, "method_not_allowed")
        try:
            return handler(user, item_id, body)
        except StoreError as error:
            return problem(*STORE_ERRORS.get(error.code, (503, "storage_unavailable")))

    def _create(self, user: str, _item_id: None, body: Any) -> Response:
        new = NewItem.parse(body)
        if new is None:
            return problem(400, "invalid_input")
        item_id = secrets.token_hex(12)
        self.collection.insert(
            {"id": item_id, "owner": user, "sku": new.sku, "name": new.name, "quantity": new.quantity, "version": 1}
        )
        return self._found(user, item_id, 201)  # 返回库里读出的，而不是自己拼的

    def _list(self, user: str, _item_id: None, _body: Any) -> Response:
        return Response(200, [view(row) for row in self.collection.find({"owner": user})])

    def _get(self, user: str, item_id: str, _body: Any) -> Response:
        return self._found(user, item_id, 200)

    def _found(self, user: str, item_id: str, status: int) -> Response:
        row = self.collection.find_one({"owner": user, "id": item_id})
        return Response(status, view(row)) if row else problem(404, "item_not_found")

    def _update(self, user: str, item_id: str, body: Any) -> Response:
        patch = ItemPatch.parse(body)  # 整个请求先校验完，再碰库
        if patch is None:
            return problem(400, "invalid_input")
        query = {"owner": user, "id": item_id}
        row = self.collection.find_one_and_update({**query, "version": patch.version}, patch.changes())
        if row is not None:
            return Response(200, view(row))
        # 没改到：不存在或是别人的（404），还是版本不对（409），只有按 owner 再查一次才分得清
        return problem(409, "version_conflict") if self.collection.find_one(query) else problem(404, "item_not_found")

    def _delete(self, user: str, item_id: str, _body: Any) -> Response:
        if self.collection.delete_one({"owner": user, "id": item_id}):
            return Response(204, None)
        return problem(404, "item_not_found")
```

## 测试覆盖（37 个）

- `test_create_then_read_back_roundtrip`
- `test_bad_identity_is_401_before_route_id_and_method`
- `test_identity_is_kept_exactly_including_spaces`
- `test_unknown_paths_are_404`
- `test_malformed_id_is_400_for_every_method_even_unsupported_ones`
- `test_unsupported_methods_are_405_after_id_validation`
- `test_ids_are_lowercase_and_accepted_in_either_case`
- `test_create_needs_exactly_three_fields`
- `test_bad_sku_is_rejected`
- `test_good_sku_is_accepted`
- `test_bad_quantity_is_rejected_not_defaulted_to_zero`
- `test_integral_numbers_are_accepted_and_stored_as_ints`
- `test_bad_name_is_rejected`
- `test_name_length_counts_utf16_units_after_trimming`
- `test_name_is_trimmed_with_ecmascript_whitespace_only`
- `test_lone_surrogate_in_name_is_bad_input_not_a_crash`
- `test_create_is_persisted_and_returns_what_was_stored`
- `test_every_response_body_is_json_serializable_with_plain_ints`
- `test_list_is_scoped_to_the_owner_and_sorted_by_sku`
- `test_other_users_items_are_invisible_and_untouched`
- `test_delete_returns_204_once_then_404_and_frees_the_sku`
- `test_update_returns_the_new_document_and_bumps_the_version`
- `test_unchanged_values_still_bump_the_version`
- `test_version_accepts_integral_float_and_decimal`
- `test_bad_version_is_400`
- `test_bad_update_body_is_400_and_leaves_the_item_alone`
- `test_update_checks_input_then_item_then_version`
- `test_failed_updates_change_nothing_not_even_the_version`
- `test_update_never_touches_owner_sku_or_id`
- `test_duplicate_sku_is_409_without_a_new_document`
- `test_storage_errors_map_by_code_without_leaking_details`
- `test_a_storage_failure_on_create_leaves_nothing_behind`
- `test_concurrent_patches_on_one_version_succeed_exactly_once`
- `test_separate_service_instances_on_one_database_also_allow_one_winner`
- `test_concurrent_creates_of_one_sku_yield_one_item`
- `test_concurrent_creates_of_different_skus_lose_nothing`
- `test_concurrent_version_chain_never_skips_or_repeats_a_version`

## 自己做一遍

从 `starter.py` 开始写，写完跑测试；参考解在 `solution.py`。

```bash
cd vault/domains/low-level-design/problems/lcp-stockroom-inventory
python3 -m pytest -q
```
