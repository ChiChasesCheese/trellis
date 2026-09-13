"""ex01 测试。运行：python -m pytest test_ex01.py -q"""

ROWS = [
    {"charge_id": "ch_1", "merchant": "m_a", "amount": 1000, "status": "ok"},
    {"charge_id": "ch_2", "merchant": "m_a", "amount": 500, "status": "disputed"},
    {"charge_id": "ch_3", "merchant": "m_b", "amount": 700, "status": "ok"},
    {"charge_id": "ch_4", "merchant": "m_c", "amount": 700, "status": "disputed"},
    {"charge_id": "ch_5", "merchant": "m_c", "amount": 100, "status": "disputed"},
    {"charge_id": "ch_6", "merchant": "m_c", "amount": 100, "status": "ok"},
]
MERCHANTS = [
    {"merchant_id": "m_a", "name": "Alpha"},
    {"merchant_id": "m_b", "name": "Beta"},
]


def test_select_where_keeps_order_and_uses_gte(ex):
    assert ex.select_where(ROWS, 700) == ["ch_1", "ch_3", "ch_4"]
    assert ex.select_where(ROWS, 10_000) == []
    assert ex.select_where([], 0) == []


def test_sum_by_merchant(ex):
    assert ex.sum_by_merchant(ROWS) == {"m_a": 1500, "m_b": 700, "m_c": 900}
    assert ex.sum_by_merchant([]) == {}


def test_join_names_left_join(ex):
    got = ex.join_names(ROWS[:4], MERCHANTS)
    assert got == [("ch_1", "Alpha"), ("ch_2", "Alpha"), ("ch_3", "Beta"), ("ch_4", "UNKNOWN")]


def test_top_k_with_tiebreak(ex):
    # 700 出现两次：ch_3 和 ch_4，按 charge_id 升序 → ch_3 在前
    assert ex.top_k(ROWS, 3) == ["ch_1", "ch_3", "ch_4"]
    assert ex.top_k(ROWS, 100) == ["ch_1", "ch_3", "ch_4", "ch_2", "ch_5", "ch_6"]
    assert ex.top_k(ROWS, 0) == []


def test_dispute_ratio_strict_and_exact(ex):
    # m_a: 1/2 = 0.5（不 > 0.5）；m_b: 0/1；m_c: 2/3 > 0.5
    assert ex.dispute_ratio_over(ROWS, 1, 2) == ["m_c"]
    # 阈值 1/3：m_a 1/2 > 1/3 ✓；m_c 2/3 ✓；字典序
    assert ex.dispute_ratio_over(ROWS, 1, 3) == ["m_a", "m_c"]
    # 恰好相等不算：m_c 2/3 与 2/3
    assert ex.dispute_ratio_over(ROWS, 2, 3) == []
