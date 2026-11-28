---
id: lct-learn-dp-4-2-1
node: dp.4.2.1
type: qa
step: 1
---
## Q
**动态规划 › 经典线性 DP › 最长递增子序列（LIS） › 基础**｜学习卡

套路是什么？

## A
**一句话。** LIS 贪心加二分：`tails[k]` 记长度 `k+1` 的递增子序列的最小结尾，新元素二分替换或追加，长度即答案。

下图：`tails` 严格递增；新数二分到第一个 `>= x` 的位置，替换或追加。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<text x="10" y="22" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">nums = 10 9 2 5 3 7 101 18</text>
<text x="10" y="52" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x = 3</text>
<rect x="70" y="34" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90.0" y="51.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="110" y="34" width="40" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="130.0" y="51.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5</text>
<text x="240" y="52" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">替换</text>
<text x="10" y="84" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)"></text>
<rect x="70" y="66" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90.0" y="83.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="110" y="66" width="40" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="130.0" y="83.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<text x="10" y="116" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x = 7</text>
<rect x="70" y="98" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90.0" y="115.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="110" y="98" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130.0" y="115.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="150" y="98" width="40" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170.0" y="115.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">7</text>
<text x="240" y="116" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">追加</text>
<text x="10" y="148" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">结束</text>
<rect x="70" y="130" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90.0" y="147.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="110" y="130" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130.0" y="147.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="150" y="130" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="147.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="190" y="130" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="210.0" y="147.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">18</text>
<text x="240" y="134" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">长度 4 = 答案</text>
<text x="170" y="168" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">tails[k]：长 k+1 的子序列的最小结尾；bisect_left 找位置</text>
</svg>

```python
def lis(nums):
    tails = []                   # tails[k]：长 k+1 的最小结尾，严格递增
    for x in nums:
        i = bisect_left(tails, x)    # 第一个 >= x 的位置
        if i == len(tails):
            tails.append(x)      # 比所有结尾都大：长度加一
        else:
            tails[i] = x         # 让该长度的结尾更小
    return len(tails)
```

**要点。**
- 为什么对？：同样长度的子序列，结尾越小越容易往后接，所以每个长度只留最小结尾；这些结尾一定严格递增，才能二分。
- 非严格递增（允许相等）怎么改？：`bisect_left` 换成 `bisect_right`。
- 要还原序列或要 `O(n^2)` 写法怎么办？：`f[i] = 1 + max(f[j])`（`j < i` 且 `nums[j] < nums[i]`）并记前驱；`tails` 本身不是真子序列，只有长度可信。

**易错点。**
- 严格递增误用 `bisect_right`：`[7,7,7,7,7,7,7]` 得 `7`，应为 `1`。
- 把 `tails` 当成答案序列：`[4,5,1]` 的 `tails = [1,5]`，但 `1` 在 `5` 后面。

**对应题目。** LC 300 最长递增子序列
