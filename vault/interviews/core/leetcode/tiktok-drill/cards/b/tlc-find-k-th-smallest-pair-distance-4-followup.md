---
id: tlc-find-k-th-smallest-pair-distance-4-followup
node: b.find-k-th-smallest-pair-distance
type: qa
step: 4
---
## Q
**LC 719 找出第 k 小的距离对**｜追问

面试官接着问：（1）要返回产生这个距离的具体数对？（2）`k` 很小（比如 `k <= 100`）时有更简单的做法吗？（3）同样的方法能解决哪些相似问题？

## A
1. **返回数对。** 得到距离 `d` 后，对排序后的每个 `x` 用 `bisect_left` 在它前面找 `x - d`：

```python
from bisect import bisect_left


def pair_with_distance(nums: list[int], d: int) -> tuple[int, int] | None:
    nums = sorted(nums)
    for i, x in enumerate(nums):
        j = bisect_left(nums, x - d)            # 第一个 >= x - d 的位置
        if j < i and nums[j] == x - d:          # 在 x 前面且恰好等于 x - d（d = 0 时需要重复元素）
            return nums[j], x
    return None
```

2. **`k` 小。** 用最小堆做多路归并（见另一种解法）：排序后每个 `i` 对应一条递增的距离序列，堆里放每条序列的当前头，弹 `k` 次，`O((n + k) log n)`，`k` 小时比二分更直接。
3. **同模板。** 凡是「第 `k` 小 / 最小化最大值」，且「不超过 `x` 的元素个数」能快速数出来：LC 378 有序矩阵中第 K 小（从角落走一遍数个数）、LC 668 乘法表中第 k 小（按行 `min(x // i, n)`）、LC 410 分割数组的最大值。

**Python 提醒**：`bisect_left(range(V + 1), k, key=count_at_most)` 可以直接对"单调的函数值"二分（需要 Python 3.10+），`range` 不占内存；但 `key` 在 3.10 之前不存在，旧环境会报 `TypeError`。
