---
id: craft-memoize-on-frozen-1-cache-needs-immutable-results
node: craft.idioms.memoize-on-frozen
type: qa
step: 1
---
## Q
**冻结与记忆化 · lru_cache 返回可变对象为什么会毒害缓存**｜写法

查询解析器把「条件字符串 → 语法树」用 `functools.lru_cache` 缓存，因为同一个条件会被反复使用。如果缓存的函数返回的是 list 或普通可变对象，一个调用者修改了自己拿到的结果，会发生什么？参数这一侧有什么要求？

## A
**要点。** 记忆化（memoization）是把函数的结果按参数存起来，下次相同参数直接返回。`lru_cache` 返回的是同一个对象，不是副本。结果可变时，一个调用者改了它，缓存里的那份也改了，之后所有调用者都拿到被改过的结果。解决办法是让结果不可变（tuple、冻结对象），共享才安全。参数一侧则要求可哈希，因为它们是缓存的键。

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def parse_bad(where: str) -> list[str]:
    return where.split(" AND ")              # 返回可变的 list

a = parse_bad("x=1 AND y=2")
a.append("HACKED")                           # 一个调用者改了「自己的」结果
print(parse_bad("x=1 AND y=2"))              # 所有后来者都拿到被改过的

@lru_cache(maxsize=None)
def parse_ok(where: str) -> tuple[str, ...]:
    return tuple(where.split(" AND "))       # 不可变：共享是安全的
b = parse_ok("x=1 AND y=2")
try:
    b.append("HACKED")
except AttributeError as e:
    print(type(e).__name__)

try:
    parse_ok(["x=1"])                        # 参数必须可哈希
except TypeError as e:
    print(e)
```

实际输出：

```
['x=1', 'y=2', 'HACKED']
AttributeError
unhashable type: 'list'
```

**为什么。** 这个 bug 的危险在于远距离：改动发生在调用者 A，症状出现在调用者 B，缓存是中间的共享状态。语法树的节点全部冻结，同一棵树可以被所有表、所有线程共享，不用为每次查询复制。

**易错。** 冻结只保证字段不能被重新绑定，不保证深层不可变：节点里放了 list，仍然可以被改。字段必须是 tuple、frozenset 或别的冻结对象。
