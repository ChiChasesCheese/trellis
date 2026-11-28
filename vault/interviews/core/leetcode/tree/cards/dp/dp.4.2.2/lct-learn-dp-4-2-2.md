---
id: lct-learn-dp-4-2-2
node: dp.4.2.2
type: qa
step: 1
---
## Q
**动态规划 › 经典线性 DP › 最长递增子序列（LIS） › 进阶**｜学习卡

套路是什么？

## A
**一句话。** LIS 的进阶题都是「先变成序列、再套 LIS」：排序处理一维、带权或带计数时回到 `O(n^2)` 的 `dp[i]` 定义（以 `i` 结尾），只算长度时用 `tails` 数组加二分。

下图：LIS 进阶题先变成序列，再按要算的东西选两种 LIS 写法之一。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<rect x="102.0" y="7.5" width="136" height="25" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">先把题目变成一个序列</text>
<rect x="10.0" y="64.5" width="100" height="55" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60" y="81.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">两维都要递增</text>
<text x="60" y="96.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一维排序</text>
<text x="60" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同宽另一维降序</text>
<rect x="112.7" y="64.5" width="114.6" height="55" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="81.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">带权或计数</text>
<text x="170" y="96.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回到 O(n²)</text>
<text x="170" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">dp[i] 以 i 结尾</text>
<rect x="237.2" y="64.5" width="95.7" height="55" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="285" y="81.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只要长度</text>
<text x="285" y="96.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">tails + 二分</text>
<text x="285" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">O(n log n)</text>
<path d="M 102.0 20.0 L 60.0 20.0 L 60.0 64.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="60.0,64.5 57.0,58.2 63.0,58.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 170.0 32.5 L 170.0 64.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,64.5 167.0,58.2 173.0,58.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 238.0 20.0 L 285.0 20.0 L 285.0 64.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="285.0,64.5 282.0,58.2 288.0,58.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 60.0 119.5 L 60.0 150.0 L 285.0 150.0 L 285.0 119.5" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="285.0,119.5 288.0,125.8 282.0,125.8" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="170" y="166" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">俄罗斯套娃：排序后对高度做严格 LIS</text>
</svg>

```python
def russian_doll(envelopes):
    # 宽升序；同宽高降序，防止同宽叠放
    envelopes.sort(key=lambda e: (e[0], -e[1]))
    tails = []                       # 各长度的最小结尾
    for _, h in envelopes:
        i = bisect_left(tails, h)    # 严格递增：找第一个 >= h 的位置
        if i == len(tails):
            tails.append(h)
        else:
            tails[i] = h             # 更小的结尾更有利于后面接
    return len(tails)
```

**要点。**
- 为什么对？：同宽高度降序，保证一个递增子序列里每个宽度至多取一个；之后对高度求严格 LIS 就是套娃层数；`tails` 始终递增，所以能二分，`O(n log n)`。
- LC 673 怎么改？：回到 `O(n^2)`，`dp[i]` 是以 `i` 结尾的最长长度，`cnt[i]` 是个数：找到更长的 `dp[j] + 1 > dp[i]` 就覆盖 `cnt[i] = cnt[j]`，一样长就累加；答案是所有最长者的 `cnt` 之和。
- LC 1691 怎么改？：每个长方体三边排序，最长边当高；整体字典序排序后做带权 LIS：`dp[i] = 高度[i] + max(dp[j])`，条件是三维都不小于，答案取 `max(dp)`。

**易错点。**
- 同宽高度没降序：`[[5,4],[5,5]]` 会得 `2`，应为 `1`。
- 严格递增用了 `bisect_right`：相等的高度会被接上，应用 `bisect_left`。
- 673 只取 `dp[n-1]`：最长子序列不一定以最后一个数结尾，要对所有 `dp[i] == max(dp)` 的 `cnt[i]` 求和。

**对应题目。** LC 1691 堆叠长方体的最大高度、LC 673 最长递增子序列的个数、LC 354 俄罗斯套娃信封问题
