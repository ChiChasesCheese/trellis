---
id: tlc-beautiful-arrangement-ii-4-followup
node: b.beautiful-arrangement-ii
type: qa
step: 4
---
## Q
**LC 667 优美的排列 II**｜追问

面试官接着问：（1）怎么写一个检查函数验证构造结果？（2）还有别的构造方式吗？（3）如果要求答案以指定的数开头，或者字典序最小，行不行？

## A
1. **检查函数**：两件事，排列合法且差的种类数为 `k`：

```python
from itertools import pairwise

def is_valid(ans: list[int], n: int, k: int) -> bool:
    return sorted(ans) == list(range(1, n + 1)) and len({abs(a - b) for a, b in pairwise(ans)}) == k
```

   `is_valid(construct_array(5, 3), 5, 3)` 为 `True`。
2. **另一种构造**：先递增放 `1..n-k-1`，再在 `[n-k, n]` 这 `k + 1` 个数上头尾交替。前半段的差全是 `1`，后半段的差是 `k, k-1, ..., 1`，接缝差介于 `1..k`；`(5, 2)` → `[1, 2, 3, 5, 4]`，差为 `{1, 2}`。两种构造都是 `O(n)`。
3. **指定开头或字典序最小**：题目只要求任意解；加上限制后，构造要重新证明（比如开头不是 `1` 就不能直接套模板）。面试里先说清楚「任意解」的前提，别随口承诺字典序最小。

**Python 提醒**：`itertools.pairwise` 需要 Python 3.10+；老版本用 `zip(ans, ans[1:])`，会多复制一份切片。集合推导式 `{abs(a - b) for ...}` 用来数「种类」，不要用列表再 `len(set(...))`，多一次中间列表。
