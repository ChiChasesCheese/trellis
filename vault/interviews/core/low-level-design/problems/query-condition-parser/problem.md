# 条件解析与内存表查询（Query Condition Parser）

运营同学要在一张放在内存里的小表上写类 SQL 的筛选条件，比如 `age >= 18 AND (city = 'NYC' OR city = 'SF')`，
返回满足条件的行。条件是用户输入的字符串，来源不可信，所以不能用 `eval`。
照机考的节奏分关来做，做完一关再看下一关。

**分关要求**

- 第 1 关（约 20 分钟）：固定列的表，支持比较（`= != < <= > >=`）、`AND`、`OR`、括号；值是整数或单引号字符串。
  `AND` 比 `OR` 结合得紧；关键字不分大小写；引号里的 `AND`、括号只是普通字符。
- 第 2 关（约 15 分钟）：加 `NOT`（比 `AND` 结合得更紧）、`IN (...)`、`NOT IN (...)`、`IS NULL`、`IS NOT NULL`。
  行里的值可以是 `None`，按 SQL 的三值逻辑处理：与 NULL 比较的结果是"未知"，`select` 只保留结果为"真"的行。
- 第 3 关（约 20 分钟）：`create_index(column)` 建等值索引，`select` 在能用索引时只检查候选行，
  结果必须与不建索引时完全一样，顺序仍是插入顺序。
- 第 4 关（选做）：文档表 `Table()`，不规定列；字段用点号路径（`address.city`），缺失的字段当作 NULL。

**接口**

```python
class QueryError(ValueError): ...      # 所有失败路径只抛这一种

class Table:
    def __init__(self, columns: Sequence[str] | None = None) -> None
    def insert(self, row: Mapping[str, Any]) -> None
    def select(self, where: str = "", columns: Sequence[str] | None = None) -> list[dict[str, Any]]
    def create_index(self, column: str) -> None                     # 第 3 关
    last_scan_count: int                                            # 第 3 关：最近一次 select 把条件算了多少行
```

- `insert`：存的是副本；固定列的表要求行的列与建表时完全一致，否则抛 `QueryError`。
- `select`：返回副本，按插入顺序；`where` 为空（或全是空白）返回所有行；`columns` 为 `None` 返回整行，否则只返回这些列；
  语法错误、未知列、整数与字符串做大小比较，都抛 `QueryError`。错误只取决于条件和表结构：即使表是空的，`b = 1` 也要报"未知列"。
- 值：整数（可以是负数）和单引号字符串（不支持转义）。`=`、`!=` 在类型不同时按"不相等"算，不报错。
- 第 3 关的 `last_scan_count`：不使用索引（包括没有条件）时等于行数；使用索引时等于候选行数。`create_index` 对未知列抛 `QueryError`，重复调用无副作用。

例子：

```python
t = Table(["id", "name", "age", "city"])
t.insert({"id": 1, "name": "Ann", "age": 30, "city": "NYC"})
t.insert({"id": 2, "name": "Bob", "age": 17, "city": "SF"})
t.insert({"id": 3, "name": "Cat", "age": 25, "city": "NYC"})
t.select("city = 'SF' OR age > 20 AND city = 'NYC'", columns=["id"])   # [{"id": 1}, {"id": 2}, {"id": 3}]
t.select("(city = 'SF' OR age > 20) AND city = 'NYC'", columns=["id"]) # [{"id": 1}, {"id": 3}]
t.select("age >")                                                      # 抛 QueryError
```

第 2 关：若某行 `age` 是 `None`，则 `age >= 18` 和 `NOT age >= 18` 都不返回它；`age IS NULL` 返回它。

**评分点**

- 词法、语法、求值分开：优先级靠"每个优先级一个解析函数"表达，不靠 `split` 或正则硬切，也不用 `eval`。
- 加 `NOT`、`IN`、`IS NULL` 只新增节点和一层解析函数，第 1 关写好的 `AND` / `OR` 解析不用重写。
- 三值逻辑：能说出并写对 "未知 AND 假 = 假""未知 OR 真 = 真""NOT 未知 = 未知"，并解释为什么 `NOT age >= 18` 不能带出 NULL 行。
- 索引只提供"候选超集"，最后一定复查；能说清 `AND` 用一边就够、`OR` 必须两边都能用索引，`NOT` 和范围比较不能用。
- 错误处理：每种坏输入都是明确的 `QueryError`，不是 `IndexError`、`KeyError` 或死循环；错误不依赖表里的数据。
- 返回副本，不把内部的行对象交出去；索引和行在同一个方法里更新。
- 能口述：范围查询用有序结构（`bisect`、B+ 树）、`LIKE`、条件字符串到语法树的缓存、并发读写。
