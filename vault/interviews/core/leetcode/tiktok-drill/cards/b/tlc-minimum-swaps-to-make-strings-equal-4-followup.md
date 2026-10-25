---
id: tlc-minimum-swaps-to-make-strings-equal-4-followup
node: b.minimum-swaps-to-make-strings-equal
type: qa
step: 4
---
## Q
**LC 1247 交换字符使得字符串相同**｜追问

面试官接着问：（1）允许交换同一个字符串内部的两个字符，答案怎么变？（2）要输出具体的交换序列？（3）用标准库把统计写短？分别怎么改。

## A
1. **允许同串内交换**：一个 `xy` 位置 `i` 和一个 `yx` 位置 `j`，在 `s1` 内部交换 `s1[i]` 与 `s1[j]` 即可一次修好，所以所有不匹配位置两两配对，答案是 `(xy + yx) // 2`（可行时总数为偶数）。`("xy", "yx")` 变成 `1`。这就是"不匹配位置数的一半"这个错误公式正好成立的情形，要问清楚题目允许哪种交换。
2. **输出交换序列**：分别收集 `xy` 位置的下标列表和 `yx` 位置的下标列表。同类每两个位置 `i`、`j` 输出一次 `(i, j)`（含义：交换 `s1[i]` 与 `s2[j]`）。若各剩一个，设为 `i`（`xy`）和 `j`（`yx`），先输出 `(i, i)` 把位置 `i` 变成 `yx` 类，再输出 `(i, j)`。
3. **标准库统计**：

```python
from collections import Counter


def minimum_swap_counter(s1: str, s2: str) -> int:
    c = Counter(zip(s1, s2))
    xy, yx = c[("x", "y")], c[("y", "x")]
    if (xy + yx) % 2:
        return -1
    return xy // 2 + yx // 2 + 2 * (xy % 2)
```

   `("xx", "yy")` → `1`，`("xy", "yx")` → `2`，`("xx", "xy")` → `-1`。

**Python 提醒**：`Counter` 对不存在的键返回 `0` 且不会把这个键加进去（和 `defaultdict` 不同），所以 `c[("y", "x")]` 在没有该类位置时安全；`zip` 在两串长度不同时静默截断，题目保证等长，若输入不可信要先比较长度。
