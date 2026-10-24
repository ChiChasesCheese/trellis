---
id: tlc-shortest-unsorted-continuous-subarray-4-followup
node: b.shortest-unsorted-continuous-subarray
type: qa
step: 4
---
## Q
**LC 581 最短无序连续子数组**｜追问

面试官接着问：（1）返回区间下标 `[start, end]` 本身？（2）用单调栈怎么做？（3）数组里有重复值时，比较该写严格还是宽松？

## A
1. **返回区间**：同一个循环结束后 `start, end` 就是区间；有序时 `end < start`（初始值 `0, -1` 保持不变），此时返回空即可。
2. **单调栈**：从左到右维护下标栈，保持对应值非降；遇到更小的值就弹栈，弹出的最小下标是左端。再从右到左对称地求右端。

```python
def find_unsorted_subarray_stack(nums: list[int]) -> int:
    n = len(nums)
    left, right = n, -1
    stack: list[int] = []
    for i in range(n):                       # 正向：被后面更小值“撞出去”的位置
        while stack and nums[stack[-1]] > nums[i]:
            left = min(left, stack.pop())
        stack.append(i)
    stack.clear()
    for i in range(n - 1, -1, -1):           # 反向：被前面更大值“撞出去”的位置
        while stack and nums[stack[-1]] < nums[i]:
            right = max(right, stack.pop())
        stack.append(i)
    return right - left + 1 if right > left else 0
```

   `[2,6,4,8,10,9,15]` → `5`，`[1,2,3,4]` → `0`。时间 `O(n)`，空间 `O(n)`，比两个标量的版本差，面试里作为“另一种思路”说出来即可。
3. **重复值**：比较必须严格。`[1,1,1]` 里没有谁需要移动，写成 `<=` / `>=` 会返回 `3`。等值元素排序前后相对位置可以互换，不算无序。

**Python 提醒**：`nums.sort()` 就地排序，会改掉入参；对比用的副本要写 `sorted(nums)`。`math.inf` 是 `float`，和整数比较没问题，但不要把它存进结果里。
