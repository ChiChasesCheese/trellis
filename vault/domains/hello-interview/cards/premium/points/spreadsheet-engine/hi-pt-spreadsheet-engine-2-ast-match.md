---
id: hi-pt-spreadsheet-engine-2-ast-match
node: qb.lld.spreadsheet-engine.points
type: qa
step: 2
---
## Q
**电子表格引擎 · 语法树与 match**｜必会 · 出自：电子表格引擎 › 深入 1

公式要存成什么？语法树的节点用什么 Python 写法表达，求值和找依赖又怎么按节点类型分派？

## A
**存什么。** 存解析好的语法树，不存字符串：错误在 `set` 当场报，`get` 不再重新解析。

**写法。** 每种节点一个 `@dataclass(frozen=True, slots=True)`，不可变所以可比较、可哈希；用 `match` 加类模式分派，字段直接拆出来。

```python
match node:
    case Ref(cell):
        return {cell}
    case Bin(_, left, right):
        return refs_of(left) | refs_of(right)
```
**对比。** `("bin", "+", l, r)` 元组靠下标取值，改字段顺序就悄悄出错。
