---
id: hi-pt-spreadsheet-engine-8-precedence
node: qb.lld.spreadsheet-engine.points
type: qa
step: 8
---
## Q
**电子表格引擎 · 递归下降与优先级**｜追问 · 出自：电子表格引擎 › 深入 6

完整表达式 `=A1+B1*2-3` 的解析器里，乘除先于加减、同级左结合是靠什么实现的？

## A
**要点。** 一个优先级一层函数：`expr`（`+ -`）调 `term`（`* /`）调 `unary`（负号）调 `atom`（数字、引用、括号）。优先级越高调用链越深，先把操作数收走。

```python
def term(self) -> Node:
    node = self.unary()
    while self.peek() in ("*", "/"):   # 同级用循环：左结合
        op = self.take()
        node = Bin(op, node, self.unary())
    return node
```
