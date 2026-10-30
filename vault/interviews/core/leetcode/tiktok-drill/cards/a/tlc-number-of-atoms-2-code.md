---
id: tlc-number-of-atoms-2-code
node: a.number-of-atoms
type: qa
step: 2
---
## Q
**LC 726 原子的数量**｜写出 Python 实现

化学式字符串 `formula`（长度 `1` 到 `1000`，由字母、数字、`(`、`)` 组成，保证有效）：原子是大写字母加若干小写字母，后面可跟数量；括号后可跟倍数。返回按原子名字典序排列的结果，数量为 `1` 时不写数字。

## A
**思路。** 正则把字符串切成三类 token：原子（含可选数字）、`(`、`)`（含可选倍数）。栈中每层是一个 `Counter`：原子累加到栈顶，`(` 压入空计数器，`)` 弹出并乘倍数并入新的栈顶。最后对栈底按名字排序拼接。

```python
import re
from collections import Counter

TOKEN = re.compile(r"([A-Z][a-z]*)(\d*)|(\()|\)(\d*)")


def count_of_atoms(formula: str) -> str:
    stack: list[Counter[str]] = [Counter()]    # 栈顶是当前括号层的计数
    for m in TOKEN.finditer(formula):
        name, num, left, close_num = m.groups()
        if name:                                # 原子：加到当前层
            stack[-1][name] += int(num or 1)
        elif left:                              # '(': 开一层新计数
            stack.append(Counter())
        else:                                   # ')': 弹出这一层，乘倍数后并回上一层
            inner = stack.pop()
            mult = int(close_num or 1)
            for atom, cnt in inner.items():
                stack[-1][atom] += cnt * mult
    return "".join(a + (str(c) if c > 1 else "") for a, c in sorted(stack[0].items()))
```

运行：`"H2O"` → `"H2O"`，`"Mg(OH)2"` → `"H2MgO2"`，`"K4(ON(SO3)2)2"` → `"K4N2O14S4"`，`"(H2O)10"` → `"H20O10"`，`"((H))"` → `"H"`，`"Uuo(U)2"` → `"U2Uuo"`。

**复杂度。** 时间 `O(n · k)`：每个 token 摊销常数，每个 `)` 遍历一层的原子种类；`k` 是原子种类数。空间 `O(n)`。

**写法要点。** 一个带三个分支的正则加 `m.groups()` 一次拆出四个捕获组：没参与匹配的组是 `None`，参与但为空的 `(\d*)` 是 `""`，所以统一用 `int(x or 1)` 处理；`Counter` 对缺失的键读出 `0`，`+=` 不需要先判断；`sorted(counter.items())` 按键（原子名）字典序排序；`"U"` 与 `"Uuo"` 比较时较短的前缀在前。
