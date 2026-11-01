---
id: tlc-tops-k-closest-points-to-origin-0-whole
node: heap-priority-queue.k-closest-points-to-origin
type: qa
---
## Q
**LC 973 最接近原点的 K 个点（K Closest Points to Origin）**｜Medium · 全公司热度第 234 名 · NeetCode 150

给定数组 `points`，其中 `points[i] = [xi, yi]` 表示 X-Y 平面上的一个点，并且给定整数 `k`，返回离原点 `(0, 0)` 最近的 `k` 个点。距离是欧几里得距离。你可以按任何顺序返回答案，除了点坐标的顺序之外，答案确保是唯一的。`1 <= k <= points.length <= 10^4`，`-10^4 < xi, yi < 10^4`。例：`points = [[1,3],[-2,2]]`，`k = 1` → `[[-2,2]]`；`points = [[3,3],[5,-1],[-2,4]]`，`k = 2` → `[[3,3],[-2,4]]`（`[[-2,4],[3,3]]` 也对）。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** Top-K：大小为 `k` 的大根堆（max-heap），比较距离的平方。

**一句话。** 堆里始终保存目前最近的 `k` 个点，堆顶是其中最远的；每来一个点先入堆，超过 `k` 个就弹出堆顶（最远的）。

**识别。** 「最近/最大/最小的 K 个」且不要求有序：Top-K，用大小 `k` 的堆，`O(n log k)`；`k` 接近 `n` 时也可以排序，要 `O(n)` 就用快速选择。比较距离只需比较 `x² + y²`，不用开方。

**推导。** 全部排序 `O(n log n)`，其实只关心前 `k` 个，不需要全序。堆只保存 `k` 个候选：要淘汰的是「候选里最远的」，所以用大根堆；Python 的 `heapq` 只有小根堆，把距离取负。

```python
import heapq


def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    heap: list[tuple[int, int]] = []              # 大根堆（距离取负）：堆顶是当前 k 个候选里最远的
    for i, (x, y) in enumerate(points):
        heapq.heappush(heap, (-(x * x + y * y), i))   # 比较距离的平方即可，不用开方
        if len(heap) > k:
            heapq.heappop(heap)                   # 超过 k 个，踢掉最远的
    return [points[i] for _, i in heap]
```

运行：`([[1,3],[-2,2]], 1)` → `[[-2, 2]]`，`([[3,3],[5,-1],[-2,4]], 2)` → `[[-2, 4], [3, 3]]`（堆内顺序，题目接受任意顺序），`([[0,1]], 1)` → `[[0, 1]]`。

**复杂度。** 时间 `O(n log k)`，空间 `O(k)`。

**拓展优化。**
- 平均 `O(n)`：快速选择（quickselect）。随机枢轴分区，只往包含第 `k` 位的一侧递归；结束时数组前 `k` 个就是最近的 `k` 个（无序）。

```python
import random


def k_closest_quickselect(points: list[list[int]], k: int) -> list[list[int]]:
    def dist(p: list[int]) -> int:
        return p[0] * p[0] + p[1] * p[1]

    lo, hi = 0, len(points) - 1                   # 不变式：前 lo 个都比 [lo, hi] 小，hi 之后都比 [lo, hi] 大
    while lo < hi:
        r = random.randint(lo, hi)                # 随机枢轴，避免有序输入退化到 O(n^2)
        points[r], points[hi] = points[hi], points[r]
        pivot, store = dist(points[hi]), lo
        for i in range(lo, hi):
            if dist(points[i]) < pivot:
                points[i], points[store] = points[store], points[i]
                store += 1
        points[store], points[hi] = points[hi], points[store]    # 枢轴落到最终位置 store
        if store + 1 == k:                        # 前 k 个正好是最小的 k 个
            break
        if store + 1 < k:
            lo = store + 1
        else:
            hi = store - 1
    return points[:k]
```

- 标准库一行：`heapq.nsmallest(k, points, key=lambda p: p[0] ** 2 + p[1] ** 2)`，内部就是同样的堆。

**易错点。**
- 用小根堆保存 `(距离, i)` 然后弹出堆顶：弹掉的是最近的，留下最远的 `k` 个。`([[1,3],[-2,2]], 1)` 得到 `[[1, 3]]`，正确 `[[-2, 2]]`。
- 对距离开方再比较：浮点误差，且多余；平方保持相同的大小顺序。
- 快速选择用固定枢轴（如总取最后一个）：输入已按距离排序时每次只缩小一格，退化成 `O(n^2)`。

**同模式。** LC 215 数组中的第 K 个最大元素、LC 347 前 K 个高频元素、LC 703 数据流中的第 K 大元素、LC 295 数据流的中位数。
