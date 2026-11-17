---
id: parsing-io-recursive-descent-power
node: parsing-io.recursive-descent
type: qa
step: 3
---
## Q
给表达式加乘方 `**` 和一元负号。要让 `2**3**2` 等于 512、`-2**2` 等于 -4（与 Python 一致），文法和函数该怎么写？

## A
**每个优先级一层，右结合的运算符递归自己所在的层**

- **文法**：`unary = "-" unary | power`；`power = 数字 ["**" unary]`；
- **`**` 比一元负号绑得紧**：`-2**2` 先解析 `unary`，看到 `-`，把后面整个 `2**2` 当作操作数再取负，得到 -4；
- **右结合**：`power` 在 `**` 之后递归调用 `unary`（最终回到 `power`），所以 `2**3**2` 是 `2**(3**2)`；
- **右边允许负号**：`2**-1` 合法，因为 `**` 的右操作数走的是 `unary`；
- **加一个运算符的流程**：决定它的优先级放在哪两层之间，新建一层函数，上一层改为调用它。

```python
import re

def calc(src: str):
    toks = re.findall(r"\d+|\*\*|[-+*/()]", src)[::-1]
    def unary():
        if toks[-1] == "-": toks.pop(); return -unary()
        return power()
    def power():
        base = int(toks.pop())
        if toks and toks[-1] == "**": toks.pop(); return base ** unary()    # 右结合
        return base
    return unary()

print(calc("2**3**2"), calc("-2**2"), calc("2**-1"))      # 512 -4 0.5
```

**知识点：**递归下降解析（Recursive Descent）
