---
id: tlc-permutation-sequence-4-followup
node: b.permutation-sequence
type: qa
step: 4
---
## Q
**LC 60 排列序列**｜追问

面试官接着问：（1）反过来，给一个排列，求它是第几个；（2）输入里有重复数字时，第 `k` 个不同的排列怎么求；（3）`n` 大到 `10^5`，`k` 是大整数，怎么做？

## A
1. **求名次**：逐位统计「比当前位小且还没用过的数字个数」乘以对应的阶乘，全部累加，最后加一。

```python
from math import factorial


def rank(perm: str) -> int:
    digits = sorted(perm)                               # 还没用的数字，升序
    r = 0
    for i, ch in enumerate(perm):
        j = digits.index(ch)                            # 比 ch 小的未用数字个数
        r += j * factorial(len(perm) - 1 - i)           # 这些数字各自带来一整块排列
        digits.pop(j)
    return r + 1
```

`rank("213")` → `3`，`rank("2314")` → `9`，`rank("123")` → `1`，`rank("321")` → `6`。
2. **有重复元素**：每个候选首位对应的块大小是「去掉这个数字后剩余多重集合的排列数」，等于 `(m-1)! / ∏ 各值出现次数!`，不同候选的块大小不同，要逐个候选累减 `k` 直到落入某个块，不能再用一次除法。
3. **`n` 很大**：阶乘不能直接算。先对 `k - 1` 做连续除法 `k, d = divmod(k, base)`，`base` 从 `1` 到 `n`，依次得到阶乘进制从低位到高位的各位 `d`；再用 Fenwick 树维护「剩余数字」，每步找第 `d + 1` 小的数字并删除，每步 `O(log n)`，整体 `O(n log n)`，Python 的大整数除法负责 `k`。

**Python 提醒**：`itertools.permutations(iterable)` 按输入元素的位置顺序产出，输入升序时产出就是字典序；`list.index` 是 `O(n)`，`list.pop(i)` 也是 `O(n)`，所以上面的两个函数都是 `O(n^2)`，对 `n <= 9` 足够。
