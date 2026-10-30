---
id: tlc-tt-die-beats-probability-4-followup
node: p5.tt-die-beats-probability
type: qa
step: 4
---
## Q
**一个骰子掷出更大点数的概率**｜追问

写完「骰子 `A` 严格大于 `B` 的概率」后，面试官接着问：（1）平局算 `A` 赢一半，怎么改？（2）三个骰子有没有可能出现 `A` 胜 `B`、`B` 胜 `C`、`C` 又胜 `A`（「胜」指获胜概率大于 `1/2`）？

## A
1. **平局算一半。** 对每个 `x`，`bisect_left` 数出严格小于 `x` 的面（赢），`bisect_right - bisect_left` 数出等于 `x` 的面（平）。概率 = `(赢 + 平/2) / (p·q)`；把分子分母同乘 2，全程整数运算：

```python
from bisect import bisect_left, bisect_right
from fractions import Fraction


def tie_half(a: list[int], b: list[int]) -> Fraction:
    sorted_b = sorted(b)
    score = 0
    for x in a:
        lo, hi = bisect_left(sorted_b, x), bisect_right(sorted_b, x)
        score += 2 * lo + (hi - lo)     # 赢记 2 分，平记 1 分，最后除以 2
    return Fraction(score, 2 * len(a) * len(b))
```

   运行：`[3]` 对 `[3]` → `1/2`；`[2,2,6]` 对 `[1,5,5]` → `5/9`（没有平局，不变）。
2. **非传递骰子（non-transitive dice）。** 可以。`A = [2,2,4,4,9,9]`，`B = [1,1,6,6,8,8]`，`C = [3,3,5,5,7,7]`：用上面的函数算，`P(A > B) = P(B > C) = P(C > A) = 5/9`。原因：「`A` 胜 `B`」只比较两个分布的一次抽样，它不是由某个单一的「强度」数值决定的，所以不满足传递性。实际含义：不能把骰子按「谁胜谁」排序选出最强的；同理，比较两组样本（如两个推荐模型的 A/B 指标）时，两两胜率高也不保证存在全局最优。

**Python 提醒**：`Fraction(0.1)` 得到的是浮点 `0.1` 的精确二进制值 `3602879701896397/36028797018963968`，不是 `1/10`；构造分数要传整数分子分母（或字符串 `"0.1"`）。
