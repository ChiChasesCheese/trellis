---
id: tlc-codetop-supp-6-2-code
node: b.codetop-supp-6
type: qa
step: 2
---
## Q
**补充题 6 手撕堆排序**｜写出 Python 实现

整数数组 `nums`（`1 <= nums.length <= 50000`，`-50000 <= nums[i] <= 50000`），用堆排序原地升序排列，不调用 `sorted`、`list.sort`、`heapq`。

## A
**思路。** 先把 `nums` 原地调整成大根堆，再反复把堆顶（最大值）换到未排序区的末尾，堆缩小一格后对新堆顶下沉。下沉用循环实现：每次和较大的孩子比较，更大就交换并继续往下，否则停止。

```python
def sort_array(nums: list[int]) -> list[int]:
    n = len(nums)

    def sift_down(root: int, size: int) -> None:
        """把 nums[root] 下沉到合适位置，堆的范围是 nums[0:size]。"""
        while (child := 2 * root + 1) < size:              # 左孩子存在
            if child + 1 < size and nums[child + 1] > nums[child]:
                child += 1                                  # 取较大的孩子
            if nums[root] >= nums[child]:
                break                                       # 已满足大根堆性质
            nums[root], nums[child] = nums[child], nums[root]
            root = child

    for i in range(n // 2 - 1, -1, -1):                     # 建堆：最后一个非叶子节点向前
        sift_down(i, n)
    for end in range(n - 1, 0, -1):                         # 每轮把当前最大值放到 end
        nums[0], nums[end] = nums[end], nums[0]
        sift_down(0, end)                                   # 堆缩小为 nums[0:end]
    return nums
```

运行：`[5,2,3,1]` → `[1,2,3,5]`，`[5,1,1,2,0,0]` → `[0,0,1,1,2,5]`，`[1]` → `[1]`，`[2,1]` → `[1,2]`，`[3,3,3]` → `[3,3,3]`，`50000 到 1 倒序的前 3 个` → `[1,2,3]`。

**复杂度。** 时间 `O(n log n)`；空间 `O(1)`。

**写法要点。** 内部函数 `sift_down` 通过闭包直接操作 `nums`，不用来回传参；海象运算符 `(child := 2 * root + 1) < size` 把「算左孩子」和「判越界」写在循环条件里；`nums[a], nums[b] = nums[b], nums[a]` 元组交换不需要临时变量；`range(n // 2 - 1, -1, -1)` 从最后一个非叶子节点倒着建堆；下沉用 `while` 而不是递归，空间保持 `O(1)`。
