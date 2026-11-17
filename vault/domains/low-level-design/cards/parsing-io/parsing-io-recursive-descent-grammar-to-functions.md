---
id: parsing-io-recursive-descent-grammar-to-functions
node: parsing-io.recursive-descent
type: qa
step: 1
---
## Q
要计算 `2+3*(4-1)` 这样的表达式，递归下降解析器怎样把语法规则变成代码？为什么乘除一定比加减「深」一层？

## A
**一条规则一个函数，优先级就是调用的深度**

- **文法**：`expr = term (("+"|"-") term)*`，`term = factor (("*"|"/") factor)*`，`factor = 数字 | "(" expr ")"`；
- **映射**：每个规则一个函数，规则里的「引用另一条规则」就是函数调用，`*` 对应 `while` 循环；
- **优先级**：`expr` 调用 `term`，`term` 才调用 `factor`；乘除先在最里层算完，才轮到加减，所以 `2+3*4` 是 `2+(3*4)`；
- **括号**：`factor` 里碰到 `(` 就回到最外层的 `expr`，递归自然实现了嵌套；
- **只看一个 token 就能决定走哪条路**：这是递归下降的前提；文法要写成这种形式。

```python
import re, operator
OPS = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
def evaluate(src: str):
    toks = re.findall(r"\d+|[-+*/()]", src)[::-1]            # 栈顶在末尾
    def level(ops, below):                                    # below (op below)*
        v = below()
        while toks and toks[-1] in ops: v = OPS[toks.pop()](v, below())
        return v
    def factor():
        t = toks.pop()
        if t == "(": v = expr(); toks.pop(); return v         # 吃掉 )
        return int(t)
    term, expr = (lambda: level("*/", factor)), (lambda: level("+-", term))
    return expr()
print(evaluate("2+3*(4-1)"))                                  # 11
```

<details class="pt"><summary>延伸</summary>

示例没有检查括号配对和多余 token（`toks.pop()` 对不上会抛 `IndexError`）；真实解析器用 `expect(")")`，遇错时抛带位置的解析错误，并在函数返回后检查 token 是否已用完。

</details>

**知识点：**递归下降解析（Recursive Descent）
