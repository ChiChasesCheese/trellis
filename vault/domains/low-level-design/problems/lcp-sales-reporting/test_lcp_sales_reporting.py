import importlib
import json
import os
import sqlite3
import threading
from decimal import Decimal

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

SCHEMA = """
CREATE TABLE sales (
    type TEXT COLLATE BINARY,
    customerId TEXT COLLATE BINARY,
    customerName TEXT COLLATE BINARY,
    customerStatus TEXT COLLATE BINARY,
    itemName TEXT COLLATE BINARY,
    itemQuantity INTEGER,
    totalPrice INTEGER,
    saleDate TEXT COLLATE BINARY,
    region TEXT COLLATE BINARY
)
"""
COLUMNS = ("type", "customerId", "customerName", "customerStatus", "itemName",
           "itemQuantity", "totalPrice", "saleDate", "region")
UNSET = object()


def sale(customer, item, qty, price, day, status="active", region="north", **overrides):
    """一份销售文档；缺省字段不写，等价于 JSON 里缺失（存成 NULL）。"""
    doc = {"type": "sale", "customerId": customer, "customerName": "Customer " + customer,
           "customerStatus": status, "itemName": item, "itemQuantity": qty,
           "totalPrice": price, "saleDate": day, "region": region}
    doc.update(overrides)
    return {k: v for k, v in doc.items() if v is not UNSET}


class Context:
    """和工作区同构的上下文：只读连接、`$name` 命名参数、字典行；另外记下每次查询，供审计行数与绑定。"""

    keyspace = '"sales"'

    def __init__(self, directory, documents):
        self.path = directory / "sales.sqlite3"
        connection = sqlite3.connect(self.path)
        with connection:
            connection.execute(SCHEMA)
            connection.executemany(
                "INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [tuple(doc.get(c) for c in COLUMNS) for doc in documents])
        connection.close()
        self.trace = []
        self._lock = threading.Lock()

    def query(self, statement, parameters):
        connection = sqlite3.connect(self.path.resolve().as_uri() + "?mode=ro", uri=True)
        try:
            connection.execute("PRAGMA query_only = ON")
            connection.row_factory = sqlite3.Row
            rows = [dict(row) for row in connection.execute(statement, parameters)]
        finally:
            connection.close()
        with self._lock:
            self.trace.append({"statement": statement, "parameters": dict(parameters), "rows": len(rows)})
        return rows

    @property
    def rows_returned(self):
        return sum(t["rows"] for t in self.trace)


def decode(text):
    """像适配器一样解码请求体：小整数（含 1.0、1e0 这些写法）是 int，其余数字是 Decimal。"""
    def number(token):
        value = Decimal(token)
        if value == value.to_integral_value() and abs(value) < 10**19:
            return int(value)
        return value
    return json.loads(text, parse_int=number, parse_float=number)


def call(ctx, body=UNSET, *, method="POST", path="/report", raw=None):
    """返回 (状态码, 响应体)；业务错误按适配器的方式翻成 `{"error": code}`。"""
    payload = decode(raw) if raw is not None else (None if body is UNSET else body)
    request = {"method": method, "path": path, "json": payload}
    try:
        status, content_type, data = impl.handle(request, ctx)
    except impl.ServiceError as error:
        return error.status, {"error": error.code}
    assert content_type == "application/json"
    return status, json.loads(data)


@pytest.fixture
def make(tmp_path):
    def build(documents):
        return Context(tmp_path, documents)
    return build


README_DOCS = [
    sale("a", "tea", 2, 500, "2026-01-01"),
    sale("a", "coffee", 3, 1500, "2026-01-10"),
    sale("b", "tea", 7, 700, "2026-01-15", status="termed", region="south"),
    sale("c", "coffee", 5, 2000, "2026-01-31"),
    sale("d", "tea", 2, 2000, "2026-02-01"),
    sale("b", "tea", 1, 500, "2026-01-20"),
]
ZERO = {"active_customers": 0, "total_quantity": 0, "total_spend_cents": 0,
        "quantity_leaders": [], "spend_leaders": [], "item_leaders": []}
WINDOW = {"start": "2026-01-01", "end": "2026-02-01"}


# ---- 例子 ----

def test_readme_example(make):
    ctx = make(README_DOCS)
    status, body = call(ctx, {**WINDOW, "k": 2})
    assert status == 200
    assert body == {
        "active_customers": 3, "total_quantity": 18, "total_spend_cents": 5200,
        "quantity_leaders": [{"customer_id": "b", "quantity": 8}, {"customer_id": "a", "quantity": 5}],
        "spend_leaders": [{"customer_id": "a", "spend_cents": 2000}, {"customer_id": "c", "spend_cents": 2000}],
        "item_leaders": [{"item": "tea", "quantity": 10}, {"item": "coffee", "quantity": 8}],
    }


def test_readme_empty_interval_and_impossible_date(make):
    ctx = make(README_DOCS)
    assert call(ctx, {"start": "2026-03-01", "end": "2026-04-01"}) == (200, ZERO)
    assert call(ctx, {"start": "2026-02-30", "end": "2026-03-01"}) == (400, {"error": "invalid_request"})


ARTICLE_DOCS = [
    sale("u1", "tea", 4, 800, "2026-03-02", region="east"),
    sale("u1", "tea", 1, 150, "2026-03-09", status="termed", region="east"),
    sale("u2", "cake", 6, 1200, "2026-03-10", status="termed", region="west"),
    sale("u3", "cake", 6, 900, "2026-03-15", region=None),
    sale("u3", "tea", 2, 300, "2026-03-31", region="east"),
    sale("u4", "jam", 9, 450, "2026-04-01", region="east"),                      # 恰好是 end，不含
    sale("u5", "tea", 5, 500, "2026-03-05", status="pending", region="east"),    # 未知状态
    sale("u6", "tea", 7, 700, None, region="east"),                              # 缺日期
    sale("u7", "tea", 3, 100, "2026-03-12", region="east", type="refund"),       # 不是 sale
    sale("u8", "tea", 3, 100, "2026-03-12", region="east", customerStatus=UNSET),  # 缺状态
]


def test_article_example_and_filters(make):
    ctx = make(ARTICLE_DOCS)
    window = {"start": "2026-03-01", "end": "2026-04-01", "k": 2}
    _, body = call(ctx, window)
    assert body["active_customers"] == 2
    assert (body["total_quantity"], body["total_spend_cents"]) == (19, 3350)
    assert body["quantity_leaders"] == [{"customer_id": "u3", "quantity": 8}, {"customer_id": "u2", "quantity": 6}]
    assert body["spend_leaders"] == [{"customer_id": "u2", "spend_cents": 1200}, {"customer_id": "u3", "spend_cents": 1200}]
    assert body["item_leaders"] == [{"item": "cake", "quantity": 12}, {"item": "tea", "quantity": 7}]
    _, east = call(ctx, {**window, "region": "east"})
    assert (east["total_quantity"], east["total_spend_cents"]) == (7, 1250)
    _, termed = call(ctx, {**window, "status": "termed"})
    assert termed["active_customers"] == 0 and termed["total_quantity"] == 7


# ---- 日期区间 ----

def test_start_inclusive_end_exclusive(make):
    ctx = make([sale("a", "tea", 1, 10, "2026-05-01"), sale("b", "tea", 2, 20, "2026-05-31"),
                sale("c", "tea", 4, 40, "2026-06-01")])
    _, body = call(ctx, {"start": "2026-05-01", "end": "2026-06-01"})
    assert body["total_quantity"] == 3
    _, body = call(ctx, {"start": "2026-05-02", "end": "2026-06-02"})
    assert body["total_quantity"] == 6


def test_sentinel_end_reaches_the_last_supported_day(make):
    ctx = make([sale("last", "x", 3, 451, "2099-12-31"), sale("prev", "y", 7, 773, "2099-12-29")])
    _, body = call(ctx, {"start": "2099-12-30", "end": "2100-01-01"})
    assert (body["total_quantity"], body["quantity_leaders"]) == (3, [{"customer_id": "last", "quantity": 3}])
    assert call(ctx, {"start": "2099-12-29", "end": "2100-01-03"}) == (400, {"error": "invalid_request"})
    _, body = call(ctx, {"start": "2099-12-29", "end": "2099-12-31"})
    assert body["item_leaders"] == [{"item": "y", "quantity": 7}]


@pytest.mark.parametrize("window", [
    {"start": "2026-02-30", "end": "2026-03-01"},    # 不存在的日子
    {"start": "2026-13-01", "end": "2026-12-31"},
    {"start": "2023-02-29", "end": "2023-03-05"},    # 平年没有 2 月 29 日
    {"start": "2026-1-1", "end": "2026-02-01"},      # 不是定宽
    {"start": "20260101", "end": "20260201"},        # fromisoformat 会收，合同不收
    {"start": "2026-W01-1", "end": "2026-W05-1"},    # ISO 周日期同理
    {"start": "2026-01-01T00:00:00", "end": "2026-02-01"},
    {"start": " 2026-01-01", "end": "2026-02-01"},
    {"start": "2026-01-01\n", "end": "2026-02-01"},  # 正则 `$` 会放过结尾换行
    {"start": "２０２６-01-01", "end": "2026-02-01"},  # 全角数字
    {"start": "2019-12-31", "end": "2026-02-01"},
    {"start": "2100-01-01", "end": "2100-01-01"},    # 哨兵只能做 end
    {"start": "2026-01-01", "end": "2100-01-02"},
    {"start": "2026-01-01", "end": "2026-01-01"},    # end 必须晚于 start
    {"start": "2026-02-01", "end": "2026-01-01"},
    {"start": "2026-01-01"},
    {"end": "2026-02-01"},
    {"start": 20260101, "end": "2026-02-01"},
    {"start": None, "end": "2026-02-01"},
    {"start": "2026-01-01", "end": ["2026-02-01"]},
])
def test_invalid_dates(make, window):
    assert call(make([]), window) == (400, {"error": "invalid_request"})


def test_year_bounds_are_accepted(make):
    ctx = make([sale("a", "tea", 1, 10, "2020-01-01"), sale("b", "tea", 1, 10, "2099-12-31")])
    assert call(ctx, {"start": "2020-01-01", "end": "2020-01-02"})[1]["total_quantity"] == 1
    assert call(ctx, {"start": "2099-12-31", "end": "2100-01-01"})[1]["total_quantity"] == 1
    assert call(ctx, {"start": "2024-02-29", "end": "2024-03-01"}) == (200, ZERO)  # 闰日合法


# ---- k 与其他字段 ----

@pytest.mark.parametrize("spelling", ["1", "1.0", "1e0", "10e-1", "0.1e1"])
def test_k_numeric_spellings_mean_the_same_integer(make, spelling):
    ctx = make([sale("a", "tea", 3, 1, "2026-01-02"), sale("b", "tea", 2, 1, "2026-01-03")])
    raw = '{"start": "2026-01-01", "end": "2026-02-01", "k": %s}' % spelling
    _, body = call(ctx, raw=raw)
    assert [x["customer_id"] for x in body["quantity_leaders"]] == ["a"]


@pytest.mark.parametrize("bad", ["0", "21", "-1", "1.5", "0.5", "1e30", "1e-1", '"5"', "true", "false", "null", "[]", "{}"])
def test_invalid_k(make, bad):
    raw = '{"start": "2026-01-01", "end": "2026-02-01", "k": %s}' % bad
    assert call(make([]), raw=raw) == (400, {"error": "invalid_request"})


def test_k_default_is_ten_and_max_is_twenty(make):
    docs = [sale("c%02d" % i, "item%02d" % i, 100 - i, 10, "2026-01-02") for i in range(30)]
    ctx = make(docs)
    _, body = call(ctx, WINDOW)
    assert all(len(body[key]) == 10 for key in ("quantity_leaders", "spend_leaders", "item_leaders"))
    _, body = call(ctx, {**WINDOW, "k": 20})
    assert len(body["quantity_leaders"]) == 20
    _, body = call(ctx, {**WINDOW, "k": 20})
    assert body["quantity_leaders"][-1]["customer_id"] == "c19"


@pytest.mark.parametrize("body", [
    {**WINDOW, "extra": 1}, {**WINDOW, "K": 3}, [WINDOW], "report", None, 7, {},
    {**WINDOW, "status": "ACTIVE"}, {**WINDOW, "status": "pending"}, {**WINDOW, "status": ""},
    {**WINDOW, "status": True}, {**WINDOW, "status": 1},
    {**WINDOW, "region": ""}, {**WINDOW, "region": 5}, {**WINDOW, "region": ["north"]},
    {**WINDOW, "item": ""}, {**WINDOW, "item": False}, {**WINDOW, "item": "x" * 101},
    {**WINDOW, "region": "\ud800"},  # 孤立代理码点
])
def test_invalid_bodies_and_filters(make, body):
    ctx = make([sale("a", "tea", 1, 1, "2026-01-02")])
    assert call(ctx, body) == (400, {"error": "invalid_request"})
    assert ctx.trace == []  # 校验先于一切查询


def test_null_filters_mean_omitted(make):
    ctx = make(README_DOCS)
    full = call(ctx, WINDOW)
    assert call(ctx, {**WINDOW, "status": None, "region": None, "item": None}) == full


def test_text_length_counts_code_points(make):
    emoji = "\U0001F600"
    ctx = make([sale("a", emoji * 100, 5, 1, "2026-01-02", region=emoji * 100)])
    _, body = call(ctx, {**WINDOW, "item": emoji * 100, "region": emoji * 100})
    assert body["total_quantity"] == 5  # 100 个码点（400 字节）合法
    assert call(ctx, {**WINDOW, "item": emoji * 101}) == (400, {"error": "invalid_request"})
    assert call(ctx, {**WINDOW, "region": "r" * 100})[0] == 200
    assert call(ctx, {**WINDOW, "region": "r" * 101})[0] == 400


def test_other_routes_are_404_before_the_body_is_read(make):
    ctx = make(README_DOCS)
    for method, path in [("GET", "/report"), ("PUT", "/report"), ("DELETE", "/report"), ("POST", "/reports"),
                         ("POST", "/"), ("POST", "/report/"), ("GET", "/anything")]:
        assert call(ctx, "garbage", method=method, path=path) == (404, {"error": "not_found"})
    assert ctx.trace == []


# ---- 统计规则 ----

def test_each_customer_counts_once_and_only_when_an_active_sale_matches(make):
    ctx = make([
        sale("a", "tea", 1, 1, "2026-01-02"), sale("a", "tea", 1, 1, "2026-01-03"),                  # 两条 active：一个客户
        sale("b", "tea", 1, 1, "2026-01-04", status="termed"), sale("b", "tea", 1, 1, "2026-01-05"),  # 混合：算 active
        sale("c", "tea", 1, 1, "2026-01-06", status="termed"),                                       # 只有 termed
        sale("d", "tea", 1, 1, "2025-12-31"),                                                        # active 但在区间外
    ])
    assert call(ctx, WINDOW)[1]["active_customers"] == 2
    assert call(ctx, {**WINDOW, "status": "active"})[1]["active_customers"] == 2
    _, termed = call(ctx, {**WINDOW, "status": "termed"})
    assert termed["active_customers"] == 0 and termed["total_quantity"] == 2  # termed 报表仍有总量


def test_quantity_and_spend_are_independent_measures(make):
    ctx = make([sale("a", "tea", 3, 500, "2026-01-02")])
    _, body = call(ctx, WINDOW)
    assert (body["total_quantity"], body["total_spend_cents"]) == (3, 500)  # 不是 1500
    assert body["spend_leaders"] == [{"customer_id": "a", "spend_cents": 500}]


def test_free_sales_count_toward_quantity(make):
    ctx = make([sale("a", "gift", 4, 0, "2026-01-02")])
    _, body = call(ctx, WINDOW)
    assert body["total_spend_cents"] == 0 and body["total_quantity"] == 4
    assert body["spend_leaders"] == [{"customer_id": "a", "spend_cents": 0}]


def test_customers_group_across_items_dates_and_names(make):
    ctx = make([sale("a", "tea", 2, 10, "2026-01-02", customerName="First"),
                sale("a", "jam", 3, 20, "2026-01-09", customerName="Second", region="south"),
                sale("b", "tea", 4, 5, "2026-01-10")])
    _, body = call(ctx, WINDOW)
    assert body["quantity_leaders"] == [{"customer_id": "a", "quantity": 5}, {"customer_id": "b", "quantity": 4}]


def test_status_filter_applies_to_every_part(make):
    ctx = make(README_DOCS)
    _, body = call(ctx, {**WINDOW, "status": "termed", "k": 5})
    assert body == {"active_customers": 0, "total_quantity": 7, "total_spend_cents": 700,
                    "quantity_leaders": [{"customer_id": "b", "quantity": 7}],
                    "spend_leaders": [{"customer_id": "b", "spend_cents": 700}],
                    "item_leaders": [{"item": "tea", "quantity": 7}]}


def test_region_is_exact_case_sensitive_and_skips_missing(make):
    ctx = make([sale("a", "tea", 1, 1, "2026-01-02", region="North"), sale("b", "tea", 2, 1, "2026-01-02"),
                sale("c", "tea", 4, 1, "2026-01-02", region=None), sale("d", "tea", 8, 1, "2026-01-02", region=UNSET),
                sale("e", "tea", 16, 1, "2026-01-02", region="north ")])
    assert call(ctx, {**WINDOW, "region": "north"})[1]["total_quantity"] == 2
    assert call(ctx, {**WINDOW, "region": "North"})[1]["total_quantity"] == 1
    assert call(ctx, WINDOW)[1]["total_quantity"] == 31  # 不筛选时缺失的地区也算


def test_item_filter_is_exact_and_values_are_never_syntax(make):
    tricky = "x' OR '1'='1"
    ctx = make([sale("a", "tea", 1, 1, "2026-01-02"), sale("b", "Tea", 2, 1, "2026-01-02"),
                sale("c", "tea ", 4, 1, "2026-01-02"), sale("d", tricky, 8, 1, "2026-01-02")])
    assert call(ctx, {**WINDOW, "item": "tea"})[1]["total_quantity"] == 1
    assert call(ctx, {**WINDOW, "item": "te%"})[1]["total_quantity"] == 0   # 不是通配符
    assert call(ctx, {**WINDOW, "item": "t_a"})[1]["total_quantity"] == 0
    assert call(ctx, {**WINDOW, "item": "x' OR '1'='1' --"})[1]["total_quantity"] == 0
    _, body = call(ctx, {**WINDOW, "item": tricky})
    assert body["total_quantity"] == 8 and body["item_leaders"] == [{"item": tricky, "quantity": 8}]


def test_filters_combine_with_and(make):
    ctx = make(README_DOCS)
    _, body = call(ctx, {**WINDOW, "region": "north", "item": "tea", "status": "active"})
    assert (body["total_quantity"], body["active_customers"]) == (3, 2)


def test_ineligible_documents_never_count(make):
    ctx = make([
        sale("a", "tea", 1, 10, "2026-01-02"),
        sale("b", "tea", 100, 1000, "2026-01-02", type="refund"),
        sale("c", "tea", 100, 1000, "2026-01-02", type=None),
        sale("d", "tea", 100, 1000, None),
        sale("e", "tea", 100, 1000, "2026-01-02", status="pending"),
        sale("f", "tea", 100, 1000, "2026-01-02", status="Active"),
        sale("g", "tea", 100, 1000, "2026-01-02", status=None),
    ])
    _, body = call(ctx, WINDOW)
    assert body["total_quantity"] == 1 and body["active_customers"] == 1
    assert body["quantity_leaders"] == [{"customer_id": "a", "quantity": 1}]


# ---- 排名与平局 ----

def test_ties_break_by_key_ascending_before_the_limit(make):
    docs = [sale(c, "tea", 5, 100, "2026-01-02") for c in ("m", "z", "a", "q", "B")]
    ctx = make(docs)
    _, body = call(ctx, {**WINDOW, "k": 3})
    assert [x["customer_id"] for x in body["quantity_leaders"]] == ["B", "a", "m"]  # 大写在小写之前
    assert [x["customer_id"] for x in body["spend_leaders"]] == ["B", "a", "m"]


def test_item_order_is_utf8_byte_order_without_folding(make):
    names = ["apple", "Zebra", "éclair", "日本", "ｚ", "\U0001F600"]
    ctx = make([sale("a", n, 2, 1, "2026-01-02") for n in names])
    _, body = call(ctx, {**WINDOW, "k": 20})
    assert [x["item"] for x in body["item_leaders"]] == sorted(names, key=lambda s: s.encode("utf-8"))
    assert [x["item"] for x in body["item_leaders"]][0] == "Zebra"


def test_ranking_sorts_by_value_first_then_cuts(make):
    docs = [sale("a", "tea", 1, 900, "2026-01-02"), sale("b", "tea", 9, 100, "2026-01-02"),
            sale("c", "tea", 5, 500, "2026-01-02")]
    _, body = call(make(docs), {**WINDOW, "k": 2})
    assert [x["customer_id"] for x in body["quantity_leaders"]] == ["b", "c"]
    assert [x["customer_id"] for x in body["spend_leaders"]] == ["a", "c"]


def test_exact_integers_above_32_bits(make):
    docs = [sale("c%d" % i, "gold", 1_000_000, 10**12, "2026-01-02") for i in range(5)]
    _, body = call(make(docs), WINDOW)
    assert body["total_spend_cents"] == 5 * 10**12 and body["total_quantity"] == 5_000_000
    assert type(body["total_spend_cents"]) is int
    assert body["spend_leaders"][0] == {"customer_id": "c0", "spend_cents": 10**12}


# ---- 查询的形状：行数预算与绑定 ----

@pytest.mark.parametrize("k", [1, 2, 10, 20])
def test_row_budget(make, k):
    docs = [sale("c%02d" % i, "item%02d" % (i % 37), i + 1, 10 * i, "2026-01-02") for i in range(80)]
    ctx = make(docs)
    _, body = call(ctx, {**WINDOW, "k": k})
    assert len(body["quantity_leaders"]) == k
    assert 0 < ctx.rows_returned <= 32 + 3 * k


def test_request_values_are_bound_not_interpolated(make):
    ctx = make([sale("a", "tea", 1, 1, "2026-01-02", region="zz-region")])
    marker_item = "it'em; DROP TABLE sales; --"
    call(ctx, {**WINDOW, "region": "zz-region", "item": marker_item})
    assert ctx.trace
    for entry in ctx.trace:
        for literal in ("zz-region", marker_item, "2026-01-01"):
            assert literal not in entry["statement"]
    assert any("zz-region" in json.dumps(t["parameters"]) for t in ctx.trace)
    assert call(ctx, WINDOW)[1]["total_quantity"] == 1  # 表还在


@pytest.mark.parametrize("status", ["active", "termed"])
def test_status_value_is_bound_and_never_spelled_in_sql(make, status):
    """工作区的审计：请求值不在任何语句里，且出现在某个参数里；`status` 的取值也是常量，同样要绑定。"""
    ctx = make(README_DOCS)
    code, body = call(ctx, {**WINDOW, "status": status})
    assert code == 200
    assert ctx.trace
    assert all(status not in t["statement"] for t in ctx.trace)
    assert any(status in json.dumps(t["parameters"]) for t in ctx.trace)
    # 没有 status 筛选时，资格条件仍然工作（常量来自绑定，不来自请求）
    assert call(ctx, WINDOW)[1]["total_quantity"] == 18


def test_database_errors_propagate_without_a_service_error(make):
    class Broken:
        keyspace = '"sales"'

        def query(self, statement, parameters):
            raise sqlite3.OperationalError("disk I/O error at /secret/path")

    request = {"method": "POST", "path": "/report", "json": dict(WINDOW)}
    with pytest.raises(sqlite3.OperationalError):
        impl.handle(request, Broken())  # 适配器把任何非 ServiceError 的异常翻成 500 internal_error


def test_concurrent_reports_agree(make):
    ctx = make(README_DOCS)
    expected = call(ctx, {**WINDOW, "k": 2})
    barrier, results = threading.Barrier(8), []

    def worker():
        barrier.wait()
        results.append(call(ctx, {**WINDOW, "k": 2}))

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert results == [expected] * 8
