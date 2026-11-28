---
id: lct-learn-greedy-1-1
node: greedy.1.1
type: qa
step: 1
---
## Q
**贪心算法 › 贪心策略 › 从最小/最大开始贪心**｜学习卡

套路是什么？

## A
**一句话。** 先排序，让最大或最小的元素先决策：固定最长边（或当前最小空位），其余的取紧挨着的值最优。

下图：LC 976，降序后依次固定最长边，只看紧挨着的两个数。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 130">
<rect x="40" y="44" width="50" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="65.0" y="62.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="90" y="44" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="115.0" y="62.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="140" y="44" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="165.0" y="62.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="190" y="44" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="215.0" y="62.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<line x1="40" y1="38" x2="40" y2="32" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="190" y1="38" x2="190" y2="32" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="40" y1="38" x2="190" y2="38" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="115.0" y="32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3 + 3 &gt; 6？否</text>
<line x1="90" y1="82" x2="90" y2="88" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="240" y1="82" x2="240" y2="88" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="90" y1="82" x2="240" y2="82" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="165.0" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3 + 2 &gt; 3？是 → 8</text>
<text x="170" y="122" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">从大到小，最长边 a 配紧挨的 b、c：b + c 已是最大可能</text>
</svg>

```python
def largest_perimeter(nums):
    nums.sort(reverse=True)          # 从大到小
    for a, b, c in zip(nums, nums[1:], nums[2:]):
        if b + c > a:                # a 是最长边，b、c 取紧挨的两个
            return a + b + c
    return 0
```

**要点。**
- 为什么对？：固定最长边 `a`，要让 `b + c` 最大，只能取排在 `a` 后面紧挨着的两个；这样都不行，`a` 做最长边就无解，直接丢掉。
- LC 945 怎么改？：升序扫描，维护下一个没被占用的最小值 `nxt`，`t = max(x, nxt)`，操作数加 `t - x`，`nxt = t + 1`。
- LC 4093 怎么改？：每个数的最优重排是数字降序，收益 `降序值 - 原值` 互相独立，原和加上最大的 `k` 个收益。

**易错点。**
- 只看最大的三条：`[2,3,4,10]` 得 `0`，应为 `9`。
- 条件写成 `b + c >= a`：等号时三点共线，`[1,2,1,10]` 得 `4`，应为 `0`。
- LC 945 的 `nxt` 更新成 `x + 1`：`[1,1,1]` 得 `2`，应为 `3`，要用抬完后的 `t + 1`。

**对应题目。** LC 945 使数组唯一的最小增量操作、LC 976 三角形的最大周长、LC 4093 至多 K 次数字重排后的最大和
