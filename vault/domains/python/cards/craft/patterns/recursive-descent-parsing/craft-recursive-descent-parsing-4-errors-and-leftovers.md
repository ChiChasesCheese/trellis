---
id: craft-recursive-descent-parsing-4-errors-and-leftovers
node: craft.patterns.recursive-descent-parsing
type: qa
step: 4
---
## Q
**递归下降解析 · 解析函数返回后，为什么还要检查「token 是否吃完」**｜模式

`parse_raw("=1 + 2 )")` 里 `expr()` 成功返回了 `1 + 2`，多出来的右括号没人理。这是个合法输入吗？应该在哪里、用什么方式让它失败？再说，语法错误应该在写入时抛，还是在读取时抛？

## A
**要点。** 递归下降的入口只保证「从头开始能读出一个完整的表达式」，不保证输入到此为止。顶层必须加一句「剩下的 token 为空」，否则 `1 + 2 )`、`1 2` 这样的输入会静默地只取前半段，用户的笔误被吞掉，结果看上去还像对的。

```python
class InvalidFormulaError(ValueError): ...

class Parser:
    def __init__(self, toks): self.t, self.i = toks, 0
    def peek(self): return self.t[self.i] if self.i < len(self.t) else None
    def take(self): self.i += 1; return self.t[self.i - 1]
    def expr(self):
        node = int(self.take())
        while self.peek() == "+":
            self.take(); node = ("+", node, int(self.take()))
        return node

def ev(n): return n if isinstance(n, int) else ev(n[1]) + ev(n[2])

def parse_raw(raw):
    p = Parser(raw.split())
    node = p.expr()
    if p.peek() is not None:                       # 没吃完 = 语法错误
        raise InvalidFormulaError(f"trailing input at {p.peek()!r}")
    return node

p = Parser("1 + 2 )".split())                      # 故意多一个右括号，且不做上面的检查
print("只调 expr():", ev(p.expr()), "剩下:", p.peek(), "<- 静默忽略了 )")
try: parse_raw("1 + 2 )")
except InvalidFormulaError as e: print("加上检查:", e)
```

不加检查的输出：

```
只调 expr(): 3 剩下: ) <- 静默忽略了 )
加上检查: trailing input at ')'
```

**为什么。** 错误要在 `set` 时当场抛，而且发生在任何状态修改之前：先 `parse_raw`，成功了才去查环、改依赖表。这样，一次失败的写入留不下半个公式。`take()` 在输入提前耗尽时也抛同样的异常类型，调用方只需要 catch 一个。

**区分两类错误。** 语法错误（括号不配、多余字符）只取决于文本，在解析阶段抛；类型错误和未知列只取决于文本加表结构，在解析时对照 schema 检查，或在求值时抛。设计目标是：错误只取决于条件和表结构，而不取决于表里恰好有没有数据，否则同一个查询在空表上成功、在有数据的表上失败。

**易错。** 报错信息带上当前 token 和位置（`got {tok!r}`），比一句「语法错误」省掉大量排查时间。
