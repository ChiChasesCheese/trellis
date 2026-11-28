---
id: lct-learn-dp-5-2
node: dp.5.2
type: qa
step: 1
---
## Q
**动态规划 › 划分型 DP › 最优划分**｜学习卡

套路是什么？

## A
**一句话。** 最优划分：`f[i]` 是前 `i` 个的最优值，枚举最后一段的长度 `L`，由 `f[i - L]` 加上这一段的贡献转移。

下图：`f[i]` 枚举最后一段的长度 `L`，从 `f[i-L]` 转移过来（这里 `k = 3`）。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="20" y="70" width="42" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="62" y="70" width="42" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="104" y="70" width="42" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="146" y="70" width="42" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="188" y="70" width="42" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="230" y="70" width="42" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="272" y="70" width="42" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="41.0" y="114" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f[0]</text>
<text x="83.0" y="114" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f[1]</text>
<text x="125.0" y="114" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f[2]</text>
<text x="167.0" y="114" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f[3]</text>
<text x="209.0" y="114" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f[4]</text>
<text x="251.0" y="114" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f[5]</text>
<text x="293.0" y="114" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">f[6]</text>
<path d="M 255.0 70 Q 273.0 42 291.0 70" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="291.0,70.0 285.8,65.4 291.3,63.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<path d="M 213.0 70 Q 252.0 28 291.0 70" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="291.0,70.0 285.1,66.2 290.2,63.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<path d="M 171.0 70 Q 231.0 14 291.0 70" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="291.0,70.0 284.9,66.6 289.8,63.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="231.0" y="39.0" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">L=3</text>
<text x="170" y="22" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f[i] = max over L ≤ k：f[i-L] + 段贡献</text>
<text x="170" y="140" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">段贡献 = mx · L，mx 随 L 增大顺手更新</text>
</svg>

```python
def max_sum_partition(arr, k):   # 每段长 <= k，段内都变成段最大值
    n = len(arr)
    f = [0] * (n + 1)            # f[i]：前 i 个的最大和
    for i in range(1, n + 1):
        mx = 0
        for L in range(1, min(k, i) + 1):    # 最后一段长 L
            mx = max(mx, arr[i - L])         # 段最大值随 L 滚动
            f[i] = max(f[i], f[i - L] + mx * L)
    return f[n]
```

**要点。**
- 为什么对？：最后一段 `arr[i-L:i]` 的贡献只和这一段有关，前面是独立子问题 `f[i-L]`；枚举 `L` 就覆盖所有划分。
- LC 91 怎么改？：计数：`f[0] = 1`，末位非 `'0'` 加 `f[i-1]`，末两位在 `10..26` 加 `f[i-2]`，滚动两个变量。
- LC 3441 怎么改？：段长至少 `3` 且同字母：从右往左 DP 求每个（字母、连续长度 `1/2/>=3`）状态补完的最小代价，再从左往右逐位取字典序最小的字母。

**易错点。**
- 每段都取满 `k`：`[1,15,7,9,2,5,10]`、`k = 3` 得 `82`，应为 `84`。
- 下标错位：最后一段第 `L` 个元素是 `arr[i - L]`，不是 `arr[i - L + 1]`。
- LC 91 两位判断只写 `<= 26`：`"06"` 得 `1`，应为 `0`，还要 `>= 10`。

**对应题目。** LC 91 解码方法、LC 1043 分隔数组以得到最大和、LC 3441 变成好标题的最少代价
