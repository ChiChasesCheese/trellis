---
id: tlc-patterns-monotonic-stack-3-why
node: patterns.monotonic-stack
type: qa
step: 3
---
## Q
**单调栈（Monotonic Stack）｜正确性：为什么弹出的就是答案，哨兵和相等怎么处理**

LC 84 柱状图最大矩形用单调栈时，弹出一个柱子为什么能立刻算出它为高的最大矩形？为什么要加哨兵 `0`？相等时用 `>=` 还是 `>`？

## A
```python
def largest_rectangle(heights: list[int]) -> int:
    st: list[int] = []                     # 下标，高度递增
    best = 0
    hs = heights + [0]                     # 哨兵：最后把栈里全部弹出
    for i, h in enumerate(hs):
        while st and hs[st[-1]] >= h:
            height = hs[st.pop()]
            left = st[-1] if st else -1    # 左边第一个更矮的位置
            best = max(best, height * (i - left - 1))
            # 宽度 = 从 left+1 到 i-1
        st.append(i)
    return best
```

运行：`[2,1,5,6,2,3]` → `10`；`[2,4]` → `4`；`[2,2,2]` → `6`。

**不变量**：栈内高度严格递增（弹出 `>=`）。一个柱子 `j` 被 `i` 弹出，说明 `i` 是它右边第一个**不高于**它的位置；栈里它下面的元素是它左边第一个更矮的位置。因此以 `hs[j]` 为高的最宽矩形恰好是 `(left, i)` 开区间，面积立刻算出。每个柱子只算一次。

**为什么要哨兵**：不加 `0`，`[2,4]` 里递增的柱子永远没有机会被弹出，返回 `0`，正确是 `4`；末尾补一个 `0` 比任何柱子都矮，强制清空栈。

**相等怎么办**：用 `>=` 弹出，相等的柱子被弹出时，`left` 可能偏小，但最后一个相等的柱子会算出完整宽度，答案不变。LC 739 里相反：要严格更高，所以用 `<`；若误写成 `<=`，`[73,73,75]` 得 `[1,1,0]`，正确是 `[2,1,0]`。
