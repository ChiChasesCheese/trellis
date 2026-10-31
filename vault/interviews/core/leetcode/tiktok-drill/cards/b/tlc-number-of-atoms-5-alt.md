---
id: tlc-number-of-atoms-5-alt
node: b.number-of-atoms
type: qa
step: 5
---
## Q
**LC 726 原子的数量**｜另一种解法

不用显式栈和正则，用递归下降（recursive descent）解析怎么写？它和栈解法比，什么时候选哪个？

## A
**思路。** 把化学式看成文法：`formula := (原子 数字? | '(' formula ')' 数字?)*`。写一个 `parse()` 函数：读到 `(` 就递归调用自己解析括号内的内容，遇到 `)` 或字符串末尾返回这一层的计数器；括号后读倍数乘进来。递归栈代替了显式栈。

```python
from collections import Counter


def count_of_atoms_rd(formula: str) -> str:
    n = len(formula)
    pos = 0

    def read_number() -> int:
        nonlocal pos
        start = pos
        while pos < n and formula[pos].isdigit():
            pos += 1
        return int(formula[start:pos] or 1)

    def parse() -> Counter[str]:           # 解析到 ')' 或字符串末尾为止
        nonlocal pos
        cnt: Counter[str] = Counter()
        while pos < n and formula[pos] != ")":
            if formula[pos] == "(":
                pos += 1
                inner = parse()
                pos += 1                   # 跳过 ')'
                mult = read_number()
                for atom, c in inner.items():
                    cnt[atom] += c * mult
            else:
                start = pos
                pos += 1
                while pos < n and formula[pos].islower():
                    pos += 1
                cnt[formula[start:pos]] += read_number()
        return cnt

    total = parse()
    return "".join(a + (str(c) if c > 1 else "") for a, c in sorted(total.items()))
```

运行：`"H2O"` → `"H2O"`，`"Mg(OH)2"` → `"H2MgO2"`，`"K4(ON(SO3)2)2"` → `"K4N2O14S4"`。

**为什么对。** `parse()` 的返回值是「从当前位置到匹配的 `)` 之前」这段的原子计数；递归调用结束时 `pos` 正好停在 `)` 上，跳过它再读倍数，与栈版「弹出这一层」完全对应。

**取舍。** 递归下降和文法一一对应，读起来最直观，扩展新语法（比如加 `.` 表示水合物）时改动小；缺点是嵌套深度受 Python 递归上限限制：长度 `1000` 的输入最多嵌套 `499` 层，刚好在默认上限 `1000` 以内，但再长就要 `sys.setrecursionlimit` 或改成显式栈。栈 + 正则版没有深度问题、代码更短，是面试里的首选；被要求「不用正则」或「按文法写」时选递归下降。
