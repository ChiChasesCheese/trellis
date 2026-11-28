---
id: lct-learn-data-structures-4-4
node: data-structures.4.4
type: qa
step: 1
---
## Q
**常用数据结构 › 队列 › 单调队列**｜学习卡

套路是什么？

## A
**一句话。** 单调队列是滑动窗口加单调栈：队里存下标，新元素进来时弹掉队尾所有不比它好的（它们更早过期又不更强），队首过期就弹，于是队首永远是窗口最优，`O(n)`。

下图：队里存下标、值从队首到队尾递减；新元素从队尾挤掉不比它大的，过期的从队首弹。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="10" y="30" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">nums</text>
<rect x="50" y="14" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70.0" y="32.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="90" y="14" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="110.0" y="32.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="130" y="14" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="150.0" y="32.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="170" y="14" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="190.0" y="32.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-3</text>
<rect x="210" y="14" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="230.0" y="32.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="70.0" y="56" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="110.0" y="56" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="150.0" y="56" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="190.0" y="56" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="230.0" y="56" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<line x1="90" y1="70" x2="90" y2="76" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="210" y1="70" x2="210" y2="76" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="90" y1="70" x2="210" y2="70" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="150.0" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">窗口 k = 3（i = 3 时）</text>
<text x="10" y="120" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">q</text>
<rect x="50" y="104" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="75" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1:3</text>
<rect x="100" y="104" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="125" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2:-1</text>
<rect x="150" y="104" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="175" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3:-3</text>
<text x="75" y="148" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">队首 = 最大</text>
<text x="175" y="148" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">值递减 →</text>
<line x1="230.0" y1="44" x2="210" y2="112" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="210.0,112.0 208.9,105.1 214.7,106.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="220" y="104" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">x = 5 进来：</text>
<text x="220" y="118" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">弹掉队尾 ≤ 5 的</text>
<text x="220" y="132" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">下标 1 已过期也弹</text>
<text x="170" y="180" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">队里存下标（标注 下标:值），从队首到队尾值递减</text>
</svg>

```python
def max_sliding_window(nums, k):     # LC 239
    ans, q = [], deque()             # q 存下标，对应值递减
    for i, x in enumerate(nums):
        while q and nums[q[-1]] <= x:
            q.pop()                  # 被 x 支配，永远不会是最大
        q.append(i)                  # 存下标才能判断过期
        if q[0] <= i - k:
            q.popleft()              # 队首已离开窗口
        if i >= k - 1:
            ans.append(nums[q[0]])   # 窗口已满，队首即最大
    return ans
```

**要点。**
- 为什么对？：队列下标递增、值递减；窗口里不在队中的元素都被更晚进来且不更小的元素支配，删掉不丢答案，最大者必在队首；每个下标进出一次，`O(n)`，堆做不到 `O(1)` 删过期。
- LC 1438 怎么改？：窗口不定长，维护一个递减队列和一个递增队列，极差 `> limit` 就左端点右移，两个队首各自检查是否过期。
- LC 862 为什么对前缀和用队列？：含负数时窗口不单调；起点 `i` 一旦满足 `pre[j] - pre[i] >= k`，更大的 `j` 只会更长，所以弹队首；`pre[i'] >= pre[j]` 且 `i' < j` 时 `i'` 被支配，所以弹队尾。

**易错点。**
- 队列里存值不存下标：无法判断队首是否离开窗口。
- LC 1438 缩左时只检查一个队列的过期队首：`[8,2,4,7]`、`limit = 4` 应得 `2`。
- LC 862 用普通双指针：`[84,-37,32,40,95]`、`k = 167` 应得 `3`，滑窗得 `5`；无解（`[1,2]`、`k = 4`）要返回 `-1`。

**对应题目。** LC 1438 绝对差不超过限制的最长连续子数组、LC 862 和至少为 K 的最短子数组、LC 239 滑动窗口最大值
