---
id: tlc-tops-kth-largest-element-in-a-stream-0-whole
node: heap-priority-queue.kth-largest-element-in-a-stream
type: qa
---
## Q
**LC 703 数据流中的第 K 大元素**｜Easy · 全公司热度第 440 名 · NeetCode 150

设计一个找到数据流中第 `k` 大元素的类。注意是排序后的第 `k` 大元素，不是第 `k` 个不同的元素。实现 `KthLargest`：`KthLargest(int k, int[] nums)` 用整数 `k` 和整数流 `nums` 初始化；`int add(int val)` 将 `val` 插入数据流后，返回当前数据流中第 `k` 大的元素。`0 <= nums.length <= 10^4`，`1 <= k <= nums.length + 1`，`-10^4 <= nums[i], val <= 10^4`，最多调用 `add` `10^4` 次。例：`KthLargest(3, [4,5,8,2])`，依次 `add(3)`、`add(5)`、`add(10)`、`add(9)`、`add(4)` 返回 `4, 5, 5, 8, 8`；`KthLargest(4, [7,7,7,7,8,3])`，依次 `add(2)`、`add(10)`、`add(9)`、`add(9)` 返回 `7, 7, 7, 8`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 大小为 `k` 的最小堆（min-heap）维护 Top-K。

**一句话。** 堆里永远只保存当前最大的 `k` 个数，堆顶（最小的那个）就是第 `k` 大。

**识别。** 「数据流 + 第 k 大」：不能每次重新排序；只关心第 `k` 大，所以只需保留前 `k` 大，淘汰比第 `k` 大还小的数。要保留最大的 `k` 个，用**最小堆**，因为需要随时能看到并淘汰这 `k` 个里最小的。

**推导。** 每次 `add` 都把所有数排序取第 `k` 个，是 `O(n log n)`，调用 `10^4` 次太慢。若第 `k` 大是 `x`，比 `x` 小的数以后永远不可能再成为前 `k` 大，没必要保留。所以维护大小为 `k` 的最小堆：新数比堆顶大就替换堆顶（`heapreplace`），否则丢掉；每次 `O(log k)`。

```python
class KthLargest:
    def __init__(self, k: int, nums: list[int]) -> None:
        self.k = k
        self.heap = sorted(nums)[-k:]            # 升序列表本身就是合法的最小堆；只保留最大的 k 个

    def add(self, val: int) -> int:
        if len(self.heap) < self.k:              # 还没攒够 k 个：直接放进去
            heappush(self.heap, val)
        elif val > self.heap[0]:                 # 比当前第 k 大还大：把堆顶（旧的第 k 大）换掉
            heapreplace(self.heap, val)
        return self.heap[0]                      # 堆顶就是第 k 大
```

运行：`KthLargest(3, [4,5,8,2])` 依次 `add(3), add(5), add(10), add(9), add(4)` 返回 `4, 5, 5, 8, 8`；`KthLargest(4, [7,7,7,7,8,3])` 依次 `add(2), add(10), add(9), add(9)` 返回 `7, 7, 7, 8`；`KthLargest(1, [])` 依次 `add(-3), add(-2), add(-4)` 返回 `-3, -2, -2`。

**复杂度。** 初始化 `O(n log n)`（排序），每次 `add` `O(log k)`，空间 `O(k)`。

**拓展优化。**
- 初始化可以更快：`heapify` 整个数组 `O(n)`，再弹出多余的 `n - k` 个最小值；或先 `nlargest(k, nums)` 再 `heapify`。
- 要支持「第 k 小」「中位数」：换成一个最大堆加一个最小堆（LC 295）。
- 需要删除任意元素时，堆做不到 `O(log n)`，要改成平衡树或带懒删除的堆。

**易错点。**
- 用最大堆保留前 `k` 大：堆顶是最大值，看不到第 `k` 大，每次都要弹 `k - 1` 次。
- 没处理堆还没满的情况：`KthLargest(1, [])` 直接写 `self.heap[0]` 或 `val > self.heap[0]` 会对空堆 `IndexError`；`k = len(nums) + 1` 时堆在第一次 `add` 之后才会满。
- 去重：题目要的是排序后第 `k` 大，重复值各算一个。`[7,7,7,7,8,3]` 的第 `4` 大是 `7`，去重后只剩 `{3,7,8}` 就错了。

**同模式。** LC 215 数组中的第 K 个最大元素、LC 347 前 K 个高频元素、LC 295 数据流的中位数、LC 973 最接近原点的 K 个点。
