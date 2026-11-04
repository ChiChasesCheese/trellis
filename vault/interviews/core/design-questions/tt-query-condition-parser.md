---
slug: tt-query-condition-parser
kind: low-level-design
---
## Q
**条件解析与内存表查询（SQL 风格）**｜低层设计

给一个条件字符串，比如 `age >= 18 AND (city = 'NYC' OR city = 'SF')`，在内存里模拟一张表，返回满足条件的行。用 Python 实现，先支持比较、`AND`、`OR` 和括号，`AND` 优先于 `OR`。

面试官可能继续追问 `NOT`、`NULL`、索引，或者字段不固定的文档（NoSQL）。

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** 把任务拆成三步：词法（字符串 → token）、语法（token → 语法树）、求值（语法树在每一行上算真假）。难点只有一个，就是 `AND` 比 `OR` 优先，靠递归下降的函数调用层次解决。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–8 分 | 问清输入格式和运算符，定接口 |
| 8–15 分 | 写 `tokenize` |
| 15–30 分 | 写节点和 `Parser`：比较 → `AND` / `OR` → 括号 |
| 30–40 分 | 写 `Table`，跑例子，修 bug |
| 40–55 分 | 追问：`NOT` / `IN`、`NULL` |
| 55–60 分 | 口述索引和 NoSQL |

**需求。**
- 先问：只有条件还是完整 `SELECT`；值有哪些类型；有没有 `NULL`；字段固定吗；语法错误怎么处理。
- 第一版约定：只有条件；整数和字符串；没有 `NULL`；字段固定；语法错误抛 `ValueError`。
- 不用 `eval`：查询字符串不可信，等于让对方执行任意代码。

**核心实体与接口。**
- `tokenize(text)`：字符串变 token 列表。
- `Parser(text).parse()`：返回语法树。
- 节点 `Cmp / And / Or`：都有 `matches(row)`，这是解释器模式（Interpreter Pattern），加运算符只加一个类。
- `Table`：`insert(row)`、`select(where, columns)`。

**整体设计。**

`a = 1 OR b = 2 AND c = 3` 解析出来是这棵树，`AND` 绑得更紧，所以在更深的位置：

```text
Or
├─ Cmp(a = 1)
└─ And
   ├─ Cmp(b = 2)
   └─ Cmp(c = 3)
```

文法，每行对应 `Parser` 的一个函数，优先级低的在上面：

```text
or_expr  := and_expr (OR and_expr)*
and_expr := primary (AND primary)*
primary  := '(' or_expr ')'
          | field op value
```

**核心实现。**
1. 词法（约 7 分钟）：引号里的内容整体算一个 token，所以字符串里的 `AND` 不会被误认，这是不能用 `split` 的原因。

```python
import operator
import re
from dataclasses import dataclass
from typing import Any

Row = dict[str, Any]
OPS = {"=": operator.eq, "!=": operator.ne, "<": operator.lt,
       "<=": operator.le, ">": operator.gt, ">=": operator.ge}
# 长的运算符写在前面，否则 <= 会被切成 < 和 =；引号里的内容整体算一个 token
TOKEN = re.compile(r"\s*(<=|>=|!=|=|<|>|\(|\)|,|'[^']*'|-?\d+|\w+)")


def tokenize(text: str) -> list[str]:
    tokens, pos = [], 0
    text = text.strip()
    while pos < len(text):
        m = TOKEN.match(text, pos)
        if not m:
            raise ValueError(f"无法识别: {text[pos:]!r}")
        tokens.append(m.group(1))
        pos = m.end()
    return tokens


def literal(token: str) -> Any:
    return token[1:-1] if token.startswith("'") else int(token)
```

2. 语法树（约 5 分钟）：每种节点只管自己怎么求值。

```python
@dataclass
class Cmp:
    field: str
    op: str
    value: Any

    def matches(self, row: Row) -> bool:
        return OPS[self.op](row[self.field], self.value)


@dataclass
class And:
    left: Any
    right: Any

    def matches(self, row: Row) -> bool:
        return self.left.matches(row) and self.right.matches(row)


@dataclass
class Or:
    left: Any
    right: Any

    def matches(self, row: Row) -> bool:
        return self.left.matches(row) or self.right.matches(row)
```

3. 语法（约 10 分钟）：优先级靠调用层次表达。先写 `primary` 的比较部分，再加 `AND`、`OR`，最后加括号。

```python
class Parser:
    def __init__(self, text: str) -> None:
        self.tokens = tokenize(text)
        self.i = 0

    def peek(self) -> str:
        return self.tokens[self.i] if self.i < len(self.tokens) else ""

    def next(self) -> str:
        if self.i == len(self.tokens):
            raise ValueError("条件意外结束")
        self.i += 1
        return self.tokens[self.i - 1]

    def parse(self) -> Any:
        node = self.or_expr()
        if self.peek():
            raise ValueError(f"多余的内容: {self.peek()}")
        return node

    def or_expr(self) -> Any:  # 优先级最低，最先调用，最后结合
        node = self.and_expr()
        while self.peek().upper() == "OR":
            self.next()
            node = Or(node, self.and_expr())
        return node

    def and_expr(self) -> Any:
        node = self.primary()
        while self.peek().upper() == "AND":
            self.next()
            node = And(node, self.primary())
        return node

    def primary(self) -> Any:
        if self.peek() == "(":
            self.next()
            node = self.or_expr()  # 括号让优先级重新从最低开始
            if self.next() != ")":
                raise ValueError("缺少右括号")
            return node
        field, op, value = self.next(), self.next(), self.next()
        if op not in OPS:
            raise ValueError(f"不支持的运算符: {op}")
        return Cmp(field, op, literal(value))
```

4. 表（约 5 分钟）：解析和存储分开，查询就是全表扫描加过滤。

```python
class Table:
    def __init__(self, columns: list[str]) -> None:
        self.columns = columns
        self.rows: list[Row] = []

    def insert(self, row: Row) -> None:
        if set(row) != set(self.columns):
            raise ValueError(f"字段不匹配: {sorted(row)}")
        self.rows.append(row)

    def select(self, where: str = "", columns: list[str] | None = None) -> list[Row]:
        cond = Parser(where).parse() if where else None
        hits = [r for r in self.rows if cond is None or cond.matches(r)]
        return [{c: r[c] for c in columns or self.columns} for r in hits]  # 返回副本
```

**运行。**

```python
t = Table(["id", "name", "age", "city"])
t.insert({"id": 1, "name": "Ann", "age": 30, "city": "NYC"})
t.insert({"id": 2, "name": "Bob", "age": 17, "city": "SF"})
t.insert({"id": 3, "name": "Cat", "age": 25, "city": "NYC"})
t.insert({"id": 4, "name": "Dan", "age": 45, "city": "LA"})
```

- **例：两条件 AND：** `age >= 18 AND city = 'NYC'` → Ann、Cat。
- **例：AND 先于 OR 结合：** `city = 'SF' OR age > 40 AND city = 'LA'` → Bob、Dan（`AND` 先结合）。
- **例：括号改变结合：** `(city = 'SF' OR age > 40) AND city = 'LA'` → Dan（括号改变结合）。
- `a > 1 OR`、`(a > 1`、`a ~ 1` → `ValueError`。

**复杂度。**
- 解析 `O(L)`，`L` 是条件长度。
- 查询 `O(n · k)`，`n` 是行数，`k` 是语法树节点数。

**逐步扩展。**
1. 【追问再讲】`NOT` 和 `IN`：加一层 `not_expr`，放在 `and_expr` 和 `primary` 之间；`and_expr` 改调 `not_expr`，`primary` 的比较部分改调 `predicate`。

```python
@dataclass
class Not:
    inner: Any

    def matches(self, row: Row) -> bool:
        return not self.inner.matches(row)


@dataclass
class In:
    field: str
    values: list[Any]

    def matches(self, row: Row) -> bool:
        return row[self.field] in self.values


def not_expr(self) -> Any:  # 新增一层，放在 and_expr 和 primary 之间
    if self.peek().upper() == "NOT":
        self.next()
        return Not(self.not_expr())
    return self.primary()


def predicate(self) -> Any:  # 从 primary 里拆出比较部分，再加 IN
    field, op = self.next(), self.next()
    if op.upper() == "IN":
        if self.next() != "(":
            raise ValueError("IN 后面需要括号")
        values = [literal(self.next())]
        while self.peek() == ",":
            self.next()
            values.append(literal(self.next()))
        if self.next() != ")":
            raise ValueError("缺少右括号")
        return In(field, values)
    if op not in OPS:
        raise ValueError(f"不支持的运算符: {op}")
    return Cmp(field, op, literal(self.next()))
```

2. 【追问再讲】`NULL`：和 `NULL` 比较的结果是「未知」，`matches` 返回 `None`；`NOT 未知` 还是未知；`select` 只保留 `is True` 的行。不这样做的话，`NOT age >= 18` 会多返回 `age` 为 `NULL` 的行。

```python
# Cmp：缺值返回 None
def matches(self, row: Row) -> bool | None:
    left = row[self.field]
    return None if left is None else OPS[self.op](left, self.value)


# And：有 False 就是 False，否则有未知就是未知（Or 反过来，看 True）
def matches(self, row: Row) -> bool | None:
    a, b = self.left.matches(row), self.right.matches(row)
    if a is False or b is False:
        return False
    return None if a is None or b is None else True


# Not：未知保持未知
def matches(self, row: Row) -> bool | None:
    v = self.inner.matches(row)
    return None if v is None else not v
```

3. 【加分】等值索引：候选集必须是结果的超集，最后一定复查。`AND` 用一边的索引就够；`OR` 用一边的索引会漏行，只能全表扫描。

```python
def candidates(self, node: Any) -> list[Row] | None:
    if isinstance(node, Cmp) and node.op == "=" and node.field in self.index:
        return self.index[node.field].get(node.value, [])
    if isinstance(node, And):  # 复查会过滤另一边
        left = self.candidates(node.left)
        return left if left is not None else self.candidates(node.right)
    return None  # None 表示只能全表扫描
```

4. 【加分】文档（NoSQL）：解析和求值不变，只换取字段的方式，再去掉字段校验。缺字段当 `NULL`，所以要先做第 2 档。

```python
def get_path(row: Row, path: str) -> Any:  # address.city
    value: Any = row
    for part in path.split("."):
        value = value.get(part) if isinstance(value, dict) else None
    return value
```

**深入。**
1. 【必讲】为什么调用层次就是优先级：`or_expr` 调 `and_expr`，所以 `AND` 先把操作数收走；括号回到 `or_expr`，优先级重新开始。
2. 【必讲】为什么解析和存储要分开：语法树只认 `matches(row)`，换存储不用改解析，加运算符不用改表。
3. 【追问再讲】为什么选递归下降：文法和代码一一对应，最容易讲清楚。`split` 处理不了括号和字符串里的 `AND`；调度场算法（Shunting-yard）不用递归，但 `IN` 这类多段语法很别扭。
4. 【加分】范围查询走索引：用 `bisect` 维护有序列表，查询 `O(log n + 结果数)`，插入 `O(n)`；真实数据库用 B+ 树。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 完整 `SELECT`：`Parser` 前面加解析列名和表名，后面加 `ORDER BY`、`LIMIT`。
- 排序遇到 `NULL`：`None < 3` 会报错，排序键用元组 `(v is not None, v)`。
- `LIKE`：`%` 转 `.*`，`_` 转 `.`，其他字符 `re.escape`，用 `re.fullmatch`。
- 频繁查询：缓存「条件字符串 → 语法树」。
- 并发：读多写少用读写锁，行和索引在同一把锁内更新。
- `JOIN`、`GROUP BY`：执行层改成算子链，60 分钟内不会要求写。

**级别期望。**
- 中级：词法和语法分开，优先级和括号正确，能跑通例子。
- 高级：再加 `NOT`、`NULL`，错误处理清楚，能讲清楚索引为什么 `OR` 用不了。
- 资深：解释取舍，主动控制范围，说清楚什么现在不做、以后怎么演进。

**先修概念。** [[hi-low-level-design-in-a-hurry-patterns|设计模式]]、[[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]、[[hi-system-design-core-concepts-data-modeling|数据建模]]

**同类题。** [[basic-calculator|LC 224 基本计算器]]、[[tt-basic-calculator-ladder|计算器梯度题]]、[[tt-ai-assisted-order-validator|OrderValidator（规则 DAG）]]、[[kv-store-eviction|可配置淘汰策略的内存键值存储]]

**完整版。** 想看 `LIKE`、`BETWEEN`、`SELECT` 全语法和索引维护的完整实现（300 多行，面试不用写）：[[tt-query-condition-parser-full|完整版笔记]]
