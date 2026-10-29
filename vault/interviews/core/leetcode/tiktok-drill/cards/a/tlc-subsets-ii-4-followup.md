---
id: tlc-subsets-ii-4-followup
node: a.subsets-ii
type: qa
step: 4
---
## Q
**LC 90 子集 II**｜追问

面试官接着问：（1）不用递归能不能写；（2）只问有多少个不同的子集，不要列出来；（3）结果里的子集要按某种顺序（比如字典序）输出。

## A
1. **按值分组的迭代写法**：用 `Counter` 数每个值出现 `c` 次；对每个不同的值 `v`，把当前所有子集各追加 `1..c` 个 `v`。

```python
from collections import Counter


def subsets_with_dup_iter(nums: list[int]) -> list[list[int]]:
    res: list[list[int]] = [[]]
    for v, c in sorted(Counter(nums).items()):          # 每个不同的值出现 c 次
        res += [s + [v] * k for s in res for k in range(1, c + 1)]   # 给已有子集追加 1..c 个 v
    return res
```

`[1,2,2]` → `[[], [1], [2], [2, 2], [1, 2], [1, 2, 2]]`，`[0]` → `[[], [0]]`，与回溯版本得到同一批子集（顺序不同）。推导式在 `res` 被扩展之前就整体求值，所以追加的是旧的子集。
2. **只数个数**：每个值可以取 `0` 到 `c` 个，共 `c + 1` 种选法，不同子集数是各值 `c + 1` 的乘积；`[1,2,2]` 是 `2 * 3 = 6`，`[1]*10` 是 `11`。`O(n)`，不需要枚举。
3. **指定顺序**：回溯天然给出深度优先的顺序（排序后即字典序的一种）；按值分组的写法顺序不同，需要时对结果 `sort`（元组或列表比较是字典序）。

**Python 提醒**：`res += [...]` 对列表是原地扩展，推导式 `for s in res` 在 `+=` 发生之前已经完整求值；若写成 `for s in res: res.append(...)`，会在遍历同一个列表时不断追加而无法停止。`Counter(nums).items()` 排序后按值升序，保证结果稳定。
