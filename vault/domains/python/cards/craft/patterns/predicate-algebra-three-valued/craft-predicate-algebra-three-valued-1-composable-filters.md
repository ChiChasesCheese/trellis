---
id: craft-predicate-algebra-three-valued-1-composable-filters
node: craft.patterns.predicate-algebra-three-valued
type: qa
step: 1
---
## Q
**谓词代数与三值逻辑 · 用户任意组合筛选条件，怎么设计才不会写出组合爆炸的函数**｜模式

实现一个 `find` 命令：按类型、文件名通配、大小、是否取反任意组合，比如「是文件，且名字以 .py 结尾，且大小至少 1000，且名字不以 test_ 开头」。每种组合写一个函数不可能。怎样让条件像积木一样拼，并保证拼出来的条件可复用、可共享给多个线程？

## A
**要点。** 把每个条件做成一个**谓词对象**（predicate），只会回答 `matches(entry) -> bool`；再提供三个组合子（combinator）：`And`、`Or`、`Not`，它们自己也是谓词，包着别的谓词。用运算符重载 `&`、`|`、`~` 让拼接读起来像条件本身。每个谓词都是 frozen 的值，组合返回新对象，不改原对象，所以同一个条件可以被多处复用、跨线程共享，也能直接打印出结构。

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from fnmatch import fnmatchcase

@dataclass(frozen=True)
class Entry: path: str; kind: str; size: int

class Filter(ABC):
    @abstractmethod
    def matches(self, e): ...
    def __and__(self, o): return And(self, o)      # 组合返回新对象，不改原对象
    def __or__(self, o): return Or(self, o)
    def __invert__(self): return Not(self)

@dataclass(frozen=True)
class And(Filter):
    l: Filter; r: Filter
    def matches(self, e): return self.l.matches(e) and self.r.matches(e)   # 短路：便宜的放左边
@dataclass(frozen=True)
class Or(Filter):
    l: Filter; r: Filter
    def matches(self, e): return self.l.matches(e) or self.r.matches(e)
@dataclass(frozen=True)
class Not(Filter):
    inner: Filter
    def matches(self, e): return not self.inner.matches(e)
@dataclass(frozen=True)
class NameGlob(Filter):
    pattern: str
    def matches(self, e): return fnmatchcase(e.path.rsplit("/", 1)[-1], self.pattern)
@dataclass(frozen=True)
class Kind(Filter):
    kind: str
    def matches(self, e): return e.kind == self.kind
@dataclass(frozen=True)
class MinSize(Filter):
    n: int
    def matches(self, e): return e.size >= self.n

entries = [Entry("/a/x.py", "file", 10), Entry("/a/y.py", "file", 5000), Entry("/a/z.txt", "file", 9000),
           Entry("/a/build", "dir", 0), Entry("/a/test_x.py", "file", 7000)]
# find -type f -name '*.py' -size +1000 ! -name 'test_*'
big_py = Kind("file") & NameGlob("*.py") & MinSize(1000) & ~NameGlob("test_*")
print([e.path for e in entries if big_py.matches(e)])
print(big_py)
```

```
['/a/y.py']
And(l=And(l=And(l=Kind(kind='file'), r=NameGlob(pattern='*.py')), r=MinSize(n=1000)), r=Not(inner=NameGlob(pattern='test_*')))
```

**为什么。** 组合子让"条件的数量"从 N 个函数变成"N 个原子条件 + 3 个组合子"，新增一个原子条件（按修改时间）自动能和所有已有条件组合。`&` 的短路求值意味着顺序影响性能（便宜的条件放左边，比如先判类型再匹配名字），但不影响结果。

**代价。** 运算符重载有优先级陷阱：Python 里 `&` 比 `==` 和 `and` 优先级高，混着写比较时要加括号；`~` 对谓词对象合法，对布尔值意味着按位取反（`~True == -2`），误用的 bug 很难察觉。基类提供 `&`、`|`、`~`，只能是抽象基类而不是 Protocol（Protocol 的实现者不必继承它，就拿不到基类里写好的 `&`、`|`、`~`）。

**对照。** 这就是 Specification 模式；Elasticsearch 的 bool 查询、权限系统里的策略条件都是同一种结构。
