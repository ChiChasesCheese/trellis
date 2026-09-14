---
id: cc-algorithms-dp-k-segments
node: algorithms.dp
type: qa
---
## Q
"Best total over at most k disjoint contiguous segments." Name the state and give the cost.

## A
**Two states per position: currently inside a segment, or between segments.**

```python
for x in a:
    for j in range(k, 0, -1):                       # descending j: no element used twice
        open_[j] = max(open_[j] + x, best[j - 1] + x)  # extend the j-th, or start it here
        best[j] = max(best[j], open_[j])            # close it, or stay closed
```

- O(n·k) time and O(k) memory in this rolling form ([[cc-algorithms-dp-rolling-rows]]).
- **Disjointness lives in `best[j - 1]`**: starting the j-th segment reads the state from *before* this segment, never `best[j]`.
- The descending `j` loop is what stops one element being consumed by two segments in the same step — the same reason 0/1 knapsack iterates capacity downwards.
- `k = 0` must yield the empty answer, and a `k` larger than the number of positive runs must never do *worse* than a smaller one. Both are hidden-test staples ([[cc-output-sentinels-empty-input]]).

## Q zh
「至多 k 段互不相交的连续区间上的最优总和。」说出状态并给出代价。

## A zh
**每个位置两个状态：当前在某段之内，或在两段之间。**

```python
for x in a:
    for j in range(k, 0, -1):                       # j 降序：同一元素不会被用两次
        open_[j] = max(open_[j] + x, best[j - 1] + x)  # 延长第 j 段，或在此开启它
        best[j] = max(best[j], open_[j])            # 关闭它，或保持关闭
```

- 这种滚动写法时间 O(n·k)、内存 O(k)（[[cc-algorithms-dp-rolling-rows]]）。
- **互不相交性藏在 `best[j - 1]` 里**：开启第 j 段时读的是本段*之前*的状态，绝不是 `best[j]`。
- `j` 降序循环正是防止同一步里一个元素被两段吃掉的原因 —— 和 0/1 背包按容量降序遍历是同一个理由。
- `k = 0` 必须给出空答案，而 k 大于正值段数时绝不能比更小的 k *更差*。两者都是隐藏测试的常客（[[cc-output-sentinels-empty-input]]）。
