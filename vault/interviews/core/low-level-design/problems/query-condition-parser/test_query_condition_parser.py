"""条件解析与内存表查询的测试：`-k part1` 选第 1 关，依此类推。"""

import importlib
import os

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def people():
    t = impl.Table(["id", "name", "age", "city"])
    for row in [
        (1, "Ann", 30, "NYC"),
        (2, "Bob", 17, "SF"),
        (3, "Cat", 25, "NYC"),
        (4, "Dan", 45, "LA"),
        (5, "Eve", 18, "SF"),
    ]:
        t.insert(dict(zip(["id", "name", "age", "city"], row)))
    return t


def ids(rows):
    return [r["id"] for r in rows]


# ---- 第 1 关：比较、AND / OR、括号 -------------------------------------------


@pytest.mark.parametrize("where,expected", [
    ("age = 30", [1]),
    ("age != 30", [2, 3, 4, 5]),
    ("age < 18", [2]),
    ("age <= 18", [2, 5]),
    ("age > 30", [4]),
    ("age >= 30", [1, 4]),
    ("city = 'NYC'", [1, 3]),
    ("name != 'Ann'", [2, 3, 4, 5]),
    ("age>=18", [1, 3, 4, 5]),          # 运算符两侧可以没有空格
    ("  age   >  44  ", [4]),
])
def test_part1_comparison_operators(where, expected):
    assert ids(people().select(where)) == expected


def test_part1_and_binds_tighter_than_or():
    t = people()
    # 等价于 city='SF' OR (age>40 AND city='LA')
    assert ids(t.select("city = 'SF' OR age > 40 AND city = 'LA'")) == [2, 4, 5]
    # 等价于 (age>40 AND city='LA') OR city='SF'，与书写顺序无关
    assert ids(t.select("age > 40 AND city = 'LA' OR city = 'SF'")) == [2, 4, 5]


def test_part1_parentheses_override_precedence():
    t = people()
    assert ids(t.select("(city = 'SF' OR age > 40) AND city = 'LA'")) == [4]
    assert ids(t.select("age >= 18 AND (city = 'NYC' OR city = 'SF')")) == [1, 3, 5]
    assert ids(t.select("((age = 30))")) == [1]


def test_part1_keywords_are_case_insensitive_and_chain():
    t = people()
    assert ids(t.select("age >= 18 and city = 'NYC' or id = 2")) == [1, 2, 3]
    assert ids(t.select("id = 1 OR id = 2 OR id = 3 OR id = 4")) == [1, 2, 3, 4]
    assert ids(t.select("age > 10 AND age < 40 AND city = 'NYC'")) == [1, 3]


def test_part1_quoted_text_is_one_token():
    t = impl.Table(["id", "note"])
    t.insert({"id": 1, "note": "a AND b"})
    t.insert({"id": 2, "note": "(x)"})
    t.insert({"id": 3, "note": ""})
    assert ids(t.select("note = 'a AND b'")) == [1]
    assert ids(t.select("note = '(x)' OR id = 3")) == [2, 3]
    assert ids(t.select("note = ''")) == [3]


def test_part1_negative_numbers():
    t = impl.Table(["id", "delta"])
    for i, d in enumerate([-5, 0, 7], start=1):
        t.insert({"id": i, "delta": d})
    assert ids(t.select("delta < -1")) == [1]
    assert ids(t.select("delta >= -5 AND delta <= 0")) == [1, 2]


def test_part1_empty_condition_returns_all_rows_in_insertion_order():
    t = people()
    assert ids(t.select()) == [1, 2, 3, 4, 5]
    assert ids(t.select("   ")) == [1, 2, 3, 4, 5]
    assert t.select("age > 100") == []


def test_part1_projection_and_returned_rows_are_copies():
    t = people()
    rows = t.select("id = 1", columns=["name", "city"])
    assert rows == [{"name": "Ann", "city": "NYC"}]
    rows[0]["name"] = "changed"
    t.select("id = 1")[0]["name"] = "changed"
    assert t.select("id = 1", columns=["name"]) == [{"name": "Ann"}]
    source = {"id": 9, "name": "Zed", "age": 1, "city": "X"}
    t.insert(source)
    source["name"] = "mutated"                      # 插入后改原字典，不能影响表
    assert t.select("id = 9", columns=["name"]) == [{"name": "Zed"}]


@pytest.mark.parametrize("where", [
    "age >", "(age > 1", "age > 1)", "age ~ 1", "age > 1 OR", "age > 1 AND AND age < 5",
    "age > 1 age < 5", "age", "= 5", "AND age > 1", "nope = 1", "age = city",
    "city = 'NYC", "age > 'abc'", "()", "age > 1 city",
])
def test_part1_bad_conditions_raise_query_error(where):
    with pytest.raises(impl.QueryError):
        people().select(where)


def test_part1_query_error_is_a_value_error_and_other_misuse():
    assert issubclass(impl.QueryError, ValueError)
    t = people()
    with pytest.raises(impl.QueryError):
        t.select("age > 1", columns=["nope"])
    with pytest.raises(impl.QueryError):
        t.insert({"id": 1})                          # 缺列
    with pytest.raises(impl.QueryError):
        t.insert({"id": 1, "name": "x", "age": 1, "city": "y", "extra": 1})


def test_part1_unknown_column_is_rejected_even_on_empty_table():
    t = impl.Table(["a"])
    with pytest.raises(impl.QueryError):
        t.select("b = 1")                           # 错误只取决于条件和表结构，不取决于有没有数据


# ---- 第 2 关：NOT、IN、NULL（三值逻辑）---------------------------------------


def with_nulls():
    t = impl.Table(["id", "age", "city"])
    for row in [(1, 30, "NYC"), (2, None, "NYC"), (3, 10, None), (4, None, None), (5, 50, "SF")]:
        t.insert(dict(zip(["id", "age", "city"], row)))
    return t


def test_part2_not_binds_tighter_than_and():
    t = people()
    assert ids(t.select("NOT city = 'NYC'")) == [2, 4, 5]
    # (NOT city='NYC') AND age>=18
    assert ids(t.select("NOT city = 'NYC' AND age >= 18")) == [4, 5]
    assert ids(t.select("NOT (city = 'NYC' AND age >= 18)")) == [2, 4, 5]
    assert ids(t.select("NOT (city = 'NYC' AND age >= 28)")) == [2, 3, 4, 5]
    assert ids(t.select("not not city = 'NYC'")) == [1, 3]


def test_part2_in_and_not_in():
    t = people()
    assert ids(t.select("city IN ('NYC', 'LA')")) == [1, 3, 4]
    assert ids(t.select("age in (17, 18)")) == [2, 5]
    assert ids(t.select("city NOT IN ('NYC')")) == [2, 4, 5]
    assert ids(t.select("city IN ('SF') AND age IN (18, 30)")) == [5]
    assert ids(t.select("id IN (1)")) == [1]


def test_part2_in_syntax_errors():
    t = people()
    for bad in ["city IN ()", "city IN 'NYC'", "city IN ('NYC'", "city IN ('NYC',)", "city IN ('NYC' 'SF')"]:
        with pytest.raises(impl.QueryError):
            t.select(bad)


def test_part2_comparison_with_null_is_unknown_and_excluded():
    t = with_nulls()
    assert ids(t.select("age >= 18")) == [1, 5]
    assert ids(t.select("age != 30")) == [3, 5]      # None != 30 不是真
    assert ids(t.select("city = 'NYC'")) == [1, 2]


def test_part2_not_of_unknown_is_still_unknown():
    t = with_nulls()
    assert ids(t.select("NOT age >= 18")) == [3]     # 不会把 age 为 NULL 的 2、4 带进来
    assert ids(t.select("NOT (age >= 18 OR city = 'NYC')")) == []      # 行 3、4 是未知，不是真
    assert ids(t.select("city NOT IN ('NYC')")) == [5]


def test_part2_three_valued_and_or():
    t = with_nulls()
    # 未知 OR 真 = 真；未知 AND 假 = 假；未知 AND 真 = 未知（排除）
    assert ids(t.select("age < 18 OR city = 'NYC'")) == [1, 2, 3]
    assert ids(t.select("age >= 18 AND city = 'NYC'")) == [1]
    assert ids(t.select("NOT (age >= 18 AND city = 'NYC')")) == [3, 5]
    assert ids(t.select("NOT (age >= 18 AND city = 'SF')")) == [1, 2, 3]   # 未知 AND 假 = 假，所以行 2 的 NOT 为真


def test_part2_is_null_and_is_not_null():
    t = with_nulls()
    assert ids(t.select("age IS NULL")) == [2, 4]
    assert ids(t.select("age IS NOT NULL")) == [1, 3, 5]
    assert ids(t.select("age is null and city is null")) == [4]
    assert ids(t.select("NOT age IS NULL")) == [1, 3, 5]
    assert ids(t.select("age IS NULL OR city IS NULL")) == [2, 3, 4]


def test_part2_null_literal_only_after_is():
    t = with_nulls()
    for bad in ["age = NULL", "age IS", "age IS 5", "age IS NOT", "age IN (NULL)"]:
        with pytest.raises(impl.QueryError):
            t.select(bad)


def test_part2_earlier_conditions_still_work_with_null_rows():
    t = with_nulls()
    assert ids(t.select("(age > 20 OR city = 'NYC') AND id != 1")) == [2, 5]
    assert ids(t.select()) == [1, 2, 3, 4, 5]        # 空条件不做任何过滤，包括含 NULL 的行


# ---- 第 3 关：等值索引 --------------------------------------------------------


def indexed_pair():
    plain, fast = people(), people()
    fast.create_index("city")
    fast.create_index("age")
    return plain, fast


CONDITIONS = [
    "city = 'NYC'",
    "city = 'NYC' AND age > 20",
    "age > 20 AND city = 'SF'",
    "city = 'NYC' OR city = 'SF'",
    "city = 'NYC' OR age > 40",
    "city IN ('SF', 'LA')",
    "city IN ('SF', 'LA') AND age = 18",
    "NOT city = 'NYC'",
    "(city = 'NYC' OR city = 'LA') AND (age = 30 OR age = 45)",
    "city = 'NOPE'",
    "age = 18 AND age = 30",
    "city != 'NYC'",
    "age >= 18",
]


@pytest.mark.parametrize("where", CONDITIONS)
def test_part3_index_never_changes_results(where):
    plain, fast = indexed_pair()
    assert fast.select(where) == plain.select(where)


def test_part3_equality_on_indexed_column_scans_only_candidates():
    t = people()
    t.create_index("city")
    assert ids(t.select("city = 'NYC'")) == [1, 3]
    assert t.last_scan_count == 2
    t.select("city = 'NOPE'")
    assert t.last_scan_count == 0


def test_part3_and_uses_any_indexed_side_or_needs_both():
    t = people()
    t.create_index("city")
    t.select("city = 'SF' AND age > 1")              # 一边有索引就够
    assert t.last_scan_count == 2
    t.select("age > 1 AND city = 'SF'")
    assert t.last_scan_count == 2
    t.select("city = 'SF' OR age > 40")              # OR 的另一边没有索引，只能全表
    assert t.last_scan_count == 5
    t.create_index("age")
    t.select("city = 'SF' OR age = 45")              # 两边都有索引：取并集
    assert t.last_scan_count == 3


def test_part3_in_uses_the_index_and_not_does_not():
    t = people()
    t.create_index("city")
    assert ids(t.select("city IN ('SF', 'LA')")) == [2, 4, 5]
    assert t.last_scan_count == 3
    t.select("NOT city = 'NYC'")                     # 否定条件不能靠等值索引缩小范围
    assert t.last_scan_count == 5


def test_part3_no_index_or_no_condition_scans_everything():
    t = people()
    t.select("city = 'NYC'")
    assert t.last_scan_count == 5
    t.create_index("city")
    t.select()
    assert t.last_scan_count == 5


def test_part3_index_follows_later_inserts_and_keeps_insertion_order():
    t = people()
    t.create_index("city")
    t.insert({"id": 6, "name": "Fay", "age": 22, "city": "NYC"})
    t.insert({"id": 7, "name": "Gus", "age": 23, "city": "SF"})
    assert ids(t.select("city = 'NYC'")) == [1, 3, 6]
    assert ids(t.select("city = 'SF' OR city = 'NYC'")) == [1, 2, 3, 5, 6, 7]   # 并集后仍是插入顺序


def test_part3_index_on_null_values_and_unknown_column():
    t = with_nulls()
    t.create_index("city")
    assert ids(t.select("city = 'NYC'")) == [1, 2]
    assert ids(t.select("city IS NULL")) == [3, 4]
    with pytest.raises(impl.QueryError):
        t.create_index("nope")
    t.create_index("city")                            # 重复建索引无副作用
    assert ids(t.select("city = 'SF'")) == [5]


# ---- 第 4 关（选做）：无固定列的文档表 ----------------------------------------


def docs():
    t = impl.Table()
    t.insert({"id": 1, "name": "Ann", "address": {"city": "NYC", "zip": "10001"}})
    t.insert({"id": 2, "name": "Bob", "address": {"city": "SF"}})
    t.insert({"id": 3, "name": "Cat"})
    t.insert({"id": 4, "tags": 7})
    return t


def test_part4_dotted_path_reads_nested_fields():
    t = docs()
    assert ids(t.select("address.city = 'NYC'")) == [1]
    assert ids(t.select("address.city IN ('NYC', 'SF')")) == [1, 2]


def test_part4_missing_fields_are_null():
    t = docs()
    assert ids(t.select("address.zip IS NULL")) == [2, 3, 4]
    assert ids(t.select("address.zip IS NOT NULL")) == [1]
    assert ids(t.select("NOT address.city = 'NYC'")) == [2]      # 缺字段是未知，NOT 之后仍是未知
    assert ids(t.select("name = 'Cat' OR name IS NULL")) == [3, 4]


def test_part4_no_schema_validation_and_projection_by_path():
    t = docs()
    t.insert({"anything": "goes"})
    assert ids(t.select("name = 'Ann'")) == [1]
    rows = t.select("id = 1", columns=["name", "address.city", "missing"])
    assert rows == [{"name": "Ann", "address.city": "NYC", "missing": None}]


def test_part4_nested_rows_are_copied_and_still_syntax_checked():
    t = docs()
    row = t.select("id = 1")[0]
    row["address"]["city"] = "changed"
    assert ids(t.select("address.city = 'NYC'")) == [1]
    with pytest.raises(impl.QueryError):
        t.select("address.city =")
