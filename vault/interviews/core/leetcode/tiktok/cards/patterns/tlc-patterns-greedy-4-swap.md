---
id: tlc-patterns-greedy-4-swap
node: patterns.greedy
type: qa
step: 4
---
## Q
**贪心（Greedy）｜从高位到低位：最大交换（LC 670）**

最多交换一次，怎样得到最大的数？交换的是哪一位和哪一位，相同数字取哪一个？

## A
想让数字最大，**高位越大越好**。从高位往低位扫描：第一个"后面有更大数字"的位置 `i`，就应该和它后面**最大的数字**交换；若最大的数字出现多次，取**最后一次出现**的位置。

```python
def maximum_swap(num: int) -> int:
    digits = list(str(num))
    last = {int(d): i for i, d in enumerate(digits)}   # 每个数字最后一次出现的位置
    for i, d in enumerate(digits):
        for bigger in range(9, int(d), -1):            # 从大到小找比当前位大的数字
            if last.get(bigger, -1) > i:               # 且它出现在更靠后的位置
                j = last[bigger]
                digits[i], digits[j] = digits[j], digits[i]
                return int("".join(digits))
    return num
print(maximum_swap(2736), maximum_swap(9973), maximum_swap(0), maximum_swap(98368))   # 7236 9973 0 98863
```

- **为什么取最后一次出现**：把大数字换到更低位，被换到后面的那个小数字影响的位权更低。`1993`：把 `1` 与**最后一个** `9` 交换得 `9913`；与第一个 `9` 交换只得 `9193`，更小。
- **为什么从最高位开始**：高位的增量权重最大，一次交换里能让最高位变大就优先。
- 已经降序（`9973`）说明没有可改善的位置，原数就是最大。
- 时间 `O(L · 10)`，`L` 是位数；`num <= 10^8`，最多 9 位。
- 暴力枚举所有 `C(L, 2)` 对交换也只有几十种，面试里可以先说暴力，再说贪心的线性解。
