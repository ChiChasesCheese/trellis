---
id: craft-match-structural-5-across-problems
node: craft.idioms.match-structural
type: qa
step: 5
---
## Q
**结构化模式匹配 · 表格、化简、查询优化里按形状分派的同一种写法**｜写法

表格引擎的求值、图像流水线的化简、查询解析器的选索引，都是对一棵数据结构按形状分情况处理。它们的 `match` 哪里一样，哪里不同？

## A
**要点。** 一样：被匹配的是一族冻结的数据类（同一个联合类型的几种形状），每个 `case` 写出一种形状并取出需要的字段，最后一个分支兜底。不同：**匹配几个值、要不要字面量、要不要守卫、兜底分支放什么**。

```python
# spreadsheet-engine.evaluate：一个值，位置字段，递归求值
match node:
    case Num(value):            return value
    case Neg(operand):          return -evaluate(operand, read)
    case Bin(op, left, right):  ...

# image-transform-pipeline._merge：两个值，守卫写在规则旁边
match a, b:
    case Flip(h1), Flip(h2) if h1 == h2:  return None
    case Brighten(d1), Brighten(d2) if d1 * d2 >= 0:
        return Brighten(d1 + d2)
    case _:                               return _NO_MERGE

# query-condition-parser._candidates：关键字模式 + 字面量 + 守卫
match node:
    case _Cmp(field=f, op="=", value=v) if f in self._index:
        return set(self._index[f].get(v, ()))
    case _And(left=l, right=r):  ...
    case _:                      return None   # 帮不上就退回全表扫描
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

兜底分支的含义因场景而异：化简里「合并不了」是正常结果，所以用 `_NO_MERGE` 哨兵；查询里「索引帮不上」也是正常的，返回 `None` 表示全表扫描。表格求值的兜底却不一样（见「穷尽性」）：那里应该是不可能到达的分支。

**见于。** spreadsheet-engine、image-transform-pipeline、query-condition-parser、inventory-management、api-circuit-breaker、credit-token-balance。

**信号。** 一个数据结构有几种形状（语法树、事件、命令、状态），代码里出现一串 `isinstance`，或者 `if x.kind == ...` 后面各自取不同的字段。
