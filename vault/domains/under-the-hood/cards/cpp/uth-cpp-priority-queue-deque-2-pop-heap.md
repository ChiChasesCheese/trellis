---
id: uth-cpp-priority-queue-deque-2-pop-heap
node: cpp.priority-queue-deque
type: qa
step: 2
---
## Q
**pop_heap 为什么先下沉到底再上浮**｜C++ · libstdc++ 16

弹出堆顶后，标准库不是把末尾元素放到堆顶再一路下沉，而是怎么做的？

## A
**背景。** 弹出堆顶后，要把堆重新整理好。常规做法：把末尾元素搬到堆顶，再一路往下换（下沉）；每层要比两次，先挑出较大的孩子，再看它比下沉的元素大不大。

**结构。** 标准库把空出的堆顶当成“洞”，让较大的孩子一路上移补洞，一直走到叶子（最底层、没有孩子的节点），再把原来的末尾元素放进洞里，从下往上浮。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<line x1="139.542" y1="35.7226" x2="95.4576" y2="68.2774" stroke="currentColor" stroke-width="1"/>
<line x1="160.458" y1="35.7226" x2="204.542" y2="68.2774" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<line x1="77.3408" y1="86.5041" x2="57.6592" y2="113.496" stroke="currentColor" stroke-width="1"/>
<line x1="92.6592" y1="86.5041" x2="112.341" y2="113.496" stroke="currentColor" stroke-width="1"/>
<line x1="207.341" y1="86.5041" x2="187.659" y2="113.496" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<line x1="222.659" y1="86.5041" x2="242.341" y2="113.496" stroke="currentColor" stroke-width="1"/>
<circle cx="150" cy="28" r="13" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="2" stroke-dasharray="4 3"/>
<text x="150" y="32.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">洞</text>
<circle cx="85" cy="76" r="13" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="85" y="80.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<circle cx="215" cy="76" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="215" y="80.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<circle cx="50" cy="124" r="13" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="50" y="128.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="120" cy="124" r="13" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="120" y="128.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="180" cy="124" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="180" y="128.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<circle cx="250" cy="124" r="13" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="250" y="128.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="196" y="44" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① 8 上移</text>
<text x="188" y="100" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② 6 上移</text>
<text x="180" y="158" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③ 洞落到叶子</text>
<text x="250" y="150" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">末尾 4</text>
<text x="170" y="188" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每层只比 1 次, 末尾的 4 再从洞里往上浮</text>
</svg>
```

**细节。**

- 下沉的每一层只比较一次：左右孩子谁大
- 传统做法每层要比较两次：先选孩子，再和下沉的元素比
- 末尾元素本来就偏小，通常会停在叶子附近，往上浮几乎不花代价

**为什么。** 每层少一次比较；比较昂贵时（比如字符串）很划算。

**例题：** LC 912 排序数组

给整数数组 `nums`，升序排列并返回，不能用内置排序，要求 O(n log n)。例：`[5,2,3,1]` → `[1,2,3,5]`。下面的解法是堆排序，`sift_down` 就是“孩子上提、空位下移”的下沉。

```python
def sort_array(nums: list[int]) -> list[int]:
    n = len(nums)

    def sift_down(root: int, size: int) -> None:
        # 把 nums[root] 下沉到 nums[:size] 这个大根堆里的正确位置
        val = nums[root]
        while (child := 2 * root + 1) < size:
            if child + 1 < size and nums[child + 1] > nums[child]:
                child += 1                      # 选较大的孩子
            if nums[child] <= val:
                break
            nums[root] = nums[child]            # 孩子上提，空位下移
            root = child
        nums[root] = val

    for i in range(n // 2 - 1, -1, -1):         # 自底向上建堆，O(n)
        sift_down(i, n)
    for end in range(n - 1, 0, -1):             # 反复把堆顶（最大值）换到末尾
        nums[0], nums[end] = nums[end], nums[0]
        sift_down(0, end)
    return nums
```
