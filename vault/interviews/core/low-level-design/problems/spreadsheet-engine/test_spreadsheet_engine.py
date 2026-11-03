"""电子表格引擎的 pytest 套件：`-k part1` 选第 1 关，依此类推。"""

import importlib
import os

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def sheet(**cells: str):
    s = impl.Spreadsheet()
    for name, raw in cells.items():
        s.set(name, raw)
    return s


def diamond():
    return sheet(A1="1", B1="=A1+1", C1="=A1+2", D1="=B1+C1")


# ---- 第 1 关：字面量、求和公式、环检测 ------------------------------


def test_part1_literals_and_empty_cells():
    s = sheet(A1="42", B1="-3.5")
    assert s.get("A1") == 42
    assert s.get("B1") == -3.5
    assert s.get("C9") == 0.0


def test_part1_formula_sees_later_changes_and_forward_references():
    s = sheet(C1="=A1+B1")  # A1、B1 还没赋值
    assert s.get("C1") == 0
    s.set("A1", "5")
    s.set("B1", "6")
    assert s.get("C1") == 11
    s.set("A1", "1")
    assert s.get("C1") == 7


def test_part1_long_chain():
    s = sheet(A1="1")
    for i in range(2, 60):
        s.set(f"A{i}", f"=A{i - 1}+1")
    assert s.get("A59") == 59


def test_part1_overwrite_and_clear():
    s = sheet(A1="1", B1="=A1+1")
    s.set("B1", "10")
    s.set("A1", "99")
    assert s.get("B1") == 10
    s.set("B1", "")
    assert s.get("B1") == 0


@pytest.mark.parametrize("name", ["a1", "A0", "AA1", "A1000", "1A", "", "A01"])
def test_part1_invalid_cell_names(name):
    s = impl.Spreadsheet()
    with pytest.raises(impl.InvalidCellError):
        s.set(name, "1")
    with pytest.raises(impl.InvalidCellError):
        s.get(name)


@pytest.mark.parametrize("raw", ["=1+", "=A1 +* 2", "=(1", "=a1", "=1 2", "=", "abc", "=1)", "=AA1+1", "=A1000"])
def test_part1_bad_formula_raises_and_keeps_the_cell(raw):
    s = sheet(A1="7")
    with pytest.raises(impl.InvalidFormulaError):
        s.set("A1", raw)
    assert s.get("A1") == 7


def test_part1_self_reference_is_rejected():
    s = sheet(A1="5")
    with pytest.raises(impl.CycleError):
        s.set("A1", "=A1+1")
    assert s.get("A1") == 5


def test_part1_indirect_cycle_is_rejected_and_sheet_unchanged():
    s = sheet(A1="1", B1="=A1+1", C1="=B1+1")
    with pytest.raises(impl.CycleError):
        s.set("A1", "=C1")
    assert (s.get("A1"), s.get("B1"), s.get("C1")) == (1, 2, 3)
    s.set("A1", "10")  # 拒绝之后表格照常工作
    assert s.get("C1") == 12


def test_part1_long_cycle():
    s = sheet(A1="1")
    for prev, cur in zip("ABCDEFG", "BCDEFGH"):
        s.set(f"{cur}1", f"={prev}1+1")
    with pytest.raises(impl.CycleError):
        s.set("A1", "=H1")


def test_part1_diamond_and_repeated_reference_are_not_cycles():
    s = diamond()
    s.set("E1", "=D1+D1+A1")
    assert s.get("E1") == 2 * 5 + 1


def test_part1_rewiring_leaves_no_stale_edge():
    s = sheet(A1="=B1", B1="3", C1="7")
    s.set("A1", "=C1")  # A1 不再读 B1
    s.set("B1", "=A1+1")  # 如果还残留 A1->B1 的旧边，这里会被误判成环
    assert s.get("B1") == 8


def test_part1_failed_cycle_keeps_old_formula_working():
    s = sheet(A1="2", B1="=A1+A1")
    with pytest.raises(impl.CycleError):
        s.set("B1", "=B1")
    s.set("A1", "3")
    assert s.get("B1") == 6


def test_part1_sum_formulas_with_references_and_numbers():
    s = sheet(A1="2", B1="3")
    s.set("C1", "=A1+B1+3")
    s.set("D1", "= A1 + 1.5 + C1 ")
    s.set("E1", "=B1")
    s.set("F1", "=1+2")
    assert (s.get("C1"), s.get("D1"), s.get("E1"), s.get("F1")) == (8, 11.5, 3, 3)


# ---- 第 2 关：完整表达式 ------------------------------


def test_part2_formula_precedence_parentheses_and_negation():
    s = sheet(A1="2", B1="3")
    s.set("C1", "=A1+B1*2")
    s.set("D1", "=(A1+B1)*2")
    s.set("E1", "=-(A1+B1)*2")
    s.set("F1", "=7/2")
    s.set("G1", "=10-4-3")  # 左结合
    assert s.get("C1") == 8
    assert s.get("D1") == 10
    assert s.get("E1") == -10
    assert s.get("F1") == 3.5
    assert s.get("G1") == 3


def test_part2_division_by_zero_is_an_error_that_recovers():
    s = sheet(B1="=1/A1")
    with pytest.raises(impl.EvalError):
        s.get("B1")
    s.set("A1", "4")
    assert s.get("B1") == 0.25


def test_part2_left_associative_and_spaces():
    s = sheet(A1="20", B1="3")
    s.set("C1", "=A1 - B1 - 2")
    s.set("D1", "=A1 / 2 / 5")
    s.set("E1", "= 2 * ( A1 - B1 ) * 2")
    s.set("F1", "=A1+-3")
    s.set("G1", "=--A1")
    assert (s.get("C1"), s.get("D1"), s.get("E1"), s.get("F1"), s.get("G1")) == (15, 2, 68, 17, 20)


@pytest.mark.parametrize("raw", ["=2**3", "=(1+2", "=1+(", "=()", "=*1", "=1+/2", "=A1 B1", "=1..2"])
def test_part2_bad_expressions_raise_and_keep_the_cell(raw):
    s = sheet(A1="7")
    with pytest.raises(impl.InvalidFormulaError):
        s.set("A1", raw)
    assert s.get("A1") == 7


def test_part2_division_errors_propagate_through_other_cells():
    s = sheet(B1="=1/A1", C1="=B1+1")
    with pytest.raises(impl.EvalError):
        s.get("C1")
    s.set("A1", "2")
    assert s.get("C1") == 1.5


def test_part2_cycle_detection_sees_references_inside_expressions():
    s = sheet(A1="1", B1="=2*(A1+1)")
    with pytest.raises(impl.CycleError):
        s.set("A1", "=-B1/2")
    assert s.get("B1") == 4


# ---- 第 3 关：按依赖顺序重算 ------------------------------


def test_part3_diamond_recomputes_each_cell_once():
    s = diamond()
    before = s.eval_count
    s.set("A1", "10")
    assert s.eval_count - before == 3  # B1、C1、D1 各一次，D1 不会因为两条路径算两次
    assert (s.get("B1"), s.get("C1"), s.get("D1")) == (11, 12, 23)


def test_part3_unrelated_cells_are_not_recomputed():
    s = sheet(A1="1", B1="=A1+1", X1="5", Y1="=X1*2")
    before = s.eval_count
    s.set("A1", "2")
    assert s.eval_count - before == 1
    assert s.get("Y1") == 10


def test_part3_get_never_evaluates():
    s = diamond()
    before = s.eval_count
    for _ in range(5):
        s.get("D1")
    assert s.eval_count == before


def test_part3_new_formula_is_evaluated_once_with_its_downstream():
    s = sheet(A1="1", C1="=B1+1")  # C1 依赖尚未存在的 B1
    before = s.eval_count
    s.set("B1", "=A1+1")  # B1 一次，下游 C1 一次
    assert s.eval_count - before == 2
    assert s.get("C1") == 3


def test_part3_deep_chain_is_computed_in_dependency_order():
    s = impl.Spreadsheet()
    for i in range(59, 1, -1):  # 反着写：先写下游，后写上游
        s.set(f"A{i}", f"=A{i - 1}+1")
    before = s.eval_count
    s.set("A1", "1")
    assert s.eval_count - before == 58
    assert s.get("A59") == 59


def test_part3_error_propagates_downstream_and_recovers():
    s = sheet(B1="=1/A1", C1="=B1+1", D1="=C1*2")
    for c in ("B1", "C1", "D1"):
        with pytest.raises(impl.EvalError):
            s.get(c)
    s.set("A1", "2")
    assert (s.get("B1"), s.get("C1"), s.get("D1")) == (0.5, 1.5, 3.0)


def test_part3_replacing_a_formula_drops_the_old_dependency():
    s = sheet(A1="1", B1="=A1")
    s.set("B1", "5")
    before = s.eval_count
    s.set("A1", "2")
    assert s.eval_count == before
    assert s.get("B1") == 5


def test_part3_clearing_a_cell_updates_its_users():
    s = sheet(A1="4", B1="=A1+1")
    s.set("A1", "")
    assert s.get("B1") == 1


def test_part3_rejected_cycle_does_not_evaluate_anything():
    s = sheet(A1="1", B1="=A1+1", C1="=B1+1")
    before = s.eval_count
    with pytest.raises(impl.CycleError):
        s.set("A1", "=C1")
    assert s.eval_count == before
    assert (s.get("A1"), s.get("B1"), s.get("C1")) == (1, 2, 3)
    s.set("A1", "10")  # 拒绝之后表格照常工作
    assert s.get("C1") == 12


# ---- 第 4 关：区间函数 ------------------------------


def test_part4_sum_min_max_over_a_rectangle():
    s = sheet(A1="1", A2="2", B1="3", B2="-4")
    s.set("C1", "=SUM(A1:B2)")
    s.set("C2", "=MIN(A1:B2)")
    s.set("C3", "=MAX(A1:B2)")
    assert (s.get("C1"), s.get("C2"), s.get("C3")) == (2, -4, 3)


def test_part4_empty_cells_are_ignored_and_filling_them_recomputes():
    s = sheet(A1="5", A3="7")
    s.set("B1", "=MIN(A1:A3)")
    s.set("B2", "=SUM(A1:A3)")
    assert (s.get("B1"), s.get("B2")) == (5, 12)  # 空的 A2 不算作 0
    s.set("A2", "-1")
    assert (s.get("B1"), s.get("B2")) == (-1, 11)


def test_part4_function_inside_an_expression_and_all_empty_range():
    s = sheet(A1="2", A2="3")
    s.set("B1", "=SUM(A1:A2)*2+MAX(A1:A2)")
    assert s.get("B1") == 13
    s.set("B2", "=MIN(C1:C3)")
    assert s.get("B2") == 0


def test_part4_range_participates_in_cycle_detection():
    s = sheet(A1="1", A2="2")
    with pytest.raises(impl.CycleError):
        s.set("A3", "=SUM(A1:A3)")
    s.set("B1", "=SUM(A1:A2)")
    with pytest.raises(impl.CycleError):
        s.set("A1", "=B1")


@pytest.mark.parametrize("raw", ["=SUM(B1:A1)", "=SUM(A3:A1)", "=SUM(A1)", "=SUM(A1:B)", "=SUM A1:A2", "=AVG(A1:A2)"])
def test_part4_bad_ranges(raw):
    s = impl.Spreadsheet()
    with pytest.raises(impl.InvalidFormulaError):
        s.set("Z1", raw)


def test_part4_error_inside_range_propagates():
    s = sheet(A1="=1/B1", A2="3")
    s.set("C1", "=SUM(A1:A2)")
    with pytest.raises(impl.EvalError):
        s.get("C1")
    s.set("B1", "1")
    assert s.get("C1") == 4
