---
slug: sum-of-total-strength-of-wizards
---
## Q
**LC 2281 巫师的总力量和**｜Hard

子数组的力量 = 最小值 × 元素和，求所有子数组力量之和 `mod 10^9+7`。`n` 到 `10^5`。

## A
**一句话。** 贡献法：单调栈求每个数当最小值的范围 `[l, r]`（左严格右不严格防重复），这些子数组的元素和总和用「前缀和的前缀和」`O(1)` 算出。

```python
def total_strength(strength):
    MOD = 10**9 + 7
    n = len(strength)
    left, right = [-1] * n, [n] * n
    st = []
    for i, x in enumerate(strength):
        while st and strength[st[-1]] >= x:
            right[st.pop()] = i      # 右侧第一个 <= 它的
        left[i] = st[-1] if st else -1   # 左侧第一个 < 它的
        st.append(i)
    s = list(accumulate(strength, initial=0))
    ss = list(accumulate(s, initial=0))  # 前缀和的前缀和
    ans = 0
    for i, x in enumerate(strength):
        l, r = left[i] + 1, right[i] - 1
        # Σ_{L=l..i} Σ_{R=i..r} (s[R+1] - s[L])
        tot = ((i - l + 1) * (ss[r + 2] - ss[i + 1])
               - (r - i + 1) * (ss[i + 1] - ss[l]))
        ans = (ans + x * tot) % MOD
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 两侧都用严格小于（或都不严格）：有重复最小值时同一子数组被算两次或漏掉。
- 对每个 `(L, R)` 枚举求和：`O(n^2)`；要先对 `R`、`L` 分别求和再相乘。

**追问。**
- `ss` 的下标怎么来？：`Σ_{R=i..r} s[R+1] = ss[r+2] - ss[i+1]`，`Σ_{L=l..i} s[L] = ss[i+1] - ss[l]`。
- 只求「最小值之和」（LC 907）？：同样的单调栈，贡献是 `x·(i-l+1)·(r-i+1)`。

**同模式。** LC 84 柱状图中最大的矩形、LC 907 子数组的最小值之和、LC 2104 子数组范围和
