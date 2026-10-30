---
id: tlc-maximum-swap-2-code
node: b.maximum-swap
type: qa
step: 2
---
## Q
**LC 670 最大交换**｜写出 Python 实现

非负整数 `num`（`0..10^8`）。至多交换一次其中两位数字，返回能得到的最大整数。

## A
**思路。** 把 `num` 转成数字字符列表，用字典 `last` 记下每个数字最后一次出现的下标。从高位到低位扫描，对每一位 `d`，从 `9` 往下枚举比 `d` 大的数字 `big`：如果 `big` 在右边出现过（`last[big] > i`），就把这一位和 `big` 的最右出现交换，立刻返回。扫完都没有换，说明已是最大，返回 `num`。

```python
def maximum_swap(num: int) -> int:
    digits = list(str(num))
    last = {d: i for i, d in enumerate(digits)}   # 每个数字最后一次出现的下标（后写覆盖前写）
    for i, d in enumerate(digits):
        for big in "9876543210":                  # 从最大的数字开始找
            if big <= d:
                break                             # 已经没有比 d 更大的了，这一位不用换
            if last.get(big, -1) > i:             # 右边有更大的数字：换最右边的那个
                digits[i], digits[last[big]] = digits[last[big]], digits[i]
                return int("".join(digits))
    return num
```

运行：`num=2736` → `7236`，`num=9973` → `9973`，`num=1993` → `9913`，`num=2998` → `9928`，`num=0` → `0`，`num=10**8` → `100000000`。

**复杂度。** 时间 `O(d · 10)`，`d` 为位数（`10^8` 时 `d ≤ 9`，实际是常数）：每一位最多看 10 个候选数字；空间 `O(d)`（数字列表与 `last` 字典，至多 10 个键）。

**写法要点。** 字典推导 `{d: i for i, d in enumerate(digits)}` 里后写入的键值覆盖先写入的，天然得到「最后一次出现」；`"9876543210"` 字符串直接当作降序数字序列迭代，且字符比较 `big <= d` 与数值比较一致（单个数字字符的字典序等于数值序）；`last.get(big, -1)` 对不存在的数字返回 `-1`，不用先判断 `in`；元组交换 `a[i], a[j] = a[j], a[i]`；`int("".join(digits))` 把字符列表还原成整数。
