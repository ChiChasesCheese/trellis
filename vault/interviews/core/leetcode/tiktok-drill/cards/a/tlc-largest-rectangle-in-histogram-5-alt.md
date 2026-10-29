---
id: tlc-largest-rectangle-in-histogram-5-alt
node: a.largest-rectangle-in-histogram
type: qa
step: 5
---
## Q
**LC 84 柱状图中最大的矩形**｜另一种解法

不用「弹出时结算」的写法，换一种更容易解释的做法：先分别算出每根柱子左右两侧第一根更矮的位置，再统一算面积。写出来，并说明和一遍扫描的栈解法相比什么时候选哪个。

## A
**思路。** 第一遍用单调栈得到 `left[i]`（左边第一根严格更矮）和 `right[i]`（右边第一根不高于它）。第二遍对每根柱子算 `heights[i] * (right[i] - left[i] - 1)`，取最大。

```python
def largest_rectangle_two_pass(heights: list[int]) -> int:
    n = len(heights)
    left = [-1] * n                            # 左边第一根更矮的下标
    right = [n] * n                            # 右边第一根更矮的下标
    stack: list[int] = []
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] >= h:
            right[stack.pop()] = i
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    return max((h * (right[i] - left[i] - 1) for i, h in enumerate(heights)), default=0)
```

运行：`[2,1,5,6,2,3]` → `10`，`[2,4]` → `4`。

**对比。** 一遍扫描版少一次遍历、不需要 `left` / `right` 两个数组，常数小；两遍版把「找边界」和「算面积」分开，每个中间量都能单独打印验证，面试里更好讲清楚，也方便扩展（比如同时要每根柱子的最大扩展宽度）。两者都是 `O(n)` 时间、`O(n)` 空间。

**不可取的做法。** 对每根柱子向两边朴素扩展的 `O(n^2)` 解法，只有 `n` 在几千以内才能过；这里 `n = 10^5`，递增或递减序列上会超时。分治（以最矮柱拆成左右两半）平均 `O(n log n)`，但有序输入下退化成 `O(n^2)`，且递归深度可达 `n`。
