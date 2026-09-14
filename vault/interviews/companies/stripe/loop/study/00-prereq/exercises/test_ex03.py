"""ex03 测试。运行：python -m pytest test_ex03.py -q"""

# 刻意让 "disputed" 出现顺序是 m_b 先、m_a 后，
# 用来戳穿 "直接用 Counter.most_common() 的并列顺序" 这个陷阱：
# 那样并列顺序会是 m_b, m_a（插入顺序），而正确答案要求字典序 m_a, m_b。
ROWS = [
    {"charge_id": "ch_1", "merchant": "m_a", "amount": 1000, "country": "US", "status": "ok"},
    {"charge_id": "ch_5", "merchant": "m_b", "amount": 100, "country": "CA", "status": "disputed"},
    {"charge_id": "ch_2", "merchant": "m_a", "amount": 500, "country": "US", "status": "disputed"},
    {"charge_id": "ch_3", "merchant": "m_b", "amount": 700, "country": "CA", "status": "ok"},
    {"charge_id": "ch_4", "merchant": "m_c", "amount": 700, "country": "US", "status": "disputed"},
    {"charge_id": "ch_6", "merchant": "m_c", "amount": 300, "country": "FR", "status": "disputed"},
]


def test_dedupe_charge_ids_keep_order(ex):
    got = ex.dedupe_charge_ids_keep_order(["ch_1", "ch_2", "ch_1", "ch_3", "ch_2"])
    assert got == ["ch_1", "ch_2", "ch_3"], f"应保序去重，得到 {got!r}"
    assert ex.dedupe_charge_ids_keep_order(["ch_1", "ch_1", "ch_1"]) == ["ch_1"]
    assert ex.dedupe_charge_ids_keep_order([]) == []


def test_clone_amounts_is_independent_copy(ex):
    original = [100, 200]
    clone = ex.clone_amounts(original)
    assert clone == [100, 200], f"clone_amounts([100, 200]) 应该等于 [100, 200]，得到 {clone!r}"
    clone.append(300)
    assert original == [100, 200], "修改克隆出来的列表不应该连累原始列表（说明返回的是同一个对象）"
    assert ex.clone_amounts([]) == []


def test_record_dispute_note_default_does_not_leak_across_calls(ex):
    # 经典可变默认参数坑：如果 notes_by_charge 的默认值是 {}，
    # 这两次不传参数的调用会共享同一个 dict，第二次调用里会看到第一次的残留。
    first = ex.record_dispute_note("ch_1", "customer disputes charge")
    assert first == {"ch_1": ["customer disputes charge"]}
    second = ex.record_dispute_note("ch_2", "unauthorized")
    assert second == {"ch_2": ["unauthorized"]}, (
        f"得到 {second!r}——如果这里混进了 ch_1，说明默认参数用了可变对象，状态在调用之间泄漏了"
    )


def test_record_dispute_note_appends_when_dict_passed_explicitly(ex):
    shared: dict[str, list[str]] = {}
    ex.record_dispute_note("ch_1", "first note", shared)
    ex.record_dispute_note("ch_1", "second note", shared)
    assert shared == {"ch_1": ["first note", "second note"]}


def test_group_charges_by_merchant_preserves_row_order(ex):
    got = ex.group_charges_by_merchant(ROWS)
    assert set(got.keys()) == {"m_a", "m_b", "m_c"}, f"分组的 key 集合不对，得到 {sorted(got)!r}"
    assert [r["charge_id"] for r in got["m_a"]] == ["ch_1", "ch_2"]
    assert [r["charge_id"] for r in got["m_b"]] == ["ch_5", "ch_3"]
    assert [r["charge_id"] for r in got["m_c"]] == ["ch_4", "ch_6"]
    assert ex.group_charges_by_merchant([]) == {}


def test_invert_status_index_sorts_each_group(ex):
    status_by_charge = {"ch_2": "disputed", "ch_1": "ok", "ch_3": "disputed", "ch_4": "ok"}
    got = ex.invert_status_index(status_by_charge)
    assert got == {"disputed": ["ch_2", "ch_3"], "ok": ["ch_1", "ch_4"]}
    assert ex.invert_status_index({}) == {}


def test_sum_amount_by_merchant_and_country_uses_tuple_key(ex):
    got = ex.sum_amount_by_merchant_and_country(ROWS)
    assert got == {
        ("m_a", "US"): 1500,
        ("m_b", "CA"): 800,
        ("m_c", "US"): 700,
        ("m_c", "FR"): 300,
    }, f"得到 {got!r}——key 应该是 (merchant, country) 元组"
    assert ex.sum_amount_by_merchant_and_country([]) == {}


def test_rank_disputed_merchants_breaks_ties_alphabetically_not_by_insertion(ex):
    # m_c 2 次最多；m_a 和 m_b 都是 1 次——按字典序 m_a 在 m_b 前面，
    # 尽管 m_b 在 ROWS 里更早被记为 disputed。
    got = ex.rank_disputed_merchants(ROWS, 3)
    assert got == ["m_c", "m_a", "m_b"], f"并列的次数要按 merchant 字典序排，得到 {got!r}"


def test_rank_disputed_merchants_respects_k_and_empty_rows(ex):
    assert ex.rank_disputed_merchants(ROWS, 1) == ["m_c"]
    assert ex.rank_disputed_merchants(ROWS, 0) == []
    assert ex.rank_disputed_merchants([], 5) == []


def test_filter_charges_for_known_merchants_keeps_input_order(ex):
    got = ex.filter_charges_for_known_merchants(ROWS, {"m_a", "m_c"})
    assert got == ["ch_1", "ch_2", "ch_4", "ch_6"], f"得到 {got!r}"
    assert ex.filter_charges_for_known_merchants(ROWS, set()) == []
    assert ex.filter_charges_for_known_merchants([], {"m_a"}) == []
