---
id: tlc-sort-an-array-2-code
node: a.sort-an-array
type: qa
step: 2
---
## Q
**LC 912 排序数组**｜写出 Python 实现

整数数组 `nums`，`1 <= len(nums) <= 5 * 10^4`，`-5 * 10^4 <= nums[i] <= 5 * 10^4`。不使用内置排序函数，`O(n log n)` 时间，空间尽量小，升序返回。

## A
**思路。** 堆排序。先自底向上把数组建成大根堆；然后反复把堆顶（当前最大）换到堆尾，堆大小减一，再对新堆顶做下沉修复。每次下沉沿一条路径走，最多 `log n` 层。

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

运行：`[5,2,3,1]` → `[1,2,3,5]`；`[5,1,1,2,0,0]` → `[0,0,1,1,2,5]`；`[7]` → `[7]`；`[3,3,3]` → `[3,3,3]`；`5 * 10^4` 个随机数 / 全相同 / 升序 / 降序，结果都是升序，各在 `0.1` 秒内。

**复杂度。** 时间 `O(n log n)`，最坏同样；空间 `O(1)`，原地且无递归。

**写法要点。** 下沉时先把 `val` 取出来，沿路径把较大的孩子上提，最后一次性放到空位，比每层都交换少一半赋值；`while (child := 2 * root + 1) < size` 用海象运算符把「取左孩子」和「越界判断」放在一处；`range(n // 2 - 1, -1, -1)` 从最后一个非叶子倒着建堆；`nums[0], nums[end] = nums[end], nums[0]` 元组交换，不需要临时变量；`sift_down` 是闭包，直接读写 `nums`，不用来回传参。
