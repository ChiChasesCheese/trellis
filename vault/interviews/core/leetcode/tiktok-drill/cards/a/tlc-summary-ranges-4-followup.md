---
id: tlc-summary-ranges-4-followup
node: a.summary-ranges
type: qa
step: 4
---
## Q
**LC 228 汇总区间**｜追问

面试官接着问：（1）输入可能无序或有重复？（2）能不能用标准库一次分好组？（3）数据流式到来，要随时给出当前的区间列表？分别怎么改。

## A
1. **无序或有重复**：先 `nums = sorted(set(nums))` 再套同一段扫描，时间变成 `O(n log n)`（排序主导）。
2. **`itertools.groupby`**：连续整数的「值 - 下标」恒定，用它当分组键：

```python
from itertools import groupby

def summary_groupby(nums: list[int]) -> list[str]:
    ans: list[str] = []
    for _, grp in groupby(enumerate(nums), key=lambda p: p[1] - p[0]):
        run = [x for _, x in grp]
        ans.append(str(run[0]) if len(run) == 1 else f"{run[0]}->{run[-1]}")
    return ans
```

   输出与双指针版一致。它读起来短，但依赖「值 - 下标」这个技巧，面试里先写双指针，再补这个。
3. **数据流**：这就是 LC 352。用有序结构保存互不相交的区间，新数 `v` 用 `bisect` 找到相邻区间，与 `v - 1`、`v + 1` 所在区间合并，每次插入 `O(log n)` 查找加合并。

**Python 提醒**：`groupby` 返回的子迭代器是**惰性**的，推进外层循环后上一组就失效了；要在本轮用 `[x for _, x in grp]` 先取出来，不能把 `grp` 存起来之后再读。
