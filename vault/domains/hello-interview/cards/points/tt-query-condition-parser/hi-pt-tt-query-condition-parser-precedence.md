---
id: hi-pt-tt-query-condition-parser-precedence
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 4
---
## Q
**条件解析与内存表查询 · 递归下降怎么表达优先级**｜必会 · 出自：条件解析与内存表查询 › 核心实现 3

`a = 1 OR b = 2 AND c = 3` 先结合谁？代码怎么做到？

## A
**要点。** `AND` 先结合。`or_expr` 调 `and_expr`，`and_expr` 调 `primary`：优先级越高函数越深，先把操作数收走。

```python
def and_expr(self) -> Any:
    node = self.primary()
    while self.peek().upper() == "AND":  # 循环：同级从左到右
        self.next()
        node = And(node, self.primary())
    return node
```
