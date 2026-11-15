---
slug: substring-with-largest-variance
---
## Q
**LC 2272 最大波动的子字符串**｜Hard

字符串 `s`（小写字母）。子串的"波动"是其中任意两个字符出现次数之差的最大值。求所有子串的最大波动。

## A
**一句话。** 枚举字符对 `(a, b)`，在字符串上做最大子数组和（Kadane）：`a` 记 `+1`、`b` 记 `-1`，要求子串里至少含一个 `b`，用两个状态 `f0`（可不含 `b`）、`f1`（至少含一个 `b`）。

```python
def largest_variance(s):
    ans = 0
    chars = set(s)
    for a in chars:
        for b in chars:
            if a == b:
                continue
            f0, f1 = 0, -inf          # f1：必须已含一个 b
            for c in s:
                if c == a:
                    f0 += 1
                    f1 += 1
                elif c == b:
                    f1 = max(f0, f1) - 1
                    f0 = max(f0 - 1, 0)
                if f1 > ans:
                    ans = f1
    return ans
```

**复杂度。** 时间 `O(26² · n)`，空间 `O(1)`。

**易错点。**
- 普通 Kadane 在负数处清零：子串必须至少含一个 `b`，不然全是 `a` 时会得到长度而不是差值。
- `f0` 不和 `0` 取最大：以当前位置结尾的和为负时应舍弃，从空串重新开始。

**追问。**
- 为什么要枚举所有有序对？：事先不知道哪个字符多、哪个少，对 `(a, b)` 和 `(b, a)` 都做一遍才能覆盖。

**同模式。** LC 53 最大子数组和、LC 1749 任意子数组和的绝对值的最大值、LC 1493 删掉一个元素以后全为 1 的最长子数组
