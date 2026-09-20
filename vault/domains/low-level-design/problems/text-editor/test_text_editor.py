"""文本编辑器的验收测试：缓冲区、撤销重做、连打合并与选区、查找替换。

断言全部只用公开 API（`text`、`cursor`、`selection`、`undo_depth`、`gap_size`），
不碰任何下划线属性——换一套内部表示（比如 piece table）也应该照样通过。
"""

from __future__ import annotations

import importlib
import os
import random

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


# ---------------------------------------------------------------------------
# 第 1 关：缓冲区、光标、选区
# ---------------------------------------------------------------------------


def test_gap_buffer_round_trips_text_and_slices() -> None:
    buffer = impl.GapBuffer("hello world")
    assert buffer.text == "hello world"
    assert len(buffer) == 11
    assert buffer.slice(0, 5) == "hello"
    assert buffer.slice(6, 11) == "world"
    assert buffer.slice(4, 7) == "o w"          # 跨过空洞的切片也必须对


def test_gap_buffer_inserts_at_head_middle_and_tail() -> None:
    buffer = impl.GapBuffer("bd")
    buffer.insert(1, "c")
    buffer.insert(0, "a")
    buffer.insert(len(buffer), "e")
    assert buffer.text == "abcde"
    assert buffer.slice(1, 4) == "bcd"


def test_gap_buffer_delete_returns_what_it_removed() -> None:
    buffer = impl.GapBuffer("abcdef")
    assert buffer.delete(2, 3) == "cde"
    assert buffer.text == "abf"
    assert len(buffer) == 3


def test_gap_buffer_grows_when_the_gap_runs_out() -> None:
    expected = "".join(chr(ord("a") + i % 26) for i in range(100))
    buffer = impl.GapBuffer("", min_gap=4)
    for char in expected:
        buffer.insert(len(buffer), char)        # 每次都在末尾追加，空洞会被用光好几次
    assert len(buffer) == 100
    assert buffer.text == expected
    buffer.insert(50, "|")
    assert buffer.slice(49, 52) == expected[49] + "|" + expected[50]


def test_gap_buffer_does_not_hoard_memory_after_a_large_deletion() -> None:
    """删掉一大段之后空洞必须被收回，否则"删掉 10 MB"的文档永远占着 10 MB。"""
    buffer = impl.GapBuffer("y" * 5000, min_gap=16)
    buffer.delete(0, 4900)
    assert buffer.text == "y" * 100
    assert buffer.gap_size <= max(64, len(buffer) * 2)


def test_out_of_range_positions_are_rejected() -> None:
    buffer = impl.GapBuffer("abc")
    with pytest.raises(impl.InvalidRangeError):
        buffer.slice(0, 99)
    with pytest.raises(impl.InvalidRangeError):
        buffer.insert(-1, "x")
    with pytest.raises(impl.EditorError):
        buffer.delete(2, 5)


def test_cursor_follows_typing() -> None:
    editor = impl.Editor()
    editor.type("abc")
    assert editor.text == "abc"
    assert editor.cursor == 3
    editor.move_cursor(1)
    editor.type("Z")
    assert editor.text == "aZbc"
    assert editor.cursor == 2


def test_moving_the_cursor_clears_the_selection() -> None:
    editor = impl.Editor("hello world")
    editor.select(0, 5)
    assert editor.selection == (0, 5)
    assert editor.selected_text == "hello"
    editor.move_cursor(8)
    assert editor.selection is None
    editor.type("X")                            # 必须插在 8 处，而不是替换掉 hello
    assert editor.text == "hello woXrld"


def test_selection_is_normalised_and_empty_selection_is_none() -> None:
    editor = impl.Editor("abcdef")
    editor.select(4, 4)
    assert editor.selection is None
    editor.select(1, 4)
    assert editor.selection == (1, 4)
    with pytest.raises(impl.InvalidRangeError):
        editor.select(4, 1)


# ---------------------------------------------------------------------------
# 第 2 关：撤销与重做
# ---------------------------------------------------------------------------


def test_edit_invert_is_a_field_swap() -> None:
    edit = impl.Edit(position=3, removed="ab", inserted="XYZ", cursor_before=3, cursor_after=6)
    back = edit.invert()
    assert (back.position, back.removed, back.inserted) == (3, "XYZ", "ab")
    assert (back.cursor_before, back.cursor_after) == (6, 3)
    assert back.invert() == edit                # 两次求逆回到原点


def test_undo_restores_both_text_and_cursor() -> None:
    editor = impl.Editor("hello")
    editor.move_cursor(5)
    editor.insert(0, "say ")
    assert editor.text == "say hello"
    assert editor.undo() is True
    assert editor.text == "hello"
    assert editor.cursor == 5                   # 光标也回到编辑之前


def test_redo_reapplies_the_edit() -> None:
    editor = impl.Editor()
    editor.insert(0, "abc")
    editor.undo()
    assert editor.can_redo is True
    assert editor.redo() is True
    assert editor.text == "abc"
    assert editor.can_redo is False


def test_a_new_edit_clears_the_redo_stack() -> None:
    editor = impl.Editor()
    editor.insert(0, "abc")
    editor.insert(3, "def")
    editor.undo()
    assert editor.can_redo is True
    editor.insert(0, "Z")                       # 历史在这里分叉了
    assert editor.can_redo is False
    assert editor.text == "Zabc"


def test_undo_past_the_branch_point_is_still_coherent() -> None:
    editor = impl.Editor()
    editor.insert(0, "abc")
    editor.insert(3, "def")
    editor.undo()
    editor.insert(0, "Z")
    assert editor.undo() is True and editor.text == "abc"
    assert editor.undo() is True and editor.text == ""
    assert editor.undo() is False               # 空历史上撤销是安静的假，不是异常


def test_history_is_bounded_and_drops_the_oldest_unit() -> None:
    editor = impl.Editor(history_limit=5)
    for i in range(20):
        editor.insert(len(editor.text), str(i % 10))
    assert editor.undo_depth == 5
    while editor.undo():
        pass
    assert editor.text != ""                    # 最旧的那些编辑已经撤不回来了
    assert len(editor.text) == 15


def test_replaying_an_edit_against_changed_text_is_refused() -> None:
    document = impl.Document("hello")
    edit = document.make_edit(0, 5, "bye")
    document.apply(edit)
    with pytest.raises(impl.InconsistentEditError):
        document.apply(edit)                    # 同一条编辑不能在新文本上再来一次


def test_random_edits_and_undos_match_a_replayed_model() -> None:
    """长随机序列：每一步之后，编辑器的文本必须等于朴素模型（逐步重放）给出的文本。"""
    rng = random.Random(20260920)
    editor = impl.Editor("start", history_limit=10_000)
    model = [editor.text]
    for _ in range(600):
        roll = rng.random()
        if roll < 0.45:
            position = rng.randint(0, len(editor.text))
            editor.insert(position, rng.choice(["a", "bc", "\n", "xyz"]))
            model.append(editor.text)
        elif roll < 0.75 and editor.text:
            start = rng.randint(0, len(editor.text) - 1)
            end = min(len(editor.text), start + rng.randint(1, 3))
            editor.delete(start, end)
            model.append(editor.text)
        elif editor.can_undo:
            editor.undo()
            model.pop()
        assert editor.text == model[-1]
    while editor.undo():
        pass
    assert editor.text == "start"               # 一路撤到底，回到最初的文本


# ---------------------------------------------------------------------------
# 第 3 关：连打合并与选区操作
# ---------------------------------------------------------------------------


def test_typing_a_word_is_one_undo_step() -> None:
    editor = impl.Editor()
    for char in "hello":
        editor.type(char)
    assert editor.text == "hello"
    assert editor.undo_depth == 1
    editor.undo()
    assert editor.text == ""


def test_a_newline_ends_the_typing_run() -> None:
    editor = impl.Editor()
    for char in "ab\ncd":
        editor.type(char)
    editor.undo()
    assert editor.text == "ab\n"                # 只撤掉换行之后敲的那段
    editor.undo()
    assert editor.text == "ab"


def test_a_long_run_is_capped_so_one_undo_is_not_a_whole_paragraph() -> None:
    editor = impl.Editor(max_run=5)
    for char in "abcdefghij":
        editor.type(char)
    assert editor.undo_depth == 2
    editor.undo()
    assert editor.text == "abcde"


def test_moving_the_cursor_breaks_the_typing_run() -> None:
    editor = impl.Editor()
    for char in "abc":
        editor.type(char)
    editor.move_cursor(0)
    for char in "XY":
        editor.type(char)
    assert editor.text == "XYabc"
    assert editor.undo_depth == 2
    editor.undo()
    assert editor.text == "abc"


def test_programmatic_inserts_never_coalesce_even_when_adjacent() -> None:
    """相邻不等于同一个意图：两次刻意的 insert 必须是两步撤销。"""
    editor = impl.Editor()
    editor.insert(0, "abc")
    editor.insert(3, "def")
    assert editor.undo_depth == 2
    editor.undo()
    assert editor.text == "abc"


def test_typing_over_a_selection_replaces_it_in_one_undo_step() -> None:
    editor = impl.Editor("hello world")
    editor.select(0, 5)
    editor.type("bye")
    assert editor.text == "bye world"
    assert editor.selection is None
    editor.undo()
    assert editor.text == "hello world"


def test_backspace_deletes_the_selection_or_one_character() -> None:
    editor = impl.Editor("abcdef")
    editor.move_cursor(3)
    editor.backspace()
    assert editor.text == "abdef"
    editor.select(0, 2)
    editor.backspace()
    assert editor.text == "def"
    editor.move_cursor(0)
    editor.backspace()                          # 开头退格什么也不做，也不该留下撤销单元
    assert editor.text == "def"
    assert editor.undo_depth == 2


def test_cut_copy_paste_round_trip() -> None:
    editor = impl.Editor("hello world")
    editor.select(0, 6)
    assert editor.cut() == "hello "
    assert editor.text == "world"
    editor.move_cursor(5)
    editor.paste()
    assert editor.text == "worldhello "
    editor.select(0, 5)
    assert editor.copy() == "world"
    assert editor.text == "worldhello "         # 复制不改文档


def test_undo_of_a_cut_restores_the_text_but_not_the_clipboard() -> None:
    editor = impl.Editor("abcdef")
    editor.select(1, 4)
    editor.cut()
    assert (editor.text, editor.clipboard) == ("aef", "bcd")
    editor.undo()
    assert editor.text == "abcdef"
    assert editor.clipboard == "bcd"            # 撤销撤的是文档，不是系统剪贴板


# ---------------------------------------------------------------------------
# 第 4 关：查找与替换（不改动命令机制）
# ---------------------------------------------------------------------------


def test_find_and_find_all_report_non_overlapping_matches() -> None:
    editor = impl.Editor("the cat sat on the mat")
    assert editor.find("at") == 5
    assert editor.find("at", 6) == 9
    assert editor.find("dog") == -1
    assert editor.find_all("at") == (5, 9, 20)
    assert editor.find_all("aaa") == ()


def test_replace_all_is_a_single_undo_step() -> None:
    editor = impl.Editor("the cat sat on the mat")
    assert editor.replace_all("at", "og") == 3
    assert editor.text == "the cog sog on the mog"
    assert editor.undo_depth == 1
    editor.undo()
    assert editor.text == "the cat sat on the mat"
    editor.redo()
    assert editor.text == "the cog sog on the mog"


def test_replace_all_handles_a_longer_replacement_without_shifting_offsets() -> None:
    editor = impl.Editor("x-x-x")
    assert editor.replace_all("x", "LONG") == 3
    assert editor.text == "LONG-LONG-LONG"
    editor.undo()
    assert editor.text == "x-x-x"


def test_replace_all_reports_zero_when_nothing_matches() -> None:
    editor = impl.Editor("abc")
    assert editor.replace_all("zz", "y") == 0
    assert editor.text == "abc"
    assert editor.can_undo is False


def test_history_rejects_a_non_positive_limit() -> None:
    with pytest.raises(ValueError):
        impl.History(limit=0)
    with pytest.raises(ValueError):
        impl.History(max_run=0)


def test_history_is_a_pure_stack_machine_over_edits() -> None:
    """`History` 不认识 `Document`：只给它 `Edit`，它照样能正确地分组、求逆、限深。"""
    history = impl.History()
    first = impl.Edit(0, "", "ab", 0, 2)
    second = impl.Edit(2, "", "cd", 2, 4)
    history.record(first, coalesce=True)
    history.record(second, coalesce=True)
    assert history.undo_depth == 1              # 首尾相接的键入并成了一个单元
    undone = history.undo()
    assert [e.inserted for e in undone] == ["", ""]
    assert [e.removed for e in undone] == ["cd", "ab"]   # 逆序求逆
    assert history.can_redo is True
