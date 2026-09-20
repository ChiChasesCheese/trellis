"""文本编辑器：插入、删除、光标与选区，以及撤销／重做。
设计：`GapBuffer` 用"光标处留一个空洞"的数组，让连续在同一处的插入删除摊销 O(1)；
`Document` 在它之上管光标与选区，并且只认一种修改——`Edit`（一次 splice：删掉一段、插入一段）。
`Edit` 是冻结的数据，`invert()` 就是把 removed/inserted 两个字段对调，所以撤销不需要任何子类。
`History` 是一台只认 `Edit` 元组的纯栈机（一个元组 = 一个撤销单元），`Editor` 是对外的门面。
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


class EditorError(Exception):
    """本设计全部失败路径的公共基类。"""


class InvalidRangeError(EditorError, ValueError):
    """位置或区间越界、或者 start > end。"""


class InconsistentEditError(EditorError):
    """要重放的编辑与当前文本对不上——说明历史栈和文档已经不同步了。"""


class GapBuffer:
    """字符数组，中间留一个"空洞"（gap）。空洞就在最近一次编辑的位置。

    插入：把空洞挪到目标位置（代价 O(移动距离)），然后填字符，摊销 O(1)。
    删除：把空洞挪到目标位置，然后把空洞向右扩大，O(1)。
    真实编辑高度局部（人一直在同一处敲字），所以"移动距离"通常是 0。
    """

    def __init__(self, text: str = "", min_gap: int = 64) -> None:
        if min_gap <= 0:
            raise ValueError(f"min_gap must be positive, got {min_gap}")
        self._min_gap = min_gap
        self._chars: list[str] = list(text) + [""] * min_gap
        self._gap_start = len(text)
        self._gap_end = len(self._chars)

    def __len__(self) -> int:
        return len(self._chars) - self.gap_size

    @property
    def gap_size(self) -> int:
        """空洞当前有多大。暴露成公开属性，是为了让"空洞不会无限膨胀"这条不变量可以被断言。"""
        return self._gap_end - self._gap_start

    @property
    def gap_position(self) -> int:
        """空洞左边界在文本中的下标，也就是"上一次编辑发生在哪"。"""
        return self._gap_start

    @property
    def text(self) -> str:
        return "".join(self._chars[:self._gap_start]) + "".join(self._chars[self._gap_end:])

    def _check(self, index: int) -> None:
        if not 0 <= index <= len(self):
            raise InvalidRangeError(f"index {index} out of range 0..{len(self)}")

    def slice(self, start: int, end: int) -> str:
        """取 [start, end) 的文本。下标是**文本下标**，空洞对调用方完全不可见。"""
        self._check(start)
        self._check(end)
        if start > end:
            raise InvalidRangeError(f"start {start} is after end {end}")
        gap_start, gap_end = self._gap_start, self._gap_end
        left = "".join(self._chars[start:min(end, gap_start)]) if start < gap_start else ""
        right = ""
        if end > gap_start:
            begin = max(start, gap_start) - gap_start + gap_end
            right = "".join(self._chars[begin:end - gap_start + gap_end])
        return left + right

    def _move_gap(self, index: int) -> None:
        """把空洞挪到 index。挪动就是把中间那段字符整体搬到空洞另一侧，代价是搬运的字符数。"""
        if index < self._gap_start:
            count = self._gap_start - index
            self._chars[self._gap_end - count:self._gap_end] = self._chars[index:self._gap_start]
            self._gap_start -= count
            self._gap_end -= count
        elif index > self._gap_start:
            count = index - self._gap_start
            self._chars[self._gap_start:self._gap_start + count] = self._chars[self._gap_end:self._gap_end + count]
            self._gap_start += count
            self._gap_end += count

    def _grow(self, needed: int) -> None:
        """空洞不够用了就扩：按当前长度的一半扩，让"连续打字"整体是摊销 O(1) 而不是每次都扩。"""
        extra = max(needed, len(self) // 2, self._min_gap)
        self._chars[self._gap_end:self._gap_end] = [""] * extra
        self._gap_end += extra

    def _shrink_if_wasteful(self) -> None:
        """删掉一大段之后，空洞会变得和被删的那段一样大。不收回来，一个"删掉 10 MB"的文档
        就会永远占着 10 MB——所以空洞超过"文本长度"且超过下限的四倍时，把多余的还给内存。"""
        if self.gap_size > max(self._min_gap * 4, len(self)):
            keep = max(self._min_gap, len(self) // 2)
            del self._chars[self._gap_start + keep:self._gap_end]
            self._gap_end = self._gap_start + keep

    def insert(self, index: int, text: str) -> None:
        self._check(index)
        if not text:
            return
        self._move_gap(index)
        if self.gap_size < len(text):
            self._grow(len(text))
        for char in text:
            self._chars[self._gap_start] = char
            self._gap_start += 1

    def delete(self, index: int, count: int) -> str:
        """删掉 [index, index+count) 并返回被删的文本——逆操作需要它。"""
        self._check(index)
        if count <= 0:
            return ""
        if index + count > len(self):
            raise InvalidRangeError(f"cannot delete {count} chars at {index}: only {len(self) - index} left")
        self._move_gap(index)
        removed = "".join(self._chars[self._gap_end:self._gap_end + count])
        self._gap_end += count
        self._shrink_if_wasteful()
        return removed

    def find(self, needle: str, start: int = 0) -> int:
        """朴素查找，找不到返回 -1。大文档上该换成在片段上流式匹配，这里保持简单。"""
        return self.text.find(needle, start)


@dataclass(frozen=True, slots=True)
class Edit:
    """一次修改的完整描述：在 `position` 处把 `removed` 换成 `inserted`。

    **所有**修改都是这一种形状：插入是 `removed == ""`，删除是 `inserted == ""`，
    替换两者都非空。因此不需要 `InsertCommand`／`DeleteCommand`／`ReplaceCommand` 三个类，
    也不需要抽象基类——撤销所需的全部信息就是这五个字段，而逆操作就是把两个字段对调。
    光标位置是唯一值得整体快照的状态（它太小、又很难从逆操作反推），所以一并带上。
    """

    position: int
    removed: str
    inserted: str
    cursor_before: int
    cursor_after: int

    @property
    def is_insertion(self) -> bool:
        """纯插入（没删任何东西）——只有这种编辑才有资格并进同一个"连打"撤销单元。"""
        return not self.removed and bool(self.inserted)

    def invert(self) -> Edit:
        """逆操作。注意它是一次纯粹的字段对调，没有任何计算，也没有任何子类分支。"""
        return Edit(self.position, self.inserted, self.removed, self.cursor_after, self.cursor_before)


class Document:
    """文本 + 光标 + 选区。它只认识一种修改动作：`apply(edit)`。

    不变量：光标永远落在 `0..len(text)`；任何一次 `apply` 都会清掉选区（改了字之后旧选区
    指向的区间已经没有意义了）；`apply` 会先核对 `edit.removed` 和当前文本是否一致，
    对不上就抛错——这把"重放到已经变了的文本上"从静默写坏变成了当场失败。
    """

    def __init__(self, text: str = "") -> None:
        self._buffer = GapBuffer(text)
        self._cursor = 0
        self._anchor: int | None = None

    @property
    def text(self) -> str:
        return self._buffer.text

    @property
    def gap_size(self) -> int:
        """转发底层空洞的大小，供测试断言"空洞不会无限膨胀"。"""
        return self._buffer.gap_size

    def __len__(self) -> int:
        return len(self._buffer)

    @property
    def cursor(self) -> int:
        return self._cursor

    @property
    def selection(self) -> tuple[int, int] | None:
        """选区，规范化成 (start, end)；没有选区时是 `None`，而不是一个空区间。"""
        if self._anchor is None or self._anchor == self._cursor:
            return None
        return (min(self._anchor, self._cursor), max(self._anchor, self._cursor))

    @property
    def selected_text(self) -> str:
        span = self.selection
        return "" if span is None else self._buffer.slice(*span)

    def _check(self, index: int) -> None:
        if not 0 <= index <= len(self):
            raise InvalidRangeError(f"position {index} out of range 0..{len(self)}")

    def move_cursor(self, position: int) -> None:
        """移动光标**一定**会清掉选区：在任何一个编辑器里，点到别处就等于取消选中。
        少了这一句，下一次输入会去替换一段离光标十万八千里的文字。"""
        self._check(position)
        self._cursor = position
        self._anchor = None

    def select(self, start: int, end: int) -> None:
        self._check(start)
        self._check(end)
        if start > end:
            raise InvalidRangeError(f"start {start} is after end {end}")
        self._anchor = start
        self._cursor = end

    def clear_selection(self) -> None:
        self._anchor = None

    def find(self, needle: str, start: int = 0) -> int:
        return self._buffer.find(needle, start)

    def make_edit(self, position: int, delete_length: int, inserted: str) -> Edit:
        """按"此刻的文本"造一个 `Edit`。

        被删掉的文本是在**这一刻**读出来的，不是在某个构造函数里提前读的：重做一串编辑时，
        每一条看到的都是上一条留下的文本，提前读只会读到错的那一段。
        """
        self._check(position)
        if delete_length < 0 or position + delete_length > len(self):
            raise InvalidRangeError(f"cannot delete {delete_length} chars at {position}")
        removed = self._buffer.slice(position, position + delete_length)
        return Edit(position, removed, inserted, self._cursor, position + len(inserted))

    def apply(self, edit: Edit) -> None:
        actual = self._buffer.slice(edit.position, min(edit.position + len(edit.removed), len(self)))
        if actual != edit.removed:
            raise InconsistentEditError(
                f"edit at {edit.position} expects {edit.removed!r} but the document has {actual!r}"
            )
        if edit.removed:
            self._buffer.delete(edit.position, len(edit.removed))
        if edit.inserted:
            self._buffer.insert(edit.position, edit.inserted)
        self._cursor = edit.cursor_after
        self._anchor = None


class History:
    """撤销／重做的栈机。它只认 `Edit`，完全不知道 `Document` 的存在，因此可以单独测试。

    一个**撤销单元**是一个 `Edit` 元组：连打出来的一串字符是一个单元，替换全部匹配项产生的
    十二处修改也是一个单元。撤销就是把单元里的编辑逆序逐条求逆再交还给调用方。
    两条容易被忽视的规则：新编辑一律清空重做栈（否则重做会把一条编辑重放到已经变了的文本上）；
    撤销栈有上限，超出时丢**最旧**的（丢最新的等于偷偷吃掉用户刚做的事）。
    """

    def __init__(self, limit: int = 200, max_run: int = 40) -> None:
        if limit <= 0:
            raise ValueError(f"limit must be positive, got {limit}")
        if max_run <= 0:
            raise ValueError(f"max_run must be positive, got {max_run}")
        self._limit = limit
        self._max_run = max_run
        self._undo: list[tuple[Edit, ...]] = []
        self._redo: list[tuple[Edit, ...]] = []
        self._run_open = False

    @property
    def limit(self) -> int:
        return self._limit

    @property
    def undo_depth(self) -> int:
        return len(self._undo)

    @property
    def redo_depth(self) -> int:
        return len(self._redo)

    @property
    def can_undo(self) -> bool:
        return bool(self._undo)

    @property
    def can_redo(self) -> bool:
        return bool(self._redo)

    def break_run(self) -> None:
        """显式结束当前连打：移动光标、改选区、撤销之后都要调用。"""
        self._run_open = False

    def _can_merge(self, unit: tuple[Edit, ...], edit: Edit) -> bool:
        """能并进同一个撤销单元的条件：都是纯插入、首尾相接、不含换行、整段不超过 `max_run`。

        换行是天然的撤销边界；长度上限保证一次撤销不会抹掉一整段——两者都是"用户心里的一步"
        的近似，而不是代码结构的产物。
        """
        last = unit[-1]
        if not (last.is_insertion and edit.is_insertion):
            return False
        if last.position + len(last.inserted) != edit.position:
            return False
        if "\n" in last.inserted or "\n" in edit.inserted:
            return False
        return sum(len(e.inserted) for e in unit) + len(edit.inserted) <= self._max_run

    def _push(self, unit: tuple[Edit, ...]) -> None:
        self._undo.append(unit)
        if len(self._undo) > self._limit:
            del self._undo[0]

    def record(self, edit: Edit, coalesce: bool = False) -> None:
        """记一次编辑。`coalesce=True` 表示"这是一次键盘输入"，允许并进上一个单元。

        合并与否是**调用方的意图**，不是两条编辑相邻与否能推出来的：两次程序化的 `insert`
        恰好首尾相接，也绝不该被偷偷折成一步。
        """
        self._redo.clear()
        if coalesce and self._run_open and self._undo and self._can_merge(self._undo[-1], edit):
            self._undo[-1] = (*self._undo[-1], edit)
            return
        self._push((edit,))
        self._run_open = coalesce

    def record_group(self, edits: Sequence[Edit]) -> None:
        """把一批编辑记成**一个**撤销单元（替换全部匹配项、缩进一段等）。顺序必须是实际执行顺序。"""
        if not edits:
            return
        self._redo.clear()
        self._push(tuple(edits))
        self._run_open = False

    def undo(self) -> tuple[Edit, ...]:
        """弹出一个撤销单元，返回**应当按序执行**的逆编辑；没有可撤销的就返回空元组。

        逆序是硬要求：单元里后执行的编辑改变了先执行的编辑所依赖的下标，必须先撤销后来的那条。
        """
        if not self._undo:
            return ()
        unit = self._undo.pop()
        self._redo.append(unit)
        self._run_open = False
        return tuple(edit.invert() for edit in reversed(unit))

    def redo(self) -> tuple[Edit, ...]:
        if not self._redo:
            return ()
        unit = self._redo.pop()
        self._undo.append(unit)
        self._run_open = False
        return unit


class Editor:
    """对外的门面：把"文档 + 历史 + 剪贴板"三样东西合成一套编辑器动作。

    它承担的责任是**翻译**：把"按了退格"这种用户动作翻译成"在哪一处、删几个字、插什么"，
    并决定这一次该不该并进上一个撤销单元。真正的活分别由 `Document` 和 `History` 干。
    """

    def __init__(self, text: str = "", history_limit: int = 200, max_run: int = 40) -> None:
        self._document = Document(text)
        self._history = History(history_limit, max_run)
        self._clipboard = ""

    @property
    def text(self) -> str:
        return self._document.text

    @property
    def cursor(self) -> int:
        return self._document.cursor

    @property
    def selection(self) -> tuple[int, int] | None:
        return self._document.selection

    @property
    def selected_text(self) -> str:
        return self._document.selected_text

    @property
    def clipboard(self) -> str:
        return self._clipboard

    @property
    def can_undo(self) -> bool:
        return self._history.can_undo

    @property
    def can_redo(self) -> bool:
        return self._history.can_redo

    @property
    def undo_depth(self) -> int:
        return self._history.undo_depth

    @property
    def gap_size(self) -> int:
        return self._document.gap_size

    def _edit(self, position: int, delete_length: int, inserted: str) -> Edit:
        edit = self._document.make_edit(position, delete_length, inserted)
        self._document.apply(edit)
        return edit

    def _perform(self, position: int, delete_length: int, inserted: str, coalesce: bool = False) -> Edit:
        edit = self._edit(position, delete_length, inserted)
        self._history.record(edit, coalesce=coalesce)
        return edit

    def move_cursor(self, position: int) -> None:
        self._history.break_run()
        self._document.move_cursor(position)

    def select(self, start: int, end: int) -> None:
        self._history.break_run()
        self._document.select(start, end)

    def clear_selection(self) -> None:
        self._document.clear_selection()

    def type(self, text: str) -> None:
        """键盘输入。有选区时先整段替换（这是一步独立的撤销），否则在光标处插入并尝试合并。"""
        span = self._document.selection
        if span is not None:
            start, end = span
            self._perform(start, end - start, text, coalesce=False)
            return
        self._perform(self._document.cursor, 0, text, coalesce=True)

    def insert(self, position: int, text: str) -> None:
        """程序化插入。**不**合并：两次刻意的调用不该被折成一次撤销。"""
        self._history.break_run()
        self._perform(position, 0, text, coalesce=False)

    def delete(self, start: int, end: int) -> str:
        """程序化删除 [start, end)，返回被删掉的文本。"""
        if start > end:
            raise InvalidRangeError(f"start {start} is after end {end}")
        self._history.break_run()
        return self._perform(start, end - start, "").removed

    def backspace(self) -> None:
        """退格：有选区就删选区，否则删光标左边一个字符。文档开头处什么也不做。"""
        span = self._document.selection
        if span is not None:
            start, end = span
            self._perform(start, end - start, "")
            return
        cursor = self._document.cursor
        if cursor == 0:
            return
        self._perform(cursor - 1, 1, "")

    def delete_forward(self) -> None:
        span = self._document.selection
        if span is not None:
            start, end = span
            self._perform(start, end - start, "")
            return
        cursor = self._document.cursor
        if cursor >= len(self._document):
            return
        self._perform(cursor, 1, "")

    def copy(self) -> str:
        self._clipboard = self._document.selected_text
        return self._clipboard

    def cut(self) -> str:
        """剪切：先复制再删除。剪贴板不属于文档，所以撤销**不会**把剪贴板还原——
        这不是疏漏，是真实编辑器的行为：撤销撤的是文档，不是系统剪贴板。"""
        span = self._document.selection
        if span is None:
            return ""
        self._clipboard = self._document.selected_text
        start, end = span
        self._perform(start, end - start, "")
        return self._clipboard

    def paste(self) -> None:
        if not self._clipboard:
            return
        span = self._document.selection
        if span is not None:
            start, end = span
            self._perform(start, end - start, self._clipboard)
            return
        self._perform(self._document.cursor, 0, self._clipboard)

    def find(self, needle: str, start: int = 0) -> int:
        return self._document.find(needle, start)

    def find_all(self, needle: str) -> tuple[int, ...]:
        """所有不重叠匹配的起点，从左到右。"""
        if not needle:
            return ()
        found: list[int] = []
        at = self._document.find(needle)
        while at != -1:
            found.append(at)
            at = self._document.find(needle, at + len(needle))
        return tuple(found)

    def replace_all(self, needle: str, replacement: str) -> int:
        """替换全部匹配项，整批算**一个**撤销单元，返回替换了几处。

        从右往左替换：这样每一处的起点都还是按原文算出来的，不需要为长度差逐个修正下标。
        注意这个方法一行都没有改动 `History` 和 `Edit`——它只是把已有的积木换个用法。
        """
        positions = self.find_all(needle)
        if not positions:
            return 0
        edits = [self._edit(at, len(needle), replacement) for at in reversed(positions)]
        self._history.record_group(edits)
        return len(positions)

    def undo(self) -> bool:
        edits = self._history.undo()
        for edit in edits:
            self._document.apply(edit)
        return bool(edits)

    def redo(self) -> bool:
        edits = self._history.redo()
        for edit in edits:
            self._document.apply(edit)
        return bool(edits)

    def __repr__(self) -> str:
        return f"Editor(len={len(self._document)}, cursor={self.cursor}, undo={self.undo_depth})"


def _demo() -> None:
    editor = Editor()
    for char in "hello":
        editor.type(char)
    print(repr(editor.text), "撤销栈深度:", editor.undo_depth)   # 五次击键 = 一个撤销单元
    editor.undo()
    print("一次撤销之后:", repr(editor.text))
    editor.redo()

    editor.type("\nthe cat sat on the mat")
    editor.replace_all("at", "og")
    print("替换之后:", repr(editor.text), "撤销栈深度:", editor.undo_depth)
    editor.undo()
    print("一次撤销全部还原:", repr(editor.text))

    editor.select(0, 5)
    print("剪切:", repr(editor.cut()), "->", repr(editor.text))


if __name__ == "__main__":
    _demo()
