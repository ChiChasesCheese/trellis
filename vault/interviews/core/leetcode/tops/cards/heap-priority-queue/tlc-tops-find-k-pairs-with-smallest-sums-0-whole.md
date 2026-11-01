---
id: tlc-tops-find-k-pairs-with-smallest-sums-0-whole
node: heap-priority-queue.find-k-pairs-with-smallest-sums
type: qa
---
## Q
**LC 373 查找和最小的 K 对数字**｜Medium · 全公司热度第 408 名 · Top Interview 150

给定两个按**非递减**顺序排列的整数数组 `nums1` 和 `nums2`，以及整数 `k`。定义一对数 `(u, v)`，`u` 来自 `nums1`，`v` 来自 `nums2`。找出和最小的 `k` 个数对，按和从小到大返回。`1 <= nums1.length, nums2.length <= 10^5`，`-10^9 <= nums1[i], nums2[i] <= 10^9`，两个数组都是升序，`1 <= k <= 10^4`，`k <= nums1.length * nums2.length`。例：`nums1 = [1,7,11]`, `nums2 = [2,4,6]`, `k = 3` → `[[1,2],[1,4],[1,6]]`；`nums1 = [1,1,2]`, `nums2 = [1,2,3]`, `k = 2` → `[[1,1],[1,1]]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 小根堆（min-heap）做 k 路归并：把"多个有序序列里取前 k 小"变成每次弹一个、补一个。

**一句话。** 把 `nums1[i]` 与整个 `nums2` 配出的和看成第 `i` 条升序序列，堆里始终放每条序列当前的头，弹出最小的，再补上同一序列的下一个。

**识别。** 「两个有序数组」「前 k 小的组合」「`k` 远小于 `n * m`」：`n * m` 最大 `10^10`，不能全部枚举；每个 `i` 对应的和 `nums1[i] + nums2[j]` 随 `j` 递增，就是合并 `n` 个有序链表（LC 23）的结构；`k <= 10^4` 保证 `O(k log k)`。

**推导。** 暴力：所有 `n * m` 个数对排序后取前 `k`，`O(nm log nm)`。观察：对固定的 `i`，`j` 增大和只会变大，所以数对 `(i, j)` 要想成为答案，必须先弹出 `(i, j - 1)`。因此初始只需放每个 `i` 的 `(i, 0)`；弹出 `(i, j)` 后再把 `(i, j + 1)` 补进去。因为 `nums1` 也升序，`i` 超过 `k` 的行不可能进前 `k`，初始只放前 `min(k, n)` 行。

```python
from heapq import heapify, heappop, heappush


def k_smallest_pairs(nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
    # 堆元素 (和, i, j)：第 i 行当前走到的位置是 j；先放每行的 (i, 0)，最多 k 行
    heap = [(nums1[i] + nums2[0], i, 0) for i in range(min(k, len(nums1)))]
    heapify(heap)
    res: list[list[int]] = []
    while heap and len(res) < k:
        _, i, j = heappop(heap)  # 当前所有行头里和最小的
        res.append([nums1[i], nums2[j]])
        if j + 1 < len(nums2):  # 同一行的下一个：只能由前一个生成，所以不会重复入堆
            heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
    return res
```

运行：示例 1 → `[[1,2],[1,4],[1,6]]`；示例 2 → `[[1,1],[1,1]]`；`([1,2], [3], 3)` 只有两对，`k` 受 `k <= n * m` 约束，取 `k = 2` → `[[1,3],[2,3]]`；`([5], [1,2,3], 2)` → `[[5,1],[5,2]]`。

**复杂度。** 时间 `O(min(k, n) + k log min(k, n))`，空间 `O(min(k, n))`（堆）加输出。

**拓展优化。**
- `k` 很大（接近 `n * m`）时堆的 `k log k` 变慢，如果只要**第 `k` 小的和**，可以二分和的取值，用双指针数"和不超过 `x` 的数对有多少个"，`O((n + m) log 值域)`。

**易错点。**
- 把全部 `n * m` 对一次性入堆：`n = m = 10^5` 时有 `10^10` 个，内存和时间都爆。
- 弹出 `(i, j)` 后同时补 `(i + 1, j)` 和 `(i, j + 1)` 又不做去重：`(i + 1, j + 1)` 会被两个来源各入堆一次。`nums1 = nums2 = [1,2,3]`, `k = 6` 会得到 `[[1,1],[1,2],[2,1],[1,3],[2,2],[2,2]]`，正确是最后一个为 `[3,1]`；本写法只单向补 `(i, j + 1)`，每个位置只有一个来源，不需要去重集合。
- 补下一个元素前不检查 `j + 1 < len(nums2)`：`nums1 = [1,2]`, `nums2 = [3]`, `k = 2` 会 `IndexError`。

**同模式。** LC 378 有序矩阵中第 K 小的元素、LC 23 合并 K 个升序链表、LC 719 找出第 K 小的数对距离、LC 786 第 K 个最小的质数分数。
