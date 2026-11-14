---
slug: number-of-zigzag-arrays-i
---
## Q
**LC 3699 锯齿形数组的总数 I**｜Hard

长度 `n` 的数组，每个值在 `[l, r]`，相邻不等，且任意连续三个数不能严格单调（升降交替）。求个数 `mod 10^9+7`。`n, r ≤ 2000`。

## A
**一句话。** `up[i][v]` / `down[i][v]` 是长 `i+1`、末值为第 `v` 小、最后一步上升 / 下降的个数；上升只能接在下降后且前值更小，用前缀和把转移降到 `O(1)`。

```python
def zig_zag_arrays(n, l, r):
    MOD = 10**9 + 7
    m = r - l + 1                # 只和值的个数有关
    up, down = [[1] * m], [[1] * m]   # 长 1：两种方向都可接
    for i in range(1, n):
        # pre[v]：上一层 down 中值 < v 的总和
        pre = list(accumulate(down[i - 1], initial=0))
        # suf[t]：上一层 up 中最大的 t 个值的总和
        suf = list(accumulate(up[i - 1][::-1], initial=0))
        up.append([x % MOD for x in pre[:m]])
        down.append([x % MOD for x in suf[m - 1::-1]])
    return (sum(up[-1]) + sum(down[-1])) % MOD
```

**复杂度。** 时间 `O(n·m)`，空间 `O(n·m)`，`m = r - l + 1`。

**易错点。**
- 转移时对每个 `v` 枚举前一个值：`O(n·m^2)`，`8·10^9` 超时。
- 上升接上升：要求方向交替，`up[i]` 只能从 `down[i-1]` 来。

**追问。**
- `n` 到 `10^9`（LC 3700）？：一层转移是对向量乘一个固定矩阵，矩阵快速幂 `O(m^3 log n)`，`m` 小时可行。
- 能省空间吗？：只用上一层，每层覆盖即可。

**同模式。** LC 376 摆动序列、LC 629 K 个逆序对数组、LC 3700 锯齿形数组的总数 II
