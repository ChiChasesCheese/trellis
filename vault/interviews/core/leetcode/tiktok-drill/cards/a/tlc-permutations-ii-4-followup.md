---
id: tlc-permutations-ii-4-followup
node: a.permutations-ii
type: qa
step: 4
---
## Q
**LC 47 全排列 II**｜追问

面试官接着问：（1）只要不重复排列的个数，不要列出来；（2）排列太多放不进内存，怎么办；（3）只要按字典序的下一个排列。

## A
1. **只数个数**：`n! / ∏ c_i!`，其中 `c_i` 是每个值的出现次数。
```python
from collections import Counter
from math import factorial, prod

def count_unique(nums: list[int]) -> int:
    return factorial(len(nums)) // prod(factorial(c) for c in Counter(nums).values())
```
   `[1,1,2,2,3,3,4,4]` → `2520`。
2. **放不进内存**：把 `dfs` 改成生成器，到叶子 `yield tuple(path)`，递归处用 `yield from dfs()`。调用方边消费边处理，内存仍是 `O(n)`。
3. **下一个排列**（LC 31）：从右找第一个 `nums[i] < nums[i+1]`，再从右找第一个比 `nums[i]` 大的与它交换，最后反转 `i+1` 之后的部分。`O(n)` 原地，从升序数组开始反复调用就能不重复地按字典序遍历全部排列。

**Python 提醒**：`set(itertools.permutations(nums))` 看起来最短，但先生成 `n!` 个再去重，重复很多时极浪费；遍历 `Counter` 的键时可以改值，不能增删键，否则抛 `RuntimeError: dictionary changed size during iteration`。
