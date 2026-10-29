---
id: tlc-minimum-moves-to-make-array-complementary-4-followup
node: b.minimum-moves-to-make-array-complementary
type: qa
step: 4
---
## Q
**LC 1674 使数组互补的最少操作次数**｜追问

面试官接着问：（1）如果 `limit` 极大（如 `10^9`）而 `n` 很小？（2）要返回取得最小代价的目标和？（3）为什么不能只试数组里已有的 `a + b` 当目标和？分别怎么改。

## A
1. **`limit` 极大**：差分数组放不下，但代价只在少数事件点变化。把所有端点收集到字典里，排序后扫描，只在端点处求值（`s = 2` 本身也是一个端点）：

```python
def min_moves_sparse(nums: list[int], limit: int) -> int:
    n = len(nums)
    events: defaultdict[int, int] = defaultdict(int)
    for a, b in zip(nums[: n // 2], reversed(nums[n // 2 :])):
        lo, hi = min(a, b), max(a, b)
        events[2] += 2
        events[lo + 1] -= 1
        events[hi + limit + 1] += 1
        events[a + b] -= 1
        events[a + b + 1] += 1
    cost, best = 0, n                            # 每对最多 2 次，总代价不超过 n
    for s in sorted(events):
        cost += events[s]
        if 2 <= s <= 2 * limit:
            best = min(best, cost)
    return best
```

   `cost` 从 `0` 起算：`events[2]` 已经把默认代价 `2` 乘以对数加进来了；`best` 的初值取 `n`，因为每对最多改 `2` 次，总代价不超过 `n`。
2. **返回目标和**：前缀和遍历时手动记录取得最小值的 `s`，或把 `cost` 存成列表后用 `min(range(2, 2 * limit + 1), key=cost.__getitem__)`。
3. **只试已有的 `a + b`**：不够。`nums = [4,3,2,1,1,1,4,4]`，`limit = 4`，四对的和是 `8, 7, 3, 2`，把其中任何一个当目标和，最少都要 `5` 次操作；而目标和 `5` 只要 `4` 次。代价函数是分段常数，下降点除了 `a+b` 还有 `lo+1`，所以要对 `[2, 2*limit]` 整段取最小。

**Python 提醒**：`accumulate` 返回迭代器，只能遍历一次；如果要多次使用结果，先 `list(accumulate(diff))`。
