---
slug: spreadsheet-engine
kind: low-level-design
---
## Q
**设计电子表格引擎（Spreadsheet Engine）**｜低层设计

设计一个电子表格的内核：格子里可以放数字，也可以放引用别的格子的公式（如 `=A1+B2+3`）；改了一个格子，依赖它的格子要自动跟着变。常见的出法是分步给的：先做 `get/set`，再加公式和自动重算，最后可能加完整表达式、区间函数。面试官看重的是：公式怎么表示、依赖关系怎么记、改一格时怎么只重算受影响的格子、环怎么拒绝，以及出错的格子怎么传播。

给出完整解答：需求、核心实现、逐步扩展、深入问题、取舍、不同级别的期望。

## A
**一句话。** 公式在 `set` 时就解析成语法树并登记"我读了谁"的依赖，语法错误和环都在动任何状态之前被拒绝；读值先用最简单的惰性现算，要求"只重算受影响的格子"时再加"谁读了我"的反向边，沿它按拓扑序把下游各算一次。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–6 分 | 问清需求：格子名范围、公式语法（只有 `+`？括号？）、空格子当 0、出错怎么表现 |
| 6–12 分 | 定接口 `set(cell, raw)` / `get(cell)` 和异常；画语法树与依赖表 |
| 12–40 分 | 写核心实现：语法树、`split` 解析、惰性 `get`、`set` 的"解析→查环→写入" |
| 40–45 分 | 跑例子：求和、改上游、先写公式后填引用、环、非法输入 |
| 45–60 分 | 追问：完整表达式、增量重算、区间函数、深链 |

**需求。**
- 功能：
  - `set(cell, raw)`：`raw` 是数字、以 `=` 开头的公式，或 `""` 清空；
  - `get(cell)`：返回数值，空格子是 `0.0`；
  - 公式可以引用还没填的格子，填上以后结果要跟着变；
  - 非法格子名、非法公式抛异常，格子保持原样；
  - 会闭成环的 `set`（含自己引用自己）被拒绝，整张表保持原样。
- 非功能：
  - 公式只解析一次，不在每次 `get` 时重新解析字符串；
  - 求值函数与"格子存在哪里"解耦，换存储策略不改解析和求值；
  - 格子名限定 `A1` 到 `Z999`（一个大写字母加 1 到 3 位行号），最多 26 × 999 = 25,974 个格子（后面谈区间的代价会用到这个数）。

**核心实体与接口。**
- `Num`、`Ref`、`Bin`：语法树节点，各是一个 `frozen=True, slots=True` 的小数据类。不可变所以可比较、可哈希，字段直接拆出来就能按类型分派。
- `parse_raw(raw)`：把字符串变成语法树；写错了当场抛 `InvalidFormulaError`。
- `refs_of(node)`：这棵树直接读了哪些格子。
- `evaluate(node, read)`：`read` 是传进来的函数，求值函数不知道格子存在哪里。
- `Spreadsheet`：`_node`（格子 → 语法树）、`_deps`（格子 → 它读了谁）；对外 `set` / `get`。
- 异常：`InvalidCellError`、`InvalidFormulaError`、`CycleError`，共同基类 `SpreadsheetError`。

**整体设计。** `set(cell, raw)` 的顺序是这个设计的骨架，所有可能失败的步骤排在任何写入之前：
1. `check_cell`：格子名合法；
2. `parse_raw`：解析成语法树，语法错在这里抛，表格没动过；
3. `refs_of` 得到新依赖，`_reaches` 从新依赖出发沿 `_deps` 走，能走回这个格子就抛 `CycleError`，表格仍然没动过；
4. 只有前三步全过，才写 `_node` 和 `_deps`。

`get(cell)` 读 `_node`，没有就是空格子；有就用 `evaluate` 递归求值，遇到引用再调回 `_read`。

**核心实现。** 约 30 分钟，下面是全部要写的代码（公式只有 `+`，用 `split` 解析）：

```python
import re
from collections.abc import Callable
from dataclasses import dataclass
from functools import reduce


class SpreadsheetError(Exception): ...
class InvalidCellError(SpreadsheetError, ValueError): ...
class InvalidFormulaError(SpreadsheetError, ValueError): ...
class CycleError(SpreadsheetError, ValueError): ...


CELL = re.compile(r"[A-Z][1-9][0-9]{0,2}")        # A1..Z999，行号不以 0 开头
NUMBER = re.compile(r"\d+(?:\.\d+)?")


def check_cell(name: object) -> str:
    if not isinstance(name, str) or not CELL.fullmatch(name):
        raise InvalidCellError(f"bad cell name: {name!r}")
    return name


# 语法树：每种节点一个不可变小类，求值和找依赖都按类型 match
@dataclass(frozen=True, slots=True)
class Num:
    value: float

@dataclass(frozen=True, slots=True)
class Ref:
    cell: str

@dataclass(frozen=True, slots=True)
class Bin:
    op: str
    left: "Node"
    right: "Node"

Node = Num | Ref | Bin


def parse_raw(raw: str) -> Node | None:
    """空串清空格子；"=A1+B2+3" 是公式；其余必须是数字。set 时就解析，错误当场抛。"""
    raw = raw.strip()
    if raw == "":
        return None
    if not raw.startswith("="):
        if not re.fullmatch(r"-?\d+(?:\.\d+)?", raw):
            raise InvalidFormulaError(f"not a number or formula: {raw!r}")
        return Num(float(raw))
    terms = [t.strip() for t in raw[1:].split("+")]
    nodes = [Ref(t) if CELL.fullmatch(t) else Num(float(t)) if NUMBER.fullmatch(t) else None for t in terms]
    if None in nodes:
        raise InvalidFormulaError(f"bad term in {raw!r}")
    return reduce(lambda a, b: Bin("+", a, b), nodes)   # 左结合折成一棵树


def refs_of(node: Node) -> set[str]:
    match node:
        case Ref(cell):
            return {cell}
        case Bin(_, left, right):
            return refs_of(left) | refs_of(right)
        case _:
            return set()


def evaluate(node: Node, read: Callable[[str], float | None]) -> float:
    """怎么读格子由 read 决定：求值函数不知道格子存在哪里。"""
    match node:
        case Num(value):
            return value
        case Ref(cell):
            v = read(cell)
            return 0.0 if v is None else v
        case Bin(_, left, right):
            return evaluate(left, read) + evaluate(right, read)


class Spreadsheet:
    def __init__(self) -> None:
        self._node: dict[str, Node] = {}
        self._deps: dict[str, set[str]] = {}   # 格子 -> 它读了哪些格子

    def get(self, cell: str) -> float:
        check_cell(cell)
        v = self._read(cell)
        return 0.0 if v is None else v

    def _read(self, cell: str) -> float | None:  # 惰性：读到才现算
        node = self._node.get(cell)
        return None if node is None else evaluate(node, self._read)

    def set(self, cell: str, raw: str) -> None:
        check_cell(cell)
        node = parse_raw(raw)                         # 1. 先解析：写错了表格没动过
        deps = refs_of(node) if node else set()
        if self._reaches(deps, cell):                 # 2. 再查环：仍然没动过
            raise CycleError(f"{cell} would depend on itself")
        if node is None:                              # 3. 最后才写
            self._node.pop(cell, None)
            self._deps.pop(cell, None)
        else:
            self._node[cell], self._deps[cell] = node, deps

    def _reaches(self, starts: set[str], target: str) -> bool:
        """从 starts 沿"读了谁"走，碰到 target 就说明新公式会闭成环。"""
        seen, stack = set(), list(starts)
        while stack:
            c = stack.pop()
            if c == target:
                return True
            if c not in seen:
                seen.add(c)
                stack.extend(self._deps.get(c, ()))
        return False
```

**运行。**
- `A1=2`、`B1=3`、`C1==A1+B1+3`：`get("C1")` 得到 `8.0`；`set("A1","1")` 之后得到 `7.0`。
- `D1==E1+1` 先于 `E1` 写下：`get("D1")` 得到 `1.0`（空格子当 0）。
- **环依赖抛 CycleError：** `set("E1","=D1")` 抛 `CycleError`，`set("A1","=A1")` 也抛；之后 `A1`、`D1` 仍是 `1.0`、`1.0`，表格没被改坏。
- **非法公式与非法单元格：** `set("F1","=A1+")` 抛 `InvalidFormulaError`；`get("a1")` 抛 `InvalidCellError`。

**逐步扩展。**
1. 【追问再讲】完整表达式：`+ - * /`、括号、一元负号。触发：面试官问"不只有加号呢"。把 `split` 换成分词加递归下降，每个优先级一层函数，优先级越高调用链越深，先把操作数收走；语法树只多一个 `Neg`，`set` 和环检测一行不动。除以零不在 `set` 时报，而在 `get` 时抛 `EvalError`（因为分母可能随上游变化）。

```python
import operator


class EvalError(SpreadsheetError, ArithmeticError): ...      # 除以零：get 时才抛，不是 set 时


@dataclass(frozen=True, slots=True)
class Neg:
    operand: "Node"

Node = Num | Ref | Neg | Bin
TOKEN = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|([A-Z]+[0-9]*)|([-+*/()]))")


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
    """递归下降：优先级越高的函数调用链越深，先把操作数收走。"""
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

    def expr(self) -> Node:                       # + -，同级左结合
        node = self.term()
        while self.peek() in ("+", "-"):
            op = self.take()
            node = Bin(op, node, self.term())
        return node

    def term(self) -> Node:                       # * /
        node = self.unary()
        while self.peek() in ("*", "/"):
            op = self.take()
            node = Bin(op, node, self.unary())
        return node

    def unary(self) -> Node:                      # 一元负号
        if self.peek() == "-":
            self.take()
            return Neg(self.unary())
        return self.atom()

    def atom(self) -> Node:                       # 数字、引用、括号
        tok = self.take()
        if tok[0].isdigit():
            return Num(float(tok))
        if tok == "(":
            node = self.expr()
            self.take(")")
            return node
        if CELL.fullmatch(tok):
            return Ref(tok)
        raise InvalidFormulaError(f"unexpected token {tok!r}")


def parse_raw(raw: str) -> Node | None:           # 只换公式分支，split 版本整个丢掉
    raw = raw.strip()
    if raw == "":
        return None
    if not raw.startswith("="):
        if not re.fullmatch(r"-?\d+(?:\.\d+)?", raw):
            raise InvalidFormulaError(f"not a number or formula: {raw!r}")
        return Num(float(raw))
    p = _Parser(_tokenize(raw[1:]))
    node = p.expr()
    if p.peek() is not None:
        raise InvalidFormulaError(f"trailing input at {p.peek()!r}")
    return node


def refs_of(node: Node) -> set[str]:
    match node:
        case Ref(cell):
            return {cell}
        case Neg(operand):
            return refs_of(operand)
        case Bin(_, left, right):
            return refs_of(left) | refs_of(right)
        case _:
            return set()


OPS = {"+": operator.add, "-": operator.sub, "*": operator.mul}


def evaluate(node: Node, read: Callable[[str], float | None]) -> float:
    match node:
        case Num(value):
            return value
        case Ref(cell):
            v = read(cell)
            return 0.0 if v is None else v
        case Neg(operand):
            return -evaluate(operand, read)
        case Bin("/", left, right):
            l, r = evaluate(left, read), evaluate(right, read)
            if r == 0:
                raise EvalError("#DIV/0!")
            return l / r
        case Bin(op, left, right):
            return OPS[op](evaluate(left, read), evaluate(right, read))
```

2. 【追问再讲】只重算受影响的格子：触发"改一个格子，不要把整张表算一遍"。加反向边 `_users`（谁读了我）、值缓存 `_val`、计数器 `eval_count`。改一格时沿 `_users` 做后序遍历，反过来就是"被依赖的在前"的拓扑序，每格恰好算一次，所以菱形的 `D1` 不会算两遍，也不会先用到还没更新的 `C1`。出错状态把 `EvalError` 本身存进缓存、读到再抛，重算不会停在半路。

```python
class Spreadsheet:  # 只列出新增或替换的方法
    def __init__(self) -> None:
        self._node: dict[str, Node] = {}
        self._deps: dict[str, set[str]] = {}
        self._users: dict[str, set[str]] = {}            # 新：谁读了我（空格子也可以有 users）
        self._val: dict[str, float | EvalError] = {}     # 新：缓存；错误本身也是一种值
        self.eval_count = 0                              # 公式被求值的累计次数

    def get(self, cell: str) -> float:                   # 只读缓存，不求值
        check_cell(cell)
        v = self._val.get(cell, 0.0)
        if isinstance(v, EvalError):
            raise v
        return v

    def _read(self, cell: str) -> float | None:          # 求值时读上游的缓存；上游出错就把错误传下去
        v = self._val.get(cell)
        if isinstance(v, EvalError):
            raise v
        return v

    def set(self, cell: str, raw: str) -> None:
        check_cell(cell)
        node = parse_raw(raw)
        new_deps = refs_of(node) if node else set()
        if self._reaches(new_deps, cell):
            raise CycleError(f"{cell} would depend on itself")
        for d in self._deps.pop(cell, set()):            # 改线：先从旧依赖的 users 里把自己摘掉
            self._users[d].discard(cell)
        if node is None:
            self._node.pop(cell, None)
            self._val.pop(cell, None)
        else:
            self._node[cell], self._deps[cell] = node, new_deps
            for d in new_deps:
                self._users.setdefault(d, set()).add(cell)
        self._recalc(cell)

    def _recalc(self, changed: str) -> None:
        """只重算 changed 和它的下游，按拓扑序，每格恰好一次。"""
        order, seen = [], set()

        def visit(c: str) -> None:                       # 沿 users 的后序遍历，反过来就是"被依赖的在前"
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
                self._val[c] = err                       # 错误即值：重算不中断，下游照样拿到一致的结果
```

3. **【加分】区间函数 SUM/MIN/MAX：** 区间函数 `SUM / MIN / MAX(A1:B3)`：触发"加个求和函数"。区间展开成它覆盖的每个格子登记依赖（空格子也登记，以后填上要触发重算），环检测和重算机制不用改。`cells_in` 是生成器，依赖和求值共用。区间忽略空格子，`MIN` 不把空格子当 0。

```python
from collections.abc import Iterator

FUNCS = ("SUM", "MIN", "MAX")


@dataclass(frozen=True, slots=True)
class Func:
    name: str
    first: str
    last: str

Node = Num | Ref | Neg | Bin | Func


def cells_in(a: str, b: str) -> Iterator[str]:       # 生成器：按需产出区间里的格子，依赖和求值共用
    for col in range(ord(a[0]), ord(b[0]) + 1):
        for row in range(int(a[1:]), int(b[1:]) + 1):
            yield f"{chr(col)}{row}"


class _Parser:  # 只列出新增或替换的方法
    def atom(self) -> Node:
        tok = self.take()
        if tok[0].isdigit():
            return Num(float(tok))
        if tok == "(":
            node = self.expr()
            self.take(")")
            return node
        if tok in FUNCS and self.peek() == "(":      # 新：SUM(A1:B3)
            self.take("(")
            a, _, b = self.take(), self.take(":"), self.take()
            self.take(")")
            if not (CELL.fullmatch(a) and CELL.fullmatch(b)) or a[0] > b[0] or int(a[1:]) > int(b[1:]):
                raise InvalidFormulaError(f"bad range {a}:{b}")
            return Func(tok, a, b)
        if CELL.fullmatch(tok):
            return Ref(tok)
        raise InvalidFormulaError(f"unexpected token {tok!r}")


TOKEN = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|([A-Z]+[0-9]*)|([-+*/():]))")   # 多认一个冒号


def refs_of(node: Node) -> set[str]:
    match node:
        case Ref(cell):
            return {cell}
        case Neg(operand):
            return refs_of(operand)
        case Bin(_, left, right):
            return refs_of(left) | refs_of(right)
        case Func(_, first, last):
            return set(cells_in(first, last))        # 区间里每个格子都是依赖，空格子也算
        case _:
            return set()


def evaluate(node: Node, read: Callable[[str], float | None]) -> float:
    match node:
        case Num(value):
            return value
        case Ref(cell):
            v = read(cell)
            return 0.0 if v is None else v
        case Neg(operand):
            return -evaluate(operand, read)
        case Bin("/", left, right):
            l, r = evaluate(left, read), evaluate(right, read)
            if r == 0:
                raise EvalError("#DIV/0!")
            return l / r
        case Bin(op, left, right):
            return OPS[op](evaluate(left, read), evaluate(right, read))
        case Func(name, first, last):
            vals = [v for c in cells_in(first, last) if (v := read(c)) is not None]   # 区间忽略空格子
            fn = {"SUM": sum, "MIN": min, "MAX": max}[name]
            return float(fn(vals)) if vals else 0.0
```

4. 【加分】深链不爆栈：触发"一条一万格的引用链"。逐步扩展 2 的后序遍历是递归的，Python 默认递归深度约 1000，链条一长就 `RecursionError`；换成手写栈的迭代版，其余不变。

```python
class Spreadsheet:  # 只列出新增或替换的方法
    def _recalc(self, changed: str) -> None:
        order, seen = [], {changed}
        stack = [(changed, iter(self._users.get(changed, ())))]   # 手写的栈代替函数调用栈
        while stack:
            c, users = stack[-1]
            for u in users:
                if u not in seen:
                    seen.add(u)
                    stack.append((u, iter(self._users.get(u, ()))))
                    break
            else:                                    # 所有下游都处理完才轮到自己：后序
                order.append(c)
                stack.pop()
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
```

**深入。**
1. 【必讲】公式存成语法树，`set` 时解析，校验在先、提交在后：
   - 存字符串、每次 `get` 重新解析，既慢又把语法错误推迟到读的时候；存语法树，错误在 `set` 当场报，并且格子保持原样；
   - 语法树节点用 `@dataclass(frozen=True, slots=True)`，求值和找依赖都用 `match` 加类模式（`case Bin(op, left, right)`）：每种节点一个分支，字段直接拆出来，漏掉一种节点在代码里一眼可见。用 `("bin", "+", l, r)` 这样的元组加字符串标签要靠下标取值，改字段顺序就悄悄出错（代数数据类型加模式匹配）；
   - `set` 里"解析→查环→写入"的顺序，是"所有可能失败的步骤排在任何写入之前"。边写边检查的版本，失败时要手工回滚两张边表和缓存，漏一处就留下脏状态。
2. 【必讲】依赖图与环检测：
   - `_deps[c]` 是 `c` 读了谁，从新公式的依赖出发沿它走，能回到被写的格子就是环；菱形、同一个格子被引用两次都不是环：只看能不能走回被写的格子，`seen` 集合避免同一个格子被重复展开；
   - 改线时（把 `C1` 的公式换成别的）旧依赖必须同步摘掉，否则残留旧边会造成误判环。核心里 `_deps[cell]` 整个被覆盖，天然没有残留；加了 `_users` 之后要手工从旧依赖的 `_users` 里摘掉自己；
   - 空格子也能有下游：先写公式、后填引用必须能工作。
3. 【必讲】惰性现算与增量重算的取舍：
   - 惰性（核心）：`get` 时递归求值，状态只有语法树和依赖，最不容易出错。代价是同一个格子在菱形里会被反复求值：`A2==A1+A1`、`A3==A2+A2`……一路写到 `A20`，`get("A20")` 一共调用了 2,097,149 次 `evaluate`（每多一层翻一倍，约 2^21），约 0.2 秒；再长就指数爆炸；
   - 增量（逐步扩展 2）：改一格时沿反向边把下游按拓扑序各算一次，`get` 只读缓存。代价是多两张表要同步，换来读是 O(1)、重算是 O(波及面)；
   - 口头说清"为什么菱形不会算两次"（后序遍历反转，每格只入表一次）就够了。
4. 【追问再讲】求值与"怎么读格子"解耦：`evaluate(node, read)` 把读格子的方式作为函数参数传入。核心里 `read` 递归求值，逐步扩展 2 里 `read` 读缓存，语法树、解析、求值函数一行不改。如果在求值里直接访问 `self._val`，惰性和缓存就得写两套（依赖注入，传函数）。
5. 【追问再讲】出错状态是值：重算时某格除以零，把 `EvalError` 实例本身存进缓存，下游读到就重新抛。放弃"算到一半抛出去"：那样重算停在中途，其余下游留着旧值，表格不一致。把上游改好之后，整条链自然恢复。
6. 【追问再讲】递归下降如何表达优先级：`expr` 管 `+ -`，调 `term` 管 `* /`，调 `unary` 管负号，调 `atom` 管数字、引用、括号。`a + b * c` 里 `b * c` 在更深的一层被先收走；同级用 `while` 循环做左结合，所以 `8 - 3 - 2` 是 `(8 - 3) - 2`。
7. 【加分】深链与栈深：递归后序遍历在一条链上改源头（一个数字格，后面 5,000 个格子依次是 `=前一格+1`），实测直接 `RecursionError`；迭代版（手写栈加 `iter()`）同样的链改一次，`eval_count` 增加 5,000，末格 `get` 得到 `5001.0`。
8. 【加分】区间的代价：一个 `SUM(A1:Z999)` 展开成 25,974 条依赖边，每次改任何一格都要在 `_users` 里翻。大表要把区间当作单独的依赖节点，按块或区间树维护；口述这一点即可。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 想让表格线程安全：`set` 是"读表、改表、重算"的整体，用一把全局写锁；`get` 只读缓存，可以用读写锁。
- 想撤销：`set` 先记下旧的 `raw`，撤销就是再 `set` 一次，边表会自动同步。
- 想显示 `#CYCLE!` 而不是拒绝赋值：环里每格存一个 `EvalError`，不再抛 `CycleError`，但重算的拓扑序要对环单独处理。
- 想跨表引用、命名区域：格子名变成 `(sheet, cell)` 二元组，`refs_of` 和边表的键随之变化。
- 一次改动波及十万个格子：重算本身是 O(波及面)；迭代遍历避免爆栈，必要时标记"脏"后台重算。
- **运算符是数据不是类：** 为什么 `Bin` 用 `op` 字符串而不是每个运算符一个类：运算符只是数据，分支靠 `OPS` 查表，新增运算符不用新增类。

**级别期望。**
- 中级：核心实现通过，`get/set` 正确，公式只含 `+`，惰性递归求值，能检测自引用。
- 高级：解析与求值分开，`set` 先解析、再查环、最后写入；完整表达式的递归下降；说清菱形为什么会重复求值，以及增量重算的拓扑序。
- 资深/专家：出错状态传播与恢复，反向边在改线和清空时的同步，区间函数的依赖代价，深链的迭代遍历，并发与撤销。

**先修概念。**
- [[hi-low-level-design-in-a-hurry-patterns|设计模式]]
- [[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]
- [[hi-low-level-design-in-a-hurry-design-principles|设计原则]]
- [[hi-system-design-core-concepts-data-modeling|数据建模]]

**同类题。**
- [[solution-amz-dag-runner|设计题解：DAG 任务执行器]]
- [[solution-amz-in-memory-db|设计题解：内存数据库]]
- [[solution-amz-file-watcher|设计题解：文件监听器]]
