---
id: tlc-tops-kth-largest-element-in-an-array-0-whole
node: heap-priority-queue.kth-largest-element-in-an-array
type: qa
---
## Q
**LC 215 数组中的第K个最大元素**｜Medium · 全公司热度第 39 名 · NeetCode 150、Hot 100、Top Interview 150、LeetCode 75

给定整数数组 `nums` 和整数 `k`，请返回数组排序后的第 `k` 个最大的元素（不是第 `k` 个不同的元素）。你必须设计并实现时间复杂度为 `O(n)` 的算法。`1 <= k <= nums.length <= 10^5`，`-10^4 <= nums[i] <= 10^4`。例：`nums = [3,2,1,5,6,4], k = 2` → `5`；`nums = [3,2,3,1,2,4,5,5,6], k = 4` → `4`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 快速选择（quickselect）：随机 pivot 的三路划分，只钻进答案所在的那一段。

**一句话。** 随机选 pivot，把数组分成「大于 / 等于 / 小于」三段，第 `k` 大一定落在其中一段，只处理那一段，其余两段整个丢掉；期望 `O(n)`。

**识别。** 「第 `k` 大」且题面要求 `O(n)`：完整排序 `O(n log n)`、大小为 `k` 的堆 `O(n log k)` 都不达标，只有选择算法（selection）能做到。「不是第 `k` 个不同的元素」和 `nums[i]` 值域只有两万多、`n` 达 `10^5`，意味着有大量重复值，划分必须把相等的元素单独成段。

**推导。** 排序后取下标，只要一个位置却排好了全部。快速排序每轮划分后，目标位置只在一边，只需递归一边；每轮期望砍掉一半，总代价 `n + n/2 + n/4 + … = O(n)`。随机 pivot 防止被构造的输入退化到 `O(n^2)`；三路划分使全是重复值的数组一轮结束。

**简单解法。** 整个数组降序排序，取下标 `k - 1`。

```python
def find_kth_largest(nums: list[int], k: int) -> int:
    # 重复值各占一个位置，正好是「排序后的第 k 个」，不用去重
    return sorted(nums, reverse=True)[k - 1]
```

时间 `O(n log n)`、空间 `O(n)`；开场可以，但题面要求 `O(n)`。

最优解：

```python
import random

def find_kth_largest(nums: list[int], k: int) -> int:
    while True:
        pivot = random.choice(nums)                # 随机 pivot：不怕有序、全相同这类构造数据
        bigger = [x for x in nums if x > pivot]
        equal = nums.count(pivot)
        if k <= len(bigger):                       # 第 k 大在比 pivot 大的那段里
            nums = bigger
        elif k <= len(bigger) + equal:             # 落在与 pivot 相等的那段：答案就是 pivot
            return pivot
        else:                                      # 在比 pivot 小的那段里，前面 bigger 和 equal 都算过了
            k -= len(bigger) + equal
            nums = [x for x in nums if x < pivot]
```

运行：`([3,2,1,5,6,4], 2)` → `5`；`([3,2,3,1,2,4,5,5,6], 4)` → `4`；`([7], 1)` → `7`；`([2,2,2], 3)` → `2`。

**复杂度。** 期望时间 `O(n)`，最坏 `O(n^2)`（概率可忽略）；空间 `O(n)`（列表推导的复制）。

**拓展优化。**
- 大小为 `k` 的小根堆，堆顶就是第 `k` 大；`k` 远小于 `n` 或数据是流时更合适，`O(n log k)`、空间 `O(k)`：
```python
import heapq

def find_kth_largest_heap(nums: list[int], k: int) -> int:
    heap = nums[:k]
    heapq.heapify(heap)                            # 前 k 个先建堆，O(k)
    for x in nums[k:]:
        if x > heap[0]:
            heapq.heapreplace(heap, x)             # 比堆顶大才有资格挤进前 k 大
    return heap[0]
```
- 值域有限（这里 `[-10^4, 10^4]`）时用计数数组，确定性 `O(n + 值域)`。

**易错点。**
- 把重复值去重：`set(nums)` 后排序，`([3,2,3,1,2,4,5,5,6], 4)` 得 `3`，正确是 `4`；题目要的是排序后的第 `k` 个，不是第 `k` 个不同的值。
- 只做二路划分（`<=` 与 `>`）且 pivot 固定取首元素：全是相同值的数组每轮只少一个，退化到 `O(n^2)`；有序输入同理。三路划分加随机 pivot 两者都避免。
- 进入「小于 pivot」那段后忘了 `k -= len(bigger) + equal`：`k` 还是原来的名次，越找越偏，最终在空列表上 `random.choice` 抛 `IndexError`（例如 `([3,2,1,5,6,4], 5)`，正确是 `2`）。

**同模式。** LC 347 前 K 个高频元素、LC 703 数据流中的第 K 大元素、LC 973 最接近原点的 K 个点、LC 75 颜色分类（三路划分）。
