---
slug: find-score-of-an-array-after-marking-all-elements
---
## Q
**LC 2593 标记所有元素后数组的分数**｜Medium

反复选未标记的最小元素（相同取下标小的），把它加进分数，并标记它和左右相邻的元素，直到全部被标记。返回分数。

## A
**一句话。** 按（值，下标）排序后依次处理，跳过已标记的，选中就加分并标记左右邻居；排序顺序就是题目的选取顺序。

```python
def find_score(nums):
    n = len(nums)
    marked = [False] * (n + 1)  # 多一格，i+1 越界不用判
    score = 0
    order = sorted(range(n), key=lambda i: (nums[i], i))
    for i in order:
        if marked[i]:
            continue
        score += nums[i]
        marked[i] = marked[i - 1] = marked[i + 1] = True
    return score
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 只按值排序：相同值要按下标从小到大，否则选中的元素不同。
- `i = 0` 时 `marked[i - 1]` 是 `marked[-1]`：正好是多开的那一格，不会误标真实元素。

**追问。**
- 为什么排序后不用每次重新找最小？：标记只会让元素失效，不会改变剩余元素的相对顺序，所以按排好的顺序跳过失效的即可。
- 能做到 `O(n)` 吗？：可以按「严格递减段」切分，每段从末尾隔一个取一个；思路更巧，面试先给排序解。

**同模式。** LC 1046 最后一块石头的重量、LC 2558 从数量最多的堆取走礼物、LC 2530 执行 K 次操作后的最大分数
