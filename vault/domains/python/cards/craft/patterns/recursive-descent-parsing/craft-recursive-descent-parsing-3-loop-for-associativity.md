---
id: craft-recursive-descent-parsing-3-loop-for-associativity
node: craft.patterns.recursive-descent-parsing
type: qa
step: 3
---
## Q
**递归下降解析 · 同级运算符用 while 循环，而不是再递归**｜模式

`expr` 的写法有两种：`while` 循环不断吞掉后面的 `+ term`；或者读完左边后直接递归调用自己处理右边。对 `10 - 3 - 2`，两种写法分别得到什么？为什么说「循环」才是对的？

## A
**要点。** 减法和除法是左结合（left-associative）的：`10-3-2` 要读成 `(10-3)-2 = 5`。循环版每吞一个运算符就把「到目前为止的树」当作新节点的左孩子，天然左结合。递归版把剩下的整段当作右孩子，得到 `10-(3-2) = 9`，对加法和乘法碰巧不影响结果，所以测试里不容易发现，换成减法才露馅。

```python
class Parser:
    def __init__(self, toks): self.t, self.i = toks, 0
    def peek(self): return self.t[self.i] if self.i < len(self.t) else None
    def take(self): self.i += 1; return self.t[self.i - 1]
    def term(self): return int(self.take())          # 为了聚焦，操作数只是整数

    def expr(self):                                   # 对：循环
        node = self.term()
        while self.peek() in ("+", "-"):
            node = (self.take(), node, self.term())   # 旧树成为新节点的左孩子
        return node

class RightRec(Parser):
    def expr(self):                                   # 错：右递归
        left = self.term()
        if self.peek() in ("+", "-"):
            return (self.take(), left, self.expr())   # 剩下的一整串成为右孩子
        return left

def ev(n):
    if isinstance(n, int): return n
    a, b = ev(n[1]), ev(n[2])
    return a + b if n[0] == "+" else a - b

for P in (Parser, RightRec):
    t = P("10 - 3 - 2".split()).expr()
    print(P.__name__, t, "=", ev(t))
```

实际输出：

```
Parser ('-', ('-', 10, 3), 2) = 5
RightRec ('-', 10, ('-', 3, 2)) = 9
```

**为什么。** 想要右结合（幂运算 `2^3^2 = 2^(3^2)`）时，则要反过来，右递归才是对的：`pow := atom ('^' pow)?`。所以结合性不是风格选择，而是文法的一部分，写方法的时候必须决定。

**代价。** 循环版里节点是在循环中不断重新赋值的，不适合直接把「正在构造的节点」暴露给错误恢复逻辑；解析器如果要在出错时给出更精确的位置，要在循环体内记录起点。

**易错。** 比较运算符（`a < b < c`）在多数语言里不能链式，这时用 `if` 而不是 `while`，只吞一次。
