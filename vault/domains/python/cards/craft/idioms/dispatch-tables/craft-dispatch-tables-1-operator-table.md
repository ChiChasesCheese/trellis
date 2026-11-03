---
id: craft-dispatch-tables-1-operator-table
node: craft.idioms.dispatch-tables
type: qa
step: 1
---
## Q
**分派表 · 为什么比较运算符写成 dict 而不是 if 链**｜写法

查询条件解析器要支持 `=`、`!=`、`<`、`<=`、`>`、`>=`。最直接的写法是一串 `if op == "=": ... elif op == "<": ...`。把运算符映射到函数的 dict 改变了什么？怎样让它在被别处修改时也安全？

## A
**要点。** 分派表（dispatch table）是一个把「键」映射到「要做的事」的 dict。每个分支的差别只有「用哪个函数」，把这一点抽成数据，求值代码就只剩一行：查表、调用。表本身也成了文档：支持哪些运算符，看键就知道。未知运算符是一个 `KeyError`，在一个地方转换成清楚的错误。

```python
import operator
from types import MappingProxyType

_OPS = MappingProxyType({"=": operator.eq, "!=": operator.ne, "<": operator.lt,
                         "<=": operator.le, ">": operator.gt, ">=": operator.ge})

def compare(op: str, a, b) -> bool:
    try:
        fn = _OPS[op]
    except KeyError:
        raise ValueError(f"unknown op {op!r}") from None
    return fn(a, b)

rows = [{"age": 17}, {"age": 18}, {"age": 30}]
print([r["age"] for r in rows if compare(">=", r["age"], 18)])
print(sorted(_OPS))                    # 支持哪些运算符：表本身就是答案
try:
    _OPS["=="] = operator.eq
except TypeError as e:
    print("TypeError:", e)
try:
    compare("~", 1, 2)
except ValueError as e:
    print(e)
```

实际输出：

```
[18, 30]
['!=', '<', '<=', '=', '>', '>=']
TypeError: 'mappingproxy' object does not support item assignment
unknown op '~'
```

**为什么。** `operator.eq` 这类现成函数比 `lambda a, b: a == b` 更省，也能在日志里显示名字。`MappingProxyType` 让模块级的表只读：别的代码不能偷偷加一个运算符而改变全局行为。

**易错。** 表适合「每个分支只是选一个函数」。如果分支之间要共享局部变量、有不同的参数、或者要按顺序短路，if 链和 `match` 更直白，不要硬塞进表里。
