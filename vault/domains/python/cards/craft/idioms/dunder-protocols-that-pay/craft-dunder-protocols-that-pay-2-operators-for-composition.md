---
id: craft-dunder-protocols-that-pay-2-operators-for-composition
node: craft.idioms.dunder-protocols-that-pay
type: qa
step: 2
---
## Q
**特殊方法 · 过滤器为什么重载 & | ~，而不是 and_() 方法**｜写法

文件查找工具要把条件组合起来：「小的日志文件或临时文件」。条件对象可以提供 `.and_()`、`.or_()` 方法，也可以重载 `&`、`|`、`~`。后者读起来像查询，但它的优先级和 Python 的 `and` / `or` 并不一致。什么时候值得这样做，要注意什么？

## A
**要点。** 特殊方法让自定义类型获得内置语法的外观。组合运算符返回新对象，不改原对象，条件是不可变的，可以复用、跨线程共享。Python 的 `and`、`or`、`not` 不能重载（它们只返回其中一个操作数，并且短路），所以组合只能借用位运算符 `&`、`|`、`~`。

```python
from dataclasses import dataclass

class Filter:
    def matches(self, e: dict) -> bool: raise NotImplementedError
    def __and__(self, o: "Filter") -> "Filter": return And(self, o)
    def __or__(self, o: "Filter") -> "Filter": return Or(self, o)
    def __invert__(self) -> "Filter": return Not(self)

@dataclass(frozen=True)
class Ext(Filter):
    ext: str
    def matches(self, e): return e["name"].endswith(self.ext)
@dataclass(frozen=True)
class Big(Filter):
    size: int
    def matches(self, e): return e["size"] > self.size
@dataclass(frozen=True)
class And(Filter):
    l: Filter; r: Filter
    def matches(self, e): return self.l.matches(e) and self.r.matches(e)
@dataclass(frozen=True)
class Or(Filter):
    l: Filter; r: Filter
    def matches(self, e): return self.l.matches(e) or self.r.matches(e)
@dataclass(frozen=True)
class Not(Filter):
    f: Filter
    def matches(self, e): return not self.f.matches(e)

log, tmp, big = Ext(".log"), Ext(".tmp"), Big(100)
q = (log | tmp) & ~big                    # 小的日志或临时文件
files = [{"name": "a.log", "size": 10}, {"name": "b.log", "size": 500},
         {"name": "c.tmp", "size": 5}, {"name": "d.py", "size": 1}]
print([f["name"] for f in files if q.matches(f)])
mixed = log | tmp & big
print(type(mixed).__name__, type(mixed.r).__name__)   # & 比 | 先算
print((log and tmp) is tmp)                           # 内置 and：只返回其中一个对象
```

实际输出：

```
['a.log', 'c.tmp']
Or And
True
```

**易错。** 运算符优先级是 Python 的而不是你的：`&` 比 `|` 先算，与布尔代数的习惯一致，但 `a & b == c` 会先比较 `b == c`。写错了不会报错而是静默改变含义，所以复杂条件要加括号；`log and tmp` 不报错也不组合，只返回 `tmp`，是常见的写错方式。

**信号。** 重载运算符只用于满足代数性质（结合、可交换、结果同类型）的组合操作。如果操作不是显然的（`+` 表示什么？），写命名方法。
