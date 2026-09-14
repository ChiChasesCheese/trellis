---
id: cc-input-gram-precedence-one-function-per-level
node: input.grammar
type: qa
---
## Q
`a OR b AND c` must mean `a OR (b AND c)`. How does a hand-written recursive-descent parser encode that without a precedence table?

## A
**One function per precedence level, the loosest at the top, each calling the next tighter one.**

```python
def parse_expr(t):                       # OR level
    node = parse_and(t)
    while t.peek() == "OR":
        t.next(); node = ("or", node, parse_and(t))
    return node

def parse_and(t):                        # AND level
    node = parse_primary(t)
    while t.peek() == "AND":
        t.next(); node = ("and", node, parse_primary(t))
    return node
```

Tighter binding lives *deeper* in the call stack, so `AND` collects its operands before `OR` ever sees them. Adding `NOT` is one more level; the grammar in the statement usually already lists them in order.

## Q zh
`a OR b AND c` 必须解释成 `a OR (b AND c)`。手写的递归下降解析器如何在不用优先级表的情况下编码这一点？

## A zh
**每个优先级一个函数，最松的在最上层，每层调用更紧的下一层。**

```python
def parse_expr(t):                       # OR level
    node = parse_and(t)
    while t.peek() == "OR":
        t.next(); node = ("or", node, parse_and(t))
    return node

def parse_and(t):                        # AND level
    node = parse_primary(t)
    while t.peek() == "AND":
        t.next(); node = ("and", node, parse_primary(t))
    return node
```

结合更紧的运算符位于调用栈**更深处**，于是 `AND` 会在 `OR` 看到它的操作数之前先把它们收走。加一个 `NOT` 就是再加一层；题面给出的文法通常已经按顺序列好了。
