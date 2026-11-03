---
id: craft-predicate-algebra-three-valued-4-refs-static-check
node: craft.patterns.predicate-algebra-three-valued
type: qa
step: 4
---
## Q
**谓词代数与三值逻辑 · 查询里写错了列名，为什么应该在执行前、对着表结构检查**｜模式

`WHERE age > 30 AND salray > 100`（手误，应为 salary）。如果谓词是在每一行上才去读 `row["salray"]`，空表上这个查询成功返回空结果，有数据的表上抛 `KeyError`。怎样让错误只取决于「查询和表结构」，不取决于「表里恰好有没有数据」？

## A
**要点。** 每个谓词对象提供一个只读属性 `refs`：它引用的所有列名的集合；组合子的 `refs` 是子谓词 `refs` 的并集。执行之前，用一个函数把 `where.refs` 与表的列集合对照一次，未知列当场抛 `SchemaError`。这个检查不碰任何一行，所以结果与数据无关。

```python
from dataclasses import dataclass
from typing import Any

class SchemaError(ValueError): ...

@dataclass(frozen=True)
class Col: name: str

@dataclass(frozen=True)
class Cmp:
    left: Any; op: str; right: Any
    @property
    def refs(self) -> frozenset[str]:
        return frozenset(x.name for x in (self.left, self.right) if isinstance(x, Col))

@dataclass(frozen=True)
class And:
    parts: tuple
    @property
    def refs(self) -> frozenset[str]:
        return frozenset().union(*(p.refs for p in self.parts))   # 子谓词引用的列的并集

def check_refs(refs, columns):
    for name in sorted(refs):
        if name not in columns: raise SchemaError(f"未知列: {name}")

where = And((Cmp(Col("age"), ">", 30), Cmp(Col("salray"), ">", 100)))      # 手误：salray
print("谓词引用的列:", sorted(where.refs))
for table_rows in ([], [{"age": 1, "salary": 1}]):
    try:
        check_refs(where.refs, {"age", "salary"})        # 执行前统一校验，不看有没有数据
    except SchemaError as e:
        print(f"表里 {len(table_rows)} 行 ->", e)
```

```
谓词引用的列: ['age', 'salray']
表里 0 行 -> 未知列: salray
表里 1 行 -> 未知列: salray
```

**为什么。** 谓词是**数据**（frozen 的树），不是闭包，所以能被遍历：不执行它也能问"你引用了哪些列"。如果谓词是 `lambda row: row["salray"] > 100`，只能在运行时发现错误。把谓词做成可检查的结构，同样的做法还能用来做：选择索引、判断能否下推到存储层、打印查询计划。

**代价。** 每加一种新谓词，都要实现 `refs`（漏了一种，那种谓词的列名拼写错误就查不出来），所以它是抽象方法，不实现就没法实例化。

**对照。** 编译器的名字解析、数据库的绑定阶段（binder）、ORM 的字段校验：都是先对结构检查，再执行。错误越早、越确定地出现，调试成本越低。
