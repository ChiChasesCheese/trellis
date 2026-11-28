---
id: lct-learn-monotonic-stack-2
node: monotonic-stack.2
type: qa
step: 1
---
## Q
**单调栈 › 矩形**｜学习卡

套路是什么？

## A
**一句话。** 最大矩形的高一定是某根柱子的高：把每根柱子当最矮柱，向左右扩到第一个更矮的柱子为止，一次单调栈同时求出左右边界。

下图：LC 84，每根柱子当最矮柱，左右边界是两边最近的更矮柱。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<rect x="43" y="98" width="38" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="62.0" y="144" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="87" y="114" width="38" height="16" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="106.0" y="144" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="131" y="50" width="38" height="80" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="150.0" y="144" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5</text>
<rect x="175" y="34" width="38" height="96" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="194.0" y="144" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="219" y="98" width="38" height="32" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="238.0" y="144" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="263" y="82" width="38" height="48" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282.0" y="144" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="128" y="50" width="88" height="80" rx="3" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="172" y="22" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">面积 5 × 2 = 10</text>
<text x="106.0" y="110" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">left</text>
<text x="238.0" y="90" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">right</text>
<text x="170" y="160" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">以 5 为最矮柱：向两边扩到第一个更矮的柱子为止</text>
</svg>

```python
def largest_rectangle(h):           # LC 84
    n = len(h)
    left = [-1] * n                 # 左边最近的严格更矮者
    right = [n] * n                 # 右边最近的更矮或等高者
    st = []                         # 下标，高度严格递增
    for i, x in enumerate(h):
        while st and h[st[-1]] >= x:
            right[st.pop()] = i     # 栈顶被 i 终结：i 是它的右边界
        if st:
            left[i] = st[-1]        # 弹完后栈顶严格更矮：左边界
        st.append(i)
    return max((x * (right[i] - left[i] - 1)
                for i, x in enumerate(h)), default=0)
```

**要点。**
- 为什么对？：以 `h[i]` 为最矮柱的最宽矩形恰好撑到两侧第一个更矮的柱子，宽 `right - left - 1`；最优矩形的最矮柱必是某个 `i`。
- LC 85 最大矩形怎么改？：逐行压成柱状图，`heights[j] = heights[j] + 1 if matrix[r][j] == '1' else 0`，每行调用一次，取最大值。
- 相等的柱子怎么处理？：一侧用 `>=`、一侧严格，相等时靠后的柱子算出完整宽度，答案不受影响。

**易错点。**
- 默认边界写错：`[1,2,3,4,5]` 应得 `9`，`right` 默认要是 `n`；`[3]` 应得 `3`，`left` 默认要是 `-1`。
- 85 高度不清零：`[["1"],["0"],["1"]]` 应得 `1`，遇到 `'0'` 必须置零，否则得到 `2`。
- 85 把字符当数字比：`ch == 1` 永远为假，字符是 `'1'`。

**对应题目。** LC 84 柱状图中最大的矩形、LC 85 最大矩形
