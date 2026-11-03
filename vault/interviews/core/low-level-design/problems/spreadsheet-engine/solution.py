"""电子表格引擎（Spreadsheet Engine）：单元格、公式、依赖顺序重算、环检测、区间函数。

核心思路：公式在 `set` 的时候就解析成一棵 AST（语法树），所以语法错误当场抛出、单元格保持原样。
第 1 关只认 `=A1+B2+3` 这种求和，用 `split` 解析，第 2 关换成递归下降解析器，语法树和求值不用改。
每个单元格记两张边表：`_deps[c]` 是 c 读了哪些格子，`_users[c]` 是谁读了 c。改一个格子时，
只沿 `_users` 往下找出受影响的格子，按拓扑序（先被依赖的先算）各算一次；`get` 只读缓存，不再求值。
环检测放在改动之前做：新公式的依赖沿 `_deps` 能走回自己，就拒绝，表格原封不动。
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterator
from dataclasses import dataclass


class SpreadsheetError(Exception):
    """所有失败路径的公共基类。"""


class InvalidCellError(SpreadsheetError, ValueError):
    """单元格名不合法：只接受 A1 到 Z999。"""


class InvalidFormulaError(SpreadsheetError, ValueError):
    """公式或字面量写错了。"""


class CycleError(SpreadsheetError, ValueError):
    """这次赋值会让公式互相依赖成环。"""


class EvalError(SpreadsheetError, ArithmeticError):
    """求值失败（除以零）；依赖它的格子也会得到同一个错误。"""


CELL = re.compile(r"[A-Z][1-9][0-9]{0,2}")
NUMBER = re.compile(r"-?\d+(?:\.\d+)?")
TOKEN = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|([A-Z]+[0-9]*)|([-+*/():]))")
FUNCS = ("SUM", "MIN", "MAX")


def check_cell(name: object) -> str:
    if not isinstance(name, str) or not CELL.fullmatch(name):
        raise InvalidCellError(f"bad cell name: {name!r}")
    return name


# ---------------------------------------------------------------- 解析与求值（第 1 关只有求和，第 2 关起是完整表达式）
# 语法树：五种节点，各是一个不可变的小数据类，求值和找依赖都用 `match` 按类型分派。


@dataclass(frozen=True, slots=True)
class Num:
    value: float


@dataclass(frozen=True, slots=True)
class Ref:
    cell: str


@dataclass(frozen=True, slots=True)
class Neg:
    operand: "Node"


@dataclass(frozen=True, slots=True)
class Bin:
    op: str
    left: "Node"
    right: "Node"


@dataclass(frozen=True, slots=True)
class Func:  # 第 4 关：SUM / MIN / MAX 加区间
    name: str
    first: str
    last: str


Node = Num | Ref | Neg | Bin | Func


def _tokenize(src: str) -> list[str]:
    src, pos, out = src.rstrip(), 0, []
    while pos < len(src):
        m = TOKEN.match(src, pos)
        if not m:
            raise InvalidFormulaError(f"bad character at {pos}: {src!r}")
        out.append(m.group(m.lastindex))
        pos = m.end()
    return out


class _Parser:
    """递归下降：expr 管 + -，term 管 * /，unary 管负号，atom 管数字、引用、括号、函数。"""

    def __init__(self, toks: list[str]) -> None:
        self.t, self.i = toks, 0

    def peek(self) -> str | None:
        return self.t[self.i] if self.i < len(self.t) else None

    def take(self, want: str | None = None) -> str:
        tok = self.peek()
        if tok is None or (want is not None and tok != want):
            raise InvalidFormulaError(f"expected {want or 'more input'}, got {tok!r}")
        self.i += 1
        return tok

    def expr(self) -> Node:
        node = self.term()
        while self.peek() in ("+", "-"):
            op = self.take()
            node = Bin(op, node, self.term())
        return node

    def term(self) -> Node:
        node = self.unary()
        while self.peek() in ("*", "/"):
            op = self.take()
            node = Bin(op, node, self.unary())
        return node

    def unary(self) -> Node:
        if self.peek() == "-":
            self.take()
            return Neg(self.unary())
        return self.atom()

    def atom(self) -> Node:
        tok = self.take()
        if tok[0].isdigit():
            return Num(float(tok))
        if tok == "(":
            node = self.expr()
            self.take(")")
            return node
        if tok in FUNCS and self.peek() == "(":  # 第 4 关
            self.take("(")
            a, _, b = self.take(), self.take(":"), self.take()
            self.take(")")
            if not (CELL.fullmatch(a) and CELL.fullmatch(b)) or a[0] > b[0] or int(a[1:]) > int(b[1:]):
                raise InvalidFormulaError(f"bad range {a}:{b}")
            return Func(tok, a, b)
        if CELL.fullmatch(tok):
            return Ref(tok)
        raise InvalidFormulaError(f"unexpected token {tok!r}")


def parse_raw(raw: str) -> Node | None:
    """`""` 清空格子（返回 None）；`=` 开头是公式；其余必须是数字字面量。"""
    raw = raw.strip()
    if raw == "":
        return None
    if raw.startswith("="):
        p = _Parser(_tokenize(raw[1:]))
        node = p.expr()
        if p.peek() is not None:
            raise InvalidFormulaError(f"trailing input at {p.peek()!r}")
        return node
    if not NUMBER.fullmatch(raw):
        raise InvalidFormulaError(f"not a number or formula: {raw!r}")
    return Num(float(raw))


def cells_in(a: str, b: str) -> Iterator[str]:
    for col in range(ord(a[0]), ord(b[0]) + 1):
        for row in range(int(a[1:]), int(b[1:]) + 1):
            yield f"{chr(col)}{row}"


def refs_of(node: Node) -> set[str]:
    """公式直接读的所有格子；区间展开成区间里的每个格子（空格子也算，以后填上要触发重算）。"""
    match node:
        case Ref(cell):
            return {cell}
        case Neg(operand):
            return refs_of(operand)
        case Bin(_, left, right):
            return refs_of(left) | refs_of(right)
        case Func(_, first, last):
            return set(cells_in(first, last))
        case _:
            return set()


def evaluate(node: Node, read: Callable[[str], float | None]) -> float:
    """`read(cell)` 返回格子的值，空格子返回 None；读到出错的格子由 read 抛 EvalError。"""
    match node:
        case Num(value):
            return value
        case Ref(cell):
            v = read(cell)
            return 0.0 if v is None else v
        case Neg(operand):
            return -evaluate(operand, read)
        case Bin(op, left, right):
            l, r = evaluate(left, read), evaluate(right, read)
            match op:
                case "+":
                    return l + r
                case "-":
                    return l - r
                case "*":
                    return l * r
                case _:
                    if r == 0:
                        raise EvalError("#DIV/0!")
                    return l / r
        case Func(name, first, last):
            vals = [v for c in cells_in(first, last) if (v := read(c)) is not None]  # 区间忽略空格子
            match name:
                case "SUM":
                    return float(sum(vals))
                case "MIN":
                    return float(min(vals, default=0.0))
                case _:
                    return float(max(vals, default=0.0))


# ---------------------------------------------------------------- 表格本体


class Spreadsheet:
    def __init__(self) -> None:
        self._node: dict[str, Node] = {}
        self._deps: dict[str, set[str]] = {}   # 格子 -> 它读了哪些格子
        self._users: dict[str, set[str]] = {}  # 格子 -> 谁读了它（空格子也可以有 users）
        self._val: dict[str, float | EvalError] = {}
        self.eval_count = 0  # 第 3 关：公式被求值的累计次数

    def get(self, cell: str) -> float:
        check_cell(cell)
        v = self._val.get(cell, 0.0)
        if isinstance(v, EvalError):
            raise v
        return v

    def set(self, cell: str, raw: str) -> None:
        check_cell(cell)
        node = parse_raw(raw)                       # 先解析：写错了就在这里抛，表格没动过
        new_deps = refs_of(node) if node else set()
        if self._reaches(new_deps, cell):           # 第 1 关：先查环，再改任何状态
            raise CycleError(f"{cell} would depend on itself")
        for d in self._deps.pop(cell, set()):
            self._users[d].discard(cell)
        if node is None:
            self._node.pop(cell, None)
            self._val.pop(cell, None)
        else:
            self._node[cell] = node
            self._deps[cell] = new_deps
            for d in new_deps:
                self._users.setdefault(d, set()).add(cell)
        self._recalc(cell)

    def _reaches(self, starts: set[str], target: str) -> bool:
        """从 starts 沿"读了谁"的边走，能不能碰到 target；碰到说明新公式会闭成一个环。"""
        seen, stack = set(), list(starts)
        while stack:
            c = stack.pop()
            if c == target:
                return True
            if c not in seen:
                seen.add(c)
                stack.extend(self._deps.get(c, ()))
        return False

    def _recalc(self, changed: str) -> None:
        """第 3 关：只重算 changed 和它的下游，按拓扑序，每格恰好一次。"""
        order, seen = [], set()

        def visit(c: str) -> None:  # 后序遍历 users 边，反过来就是"被依赖的在前"
            seen.add(c)
            for u in self._users.get(c, ()):
                if u not in seen:
                    visit(u)
            order.append(c)

        visit(changed)
        for c in reversed(order):
            node = self._node.get(c)
            if node is None:
                continue
            if isinstance(node, Num):
                self._val[c] = node.value
                continue
            self.eval_count += 1
            try:
                self._val[c] = evaluate(node, self._read)
            except EvalError as err:
                self._val[c] = err

    def _read(self, cell: str) -> float | None:
        v = self._val.get(cell)
        if isinstance(v, EvalError):
            raise v
        return v
