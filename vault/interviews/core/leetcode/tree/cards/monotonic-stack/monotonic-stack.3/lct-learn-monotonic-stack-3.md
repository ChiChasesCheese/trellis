---
id: lct-learn-monotonic-stack-3
node: monotonic-stack.3
type: qa
step: 1
---
## Q
**单调栈 › 贡献法**｜学习卡

套路是什么？

## A
**一句话。** 汇总所有子数组的最小值时，换成枚举“谁是最小值”：每个元素管辖一个由左右最近的更小者划出的范围，贡献 = 值 × 它当最小值的子数组个数。

下图：LC 907，元素 1 管辖的范围由两侧最近的更小者划出；贡献 = 值 × 左选法 × 右选法。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="40" y="50" width="60" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="100" y="50" width="60" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="130.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<rect x="160" y="50" width="60" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="190.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="220" y="50" width="60" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="250.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<line x1="25" y1="34" x2="25" y2="48" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="25.0,48.0 22.0,41.7 28.0,41.7" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="25" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">left = -1</text>
<line x1="290" y1="34" x2="290" y2="48" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="290.0,48.0 287.0,41.7 293.0,41.7" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="290" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">right = 4</text>
<line x1="40" y1="84" x2="40" y2="90" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="160" y1="84" x2="160" y2="90" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="40" y1="84" x2="160" y2="84" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="100.0" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">左端点 2 种</text>
<line x1="100" y1="112" x2="100" y2="118" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="280" y1="112" x2="280" y2="118" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="100" y1="112" x2="280" y2="112" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="190.0" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">右端点 3 种</text>
<text x="170" y="146" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1 当最小值的子数组 2 × 3 = 6 个，贡献 1 × 6</text>
</svg>

```python
def sum_subarray_mins(arr):         # LC 907
    n = len(arr)
    left = [-1] * n                 # 左边第一个严格更小
    right = [n] * n                 # 右边第一个更小或相等
    st = []
    for i, x in enumerate(arr):
        while st and arr[st[-1]] >= x:
            right[st.pop()] = i     # 栈顶 >= x：x 是它的右边界
        if st:
            left[i] = st[-1]        # 弹完后栈顶严格更小
        st.append(i)
    ans = 0
    for i, x in enumerate(arr):
        ans += x * (i - left[i]) * (right[i] - i)   # 左 × 右
    return ans % (10**9 + 7)
```

**要点。**
- 为什么对？：左端点在 `(left[i], i]`、右端点在 `[i, right[i])` 的子数组，最小值（取最靠左的那个）恰是 `arr[i]`，个数是两段长度之积；一边严格一边不严格，相等的值只算一次。
- LC 2334 元素值大于变化阈值的子数组怎么改？：不求和，对每个 `i` 的管辖长度 `k = right[i] - left[i] - 1` 验证 `nums[i] * k > threshold`，满足就返回 `k`。
- 求最大值之和怎么改？：比较反过来；子数组范围和 = 最大值之和 − 最小值之和。

**易错点。**
- 两边都用严格小：`arr = [2,2]` 应得 `6`，会得到 `8`，`[2,2]` 被两个 `2` 都算了一遍。
- 两边都用小于等于：同一输入得到 `4`，`[2,2]` 一个也没算。
- 2334 返回的是长度不是下标：`nums = [1,3,4,3,1]`、`threshold = 6` 应得 `3`。

**对应题目。** LC 2334 元素值大于变化阈值的子数组、LC 907 子数组的最小值之和
