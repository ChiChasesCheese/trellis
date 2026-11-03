---
id: hi-pt-tt-query-condition-parser-4-precedence
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 4
---
## Q
**条件解析与内存表查询 · 递归下降怎么表达优先级**｜出自：条件解析与内存表查询 › 深入 1

`a = 1 OR b = 2 AND NOT c = 3` 要先结合谁？递归下降的代码怎么做到？

## A
**要点。** `NOT` > `AND` > `OR`。`or_expr` 调 `and_expr`，`and_expr` 调 `not_expr`：优先级越高的函数越深，先把操作数收走。

**括号。** 在最深一层遇到 `(` 就回到 `or_expr`，优先级重新开始。

```python
def and_expr(self) -> Any:
    node = self.not_expr()
    while self.accept("kw", "AND"):  # 循环保证同级从左到右
        node = And(node, self.not_expr())
    return node
```
