---
id: craft-recursive-descent-parsing-1-precedence-is-call-depth
node: craft.patterns.recursive-descent-parsing
type: qa
step: 1
---
## Q
**递归下降解析 · 优先级为什么就是方法的调用层次**｜模式

电子表格要支持公式 `=6-4/2` 和 `=2*(5+5*2)/3`。从左到右依次算会得到 `(6-4)/2 = 1`，而正确答案是 4。要让「乘除比加减紧、括号最优先」成立，又不写一张优先级表，代码该怎么组织？

## A
**要点。** 递归下降（recursive descent）：文法里每个优先级写成一个方法，低优先级的方法调用高优先级的方法。`expr` 管 `+ -`，它的操作数交给 `term`；`term` 管 `* /`，操作数交给最底层的 `atom`（数字和括号）；负号再占一层 `unary`，夹在 `term` 与 `atom` 之间。谁被调得更深，谁就结合得更紧。括号里重新调用 `expr`，所以优先级从最低重新开始。

```python
import re

tokenize = lambda s: re.findall(r"\d+|[-+*/()]", s)

class Parser:                                     # expr > term > atom：被调得越深，结合得越紧
    def __init__(self, toks): self.t, self.i = toks, 0
    def peek(self): return self.t[self.i] if self.i < len(self.t) else None
    def take(self): self.i += 1; return self.t[self.i - 1]

    def expr(self):
        node = self.term()                        # 操作数交给更紧的一层
        while self.peek() in ("+", "-"):          # 同级运算符用循环
            node = (self.take(), node, self.term())
        return node
    def term(self):                               # 与 expr 同形，运算符换成 * /
        node = self.atom()
        while self.peek() in ("*", "/"):
            node = (self.take(), node, self.atom())
        return node
    def atom(self):
        tok = self.take()
        if tok.isdigit(): return int(tok)
        node = self.expr()                        # 只剩 "("：括号里回到最低优先级
        self.take()                               # 吃掉 ")"
        return node

def ev(n):
    if isinstance(n, int): return n
    a, b = ev(n[1]), ev(n[2])
    return {"+": a + b, "-": a - b, "*": a * b, "/": a / b}[n[0]]

for src in ("6 - 4 / 2", "2 * (5 + 5 * 2) / 3"):
    tree = Parser(tokenize(src)).expr()
    print(tree, "=", ev(tree))
print("6 - 4 / 2 从左到右硬算:", (6 - 4) / 2)
```

实际输出：

```
('-', 6, ('/', 4, 2)) = 4.0
('/', ('*', 2, ('+', 5, ('*', 5, 2))), 3) = 10.0
6 - 4 / 2 从左到右硬算: 1.0
```

**为什么。** 解析的产物是语法树（AST，abstract syntax tree），树的形状已经编码了优先级，求值只要后序遍历。用 `eval()` 或「先找最低优先级运算符再切开」的写法，要么不安全，要么每增加一级就多一个特例。

**代价。** 每多一个优先级就多一个方法（加一个幂运算 `^` 就在 `term` 和 `atom` 之间加一层），但每层都是同一个形状的 5 行，改动是局部的。
