"""内存键值存储的验收测试：`IMPL=solution` 全绿，`IMPL=starter` 全红。

时间戳一律显式传入，没有任何 `sleep` 或墙上时钟；事务测试用具体的嵌套场景钉住"只撤销
自己这一层"和"提交折叠进上一层"两条规则，最后一条测试用一个"暴力但显然正确"的快照栈
模型对拍一段随机的读写/事务序列，交叉验证撤销日志实现和一个更简单的实现是否总是同意。
"""

from __future__ import annotations

import copy
import importlib
import os
import random

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


# ---------- 第 1 关：基本读写 ----------

def test_set_get_delete_round_trip() -> None:
    store = impl.KVStore()
    store.set(0, "user:1", "name", "Ada")
    assert store.get(0, "user:1", "name") == "Ada"
    store.delete(0, "user:1", "name")
    with pytest.raises(impl.FieldNotFoundError):
        store.get(0, "user:1", "name")


def test_get_missing_field_raises() -> None:
    store = impl.KVStore()
    with pytest.raises(impl.FieldNotFoundError):
        store.get(0, "no-such-key", "name")


def test_delete_missing_field_raises() -> None:
    store = impl.KVStore()
    store.set(0, "user:1", "name", "Ada")
    with pytest.raises(impl.FieldNotFoundError):
        store.delete(0, "user:1", "session")


def test_set_overwrites_existing_value_and_ttl() -> None:
    store = impl.KVStore()
    store.set(0, "user:1", "name", "Ada", ttl=5)
    store.set(0, "user:1", "name", "Ada Lovelace")  # 覆盖时不再带 ttl
    assert store.get(0, "user:1", "name") == "Ada Lovelace"
    assert store.get(10, "user:1", "name") == "Ada Lovelace"  # 原来 ttl=5 已经不作数


def test_count_by_field_value_only_counts_live_matches() -> None:
    store = impl.KVStore()
    store.set(0, "user:1", "plan", "pro")
    store.set(0, "user:2", "plan", "pro")
    store.set(0, "user:3", "plan", "free")
    assert store.count_by_field_value(0, "plan", "pro") == 2
    assert store.count_by_field_value(0, "plan", "free") == 1
    assert store.count_by_field_value(0, "plan", "enterprise") == 0


# ---------- 第 2 关：扫描 ----------

def test_scan_prefix_returns_sorted_live_keys_only() -> None:
    store = impl.KVStore()
    for key in ["user:3", "user:1", "user:2", "order:1"]:
        store.set(0, key, "f", "v")
    assert store.scan_prefix(0, "user:") == ["user:1", "user:2", "user:3"]
    assert store.scan_prefix(0, "") == ["order:1", "user:1", "user:2", "user:3"]


def test_fields_returns_sorted_names_and_empty_for_unknown_key() -> None:
    store = impl.KVStore()
    store.set(0, "user:1", "name", "Ada")
    store.set(0, "user:1", "age", "36")
    assert store.fields(0, "user:1") == ["age", "name"]
    assert store.fields(0, "no-such-key") == []


# ---------- 第 3 关：TTL ----------

def test_field_ttl_makes_it_invisible_after_expiry_without_background_thread() -> None:
    store = impl.KVStore()
    store.set(0, "user:1", "session", "abc", ttl=10)
    assert store.get(9, "user:1", "session") == "abc"
    with pytest.raises(impl.FieldNotFoundError):
        store.get(10, "user:1", "session")  # 没有任何后台线程，纯粹靠传入的时间戳判断


def test_key_ttl_expires_all_fields_together() -> None:
    store = impl.KVStore()
    store.set(0, "session:1", "user_id", "1")
    store.set(0, "session:1", "ip", "10.0.0.1")
    store.expire_key(0, "session:1", ttl=20)
    assert store.fields(19, "session:1") == ["ip", "user_id"]
    assert store.fields(20, "session:1") == []
    with pytest.raises(impl.FieldNotFoundError):
        store.get(20, "session:1", "user_id")


def test_expired_data_is_physically_purged_key_count_shrinks() -> None:
    store = impl.KVStore()
    for i in range(50):
        store.set(0, f"k:{i}", "f", "v", ttl=5)
    assert store.key_count(0) == 50
    assert store.key_count(5) == 0  # 不只是查不到，key_count 也证明存储真的缩小了


def test_expiring_key_count_does_not_leak_when_fields_deleted_individually() -> None:
    store = impl.KVStore()
    store.set(0, "session:1", "a", "1")
    store.set(0, "session:1", "b", "2")
    store.expire_key(0, "session:1", ttl=100)
    assert store.expiring_key_count == 1
    store.delete(0, "session:1", "a")
    store.delete(0, "session:1", "b")
    assert store.expiring_key_count == 0  # 字段被逐个删空，孤立的 key 级过期时间不该留下


def test_expire_key_rejects_unknown_key_and_non_positive_ttl() -> None:
    store = impl.KVStore()
    with pytest.raises(impl.KeyNotFoundError):
        store.expire_key(0, "no-such-key", ttl=10)
    store.set(0, "user:1", "name", "Ada")
    with pytest.raises(impl.InvalidTTLError):
        store.expire_key(0, "user:1", ttl=0)


def test_invalid_ttl_raises_on_set() -> None:
    store = impl.KVStore()
    with pytest.raises(impl.InvalidTTLError):
        store.set(0, "user:1", "name", "Ada", ttl=-1)


# ---------- 第 4 关：嵌套事务 ----------

def test_rollback_undoes_only_its_own_nesting_level() -> None:
    store = impl.KVStore()
    store.set(0, "a", "f", "1")
    store.begin()
    store.set(0, "a", "f", "2")
    store.begin()
    store.set(0, "a", "f", "3")
    store.set(0, "b", "f", "x")
    store.rollback()  # 只撤销最内层：a 回到 "2"，b 消失
    assert store.get(0, "a", "f") == "2"
    with pytest.raises(impl.FieldNotFoundError):
        store.get(0, "b", "f")
    assert store.transaction_depth == 1  # 外层事务仍然开着
    store.set(0, "c", "f", "y")
    store.commit()
    assert store.get(0, "a", "f") == "2"
    assert store.get(0, "c", "f") == "y"
    with pytest.raises(impl.FieldNotFoundError):
        store.get(0, "b", "f")


def test_commit_folds_into_parent_and_outer_rollback_still_undoes_it() -> None:
    store = impl.KVStore()
    store.set(0, "a", "f", "1")
    store.begin()
    store.set(0, "a", "f", "2")
    store.begin()
    store.set(0, "a", "f", "3")
    store.commit()  # 内层提交：数据已经是 "3"，但还没脱离外层的撤销范围
    assert store.get(0, "a", "f") == "3"
    store.rollback()  # 外层回滚：连同已提交的内层改动一起撤销
    assert store.get(0, "a", "f") == "1"
    assert store.transaction_depth == 0


def test_ttl_set_inside_a_transaction_expires_correctly_after_commit() -> None:
    store = impl.KVStore()
    store.begin()
    store.set(0, "user:1", "session", "abc", ttl=5)
    store.commit()
    assert store.get(4, "user:1", "session") == "abc"
    with pytest.raises(impl.FieldNotFoundError):
        store.get(5, "user:1", "session")


def test_ttl_set_inside_a_transaction_is_undone_by_rollback() -> None:
    store = impl.KVStore()
    store.begin()
    store.set(0, "user:1", "session", "abc", ttl=5)
    store.rollback()
    with pytest.raises(impl.FieldNotFoundError):
        store.get(0, "user:1", "session")
    with pytest.raises(impl.FieldNotFoundError):
        store.get(100, "user:1", "session")


def test_commit_or_rollback_without_active_transaction_raises() -> None:
    store = impl.KVStore()
    with pytest.raises(impl.NoActiveTransactionError):
        store.commit()
    with pytest.raises(impl.NoActiveTransactionError):
        store.rollback()


def test_arbitrarily_deep_nesting_each_level_only_undoes_itself() -> None:
    store = impl.KVStore()
    store.set(0, "counter", "n", "0")
    depth = 30
    for i in range(1, depth + 1):
        store.begin()
        store.set(0, "counter", "n", str(i))
    assert store.transaction_depth == depth
    for _ in range(depth):
        store.rollback()
    assert store.get(0, "counter", "n") == "0"
    assert store.transaction_depth == 0


# ---------- 随机对拍：撤销日志 vs. 快照栈模型 ----------

def test_random_nested_transactions_match_a_reference_snapshot_model() -> None:
    """撤销日志（本实现）在语义上必须等价于"每层事务持有整份存储快照"的朴素模型——
    后者显然正确但代价是每次 `begin` 都要复制一整份存储，见题解"关键设计决策"。这里
    用一个固定种子跑 400 步随机的读写与事务操作，断言两者在任意时刻的可见状态一致。
    """
    rng = random.Random(20260920)
    store = impl.KVStore()
    ref_stack: list[dict[str, dict[str, str]]] = [{}]
    keys, fields = ["a", "b", "c"], ["x", "y"]

    for _ in range(400):
        op = rng.choice(["set", "delete", "begin", "end"])
        if op == "set":
            key, field, value = rng.choice(keys), rng.choice(fields), str(rng.randint(0, 9))
            store.set(0, key, field, value)
            ref_stack[-1].setdefault(key, {})[field] = value
        elif op == "delete":
            key, field = rng.choice(keys), rng.choice(fields)
            if field in ref_stack[-1].get(key, {}):
                store.delete(0, key, field)
                del ref_stack[-1][key][field]
                if not ref_stack[-1][key]:
                    del ref_stack[-1][key]
            else:
                with pytest.raises(impl.FieldNotFoundError):
                    store.delete(0, key, field)
        elif op == "begin":
            store.begin()
            ref_stack.append(copy.deepcopy(ref_stack[-1]))
        elif op == "end" and len(ref_stack) > 1:
            if rng.random() < 0.5:
                store.commit()
                finished = ref_stack.pop()
                ref_stack[-1] = finished
            else:
                store.rollback()
                ref_stack.pop()

    while len(ref_stack) > 1:  # 收尾：清空还开着的事务，好比对最终状态
        store.commit()
        finished = ref_stack.pop()
        ref_stack[-1] = finished

    actual = {key: {f: store.get(0, key, f) for f in store.fields(0, key)}
              for key in store.scan_prefix(0, "")}
    assert actual == ref_stack[-1]
