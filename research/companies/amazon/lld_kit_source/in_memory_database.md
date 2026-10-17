# LLD：内存数据库（CRUD + 用 Python 模拟 `SELECT … FROM … JOIN … WHERE … ORDER BY`）——教科书模式

> **来源**：Chi 亲历（2026-10-16 当面告知：过去被问过这题，当时写不出来）+ LeetCode 近亲 **LC 2408 Design SQL**。原话："design an in-memory database——CRUD，并且用 Python 模拟 `SELECT … FROM … JOIN … WHERE … ORDER BY`"。
> 这是**第一手**材料（不是论坛转述），所以优先级高于 `route.md` 里按论坛频次排的题；它不在 `catalog/raw/forums.md` 的 110 条里（`推断`：属于 "File search / filter API" 的近亲——都是"查询对象 + 组合条件"）。
> 代码：`code/in_memory_database.py`（完整参考，`python3 -I code/in_memory_database.py` 打印 `OK in_memory_database`）；`code/in_memory_database_45min.py`（面试里真正写的紧凑版，打印 `OK in_memory_database_45min`）。
> 本文所有标记为 `python` 的代码块都是从上述两个文件**逐字摘出**的（由脚本按函数 / 类名截取，不是手抄）；`sql` / `text` 块是示例与文法。
> 官方评分口径（`../catalog/raw/official.md` §4.3）："organize your methods and classes to ensure a clear separation of concerns … Your test names should describe business and technical requirements"。本题的"关注点分离"就是：**存储 / 谓词 / 排序 / 连接 / 解析**五块各自独立。

## 目录
0. 这道题在问什么
1. 从零讲起：表、行、主键、索引、NULL，以及 SQL 的**逻辑执行顺序**（含逐行手算）
2. Part 1：LC 2408 Design SQL（题面、解法、复杂度、follow-up）
3. Part 2：类型化的表与 CRUD
4. Part 3：谓词（三值逻辑）与 ORDER BY
5. Part 4：JOIN（嵌套循环 → 哈希连接 → LEFT JOIN → 限定列名）
6. Part 5：迷你 SQL 前端（tokenizer + 递归下降）
7. Part 6（senior）：索引与规划器、GROUP BY 聚合、事务、线程安全
8. 45 分钟怎么写（面试答卷的顺序与口述稿）
9. 追问预演 · 常见 bug · 自测题 · 延伸阅读

---

## 0. 这道题在问什么

面试官的原话很短，但里面其实压着三层要求：

| 层 | 面试官想看到 | 对应本文 |
|---|---|---|
| ① 数据模型 | 表 = 列定义 + 主键 + 一堆行；类型、主键唯一、自增 | Part 2 |
| ② 查询语义 | `WHERE` / `ORDER BY` / `JOIN` 不是"拼几个 for 循环"，而是**有明确语义**：NULL 怎么比、排序稳不稳、没匹配的行怎么办 | Part 3、4 |
| ③ 工程判断 | 哪些先做、哪些口头带过；扩展点在哪（加一种比较符改几处）；复杂度；并发 | 45 分钟一节、Part 6 |

Chi 说"忘了怎么写"——这类题最容易卡在**不知道从哪下手**：既想做 SQL 解析器，又想做索引，结果 45 分钟里连 `select` 都没跑通。
本文的解法是把整题拆成**可以独立交付的 6 层**，每一层写完就是一个能跑的东西；面试里按顺序交付，时间到了就停在某一层，仍然是"完整的东西"。

**和 LC 2408 的关系**：LC 2408 是"没有类型、没有 WHERE / JOIN、只能按 rowId 取"的最小版（Part 1）。它的骨架——**表 = 以自增 id 为键的字典、删除不回退计数器**——正是 Part 2 的起点。面试官问你"内存数据库"时，Part 1 能当热身，也能让你证明"我知道最小版怎么写，然后往上扩"。

---

## 1. 从零讲起

### 1.1 表（table）、行（row）、列（column）
- **是什么**：表是一张二维表格。每一**列**有名字和类型（`id: int`, `name: str`）；每一**行**是一条记录。
- **为什么需要类型**：没有类型，`age = "30"` 和 `age = 30` 会混进同一列，之后 `ORDER BY age` 就会在比较 `"30" < 5` 时崩溃，或者得到"字典序"这种错误结果。类型检查应当发生在**写入时**（早失败），而不是读取时。
- **Python 怎么表示**：一行 = `dict[str, Any]`（`{"id": 1, "name": "ann"}`）。一张表 = `{主键: 行字典}`。

### 1.2 主键（primary key）
- **是什么**：每行唯一的标识列。不能重复，不能为 NULL。
- **为什么**：没有主键，`UPDATE` / `DELETE` 就只能"按内容找"，两行内容相同时无法区分；有了主键，按主键取行是 O(1)（字典查找），并且 JOIN 的"外键 → 主键"关系有了锚点。
- **自增（auto-increment）**：插入时省略 int 主键，数据库自动分配 `1, 2, 3…`。**删除不会让计数器回退**——否则刚删掉的 id 被重新分配，指向旧 id 的外键会错误地指向新行（LC 2408 题面把这条写进了规则里）。

### 1.3 NULL
- **是什么**：NULL 不是 0 也不是空串，而是"**未知 / 不存在**"。Python 里用 `None`。
- **后果**：`NULL = NULL` 的结果不是 True，而是"未知"（UNKNOWN）。所以 SQL 是**三值逻辑**：True / False / UNKNOWN。`WHERE` 只保留结果**恰好是 True** 的行，UNKNOWN 和 False 都被丢掉。
- 这就是为什么 `WHERE age <> 30` **不会**选出 age 为 NULL 的行，以及为什么要有专门的 `IS NULL`。Part 3 详细展开。

### 1.4 索引（index）
- **是什么**：一份"额外维护的、按某列组织的查找结构"。书后面的索引页：想找"哈希"这个词，不用从第 1 页翻到最后一页，直接查索引页得到页码。
- **为什么**：没有索引，`WHERE city = 'sf'` 必须扫描每一行（O(n)）。有索引，直接定位到匹配的行。
- **代价**：每次写入都要同时更新索引（写变慢、占内存）。所以不是"越多越好"。
- **两种常见结构**：哈希索引（`dict`：值 → 行集合，只回答 `=`）；有序索引（B 树 / 我们用 `bisect` 维护的有序列表，能回答 `=` 和范围 `<`、`BETWEEN`、以及 `ORDER BY`）。Part 6。

### 1.5 SQL 的**逻辑执行顺序** vs 书写顺序（本题最重要的一张表）

你**写**的顺序是 `SELECT … FROM … JOIN … WHERE … GROUP BY … ORDER BY … LIMIT`；数据库**逻辑上执行**的顺序是：

| 步 | 子句 | 输入 → 输出 | 为什么在这个位置 |
|---|---|---|---|
| 1 | `FROM` | 表名 → 该表的所有行 | 先要有数据 |
| 2 | `JOIN … ON` | 两个行集 → 配对后的行集 | 之后的子句都看得见两张表的列 |
| 3 | `WHERE` | 行集 → 过滤后的行集 | 在**分组和投影之前**丢掉不需要的行，后面的工作量更小 |
| 4 | `GROUP BY` + 聚合 | 行集 → 每组一行 | 聚合发生在过滤之后（所以 `WHERE` 里不能用 `COUNT(*)`，那是 `HAVING` 的活） |
| 5 | `SELECT` | 行 → 选出列（计算表达式、起别名） | 到这一步才产生"别名"，所以 `WHERE` 里**不能**用 `SELECT` 里起的别名 |
| 6 | `ORDER BY` | 排序 | 在投影之后，所以**可以**用别名 |
| 7 | `LIMIT` | 取前 n 行 | 必须在排序之后，否则"前 n 行"没有意义 |

**我们的 `select()` 的代码就是按这个顺序写的**（见 Part 4 的 `Database.select`）。一个实现上的小优化：我们在投影**之前**排序（这样 `ORDER BY` 能用没被选出来的列），效果与标准一致，因为没有支持别名。

### 1.6 一个手算例子：逐行追踪

数据（`users` 有 4 行，`orders` 有 5 行；`dan` 的 `age` 是 NULL；订单 13 的 `user_id=9` 找不到用户；`cat` 没有订单）：

```
users                                  orders
 id | name | age  | city                 id | user_id | amount
  1 | ann  | 30   | sf                   10 |   1     |  50
  2 | bob  | 25   | nyc                  11 |   1     |  20
  3 | cat  | 35   | sf                   12 |   2     |  70
  4 | dan  | NULL | nyc                  13 |   9     |   5     ← 没有 id=9 的用户
                                          14 |   4     |  40
```

查询：

```sql
SELECT u.name, o.amount
FROM users u JOIN orders o ON u.id = o.user_id
WHERE o.amount >= 20 AND u.age IS NOT NULL
ORDER BY o.amount DESC
LIMIT 2
```

**逐步追踪**（`code/in_memory_database.py` 的 `test_worked_example` 对每一步都有 assert）：

1. `FROM users u`：4 行 → ann, bob, cat, dan。
2. `JOIN orders o ON u.id = o.user_id`：对每个用户找 `user_id` 相同的订单：
   - ann(1) → 订单 10、11；bob(2) → 订单 12；cat(3) → 没有，**inner join 丢掉 cat**；dan(4) → 订单 14；订单 13 的 `user_id=9` 没有用户，也丢掉。
   - 中间结果 4 行：`(ann,30,10,50) (ann,30,11,20) (bob,25,12,70) (dan,NULL,14,40)`。
3. `WHERE o.amount >= 20 AND u.age IS NOT NULL`：
   - `(ann,…,50)`：50≥20 True，age 非空 True → 留；`(ann,…,20)`：20≥20 True → 留；`(bob,…,70)` → 留；
   - `(dan,NULL,…,40)`：`40≥20` 为 True，但 `age IS NOT NULL` 为 False → 丢。
   - 剩 3 行。
4. `ORDER BY o.amount DESC`：70, 50, 20 → `bob/70, ann/50, ann/20`。
5. `LIMIT 2`：`bob/70, ann/50`。
6. `SELECT u.name, o.amount`：投影成 `[{"u.name":"bob","o.amount":70}, {"u.name":"ann","o.amount":50}]`。

如果把第 2 步换成 `LEFT JOIN`：cat 会以 `(cat,35,NULL,NULL)` 保留；第 3 步 `o.amount >= 20` 对 NULL 是 UNKNOWN → cat 被 WHERE 丢掉——这就是"LEFT JOIN + 右表非 NULL 条件 = 悄悄变成 INNER JOIN"的经典坑（Part 4 有测试）。

---

## 2. Part 1：LC 2408 Design SQL

### 2.1 题面（逐字摘自 LeetCode，2026-10-16 通过 r.jina.ai 镜像抓取：https://leetcode.com/problems/design-sql/ ；`WebFetch` 直连只给了改写摘要，所以改用镜像取原文）

> You are given two string arrays, `names` and `columns`, both of size `n`. The `ith` table is represented by the name `names[i]` and contains `columns[i]` number of columns.
>
> You need to implement a class that supports the following **operations**:
> - **Insert** a row in a specific table with an id assigned using an _auto-increment_ method, where the id of the first inserted row is 1, and the id of each _new_ row inserted into the same table is **one greater** than the id of the **last inserted** row, even if the last row was _removed_.
> - **Remove** a row from a specific table. Removing a row **does not** affect the id of the next inserted row.
> - **Select** a specific cell from any table and return its value.
> - **Export** all rows from any table in csv format.
>
> Implement the `SQL` class:
> - `SQL(String[] names, int[] columns)` — Creates the `n` tables.
> - `bool ins(String name, String[] row)` — Inserts `row` into the table `name` and returns `true`. If `row.length` **does not** match the expected number of columns, or `name` is **not** a valid table, returns `false` without any insertion.
> - `void rmv(String name, int rowId)` — Removes the row `rowId` from the table `name`. If `name` is **not** a valid table or there is no row with id `rowId`, no removal is performed.
> - `String sel(String name, int rowId, int columnId)` — Returns the value of the cell at the specified `rowId` and `columnId` in the table `name`. If `name` is **not** a valid table, or the cell `(rowId, columnId)` is **invalid**, returns `"<null>"`.
> - `String[] exp(String name)` — Returns the rows present in the table `name`. If name is **not** a valid table, returns an empty array. Each row is represented as a string, with each cell value (**including** the row's id) separated by a `","`.
>
> **Constraints:** `n == names.length == columns.length`; `1 <= n <= 10^4`; `1 <= names[i].length, row[i].length, name.length <= 10`; `names[i]`, `row[i]`, `name` consist only of lowercase English letters; `1 <= columns[i] <= 10`; `1 <= row.length <= 10`; all `names[i]` are distinct; at most `2000` calls to `ins` and `rmv`; at most `10^4` calls to `sel`; at most `500` calls to `exp`.
>
> **Follow-up:** Which approach would you choose if the table might become sparse due to many deletions, and why? Consider the impact on memory usage and performance.

**API 版本说明**：当前 LeetCode 页面（2026-10-16 抓取）的方法名是 **`ins` / `rmv` / `sel` / `exp`**，不是 `insertRow` / `deleteRow` / `selectCell` / `exportTable`。`推断`：网上较旧的题解 / 博客里可能还看到长名字的写法，那是题面改版之前的名字（我没有核对旧版页面）；以当前页面为准。

**Example 1**（题面）：`SQL(["one","two","three"],[2,3,1])` → `ins("two",["first","second","third"])` 返回 true → `sel("two",1,3)` 返回 `"third"` → `ins("two",["fourth","fifth","sixth"])` 返回 true → `exp("two")` 返回 `["1,first,second,third","2,fourth,fifth,sixth"]` → `rmv("two",1)` → `sel("two",2,2)` 返回 `"fifth"`（行 2 的 id 没变）→ `exp("two")` 返回 `["2,fourth,fifth,sixth"]`。
**Example 2** 的要点：删除后 `sel("two",1,2)` 返回 `"<null>"`；列数不对的 `ins` 返回 false，**并且不消耗 id**，之后合法的 `ins` 拿到 id 2。

### 2.2 先想最笨的写法
每张表一个 `list[list[str]]`，行的 id = 下标 + 1，删除时 `rows[id-1] = None`（墓碑）。
- `sel` O(1) 没问题；但 `exp` 要遍历所有槽位（包括墓碑），O(曾经插入的总行数)；如果插入了 2000 行又删掉 1999 行，`exp` 仍要扫 2000 个槽位，内存也不释放。——这正是题目 follow-up 问的"稀疏"。

### 2.3 参考解（字典）

```python
class SQL:
    """LC 2408。表 = {rowId: 行}；dict 保持插入顺序，而 id 单调递增，所以 exp 的顺序天然是 id 升序。

    删除不会让 next_id 回退（题面："even if the last row was removed"）。
    """

    def __init__(self, names: list[str], columns: list[int]):
        self._width = dict(zip(names, columns))
        self._rows: dict[str, dict[int, list[str]]] = {n: {} for n in names}
        self._next_id = dict.fromkeys(names, 1)

    def ins(self, name: str, row: list[str]) -> bool:
        if name not in self._rows or len(row) != self._width[name]:
            return False
        row_id = self._next_id[name]
        self._next_id[name] = row_id + 1
        self._rows[name][row_id] = list(row)
        return True

    def rmv(self, name: str, rowId: int) -> None:  # noqa: N803 - 名字与 LeetCode 签名一致
        table = self._rows.get(name)
        if table is not None:
            table.pop(rowId, None)

    def sel(self, name: str, rowId: int, columnId: int) -> str:  # noqa: N803
        row = self._rows.get(name, {}).get(rowId)
        if row is None or not 1 <= columnId <= len(row):
            return "<null>"
        return row[columnId - 1]

    def exp(self, name: str) -> list[str]:
        return [",".join([str(row_id), *row]) for row_id, row in self._rows.get(name, {}).items()]
```

**为什么用 `dict`**：
- 键是 rowId，值是行；`sel` / `rmv` 都是 O(1)；`exp` 遍历 `dict.items()`，只访问**存活的行**，O(存活行数 × 列数)，不受已删除行数影响。
- Python 3.7+ 的 `dict` 保持**插入顺序**，而 rowId 严格递增，所以 `exp` 天然按 id 升序，不需要排序。
- `_next_id` 单独存一个计数器，删除不动它——题面"even if the last row was removed"。
- 失败的 `ins`（列数不对或表不存在）在**修改任何状态之前**就返回，所以不消耗 id（Example 2 最后一行）。

**复杂度**（n 表数，w 列数 ≤ 10，k 表中存活行数）：构造 O(n)；`ins` O(w)；`rmv` O(1)；`sel` O(1)；`exp` O(k·w)。空间 O(存活单元格数 + n)。

**Follow-up（稀疏）怎么答**：
- 若用"下标 = id"的数组 + 墓碑：`sel` 最快（连哈希都省了），但内存与 `exp` 都是 O(曾经插入的行数)，稀疏时浪费。
- `dict`：内存只和存活行成正比（`dict` 自身有 ~1.5× 的哈希表开销），`exp` 与存活行成正比。是默认答案。
- 若还要**按 id 范围**导出，或者想要比 `dict` 更紧凑的内存：保持一个**有序的 id 列表** + 对应行列表，`bisect` 定位（`sel` 变成 O(log k)），删除用 `del`（O(k) 搬移）；或者"墓碑 + 当墓碑占比超过一半时压缩（compaction）"，均摊 O(1)。
- 说出**取舍**：这题 `sel` 调用上限是 `exp` 的 20 倍，所以 `sel` 要 O(1)，选 `dict`。

---

## 3. Part 2：类型化的表与 CRUD

### 3.1 要求
`create_table(name, columns, primary_key)`、`insert`、`update(table, set, where)`、`delete(table, where)`、`select(table, columns, where, order_by, limit)`；自增 id；错误：未知表 / 未知列 / 主键重复 / 类型不匹配。

### 3.2 错误怎么表示
一个基类 `DBError`，每种错误一个子类（`NoSuchTable`、`NoSuchColumn`、`DuplicateKey`、`TypeMismatch`、`NotNullViolation`……）。
**为什么是异常而不是返回 False**：LC 2408 返回布尔值，因为它是"评测接口"；真实 API 要告诉调用者**哪里错了**。调用方 `except DBError` 能接住全部，也能 `except DuplicateKey` 精确处理。

```python
class DBError(Exception):
    """所有数据库错误的基类。调用方 `except DBError` 能接住全部。"""


class NoSuchTable(DBError): pass
class NoSuchColumn(DBError): pass
class AmbiguousColumn(DBError): pass
class DuplicateKey(DBError): pass
class TypeMismatch(DBError): pass
class NotNullViolation(DBError): pass
class TransactionError(DBError): pass
class SQLSyntaxError(DBError): pass
```

### 3.3 列与类型检查

```python
@dataclass(frozen=True)
class Column:
    name: str
    type: type = str
    nullable: bool = True


def coerce(column: Column, value: Any) -> Any:
    """存入前的类型检查。精确比较 `type(v) is t`：这样 True 不会混进 int 列（bool 是 int 的子类）。
    唯一的隐式转换：int 可以存进 float 列。"""
    if value is None:
        if not column.nullable:
            raise NotNullViolation(f"column {column.name!r} is NOT NULL")
        return None
    if column.type is float and type(value) is int:
        return float(value)
    if type(value) is not column.type:
        raise TypeMismatch(f"column {column.name!r} expects {column.type.__name__}, got {value!r}")
    return value
```

**要点**：
- 用 `type(value) is column.type` 而不是 `isinstance`：`True` 是 `int` 的子类，`isinstance(True, int)` 为 True，会让布尔值混进 int 列。
- 唯一的隐式转换：int → float 列（`3` 存成 `3.0`）。
- NOT NULL：主键列自动是 NOT NULL（`Table.__init__` 里强制）。

### 3.4 Table：两个原语

所有对数据的改动，最终都只经过 `_add(pk, row, seq)` 和 `_drop(pk)` 两个原语：

```python
def _add_raw(self, pk: Any, row: Row, seq: int) -> None:
    self.rows[pk] = row
    self.seq[pk] = seq
    for ix in self.indexes.values():
        ix.add(row[ix.column], pk)

def _drop_raw(self, pk: Any) -> Row:
    row = self.rows.pop(pk)
    del self.seq[pk]
    for ix in self.indexes.values():
        ix.remove(row[ix.column], pk)
    return row

def _add(self, pk: Any, row: Row, seq: int) -> None:
    self._add_raw(pk, row, seq)
    self._journal.append(lambda: self._drop_raw(pk))

def _drop(self, pk: Any) -> None:
    seq = self.seq[pk]
    row = self._drop_raw(pk)
    self._journal.append(lambda: self._add_raw(pk, row, seq))
```

**为什么**：索引维护（`_add_raw` / `_drop_raw` 里循环所有索引）和 undo log（`_add` / `_drop` 往 journal 里记逆操作）都只需要挂在这两个点上。`update` 就是"drop 旧行 + add 新行"。这是 Part 6 能"免费"得到索引和事务的原因。`seq` 是行的插入序号：没有 `ORDER BY` 时结果总是按插入顺序，**与是否走索引无关**。

### 3.5 insert

```python
def insert(self, values: Mapping[str, Any]) -> Any:
    for name in values:
        if name not in self.col:
            raise NoSuchColumn(name)
    row: Row = {}
    for c in self.columns:
        v = values.get(c.name)
        if v is None and c.name == self.pk and c.type is int:
            v = self._next_auto  # 主键省略 → 自增
        row[c.name] = coerce(c, v)
    pk = row[self.pk]
    if pk in self.rows:
        raise DuplicateKey(f"duplicate primary key {pk!r} in {self.name!r}")
    old_counters = (self._next_auto, self._next_seq)
    self._add(pk, row, self._next_seq)
    self._next_seq += 1
    if self.col[self.pk].type is int:
        self._next_auto = max(self._next_auto, pk + 1)  # 显式给的大主键也要推进计数器；删除不会让它回退
    self._journal.append(lambda: self._set_counters(*old_counters))
    return pk
```

逐行解释：
1. 先检查传入的列名都存在（未知列 → `NoSuchColumn`）。
2. 对每一列：缺省值是 `None`；如果是 int 主键且没给 → 用 `_next_auto`（自增）；然后 `coerce`（类型 / NOT NULL 检查）。
3. 主键已存在 → `DuplicateKey`。**所有校验都在改动之前完成**，所以失败不会留下半截状态。
4. 计数器 `_next_auto = max(_next_auto, pk + 1)`：显式给了大主键（`id=10`）后，下一个自增是 11；**删除不会让它回退**。
5. 最后一行把"恢复计数器"的逆操作写进 journal，这样事务回滚时 id 也不会被"消耗"（测试里 `test_transactions` 验证）。

### 3.6 update 与 delete

```python
def update(self, set_: Mapping[str, Any], pred: Pred | None) -> int:
    """set_ 的值可以是常量，也可以是 callable(旧行) → 新值（例如 lambda r: r["age"] + 1）。
    先算出全部新行并校验（类型、NOT NULL、主键冲突），全部通过才动手，所以失败不会留下半截。"""
    for name in set_:
        if name not in self.col:
            raise NoSuchColumn(name)
    targets = self.matching(pred)
    new_rows = []
    for row in targets:
        new = dict(row)
        for name, v in set_.items():
            new[name] = coerce(self.col[name], v(row) if callable(v) else v)
        new_rows.append(new)
    if self.pk in set_:
        old_keys = {r[self.pk] for r in targets}
        new_keys = [r[self.pk] for r in new_rows]
        if len(set(new_keys)) != len(new_keys) or any(k in self.rows and k not in old_keys for k in new_keys):
            raise DuplicateKey(f"update would duplicate primary key in {self.name!r}")
    seqs = [self.seq[r[self.pk]] for r in targets]
    for r in targets:  # 先全删再全加：主键互换（1→2, 2→1）也正确；沿用旧 seq 保持位置
        self._drop(r[self.pk])
    for new, seq in zip(new_rows, seqs):
        self._add(new[self.pk], new, seq)
    return len(targets)


def delete(self, pred: Pred | None) -> int:
    targets = self.matching(pred)
    for r in targets:
        self._drop(r[self.pk])
    return len(targets)
```

**update 的设计决定**（面试官常追问）：
- **先算出所有新行并校验，再动手**：类型错误、NOT NULL 违例、主键冲突都发生在第一次修改之前，所以语句要么全成功要么没有任何效果。
- **主键冲突的检查**：多行被改成同一个主键（`len(set(new_keys)) != len(new_keys)`），或者新主键撞上**不在被更新集合里**的现有行。
- **先全删再全加**：这样把主键 1↔2 互换（`SET id = 3 - id`）也是合法的——如果逐行"改一行检查一行"，互换的中间状态会有重复主键。
- **`set_` 的值可以是 callable**：`{"age": lambda r: r["age"] + 1}` 就是 `SET age = age + 1`。我们的 SQL 文本前端只支持常量（保持简单），但 Python API 有这个口子。
- 参数叫 `set_` 是因为 `set` 会遮蔽内置名。

### 3.7 Database 门面

```python
def create_table(self, name: str, columns: Sequence[Column | tuple], primary_key: str) -> None:
    if name in self.tables:
        raise TableExists(name)
    cols = [c if isinstance(c, Column) else Column(*c) for c in columns]
    with self._statement():
        self.tables[name] = Table(name, cols, primary_key, self._journal)
        self._journal.append(lambda: self.tables.pop(name))


def insert(self, table: str, values: Mapping[str, Any]) -> Any:
    t = self._table(table)
    with self._statement():
        return t.insert(values)


def update(self, table: str, set_: Mapping[str, Any], where: Pred | Mapping | None = None) -> int:
    t = self._table(table)
    scope = Scope(qualified=False)
    scope.add(table, t)
    pred = as_pred(where)
    bound = pred.bind(scope) if pred else None
    for name in set_:  # `u.age` 形式也接受
        scope.lookup(name)
    with self._statement():
        return t.update({scope.lookup(k)[0]: v for k, v in set_.items()}, bound)


def delete(self, table: str, where: Pred | Mapping | None = None) -> int:
    t = self._table(table)
    scope = Scope(qualified=False)
    scope.add(table, t)
    pred = as_pred(where)
    bound = pred.bind(scope) if pred else None
    with self._statement():
        return t.delete(bound)
```

门面做两件事：①把用户写的名字（可能是 `u.age`）**绑定**成行字典里的 key，并在执行前就报告未知列（空表也会报，因为列校验不依赖数据）；②用 `_statement()` 包住（Part 6 §7.3 讲）保证语句原子。

---

## 4. Part 3：谓词与 ORDER BY

### 4.1 谓词是小对象

`WHERE` 条件被表示成一棵小的对象树：叶子是比较（`Eq`、`Lt`…、`In`、`IsNull`），内部节点是 `And` / `Or` / `Not`。每个对象只有一个方法 `eval(row) -> True | False | None`。
**为什么用对象而不是 lambda**：①可以**检查**它（规划器要看出"这是 `col = 常量`"才能用索引）；②可以**绑定**列名并在执行前做类型检查；③可以打印（`repr`）用于 `explain`；④新增一种比较符 = 新增一个类，其它代码不动（Open/Closed）。

```python
class Pred:
    """谓词基类。eval 返回 True / False / None（UNKNOWN）；WHERE 只保留 `is True` 的行。"""

    def eval(self, row: Mapping[str, Any]) -> bool | None:
        raise NotImplementedError

    def bind(self, scope: Scope) -> Pred:
        raise NotImplementedError

    def conjuncts(self) -> list[Pred]:
        return [self]

    def __and__(self, other: Pred) -> Pred:
        return And(self, other)

    def __or__(self, other: Pred) -> Pred:
        return Or(self, other)

    def __invert__(self) -> Pred:
        return Not(self)


class Compare(Pred):
    """col <op> (字面量 | 另一列)。第一个参数永远是列；第二个参数是字面量，除非它是 Col(...)。"""

    sym = "?"
    fn: Callable[[Any, Any], bool]

    def __init__(self, left: str | Col, right: Any):
        self.left = left if isinstance(left, Col) else Col(left)
        self.right = right

    def eval(self, row):
        a = self.left.get(row)
        b = self.right.get(row) if isinstance(self.right, Col) else self.right
        if a is None or b is None:
            return None  # 任何和 NULL 的比较都是 UNKNOWN，包括 NULL = NULL
        return self.fn(a, b)

    def bind(self, scope):
        left = self.left.bind(scope)
        if isinstance(self.right, Col):
            right = self.right.bind(scope)
            if not _types_ok(left.ctype, right.ctype):
                raise TypeMismatch(f"cannot compare {left} with {right}")
        else:
            right = self.right
            if not _literal_ok(left.ctype, right):
                raise TypeMismatch(f"cannot compare {left} ({left.ctype.__name__}) with {right!r}")
        return type(self)(left, right)

    def __repr__(self):
        return f"{self.left} {self.sym} {self.right!r}"
```

六个比较符只需要一行一个（`operator` 模块里现成的函数）：

```python
class Eq(Compare): sym, fn = "=", staticmethod(operator.eq)
class Ne(Compare): sym, fn = "<>", staticmethod(operator.ne)
class Lt(Compare): sym, fn = "<", staticmethod(operator.lt)
class Le(Compare): sym, fn = "<=", staticmethod(operator.le)
class Gt(Compare): sym, fn = ">", staticmethod(operator.gt)
class Ge(Compare): sym, fn = ">=", staticmethod(operator.ge)
```

加一个新比较符（比如 `Like`）：新类 + 它的 `fn`，`And` / `Or` / 规划器 / 解析器（一张映射表）全不用改——这就是面试官"追加需求只改一行"的评分点。

### 4.2 NULL 与三值逻辑（必须说出口的规则）

**规则**：任何比较，只要有一边是 NULL，结果都是 UNKNOWN（`None`）——包括 `NULL = NULL` 和 `NULL <> 1`。`WHERE` 只保留结果 `is True` 的行。

三值真值表（`test_predicates` 对 3×3 全部组合做了 assert）：

| `AND` | T | F | U |  | `OR` | T | F | U |  | `NOT` |  |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **T** | T | F | U |  | **T** | T | T | T |  | T | F |
| **F** | F | F | F |  | **F** | T | F | U |  | F | T |
| **U** | U | F | U |  | **U** | T | U | U |  | U | U |

记忆法：`AND` 取"最悲观"（False 压过 UNKNOWN 压过 True），`OR` 取"最乐观"，`NOT UNKNOWN` 还是 UNKNOWN。

```python
class And(Pred):
    """任一为 False → False；否则任一为 UNKNOWN → UNKNOWN；否则 True。"""

    def __init__(self, *parts: Pred):
        self.parts = parts

    def eval(self, row):
        result: bool | None = True
        for p in self.parts:
            v = p.eval(row)
            if v is False:
                return False
            if v is None:
                result = None
        return result

    def bind(self, scope):
        return And(*(p.bind(scope) for p in self.parts))

    def conjuncts(self):
        return [c for p in self.parts for c in p.conjuncts()]

    def __repr__(self):
        return "(" + " AND ".join(map(repr, self.parts)) + ")"


class Or(Pred):
    """任一为 True → True；否则任一为 UNKNOWN → UNKNOWN；否则 False。"""

    def __init__(self, *parts: Pred):
        self.parts = parts

    def eval(self, row):
        result: bool | None = False
        for p in self.parts:
            v = p.eval(row)
            if v is True:
                return True
            if v is None:
                result = None
        return result

    def bind(self, scope):
        return Or(*(p.bind(scope) for p in self.parts))

    def __repr__(self):
        return "(" + " OR ".join(map(repr, self.parts)) + ")"


class Not(Pred):
    """NOT UNKNOWN 仍然是 UNKNOWN，所以 `NOT (x = 1)` 不会选中 x 为 NULL 的行。"""

    def __init__(self, part: Pred):
        self.part = part

    def eval(self, row):
        v = self.part.eval(row)
        return None if v is None else not v

    def bind(self, scope):
        return Not(self.part.bind(scope))

    def __repr__(self):
        return f"NOT {self.part!r}"
```

**几条值得背的后果**（都在测试里）：
- `age <> 30` 不选 `age IS NULL` 的行；`NOT (age = 30)` 也不选（NOT UNKNOWN = UNKNOWN）。想要"不是 30 或者未知"必须写 `age <> 30 OR age IS NULL`。
- `age = NULL` 永远选不出任何行；要用 `IS NULL`（`IsNull` 是唯一能"看见" NULL 的谓词，永远返回 True/False）。
- **`NOT IN` 含 NULL 的陷阱**：`x NOT IN (1, NULL)` 一行都选不出。因为 `x IN (1, NULL)` 在 x 不等于 1 时是 UNKNOWN（"可能等于那个 NULL"），NOT 之后仍是 UNKNOWN。

```python
class In(Pred):
    """col IN (v1, v2, …)。三值：命中 → True；没命中但列表里有 NULL → UNKNOWN；否则 False。"""

    def __init__(self, left: str | Col, values: Iterable[Any]):
        self.left = left if isinstance(left, Col) else Col(left)
        self.values = list(values)

    def eval(self, row):
        a = self.left.get(row)
        if a is None:
            return None
        saw_null = False
        for v in self.values:
            if v is None:
                saw_null = True
            elif a == v:
                return True
        return None if saw_null else False

    def bind(self, scope):
        left = self.left.bind(scope)
        for v in self.values:
            if not _literal_ok(left.ctype, v):
                raise TypeMismatch(f"cannot compare {left} with {v!r}")
        return In(left, self.values)

    def __repr__(self):
        return f"{self.left} IN {self.values!r}"


class IsNull(Pred):
    """col IS NULL。这是唯一能"看见" NULL 的谓词：永远返回 True / False，不会 UNKNOWN。"""

    def __init__(self, left: str | Col):
        self.left = left if isinstance(left, Col) else Col(left)

    def eval(self, row):
        return self.left.get(row) is None

    def bind(self, scope):
        return IsNull(self.left.bind(scope))

    def __repr__(self):
        return f"{self.left} IS NULL"
```

### 4.3 `where` 的三种写法与类型检查

```python
def as_pred(where: Pred | Mapping[str, Any] | None) -> Pred | None:
    """where 可以是 None、Pred，或 {列: 值} 字典（等值条件的 AND；值为 None 表示 IS NULL）。"""
    if where is None or isinstance(where, Pred):
        return where
    return And(*(IsNull(k) if v is None else Eq(k, v) for k, v in where.items()))
```

`where` 可以是 `None`、谓词对象，或 `{列: 值}`（等值的 AND；值为 `None` 就是 `IS NULL`）。谓词在执行前先 `bind(scope)`：把列名解析成行字典里的 key（未知列 → `NoSuchColumn`，重名 → `AmbiguousColumn`），并检查**字面量类型和列类型可比**（`Eq("age", "x")` → `TypeMismatch`）——空表也会报，因为这是静态检查。

### 4.4 ORDER BY：多键、混合方向、稳定、NULL 的位置

**需求**：`ORDER BY dept ASC, salary DESC`——先按 dept 升序，dept 相同的再按 salary 降序，仍相同的保持原有顺序（稳定）。

**最笨的做法**：写一个 `cmp(a, b)`，逐键比较，再 `functools.cmp_to_key`。可行，但写起来容易错，且慢。

**更简单的做法：多遍稳定排序**。Python 的 `list.sort` 是**稳定**的（官方文档 Sorting HOW TO："Sorts are guaranteed to be stable"，并且 "The reverse parameter still maintains sort stability"）。所以：**从最后一个键开始，往前每个键各排一遍**，每遍用自己的方向（`reverse=desc`）。后排的主键不会打乱先排的次键内部顺序。

```python
def _null_first(value: Any) -> tuple[bool, Any]:
    """排序键：NULL 比任何值都小（SQLite 的规则）。元组比较先比第一个分量，
    两个 None 比较时 None == None 成立，不会触发 None < None 的 TypeError。"""
    return (value is not None, value)


def sort_rows(rows: list[Row], keys: Sequence[tuple[str, bool]]) -> list[Row]:
    """多键、混合方向、稳定。keys = [(行字典 key, 是否 DESC), …]，第一个是最主要的键。
    做法：从最后一个键往前，各排一遍。list.sort 是稳定的，reverse=True 也保持稳定，
    所以后排的主键不会打乱先排的次键。"""
    for key, desc in reversed(keys):
        rows.sort(key=lambda r, k=key: _null_first(r[k]), reverse=desc)
    return rows
```

**NULL 的位置规则**（要说出口）：本实现和 SQLite 一致——**NULL 比任何值都小**，所以 `ASC` 时 NULL 在最前，`DESC` 时 NULL 在最后（SQLite 文档 lang_select："SQLite considers NULL values to be smaller than any other values for sorting purposes. Hence, NULLs naturally appear at the beginning of an ASC order-by and at the end of a DESC order-by"，2026-10-16 核对：https://www.sqlite.org/lang_select.html ）。PostgreSQL 的默认相反（NULL 最大）；标准 SQL 提供 `NULLS FIRST / NULLS LAST`。要支持它们，只需把排序键里 `value is not None` 这一位按需取反（追问 Q8）。

`_null_first` 的小技巧：键是 `(value is not None, value)`。元组比较先比第一个分量，NULL（False）排在所有非 NULL（True）前面；两个 NULL 比较时 `None == None` 成立，元组比较不会继续比较 `None < None`（那会 `TypeError`）。

**稳定性的测试**：`test_order_by` 里 id 1 和 id 6 的 `(dept, sal)` 完全相同，断言 1 排在 6 前；并且用一个独立的 Python 参考实现，对四种键组合（含混合方向）对拍。

### 4.5 LIMIT
排序之后再切片。`LIMIT 0` 返回空；负数或非 int → `DBError`。优化追问：`ORDER BY … LIMIT k` 不需要全排序，用堆（`heapq.nsmallest`）O(n log k)；但混合方向 / 多键时要把键包装一下，不如多遍排序直观——面试里先写排序版，口头说明堆的优化。

---

## 5. Part 4：JOIN

### 5.1 先把"限定列名"和"名字冲突"解决

两张表都有 `id` 列，`JOIN` 之后一行里有两个 `id`——一个 Python `dict` 装不下。解决办法：**连接后的行字典 key 用 `别名.列名`**（`u.id`、`o.id`）。用户写不带限定的 `name` 时，由 `Scope` 解析：恰好一张表有这个列 → 唯一匹配，用它；多张表都有 → `AmbiguousColumn`（标准 SQL 也是报错）；没有 → `NoSuchColumn`。

```python
class Scope:
    """把用户写的名字（'age' 或 'u.age'）解析成行字典里的 key，并报告重名 / 不存在。

    单表查询：行字典沿用存储的 {列名: 值}，key 是裸列名（零拷贝）。
    有 JOIN：行字典的 key 是 'alias.列名'（保证不同表同名列不会互相覆盖）。
    """

    def __init__(self, qualified: bool):
        self.qualified = qualified
        self.tables: list[tuple[str, Table]] = []

    def add(self, alias: str, table: Table) -> None:
        if any(a == alias for a, _ in self.tables):
            raise DBError(f"duplicate table alias {alias!r} (self-join needs an alias)")
        self.tables.append((alias, table))

    def key(self, alias: str, col: str) -> str:
        return f"{alias}.{col}" if self.qualified else col

    def lookup(self, name: str) -> tuple[str, Column]:
        if "." in name:
            alias, col = name.split(".", 1)
            for a, t in self.tables:
                if a == alias:
                    if col not in t.col:
                        raise NoSuchColumn(name)
                    return self.key(a, col), t.col[col]
            raise NoSuchColumn(name)
        hits = [(a, t.col[name]) for a, t in self.tables if name in t.col]
        if not hits:
            raise NoSuchColumn(name)
        if len(hits) > 1:
            raise AmbiguousColumn(f"column {name!r} is ambiguous: {[a for a, _ in hits]}")
        return self.key(hits[0][0], name), hits[0][1]

    def star(self) -> list[str]:
        return [self.key(a, c.name) for a, t in self.tables for c in t.columns]
```

要点：
- **单表查询**不用限定（key 是裸列名，直接用存储的行字典，零拷贝）；**有 JOIN** 才用限定 key。这是一个"热路径不付代价"的取舍。
- 起了别名（`FROM users u`）之后就必须用别名（`users.id` 报错）——和标准 SQL 一致。
- **自连接**（员工 → 经理）必须起别名，否则别名冲突，`Scope.add` 报错（测试里有）。

### 5.2 嵌套循环连接（nested-loop join）：最直接的写法

**想法**：对左表的每一行，扫描右表所有行，凡是满足 `ON` 条件的就配成一行输出。

```python
@staticmethod
def _nested_loop_join(left_rows, right_rows, on: Pred, kind: str, nulls: Row) -> list[Row]:
    """O(|L|·|R|)。任意 ON 条件都能用。"""
    out = []
    for lrow in left_rows:
        matched = False
        for rrow in right_rows:
            merged = {**lrow, **rrow}
            if on.eval(merged) is True:
                matched = True
                out.append(merged)
        if not matched and kind == "left":
            out.append({**lrow, **nulls})
    return out
```

复杂度 O(|L|·|R|)（n 行 × m 行 = n·m 次条件判断）。任何 `ON` 条件都能用（`u.age < o.amount` 这种非等值条件也行）。**LEFT JOIN**：内层循环结束后如果这一行一次都没匹配（`matched` 为 False），仍然输出这一行，右表的所有列补 `None`（`nulls`）。

### 5.3 哈希连接（hash join）：推导为什么能更快

**观察**：大多数 `ON` 是**等值**条件 `u.id = o.user_id`。嵌套循环里内层循环绝大多数判断都是 False——我们为这些必然失败的比较白白付了代价。

**推导**：
1. 对左表的某一行，我们想要的是"右表里 `user_id` 恰好等于 `u.id` 的那些行"。这是一个**按键查找**问题。
2. 按键查找最快的结构是哈希表：如果提前把右表按 `user_id` 分桶（`dict[user_id → [行…]]`），那么对每个左行，直接 `buckets[u.id]` 取出候选，O(1)。
3. 建桶（**build**）扫右表一遍：O(|R|)。探测（**probe**）扫左表一遍，每行 O(1) 取候选，加上输出的行数：O(|L| + 输出)。
4. 总计 O(|L| + |R| + 输出)，对比 O(|L|·|R|)。600×600 的表实测快约 65 倍（`test_perf`，一次实测，数字随机器浮动）。

```python
@staticmethod
def _hash_join(left_rows, right_rows, equi, kind: str, nulls: Row) -> list[Row]:
    """build：把右表按连接键放进 dict（O(|R|)）；probe：左表每行 O(1) 取候选（O(|L| + 输出)）。
    NULL 键永远不匹配（NULL = NULL 是 UNKNOWN），所以不进桶、也不去探测。"""
    lkey, rkey, residual = equi
    buckets: dict[Any, list[Row]] = defaultdict(list)
    for rrow in right_rows:
        if rrow[rkey] is not None:
            buckets[rrow[rkey]].append(rrow)
    out = []
    for lrow in left_rows:
        matched = False
        k = lrow[lkey]
        if k is not None:
            for rrow in buckets.get(k, ()):
                merged = {**lrow, **rrow}
                if residual is None or residual.eval(merged) is True:  # LEFT JOIN：residual 属于"匹配条件"，不是事后过滤
                    matched = True
                    out.append(merged)
        if not matched and kind == "left":
            out.append({**lrow, **nulls})
    return out
```

**细节**（面试官会看你有没有想到）：
- **NULL 键不匹配任何东西**：`NULL = NULL` 是 UNKNOWN，所以 `rrow[rkey] is None` 的行不进桶，`k is None` 的左行也不探测。测试里：两边各有 NULL 键、各有 2 个重复键值 1 的表，inner join 结果是 2×2 的重复配对，**没有** NULL 行。
- **重复键**：桶是列表，所以一对多 / 多对多都自然正确。
- **residual**：`ON a.x = b.y AND b.amount > 45` 里等值部分走哈希，其余条件（residual）在桶内候选上继续检查。对 LEFT JOIN，residual 是**匹配条件的一部分**，不是事后过滤：不满足 residual 的候选不算"匹配"，该左行仍然会以 NULL 补齐输出（测试里的 `left_big` 就是这个情形：cat 与 dan 都输出，右侧为 NULL）。
- **build 哪一侧**：我们总是 build 右表（被连接的表）。对 INNER JOIN，build 较小的一侧更省内存；LEFT JOIN 要保留左侧所有行，所以必须以左侧为 probe。

```python
@staticmethod
def _split_equi(on: Pred, right_keys: set[str]) -> tuple[str, str, Pred | None] | None:
    """从 ON 的顶层合取项里找一条 '左侧列 = 右侧列'，它就是哈希连接的键；其余条件作为 residual 继续检查。"""
    conjuncts = on.conjuncts()
    for i, c in enumerate(conjuncts):
        if isinstance(c, Eq) and isinstance(c.right, Col) and (c.left.name in right_keys) != (c.right.name in right_keys):
            lkey, rkey = (c.right.name, c.left.name) if c.left.name in right_keys else (c.left.name, c.right.name)
            rest = conjuncts[:i] + conjuncts[i + 1:]
            return lkey, rkey, (And(*rest) if rest else None)
    return None
```

`_split_equi` 在 `ON` 的顶层 AND 合取项里找一条"一边属于新表、另一边属于已有表"的等值条件作为哈希键；找不到（非等值，或 OR 连接）就回退到嵌套循环。`Database._join` 负责选择：

```python
def _join(self, left_rows: list[Row], right: Table, alias: str, on: Pred, kind: str) -> list[Row]:
    if kind not in ("inner", "left"):
        raise DBError(f"unsupported join kind {kind!r}")
    right_rows = [self._qualify(alias, r) for r in right.matching(None)]
    nulls = {f"{alias}.{c.name}": None for c in right.columns}  # LEFT JOIN 没匹配时右侧补 NULL
    equi = None if self.join_strategy == "nested" else self._split_equi(on, set(nulls))
    if equi is None:
        return self._nested_loop_join(left_rows, right_rows, on, kind, nulls)
    return self._hash_join(left_rows, right_rows, equi, kind, nulls)
```

`join_strategy = "nested"` 是测试开关：**强制用嵌套循环，与哈希连接逐行对拍**（`test_join` 对 inner/left × 三种 ON 条件断言结果完全相同，包括输出顺序——两种算法都是"左表顺序、右表插入顺序"）。

### 5.4 LEFT JOIN 的语义要点
- 保留左表所有行；没匹配就右侧补 NULL。
- **ON vs WHERE**：`LEFT JOIN o ON … AND o.amount > 45` 与 `LEFT JOIN o ON … WHERE o.amount > 45` 不同：前者没匹配的左行仍在（右侧 NULL），后者把补 NULL 的行当 `NULL > 45` = UNKNOWN 丢掉，等价于 INNER JOIN。
- **反连接（anti-join）**：`LEFT JOIN … WHERE o.id IS NULL` = "没有订单的用户"。
- RIGHT / FULL JOIN：RIGHT = 交换两边的 LEFT；FULL = LEFT 的结果 + 右表中从未被匹配到的行（哈希连接里记录"桶里哪些行被匹配过"）。追问 Q11。

### 5.5 把整个流水线串起来：`Database.select`

```python
def select(self, table: str, columns: Sequence[str | Agg] | None = None, where: Pred | Mapping | None = None,
           order_by: Sequence[Any] | None = None, limit: int | None = None, joins: Sequence[Join] = (),
           group_by: Sequence[str] = (), alias: str | None = None) -> list[Row]:
    if limit is not None and (type(limit) is not int or limit < 0):
        raise DBError(f"bad LIMIT {limit!r}")
    t = self._table(table)
    scope = Scope(qualified=bool(joins))
    from_alias = alias or table
    scope.add(from_alias, t)
    where = as_pred(where)

    # 1) FROM / 2) JOIN / 3) WHERE
    if not joins:
        rows = t.matching(where.bind(scope) if where else None)  # 单表：WHERE 可以走索引
    else:
        rows = [self._qualify(from_alias, r) for r in t.matching(None)]
        for j in joins:
            right = self._table(j.table)
            right_alias = j.alias or j.table
            scope.add(right_alias, right)
            rows = self._join(rows, right, right_alias, j.on.bind(scope), j.kind)
        if where:
            bound = where.bind(scope)
            rows = [r for r in rows if bound.eval(r) is True]

    # 4) GROUP BY + 聚合 / 5) SELECT / 6) ORDER BY / 7) LIMIT
    items = list(columns) if columns else ["*"]
    order = _norm_order(order_by)
    if group_by or any(isinstance(c, Agg) for c in items):
        out, labels = self._aggregate(scope, rows, items, group_by)
        for name, _ in order:
            if name not in labels:
                raise NoSuchColumn(f"ORDER BY {name!r}: must be one of the selected columns {labels}")
        sort_rows(out, order)
        return out[:limit]
    sort_rows(rows, [(scope.lookup(name)[0], desc) for name, desc in order])  # 先排序再投影：ORDER BY 可以用没选出来的列
    rows = rows[:limit]
    projection: list[tuple[str, str]] = []  # (输出标签, 行字典 key)
    for c in items:
        if c == "*":
            projection.extend((k, k) for k in scope.star())
        else:
            projection.append((c, scope.lookup(c)[0]))
    return [{label: r[key] for label, key in projection} for r in rows]
```

逐段对照 §1.5 的逻辑顺序：
1. **FROM**：`t.matching(…)` 或 `t.matching(None)`（全部行）。
2. **JOIN**：对每个 `Join`，先把右表加入 `scope`，然后用**已包含右表的 scope** 绑定 `ON`（所以 `ON` 能引用前面所有表的列）。
3. **WHERE**：单表时直接交给 `Table.matching`（可以走索引，Part 6）；有 JOIN 时在连接之后过滤。（*谓词下推* 是追问 Q12：把只涉及 FROM 表的合取项在 JOIN 之前过滤，本实现没做。）
4. **GROUP BY / 聚合**：`_aggregate`（Part 6）。
5. **ORDER BY / LIMIT / SELECT**：先排序（`sort_rows`）再切片再投影。输出字典的 key 是用户写的名字（`SELECT *` 时单表是裸列名、有 JOIN 时是 `别名.列名`）。

返回的是**新字典**（投影时拷贝），调用者修改结果不会影响库（`test_crud` 有断言）。

---

## 6. Part 5：迷你 SQL 前端

目标：让 `db.execute("SELECT … FROM … WHERE … ORDER BY …")` 能跑，而不是只能调 Python API。分两步：**tokenizer**（字符串 → token 列表）+ **recursive-descent parser**（token → 我们已有的 `Pred` / `Join` / `Agg` 对象）。解析器直接产出 Part 2–4 的对象，所以不需要另造一套 AST。

### 6.1 文法（EBNF，原样摘自代码注释）

```text
# 文法（EBNF；大写是关键字，不区分大小写；标识符区分大小写）：
#
#   statement  := ( select | insert | update | delete | create | BEGIN | COMMIT | ROLLBACK ) [ ';' ] EOF
#   select     := SELECT ( '*' | item { ',' item } )
#                 FROM table_ref { join }
#                 [ WHERE expr ] [ GROUP BY colref { ',' colref } ]
#                 [ ORDER BY order_item { ',' order_item } ] [ LIMIT int ]
#   item       := colref | agg
#   agg        := ( COUNT | SUM | AVG | MIN | MAX ) '(' ( '*' | colref ) ')'
#   table_ref  := ident [ [ AS ] ident ]
#   join       := [ INNER | LEFT [ OUTER ] ] JOIN table_ref ON expr
#   order_item := ( colref | agg ) [ ASC | DESC ]
#   insert     := INSERT INTO ident [ '(' ident { ',' ident } ')' ] VALUES row { ',' row }
#   row        := '(' literal { ',' literal } ')'
#   update     := UPDATE ident SET ident '=' literal { ',' ident '=' literal } [ WHERE expr ]
#   delete     := DELETE FROM ident [ WHERE expr ]
#   create     := CREATE TABLE ident '(' coldef { ',' coldef } ')'
#   coldef     := ident ident [ PRIMARY KEY ] [ NOT NULL ]
#
#   expr       := or_expr
#   or_expr    := and_expr { OR and_expr }              -- 优先级最低
#   and_expr   := not_expr { AND not_expr }
#   not_expr   := NOT not_expr | predicate               -- NOT 比 AND 紧
#   predicate  := '(' expr ')'
#               | operand cmp operand                    -- cmp: = <> != < <= > >=
#               | colref [ NOT ] IN '(' literal { ',' literal } ')'
#               | colref [ NOT ] BETWEEN literal AND literal
#               | colref IS [ NOT ] NULL
#   operand    := colref | literal
#   literal    := int | float | 'string' | TRUE | FALSE | NULL | '-' number | '?'
#   colref     := ident | ident '.' ident                -- tokenizer 把 t.col 作为一个 token
```

**优先级就是文法的分层**：`or_expr` 调用 `and_expr`，`and_expr` 调用 `not_expr`，`not_expr` 调用 `predicate`。越靠下的层结合越紧：`NOT` 最紧，然后 `AND`，最后 `OR`。所以 `a = 1 OR b = 2 AND c = 3` 解析成 `a = 1 OR (b = 2 AND c = 3)`；`NOT a = 1 AND b = 2` 解析成 `(NOT a = 1) AND (b = 2)`。括号只出现在 `predicate` 里，括号里重新从 `expr` 开始。这就是**递归下降**：一个文法规则 = 一个函数，递归的文法 = 递归的函数。

### 6.2 tokenizer

```python
KEYWORDS = {
    "SELECT", "FROM", "WHERE", "JOIN", "INNER", "LEFT", "OUTER", "ON", "AND", "OR", "NOT", "IN", "IS", "NULL",
    "ORDER", "BY", "GROUP", "ASC", "DESC", "LIMIT", "INSERT", "INTO", "VALUES", "UPDATE", "SET", "DELETE",
    "CREATE", "TABLE", "PRIMARY", "KEY", "TRUE", "FALSE", "BETWEEN", "AS", "BEGIN", "COMMIT", "ROLLBACK",
}
SQL_TYPES = {"INT": int, "INTEGER": int, "TEXT": str, "VARCHAR": str, "REAL": float, "FLOAT": float, "BOOL": bool, "BOOLEAN": bool}
_TOKEN = re.compile(
    r"""\s*(?:(?P<num>\d+\.\d+|\d+)|(?P<str>'(?:[^']|'')*')|(?P<id>[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)?)|(?P<op><=|>=|<>|!=|[=<>(),*?;-]))"""
)


def tokenize(sql: str) -> list[tuple[str, Any, int]]:
    """返回 [(kind, value, 位置)]，kind ∈ lit / kw / id / op / eof。"""
    out: list[tuple[str, Any, int]] = []
    pos = 0
    while True:
        m = _TOKEN.match(sql, pos)
        if not m:
            rest = sql[pos:].strip()
            if rest:
                raise SQLSyntaxError(f"unexpected character {rest[0]!r} at position {sql.index(rest[0], pos)}")
            break
        kind, text = m.lastgroup, m.group(m.lastgroup)
        if kind == "num":
            out.append(("lit", float(text) if "." in text else int(text), m.start(kind)))
        elif kind == "str":
            out.append(("lit", text[1:-1].replace("''", "'"), m.start(kind)))
        elif kind == "id":
            out.append(("kw", text.upper(), m.start(kind)) if text.upper() in KEYWORDS else ("id", text, m.start(kind)))
        else:
            out.append(("op", text, m.start(kind)))
        pos = m.end()
    out.append(("eof", None, len(sql)))
    return out
```

要点：
- 一个正则、四个命名分组：数字、字符串（`''` 转义单引号）、标识符（`t.col` 作为**一个** token，省得 parser 处理点号）、运算符（`<=` `>=` `<>` `!=` 写在单字符前，否则 `<=` 会被拆成 `<` 和 `=`）。
- 关键字不区分大小写（统一转大写），标识符区分大小写（简化；真实数据库一般不区分）。
- 遇到无法识别的字符（`$`、未闭合的字符串）→ `SQLSyntaxError`，带位置。
- 负号是单独的 `-` token，由 `literal()` 处理（`age > -1`）。

### 6.3 Parser：token 工具 + 语句

```python
def peek(self) -> tuple[str, Any, int]:
    return self.toks[self.i]

def advance(self) -> tuple[str, Any, int]:
    tok = self.toks[self.i]
    if tok[0] != "eof":
        self.i += 1
    return tok

def error(self, message: str) -> SQLSyntaxError:
    kind, value, pos = self.peek()
    got = "end of input" if kind == "eof" else repr(value)
    return SQLSyntaxError(f"{message} at position {pos} (got {got})")

def accept_kw(self, *names: str) -> str | None:
    kind, value, _ = self.peek()
    if kind == "kw" and value in names:
        self.i += 1
        return value
    return None

def expect_kw(self, name: str) -> None:
    if not self.accept_kw(name):
        raise self.error(f"expected {name}")

def accept_op(self, op: str) -> bool:
    kind, value, _ = self.peek()
    if kind == "op" and value == op:
        self.i += 1
        return True
    return False

def expect_op(self, op: str) -> None:
    if not self.accept_op(op):
        raise self.error(f"expected {op!r}")

def ident(self) -> str:
    kind, value, _ = self.peek()
    if kind != "id":
        raise self.error("expected an identifier")
    self.i += 1
    return value
```

```python
def literal(self) -> Any:
    kind, value, _ = self.peek()
    if kind == "lit":
        self.i += 1
        return value
    if self.accept_kw("NULL"):
        return None
    if self.accept_kw("TRUE"):
        return True
    if self.accept_kw("FALSE"):
        return False
    if self.accept_op("-"):
        kind, value, _ = self.peek()
        if kind != "lit" or isinstance(value, str):
            raise self.error("expected a number after '-'")
        self.i += 1
        return -value
    if self.accept_op("?"):  # 参数占位符：值不经过 SQL 文本，天然没有注入问题
        if self.next_param >= len(self.params):
            raise self.error("not enough parameters for '?'")
        self.next_param += 1
        return self.params[self.next_param - 1]
    raise self.error("expected a literal")
```

`?` 占位符：值从 `params` 取，**不经过 SQL 文本**，所以 `WHERE name = ?` 传入 `"x' OR '1'='1"` 只是一个普通字符串（`test_parser` 里验证返回空）——这就是**参数化查询防注入**的原理（追问 Q9）。

```python
def statement(self) -> tuple[str, dict]:
    word = self.accept_kw("SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "BEGIN", "COMMIT", "ROLLBACK")
    if word is None:
        raise self.error("expected a statement")
    if word in ("BEGIN", "COMMIT", "ROLLBACK"):
        result: tuple[str, dict] = (word.lower(), {})
    else:
        result = (word.lower(), getattr(self, f"parse_{word.lower()}")())
    self.accept_op(";")
    if self.peek()[0] != "eof":
        raise self.error("unexpected trailing input")
    return result
```

```python
def parse_select(self) -> dict:
    columns: list[str | Agg] | None = None
    if not self.accept_op("*"):
        columns = []
        while True:
            columns.append(self.aggregate() if self.aggregate_ahead() else self.ident())
            if not self.accept_op(","):
                break
    self.expect_kw("FROM")
    table, alias = self.table_ref()
    joins: list[Join] = []
    while True:
        kind = "inner"
        if self.accept_kw("LEFT"):
            kind = "left"
            self.accept_kw("OUTER")
        elif self.accept_kw("INNER"):
            pass
        elif self.peek() != ("kw", "JOIN", self.peek()[2]):
            break
        self.expect_kw("JOIN")
        jt, ja = self.table_ref()
        self.expect_kw("ON")
        joins.append(Join(jt, self.expr(), kind, ja))
    where = self.expr() if self.accept_kw("WHERE") else None
    group_by: list[str] = []
    if self.accept_kw("GROUP"):
        self.expect_kw("BY")
        group_by.append(self.ident())
        while self.accept_op(","):
            group_by.append(self.ident())
    order_by: list[tuple[Any, str]] = []
    if self.accept_kw("ORDER"):
        self.expect_kw("BY")
        while True:
            key = self.aggregate() if self.aggregate_ahead() else self.ident()
            order_by.append((key, self.accept_kw("ASC", "DESC") or "ASC"))
            if not self.accept_op(","):
                break
    limit = None
    if self.accept_kw("LIMIT"):
        kind, value, _ = self.peek()
        if kind != "lit" or type(value) is not int:
            raise self.error("LIMIT needs an integer")
        self.i += 1
        limit = value
    return dict(table=table, columns=columns, where=where, order_by=order_by, limit=limit,
                joins=joins, group_by=group_by, alias=alias)
```

`parse_select` 的结构就是文法的逐行翻译：`SELECT` 列表 → `FROM` 表引用 → `{join}` 循环 → 可选 `WHERE` / `GROUP BY` / `ORDER BY` / `LIMIT`。其余三种语句：

```python
def parse_insert(self) -> dict:
    self.expect_kw("INTO")
    table = self.ident()
    columns = None
    if self.accept_op("("):
        columns = [self.ident()]
        while self.accept_op(","):
            columns.append(self.ident())
        self.expect_op(")")
    self.expect_kw("VALUES")
    rows = []
    while True:
        self.expect_op("(")
        values = [self.literal()]
        while self.accept_op(","):
            values.append(self.literal())
        self.expect_op(")")
        rows.append(values)
        if not self.accept_op(","):
            break
    return dict(table=table, columns=columns, rows=rows)

def parse_update(self) -> dict:
    table = self.ident()
    self.expect_kw("SET")
    set_: dict[str, Any] = {}
    while True:
        col = self.ident()
        self.expect_op("=")
        set_[col] = self.literal()
        if not self.accept_op(","):
            break
    return dict(table=table, set_=set_, where=self.expr() if self.accept_kw("WHERE") else None)

def parse_delete(self) -> dict:
    self.expect_kw("FROM")
    table = self.ident()
    return dict(table=table, where=self.expr() if self.accept_kw("WHERE") else None)
```

### 6.4 表达式解析：每层文法一个函数

```python
def expr(self) -> Pred:
    parts = [self.and_expr()]
    while self.accept_kw("OR"):
        parts.append(self.and_expr())
    return parts[0] if len(parts) == 1 else Or(*parts)

def and_expr(self) -> Pred:
    parts = [self.not_expr()]
    while self.accept_kw("AND"):
        parts.append(self.not_expr())
    return parts[0] if len(parts) == 1 else And(*parts)

def not_expr(self) -> Pred:
    if self.accept_kw("NOT"):
        return Not(self.not_expr())
    return self.predicate()

def operand(self) -> Col | Any:
    if self.peek()[0] == "id":
        return Col(self.ident())
    return self.literal()

def predicate(self) -> Pred:
    if self.accept_op("("):
        inner = self.expr()
        self.expect_op(")")
        return inner
    left = self.operand()
    kind, value, _ = self.peek()
    if kind == "op" and value in _CMP:
        self.i += 1
        right = self.operand()
        if isinstance(left, Col):
            return _CMP[value](left, right)
        if isinstance(right, Col):
            return _FLIP[value](right, left)
        if left is None or right is None:
            return Const(None)
        return Const(_CMP[value].fn(left, right))
    if not isinstance(left, Col):
        raise self.error("expected a comparison operator")
    if self.accept_kw("IS"):
        negate = bool(self.accept_kw("NOT"))
        self.expect_kw("NULL")
        return Not(IsNull(left)) if negate else IsNull(left)
    negate = bool(self.accept_kw("NOT"))
    if self.accept_kw("IN"):
        self.expect_op("(")
        values = [self.literal()]
        while self.accept_op(","):
            values.append(self.literal())
        self.expect_op(")")
        p: Pred = In(left, values)
    elif self.accept_kw("BETWEEN"):
        lo = self.literal()
        self.expect_kw("AND")
        p = And(Ge(left, lo), Le(left, self.literal()))
    else:
        raise self.error("expected a comparison operator, IN, BETWEEN or IS")
    return Not(p) if negate else p
```

细节：
- `5 < age`（字面量在左）会被**翻转**成 `age > 5`（`_FLIP` 表），因为 `Compare` 的左边必须是列；`1 = 1`（两边都是字面量）折叠成 `Const`。
- `x NOT IN (…)` / `x NOT BETWEEN a AND b`：先吃掉可选的 `NOT`，解析完谓词再包一层 `Not`。
- `BETWEEN a AND b` 里的 `AND` 是 `predicate` 内部消耗的，不会被上层的 `and_expr` 当成逻辑与——这就是为什么 `BETWEEN` 必须在 `predicate` 层处理而不能在 `and_expr` 层。

### 6.5 执行入口

```python
def execute(self, sql: str, params: Sequence[Any] = ()) -> Any:
    """SELECT → list[dict]；INSERT / UPDATE / DELETE → 受影响行数；其余 → None。"""
    kind, a = Parser(sql, params).statement()
    if kind == "select":
        return self.select(**a)
    if kind == "insert":
        t = self._table(a["table"])
        cols = a["columns"] or [c.name for c in t.columns]
        with self._statement():  # 多行 VALUES 要么全进要么全不进
            for values in a["rows"]:
                if len(values) != len(cols):
                    raise DBError(f"INSERT has {len(cols)} columns but {len(values)} values")
                t.insert(dict(zip(cols, values)))
        return len(a["rows"])
    if kind == "update":
        return self.update(a["table"], a["set_"], a["where"])
    if kind == "delete":
        return self.delete(a["table"], a["where"])
    if kind == "create":
        return self.create_table(a["table"], a["columns"], a["primary_key"])
    return {"begin": self.begin, "commit": self.commit, "rollback": self.rollback}[kind]()
```

SELECT 返回 `list[dict]`；INSERT / UPDATE / DELETE 返回受影响行数；多行 `INSERT … VALUES (…), (…)` 包在 `_statement()` 里——第二行主键重复时第一行也不会留下（`test_parser` 验证）。

**测试策略**：`test_sqlite_crosscheck` 随机生成**文本形式**的 SQL（大量不加括号的 `AND/OR/NOT` 链，随机 `IN`/`BETWEEN`/`IS NULL`/列与列比较），同时喂给我们的 `execute` 和标准库的 `sqlite3`，要求结果逐行相同。优先级、NULL、排序方向、JOIN 语义的任何偏差都会被抓到（我用变异测试验证过：把 NULL 排序方向或 `NOT` 的三值性改坏，对拍立刻失败）。

---

## 7. Part 6（senior）

### 7.1 索引与最小规划器

**索引**：两种。

```python
class HashIndex:
    """value → {pk}。只能回答 '=' 和 IN。NULL 不进索引（`= NULL` 永远不是 True）。"""

    kind = "hash"

    def __init__(self, column: str):
        self.column = column
        self.map: dict[Any, set] = {}

    def add(self, value: Any, pk: Any) -> None:
        if value is not None:
            self.map.setdefault(value, set()).add(pk)

    def remove(self, value: Any, pk: Any) -> None:
        if value is None:
            return
        bucket = self.map[value]
        bucket.discard(pk)
        if not bucket:
            del self.map[value]

    def eq(self, value: Any) -> list:
        return list(self.map.get(value, ()))
```

```python
class SortedIndex:
    """两个平行的有序列表 keys / pks，按 key 排序；用 bisect 回答 '=' 和范围查询。
    插入 / 删除是 O(n)（list 搬移，常数很小）；查询是 O(log n + 命中数)。"""

    kind = "sorted"

    def __init__(self, column: str):
        self.column = column
        self.keys: list[Any] = []
        self.pks: list[Any] = []

    def add(self, value: Any, pk: Any) -> None:
        if value is None:
            return
        i = bisect.bisect_right(self.keys, value)
        self.keys.insert(i, value)
        self.pks.insert(i, pk)

    def remove(self, value: Any, pk: Any) -> None:
        if value is None:
            return
        i = bisect.bisect_left(self.keys, value)
        while self.pks[i] != pk:  # 同值的多个 pk 排在一起，线性找到那一个
            i += 1
        del self.keys[i]
        del self.pks[i]

    def range(self, lo: Any = None, lo_incl: bool = True, hi: Any = None, hi_incl: bool = True) -> tuple[int, int]:
        """返回命中区间 [i, j)（只是下标，不拷贝），None 表示无界。j - i 就是命中数，规划器用它估代价。"""
        i = 0 if lo is None else (bisect.bisect_left(self.keys, lo) if lo_incl else bisect.bisect_right(self.keys, lo))
        j = len(self.keys) if hi is None else (bisect.bisect_right(self.keys, hi) if hi_incl else bisect.bisect_left(self.keys, hi))
        return i, max(i, j)

    def eq(self, value: Any) -> list:
        i, j = self.range(value, True, value, True)
        return self.pks[i:j]
```

- `HashIndex`：值 → 主键集合；`=` / `IN` O(1)。NULL 不进索引（`= NULL` 永远不是 True）。
- `SortedIndex`：两个平行有序列表（`keys` / `pks`），按 key 排序。`bisect_left` / `bisect_right` 定位；`range()` 返回**下标区间 [i, j)**，所以"命中多少行"是 `j - i`，O(log n) 就知道，不用先取出来数——规划器用它估代价。
- 为什么不用 `(value, pk)` 元组的有序列表：同值时要比较 pk，pk 类型任意；平行数组避开了这个问题。
- 代价：`SortedIndex` 的插入 / 删除是 O(n)（`list.insert` 搬移，常数很小）。真实数据库用 B 树 O(log n)。口头说明即可。

**规划器**（`Table.plan`）：从 `WHERE` 的**顶层 AND 合取项**里找能用索引的：
- `col = 常量`：主键（天然哈希）、哈希索引或有序索引；
- `col IN (常量…)`：每个值各查一次，合并；
- `col < / <= / > / >= 常量` 且该列有 `SortedIndex`：把同一列的多个范围条件合并成一个区间（取更紧的下界 / 上界；同值时开区间更紧）。
然后在所有候选路径里选**候选行数最少**的，和全表扫描（候选数 = 总行数）比较。**规划器只缩小候选集，之后仍用完整 WHERE 过滤**，所以它永远不会改变结果，只会改变速度——这使得规划器的正确性很容易测（有索引 / 无索引结果必须一致）。

```python
def plan(self, pred: Pred | None) -> tuple[str, list | None]:
    """极简规划器：从 WHERE 的顶层 AND 合取项里找能用索引的（'=' / IN / 范围），
    挑候选行数最少的那条路径；没有就全表扫描。返回 (说明, 候选主键列表 | None=全表)。
    规划器只负责"缩小候选集"，之后仍用完整 WHERE 过滤，所以它永远不会改变结果。"""
    total = len(self.rows)
    best: tuple[int, str, list | None] = (total, f"SCAN {self.name} ({total} rows)", None)
    if pred is None:
        return best[1], best[2]
    bounds: dict[str, list] = {}  # 列 → [lo, lo_incl, hi, hi_incl]

    def consider(cost: int, text: str, pks: Callable[[], list]) -> None:
        nonlocal best
        if cost < best[0]:
            best = (cost, text, pks())

    for c in pred.conjuncts():
        if isinstance(c, Compare) and not isinstance(c.right, Col) and c.right is not None:
            col, v = c.left.name, c.right
            if isinstance(c, Eq):
                found = self._lookup_eq(col, [v])
                if found is not None:
                    consider(len(found[1]), f"INDEX {found[0]} {self.name}.{col} = {v!r} ({len(found[1])} of {total})", lambda f=found: f[1])
            elif isinstance(c, (Lt, Le, Gt, Ge)) and isinstance(self.indexes.get(col), SortedIndex):
                b = bounds.setdefault(col, [None, True, None, True])
                if isinstance(c, (Gt, Ge)):  # 取更紧的下界（同值时开区间更紧）
                    if b[0] is None or v > b[0] or (v == b[0] and isinstance(c, Gt)):
                        b[0], b[1] = v, isinstance(c, Ge)
                elif b[2] is None or v < b[2] or (v == b[2] and isinstance(c, Lt)):
                    b[2], b[3] = v, isinstance(c, Le)
        elif isinstance(c, In) and None not in c.values:
            found = self._lookup_eq(c.left.name, c.values)
            if found is not None:
                consider(len(found[1]), f"INDEX {found[0]} {self.name}.{c.left.name} IN (…{len(c.values)}) ({len(found[1])} of {total})", lambda f=found: f[1])
    for col, (lo, lo_incl, hi, hi_incl) in bounds.items():
        ix = self.indexes[col]
        i, j = ix.range(lo, lo_incl, hi, hi_incl)
        consider(j - i, f"INDEX sorted {self.name}.{col} range {lo!r}..{hi!r} ({j - i} of {total})", lambda ix=ix, i=i, j=j: ix.pks[i:j])
    return best[1], best[2]
```

```python
def _lookup_eq(self, col: str, values: Iterable[Any]) -> tuple[str, list] | None:
    """用主键字典或该列的索引取等值候选；没有可用的就返回 None。"""
    if col == self.pk:
        return "pk", [v for v in dict.fromkeys(values) if v in self.rows]
    ix = self.indexes.get(col)
    if ix is None:
        return None
    pks: dict[Any, None] = {}
    for v in values:
        for pk in ix.eq(v):
            pks[pk] = None
    return ix.kind, list(pks)
```

```python
def matching(self, pred: Pred | None) -> list[Row]:
    """满足 WHERE 的行（存储的行字典本身，调用者不得修改），按插入顺序。"""
    _, pks = self.plan(pred)
    pool = self.rows.values() if pks is None else (self.rows[pk] for pk in pks)
    out = [r for r in pool if pred is None or pred.eval(r) is True]
    out.sort(key=lambda r: self.seq[r[self.pk]])
    return out
```

`explain` 让规划结果可见（也用于测试）：

```text
db.explain("e", Eq("uid", 3))                      →  INDEX hash e.uid = 3 (… of 300)
db.explain("e", {"id": 5})                         →  INDEX pk e.id = 5 …
db.explain("e", And(Ge("ts", 100), Lt("ts", 120))) →  INDEX sorted e.ts range 100..120 …
db.explain("e", Or(Eq("uid", 3), Eq("ts", 4)))     →  SCAN e (… rows)        ← OR 不拆，保守地全表扫描
db.explain("e", Ne("uid", 3))                      →  SCAN e (… rows)        ← <> 用不上索引
```

**实测加速**（`test_perf`：2 万行，`uid` 有 2000 个不同值，40 次查询；一次实测，数字随机器浮动）：

| 查询 | 每次命中 | 索引 / 算法 | 相对全表扫描（或嵌套循环）的加速 |
|---|---|---|---|
| `uid = ?`（2000 个不同值） | 约 10 行 | 哈希索引 | 约 **70–150 倍**（多次运行的范围） |
| `ts >= s AND ts < s+100`（值域 0–10⁶） | 约 2 行 | 有序索引（`bisect`） | 约 **500–600 倍** |
| 600×600 等值 JOIN | — | 哈希连接 vs 嵌套循环 | 约 **65 倍** |

测试里的断言阈值设得很保守（>20 倍、连接 >5 倍），防止机器抖动；同时断言**有索引与无索引结果完全相同**。

**索引维护的正确性**：`Table.check_invariants()` 把每个索引与"从行数据重建的索引"比较；`test_indexes_and_planner` 与 `test_sqlite_crosscheck` 的随机 DML 序列之后都调用它。

### 7.2 GROUP BY + 聚合

```python
class Agg:
    """COUNT / SUM / AVG / MIN / MAX。NULL 被忽略（COUNT(*) 数行，不看值）；
    没有非 NULL 值时 SUM / AVG / MIN / MAX 是 NULL，COUNT 是 0。"""

    FUNCS = ("count", "sum", "avg", "min", "max")

    def __init__(self, func: str, column: str = "*", label: str | None = None):
        func = func.lower()
        if func not in self.FUNCS:
            raise DBError(f"unknown aggregate {func!r}")
        if column == "*" and func != "count":
            raise DBError(f"{func}(*) is not allowed")
        self.func, self.column = func, column
        self.label = label or f"{func}({column})"

    def bind(self, scope: Scope) -> str | None:
        """返回行字典里的 key（COUNT(*) 返回 None）；SUM / AVG 要求数值列。"""
        if self.column == "*":
            return None
        key, column = scope.lookup(self.column)
        if self.func in ("sum", "avg") and not _numeric(column.type):
            raise TypeMismatch(f"{self.func}() needs a numeric column, got {column.name!r}")
        return key

    def compute(self, rows: list[Row], key: str | None) -> Any:
        if key is None:
            return len(rows)
        values = [r[key] for r in rows if r[key] is not None]
        if self.func == "count":
            return len(values)
        if not values:
            return None
        if self.func == "sum":
            return sum(values)
        if self.func == "avg":
            return sum(values) / len(values)
        return min(values) if self.func == "min" else max(values)
```

**规则**（都在 `test_aggregates` 里）：
- `COUNT(*)` 数行；`COUNT(col)` 只数非 NULL；`SUM / AVG / MIN / MAX` 忽略 NULL。
- 没有非 NULL 值时：`COUNT` = 0，其余 = NULL。
- **没有 GROUP BY 的聚合，即使输入为空也输出一行**（`SELECT COUNT(*) FROM t` 在空表上返回 `0`）；**有 GROUP BY 且输入为空则没有行**。
- NULL 在分组时被当作同一个组（`GROUP BY city` 里所有 `city IS NULL` 的行一组）。
- `SELECT` 里的非聚合列必须出现在 `GROUP BY` 里（否则 `DBError`）。
- `SUM / AVG` 作用于非数值列 → `TypeMismatch`（绑定阶段）。

```python
def _aggregate(self, scope: Scope, rows: list[Row], items: list, group_by: Sequence[str]) -> tuple[list[Row], list[str]]:
    gkeys = [scope.lookup(g)[0] for g in group_by]
    plan: list[tuple[str, Agg | None, str | None]] = []
    for it in items:
        if isinstance(it, Agg):
            plan.append((it.label, it, it.bind(scope)))
        elif it == "*":
            raise DBError("SELECT * cannot be combined with GROUP BY / aggregates")
        else:
            key = scope.lookup(it)[0]
            if key not in gkeys:
                raise DBError(f"column {it!r} must appear in GROUP BY or inside an aggregate")
            plan.append((it, None, key))
    groups: dict[tuple, list[Row]] = {}
    for r in rows:
        groups.setdefault(tuple(r[k] for k in gkeys), []).append(r)  # NULL 会分到同一组（None 可哈希）
    if not gkeys and not groups:
        groups[()] = []  # 没有 GROUP BY 的聚合：空表也输出一行（COUNT=0，其余 NULL）
    out = [{label: agg.compute(grp, key) if agg else grp[0][key] for label, agg, key in plan} for grp in groups.values()]
    return out, [label for label, _, _ in plan]
```

实现就是**哈希分组**：`groups: dict[分组键元组 → 行列表]`，再对每组算聚合，O(n)。分组之后 `ORDER BY` 只能引用输出列（标签）——因为聚合之后原始行已经不存在了。`HAVING` 没做：它是"对分组结果的 WHERE"，加一个对输出行求值的 `Pred` 即可（追问 Q13）。

### 7.3 事务：BEGIN / COMMIT / ROLLBACK 与 undo log

**问题**：转账要"A 扣 30，B 加 30"，中途失败必须全部撤销。
**方案**：**undo log（撤销日志）**。每个改动原语（`_add` / `_drop` / 计数器更新 / `create_table` / `create_index`）在执行的同时，往 `journal` 里压一个"逆操作"闭包。`ROLLBACK` = 从后往前弹出并执行所有逆操作。`COMMIT` = 清空 journal（改动已经就地生效，不需要做别的）。

```python
def _undo_to(self, mark: int) -> None:
    while len(self._journal) > mark:
        self._journal.pop()()

@contextmanager
def _statement(self):
    """每条语句要么全做要么全不做：出错就把 journal 撤销回语句开始处。
    没有显式事务时语句结束即"自动提交"（清空 journal）。"""
    mark = len(self._journal)
    try:
        yield
    except BaseException:
        self._undo_to(mark)
        raise
    else:
        if not self._in_txn:
            self._journal.clear()
```

```python
def begin(self) -> None:
    if self._in_txn:
        raise TransactionError("transaction already active (savepoints are not supported)")
    self._in_txn = True

def commit(self) -> None:
    if not self._in_txn:
        raise TransactionError("no active transaction")
    self._journal.clear()
    self._in_txn = False

def rollback(self) -> None:
    if not self._in_txn:
        raise TransactionError("no active transaction")
    self._undo_to(0)
    self._in_txn = False

@contextmanager
def transaction(self):
    self.begin()
    try:
        yield self
    except BaseException:
        self.rollback()
        raise
    else:
        self.commit()
```

**两个层次的原子性共用同一个 journal**：
- **语句原子**（`_statement`）：一条 `UPDATE` / 多行 `INSERT` 中途出错，journal 撤销回语句开始的位置（`mark`），错误向上抛。没有显式事务时，语句成功后 journal 清空（自动提交）。
- **事务原子**（`begin … commit/rollback`）：事务里的语句成功后 journal 不清空，直到 commit / rollback；事务里某条语句失败，只撤销**它自己**，事务仍然活着，调用方决定是 rollback 还是继续（`test_transactions` 验证）。

`with db.transaction():` 是上下文管理器：正常退出 commit，异常退出 rollback 并继续抛。

**为什么是 undo log 而不是"写时拷贝整库快照"**：快照是 O(数据量) 的；undo log 是 O(事务里改动的行数)。代价：只能做**单事务**（不支持嵌套 / 保存点，已在代码里明确报错），也没有持久化（没有 redo log / WAL）。

**测试**：`test_transactions`：多步操作后 rollback 与快照完全相同；自增计数器被恢复；`create_table` 在事务里被回滚；40 轮随机操作 + 随机回滚，每轮之后 `check_invariants()`。

### 7.4 线程安全：三个选项

| 方案 | 做法 | 优点 | 缺点 |
|---|---|---|---|
| **粗粒度锁（本实现）** | 整个数据库一把 `RLock`，每个公开方法持锁执行；事务从 `begin` 持锁到 `commit/rollback` | 最简单；天然串行化（serializable），不需要考虑死锁与读写冲突 | 并发度为 1：读也被写阻塞 |
| 每表一把锁 | 每张表一把锁；JOIN 要锁多张表 | 不同表的操作可以并行 | 必须规定**加锁顺序**（如按表名排序）避免死锁；事务跨多表要持有多把锁；索引 / 外键引用要小心 |
| MVCC 快照 | 每次写产生新版本（copy-on-write 或版本链），读事务看到的是开始时刻的快照，读不阻塞写 | 读多写少时并发度高；读不加锁 | 实现复杂：版本回收（vacuum）、写写冲突检测（first-committer-wins）、快照可见性规则 |

**为什么先选粗粒度锁**：面试里"最简单的**正确**方案"优于"复杂但可能有 bug 的方案"。CPython 的 GIL 只保证**单个字节码级操作**（如一次 `dict` 赋值）原子，不保证"读余额 → 判断 → 写余额"这类**多步不变量**，所以仍然需要显式的锁。

```python
def _synchronized(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)
    return wrapper


class ThreadSafeDatabase(Database):
    """每个公开方法都在同一把 RLock 里执行；`begin()` 拿到锁后一直持有到 commit / rollback，
    于是一个事务内的"读-改-写"不会被别的线程插队（等价于串行执行，隔离级别是 serializable）。
    RLock 可重入：持锁线程在事务内再调用 select / update 不会死锁。"""

    def __init__(self):
        super().__init__()
        self._lock = threading.RLock()

    create_table = _synchronized(Database.create_table)
    create_index = _synchronized(Database.create_index)
    insert = _synchronized(Database.insert)
    update = _synchronized(Database.update)
    delete = _synchronized(Database.delete)
    select = _synchronized(Database.select)
    explain = _synchronized(Database.explain)
    execute = _synchronized(Database.execute)

    def begin(self) -> None:
        self._lock.acquire()
        try:
            super().begin()
        except BaseException:
            self._lock.release()
            raise

    def commit(self) -> None:
        super().commit()  # 没有事务时这里抛错，锁不会被多释放
        self._lock.release()

    def rollback(self) -> None:
        super().rollback()
        self._lock.release()
```

关键点：
- **`RLock`（可重入）**：持锁线程在事务内再调 `select` / `update` 不会死锁自己。
- **`begin` 拿锁、`commit/rollback` 放锁**：事务期间别的线程的任何操作都被挡在锁外——读到的永远是已提交的状态，转账的中间状态不可见。
- 如果 `commit()` 在没有事务时被误调，`super().commit()` 先抛 `TransactionError`，**不会多释放锁**（`test_threads` 里验证之后别的线程仍能拿到锁）。
- `with db.transaction():` 保证异常路径也会 rollback 并释放锁。

**测试**（`test_threads`）：6 个线程各做 300 次"读计数器 → +1 → 写回"（事务里），最终必须恰好 1800；3 个线程随机转账，1 个审计线程在事务里反复断言 4 个账户总额恒为 400。

**MVCC 怎么答（不实现）**：给每行存 `(created_txn, deleted_txn)`；读事务启动时记录快照号 S，一行对它可见当且仅当 `created ≤ S < deleted`（且创建者已提交）；写事务提交时检查它修改的行有没有被更晚提交的事务改过（冲突则中止重试）；后台线程清理没有任何活跃快照能看到的旧版本。我们的 `seq` / journal 结构可以演化成这个，但不在 45 分钟范围内。

---

## 8. 45 分钟怎么写

> 这一节与上面的"完整参考"分开：上面是**学**的，这一节是**面试里照着做**的。对应代码：`code/in_memory_database_45min.py`（约 370 行，其中测试约 150 行；Parts 2–4 的核心）。

### 8.1 时间表与口述稿

| 分钟 | 做什么 | 你要**说出口**的话 |
|---|---|---|
| 0–5 | 澄清需求，别急着写 | "我先确认几件事：数据都在内存、单线程先不管并发；列有类型吗（我假设有：int/str/float/bool）；主键是单列吗；SELECT 要支持哪些子句——WHERE、ORDER BY、LIMIT，还有 JOIN 对吧；JOIN 先做等值的 inner 和 left；NULL 要支持吗（我会支持，并且 NULL 比较按 SQL 的三值逻辑）；错误用异常表示。" |
| 5–10 | 画出数据模型与分层，说出**取舍** | "Table 是 `{主键: 行字典}`；谓词做成小对象，能组合；`select` 的流水线我按 SQL 的**逻辑顺序**写：FROM → JOIN → WHERE → ORDER BY → LIMIT → SELECT。" |
| 10–22 | **写 CRUD**（`create_table / insert / update / delete`）+ 类型检查 + 自增 | 边写边说："校验全部放在改动之前，失败不留半截状态。" "自增计数器删除不回退。" "bool 是 int 的子类，所以类型检查用 `type(v) is`。" |
| 22–32 | **谓词 + select + ORDER BY**（单表） | "比较有一边是 NULL 返回 None，WHERE 只留 `is True`。" "ORDER BY 多键我从最后一个键往前各排一遍，利用 Python sort 的稳定性，每遍可以有自己的方向。" "NULL 我定为最小，ASC 在前——和 SQLite 一致，面试官要反过来只改一个位。" |
| 32–40 | **JOIN**：先口述嵌套循环 O(n·m)，然后写哈希连接 | "等值连接可以 build 右表 probe 左表，O(n+m)。NULL 键不匹配。LEFT JOIN 没匹配的左行补 NULL。连接后列名用 `别名.列名`，不重名的列允许不限定，重名报错。" |
| 40–45 | 写 2–3 个测试断言，**口头**讲没写的 | "我没写但会加的：索引（哈希 `=`，有序 `bisect` 范围）、SQL 解析（tokenizer + 递归下降，优先级 NOT>AND>OR）、事务（undo log）、线程安全（先上一把 RLock）、聚合。" |

### 8.2 一份合格答卷的"内容清单"（按优先级，时间不够就从下往上砍）

1. ✅ **必须**：`Table` + `create_table / insert`（类型、重复主键、自增）。
2. ✅ **必须**：`select` 的 WHERE（谓词对象，含 NULL 语义）+ ORDER BY（多键，稳定）+ LIMIT。
3. ✅ **必须**：`update / delete`（用同一个 WHERE；先校验再改）。
4. ✅ 强烈建议：inner join（先嵌套循环，能跑通）。
5. ⭐ 加分：哈希连接 + LEFT JOIN；列名限定。
6. ⭐ 加分：2–3 个测试用例（测试名描述业务需求，如 `test_where_never_matches_null_with_equals`）。
7. 🗣 口头带过：索引、SQL 解析、事务、并发、聚合。

**如果只剩 10 分钟还没写 JOIN**：不要硬赶哈希连接——先写 20 行嵌套循环 inner join，跑通，再说"哈希连接把它从 O(n·m) 降到 O(n+m)，思路是……"。**跑通的简单版 > 没跑通的优化版**。

### 8.3 紧凑版的取舍（对照 `in_memory_database_45min.py`）

| 完整版 | 45 分钟版 | 为什么可以省 |
|---|---|---|
| 谓词是 `Pred` 子类（可绑定、可检查） | 谓词是可调用对象 / 闭包（`Cmp`、`In`、`And`…） | 没有规划器就不需要"检查谓词"；闭包写起来快 |
| `Scope` 在执行前绑定名字、做类型检查 | 运行时 `row[col]`，`KeyError` 转成 `DBError` | 少 60 行；代价：空表上的拼写错误发现不了（口头承认） |
| 多种错误子类 | 一个 `DBError` | 面试里一个异常类 + 清晰消息足够 |
| 嵌套循环 + 哈希连接 + 残余条件 | 只有哈希连接，等值 ON | 非等值 ON 口头说"退回嵌套循环" |
| 索引 / journal / 事务 | 无 | 口头 |

紧凑版的 `select` 核心（流水线顺序 = 逻辑顺序）：

```python
def select(self, table: str, columns: list[str] | None = None, where=None, order_by=None,
           limit: int | None = None, joins: list[Join] | None = None, alias: str | None = None) -> list[dict]:
    t = self._table(table)
    a0 = alias or table
    if not joins:
        rows = self._matching(t, where)                       # 单表：直接用存储的行（列名不带限定）
    else:
        rows = [{f"{a0}.{c}": v for c, v in r.items()} for r in t.rows.values()]   # FROM
        members = [(a0, t)]
        for j in joins:                                       # JOIN（逐个）
            rt = self._table(j.table)
            members.append((j.alias or j.table, rt))
            rows = self._hash_join(rows, rt, j.alias or j.table, j)
        counts = Counter(c for _, m in members for c in m.columns)
        for r in rows:                                        # 不重名的列也可以不限定
            for a, m in members:
                for c in m.columns:
                    if counts[c] == 1:
                        r[c] = r[f"{a}.{c}"]
        if where is not None:                                 # WHERE 在 JOIN 之后
            rows = [r for r in rows if where(r) is True]
    try:
        for col, desc in reversed(self._norm(order_by)):     # ORDER BY：从最后一个键往前各排一遍（稳定）
            rows.sort(key=lambda r, c=col: (r[c] is not None, r[c]), reverse=desc)
        rows = rows[:limit]                                   # LIMIT
        if columns is None:
            return [dict(r) for r in rows] if not joins else [{k: v for k, v in r.items() if "." in k} for r in rows]
        return [{c: r[c] for c in columns} for r in rows]     # SELECT 投影
    except KeyError as e:
        raise DBError(f"unknown column {e.args[0]!r}") from None
```

哈希连接：

```python
@staticmethod
def _hash_join(left_rows: list[dict], rt: Table, alias: str, j: Join) -> list[dict]:
    """build 右表（O(|R|)），probe 左表（O(|L| + 输出)）。NULL 键不匹配任何东西。"""
    buckets: dict[Any, list[dict]] = defaultdict(list)
    right_rows = [{f"{alias}.{c}": v for c, v in r.items()} for r in rt.rows.values()]
    for r in right_rows:
        if r[j.right] is not None:
            buckets[r[j.right]].append(r)
    nulls = {f"{alias}.{c}": None for c in rt.columns}
    out = []
    for l in left_rows:
        matches = buckets.get(l[j.left], []) if l[j.left] is not None else []
        out.extend({**l, **r} for r in matches)
        if not matches and j.kind == "left":                  # LEFT JOIN：没匹配也保留，右侧补 NULL
            out.append({**l, **nulls})
    return out
```

谓词（可调用对象，三值逻辑）：

```python
class Cmp:
    def __init__(self, col: str, fn: Callable[[Any, Any], bool], right: Any):
        self.col, self.fn, self.right = col, fn, right

    def __call__(self, row: dict) -> bool | None:
        a = row[self.col]
        b = row[self.right.name] if isinstance(self.right, Col) else self.right
        return None if a is None or b is None else self.fn(a, b)   # 和 NULL 比较 → UNKNOWN


def In(c: str, values: list):  # noqa: N802
    def pred(row: dict) -> bool | None:
        a = row[c]
        if a is None:
            return None
        if any(v is not None and a == v for v in values):
            return True
        return None if None in values else False   # 没命中但列表里有 NULL → UNKNOWN
    return pred


def And(*ps):  # noqa: N802
    def pred(row: dict) -> bool | None:
        vals = [p(row) for p in ps]
        return False if False in vals else (None if None in vals else True)
    return pred


def Or(*ps):  # noqa: N802
    def pred(row: dict) -> bool | None:
        vals = [p(row) for p in ps]
        return True if True in vals else (None if None in vals else False)
    return pred


def Not(p):  # noqa: N802
    return lambda row: None if (v := p(row)) is None else not v
```

紧凑版的测试里也有一个 `test_vs_sqlite`：对象和 SQL 文本同时随机生成、与 `sqlite3` 对拍——**面试里不需要写这个**，但用它来练习时它能立刻告诉你实现是否有语义 bug。

---

## 9. 追问预演

每条：问题 → 答案要点 → 可以说出口的一段话。

**Q1. 再加一种比较符 `LIKE`（或 `<>` 以外的新运算）要改几处？**
要点：一个新的 `Compare` 子类（写它的 `fn`），`And/Or/Not/规划器` 都不动；SQL 前端加一个 token / 映射表条目。规划器默认当作"无法用索引"，仍然正确。
说：「新增一个类、一张映射表里加一行；其它代码不知道比较符的种类。」

**Q2. `WHERE age <> 30` 为什么没选出 age 是 NULL 的行？想要怎么办？**
要点：NULL 的任何比较都是 UNKNOWN，WHERE 只留 True；要写 `age <> 30 OR age IS NULL`。（测试 `test_predicates`。）

**Q3. `NOT IN` 的列表里有 NULL 会怎样？**
要点：一行都选不出（`x IN (1, NULL)` 在 x≠1 时是 UNKNOWN，NOT 后仍 UNKNOWN）。工程上：构造 `NOT IN` 的列表时先过滤 NULL，或改用 `NOT EXISTS`。

**Q4. ORDER BY 多键混合方向怎么实现？为什么对？**
要点：从最后一个键往前各稳定排序一遍，每遍自己的 `reverse`；因为稳定排序保证"先前的顺序在新键相同时保留"，主键最后排，它的相等块内保持次键顺序。`reverse=True` 也保持稳定（Python 文档）。反例：把 `reverse` 实现成"排完升序再整体反转"会破坏稳定性（相等元素的顺序被反了）。

**Q5. 要 `NULLS LAST`（或 PostgreSQL 的默认：NULL 最大）怎么改？**
要点：排序键里 `value is not None` 这一位取反：`(value is None, value)` 就是 NULL 最大；每个键可以配一个 `nulls_first` 标志。ASC/DESC 与 NULL 位置是两个独立维度。

**Q6. 哈希连接为什么快？什么时候不快？**
要点：O(|L|+|R|+输出) 对比 O(|L|·|R|)。不快 / 用不了：①非等值条件（`<`、范围）→ 退回嵌套循环，或排序合并（sort-merge）+ 双指针；②右表很大放不进内存（真实数据库用 grace hash join 分区落盘）；③键严重倾斜（一个键对应一半的行）→ 输出本身就大。**build 较小的一侧**。

**Q7. 三表连接怎么办？顺序有影响吗？**
要点：逐个连接，`ON` 可以引用前面所有表；INNER JOIN 满足结合律所以顺序只影响性能（先连接结果小的）；LEFT JOIN 的顺序影响语义。真实数据库的优化器基于基数估计选连接顺序。

**Q8. `SELECT *` 在 JOIN 时重名列怎么办？**
要点：输出 key 用 `别名.列名`，所以不冲突；不带限定引用重名列 → `AmbiguousColumn`。（SQLite 的 `SELECT *` 返回重复的列名，Python dict 装不下，所以我们用限定名。）

**Q9. 怎么防 SQL 注入？**
要点：参数化 `?`，参数值**不经过** tokenizer；我们的 `Parser.literal` 直接从 `params` 取值。反例：字符串拼接 `f"... WHERE name = '{x}'"`。（测试里传入 `x' OR '1'='1` 返回空。）

**Q10. 为什么 `UPDATE` 要先算出全部新行再动手？**
要点：①语句原子性：中途失败（类型错、NOT NULL、主键冲突）不留半截；②主键互换（1↔2）在"逐行改"下会有瞬时重复；③`UPDATE … SET x = x + 1 WHERE x > 5` 如果边改边扫，会再次匹配自己改过的行（Halloween problem）。

**Q11. 实现 RIGHT / FULL JOIN。**
要点：RIGHT = 交换左右后做 LEFT，再调整列顺序；FULL = LEFT 的结果 + 右表中从未被匹配的行（左侧补 NULL）。哈希连接里用一个 `matched_right` 集合记录被命中的桶行即可。

**Q12. 谓词下推（predicate pushdown）是什么？**
要点：把只涉及单个表的 WHERE 合取项，在 JOIN **之前**对那张表过滤，减少连接的输入。对 INNER JOIN 两边都安全；对 LEFT JOIN 只对左表安全（对右表下推会改变语义，把本该补 NULL 的行丢掉）。本实现没做，因为单表 WHERE 已经能走索引，而 JOIN 查询的 WHERE 在连接之后求值，语义最直观。

**Q13. 加 `HAVING` / `DISTINCT` / 子查询。**
要点：`HAVING` = 对分组输出行的过滤（再来一个 `Pred`，在 `_aggregate` 之后、`ORDER BY` 之前求值）；`DISTINCT` = 投影之后去重（对行元组用 `dict.fromkeys`，NULL 视为相等）；标量子查询 = 先递归执行内层 `select`，把结果当常量代入。

**Q14. 并发：两个线程同时转账会怎样？你的方案是什么？**
要点：GIL 不保证多步不变量；读-判断-写必须在同一临界区。选粗粒度 `RLock` + 事务持锁（串行化），说出每表锁需要的加锁顺序、MVCC 的版本可见性规则，并解释为什么先选最简单的正确方案。

**Q15. 怎么持久化？**
要点：WAL（预写日志）：每个事务提交前先把改动顺序追加到日志并 `fsync`，再认为提交成功；崩溃恢复时重放日志；定期做 checkpoint（把内存快照写盘并截断日志）。我们的 journal 是 undo（回滚用），持久化需要 redo。

**Q16. 内存会爆吗？怎么限制？**
要点：行字典每行有哈希表开销；可以用 `__slots__` 类 / 元组 + 列下标表示行（省 3–5 倍内存）；列式存储（每列一个数组）对聚合更友好；超过阈值溢写磁盘。

**Q17. LC 2408 的稀疏表 follow-up。**（见 §2.3）

---

## 10. 常见 bug

1. **把 `NULL = NULL` 当成 True**（用 Python 的 `==` 直接比 `None == None`）。→ 比较前检查 `None`，返回 UNKNOWN。
2. **`WHERE` 里保留 `bool(result)` 而不是 `result is True`**：UNKNOWN（`None`）和 False 看起来一样没问题，但 `NOT` 之后会出错——`not None` 是 True，会把 NULL 行选进来。→ 三值逻辑里 `Not` 必须保持 `None`。
3. **`isinstance(v, int)` 接受了 `True`**。→ `type(v) is int`。
4. **自增计数器用 `len(rows) + 1`**：删除后会重复分配 id、与未删除的主键冲突。→ 独立计数器，删除不回退，显式大主键推进它。
5. **多键排序里用 `reverse=True` 一次性排所有键**（只能全升或全降）；或者对 DESC 键取负数（字符串不能取负）。→ 多遍稳定排序。
6. **排序键里直接用 `row[col]`，遇到 NULL 抛 `TypeError`（`None < 3`）**。→ `(v is not None, v)`。
7. **`UPDATE` 边扫边改**：Halloween problem；或者逐行改主键导致瞬时重复。→ 先收集目标行并校验，再统一应用。
8. **哈希连接忘了 NULL 键**：`None` 进了桶，两边的 NULL 键错误地配上对。→ NULL 键不进桶、不探测。
9. **LEFT JOIN 把右表条件放在 WHERE**：悄悄变成 INNER JOIN。→ 右表条件放 `ON`。
10. **连接后用 `{**left, **right}` 合并裸列名**：重名列被后者静默覆盖。→ 限定 key `别名.列名`。
11. **`select` 返回存储的行字典本身**：调用者改结果就改了数据库。→ 投影时新建字典。
12. **规划器用索引后没有再用完整 WHERE 过滤**：`a = 1 AND b = 2` 只用 `a` 的索引就返回，漏掉了 `b = 2`。→ 索引只缩小候选，之后总是完整过滤。
13. **索引没有随 update/delete 维护**：旧值还留在索引里。→ 所有改动经过 `_add/_drop` 两个原语，索引维护只写一次。
14. **事务回滚没恢复自增计数器 / 没撤销 `create_table`**：id 被"消耗"，表还在。→ 所有状态变化（含计数器、DDL）都进 journal。
15. **持锁事务里异常没释放锁**：整个库卡死。→ `with db.transaction()`；`begin` 失败也要释放。
16. **解析器里 `a OR b AND c` 按从左到右结合**：优先级写反。→ 文法分层：`or_expr → and_expr → not_expr`。
17. **tokenizer 先匹配 `<` 再匹配 `<=`**：`<=` 被拆成两个 token。→ 长运算符放在正则的前面。

---

## 11. 自测题

1. 写出 SQL 的逻辑执行顺序，并说明为什么 `WHERE` 里不能用 `SELECT` 里的别名。
<details><summary>答案</summary>FROM → JOIN → WHERE → GROUP BY/聚合 → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT。别名是在 SELECT 这一步才产生的，WHERE 在它之前执行，那时别名还不存在；ORDER BY 在 SELECT 之后，所以可以用别名。</details>

2. 表 `t(a)` 里有 `1, 2, NULL`。下面各返回几行：`a = 1`、`a <> 1`、`NOT (a = 1)`、`a IS NULL`、`a NOT IN (1, NULL)`、`a = NULL`？
<details><summary>答案</summary>1、1（只有 2）、1（只有 2）、1（NULL 那行）、0、0。</details>

3. `ORDER BY dept ASC, salary DESC` 用 Python 怎么写，为什么顺序是"先 salary 后 dept"？
<details><summary>答案</summary>`rows.sort(key=salary_key, reverse=True)`，然后 `rows.sort(key=dept_key)`。稳定排序保证第二遍排 dept 时，dept 相同的行保持第一遍的（salary 降序）相对顺序。最主要的键最后排。</details>

4. `users(id 1..4)` 和 `orders(user_id: 1, 1, 2, 9, 4)`：`users LEFT JOIN orders ON users.id = orders.user_id` 有几行？`INNER JOIN` 呢？订单 `user_id=9` 出现吗？
<details><summary>答案</summary>LEFT：ann×2、bob×1、cat×1（右侧 NULL）、dan×1 = 5 行；INNER：4 行（没有 cat）；`user_id=9` 在两种连接里都不出现（LEFT JOIN 保留的是左表）。</details>

5. 哈希连接的 build 与 probe 各做什么，复杂度？为什么 NULL 键不能进桶？
<details><summary>答案</summary>build：扫右表，按连接键放入 `dict[键 → 行列表]`，O(|R|)；probe：扫左表，每行取 `buckets[键]`，O(|L| + 输出)。NULL = NULL 是 UNKNOWN，不应匹配；放进桶会让两边的 NULL 行错误配对。</details>

6. `LEFT JOIN o ON u.id = o.uid AND o.amount > 45` 与 `LEFT JOIN o ON u.id = o.uid WHERE o.amount > 45` 有何区别？
<details><summary>答案</summary>前者没有满足 amount>45 的用户仍然保留一行（右侧 NULL）；后者把补 NULL 的行 `NULL > 45` = UNKNOWN 过滤掉，等价于 INNER JOIN。</details>

7. 规划器为什么在用了索引之后仍然要跑完整的 WHERE？
<details><summary>答案</summary>索引只用了 WHERE 的一部分（一个合取项）；候选集可能包含不满足其它条件的行。完整过滤保证规划器不会改变结果，只改变速度，也使"有无索引结果一致"成为可测的不变量。</details>

8. 为什么 `UPDATE` 要"先算出所有新行并校验，再统一应用"？举一个逐行修改会出错的例子。
<details><summary>答案</summary>①语句原子；②`SET id = 3 - id WHERE id IN (1, 2)` 逐行改会在中间产生两个相同主键；③`SET x = x + 1 WHERE x > 5` 边扫边改可能重复处理同一行。</details>

9. undo log 回滚时，为什么要"从后往前"执行逆操作？
<details><summary>答案</summary>后面的操作可能依赖前面操作的结果（先 insert 再 delete 同一行：撤销时必须先撤销 delete——把行放回去——才能再撤销 insert——把行删掉）。逆序执行才能精确还原状态。</details>

10. 粗粒度锁下，事务内为什么需要 `RLock` 而不是 `Lock`？`begin` 持锁到 `commit` 释放，会有什么副作用？
<details><summary>答案</summary>事务内同一线程会多次调用被锁保护的方法（select / update），普通 `Lock` 会自己把自己死锁；`RLock` 可重入。副作用：事务期间其它线程被完全阻塞（包括只读），并发度为 1；长事务会拖慢所有人。MVCC 是为此而生。</details>

11. （senior）为什么不用 `(值, 主键)` 元组的有序列表做 `SortedIndex`？
<details><summary>答案</summary>同值时要比较主键，主键类型任意（甚至混合不可比）；用 `keys` / `pks` 两个平行数组按 key 二分，再在同值区间里线性找主键，避开了比较主键。</details>

12. （senior）如何让这个数据库在崩溃后恢复？
<details><summary>答案</summary>WAL / redo log：先顺序追加日志并 fsync 再应用；定期 checkpoint 快照；恢复 = 加载最近快照 + 重放其后的日志，丢弃未提交事务。当前的 undo journal 只服务于内存回滚。</details>

---

## 12. 延伸阅读（已核对）
- LeetCode 2408 Design SQL（题面原文，2026-10-16 通过 r.jina.ai 镜像核对）：https://leetcode.com/problems/design-sql/
- SQLite `SELECT` 文档，"ORDER BY" 一节：NULL 排序规则（2026-10-16 核对）：https://www.sqlite.org/lang_select.html
- Python Sorting HOW TO，"Sort Stability and Complex Sorts"：稳定性保证与 `reverse` 保持稳定（2026-10-16 核对）：https://docs.python.org/3/howto/sorting.html
- 本地验证：`code/in_memory_database.py` 的 `test_sqlite_crosscheck` 用标准库 `sqlite3`（SQLite 3.53.1）对约 1500 条随机查询 + 随机 DML 逐行对拍，是语义细节（NULL、排序、JOIN）的最终裁判。
- 相邻题：`file_search.md`（谓词组合 / 规范模式）、`occupancy_tracker.md`（小型数据模型 + SQL 版）、`pricing_billing.md`（规则引擎）；题库 [lld:design-in-memory-file-system](../../../../domains/low-level-design/drills/problems/design-in-memory-file-system.md)。
