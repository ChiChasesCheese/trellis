---
id: tlc-subarray-with-elements-greater-than-varying-threshold-5-alt
node: a.subarray-with-elements-greater-than-varying-threshold
type: qa
step: 5
---
## Q
**LC 2334 元素值大于变化阈值的子数组**｜另一种解法

不用单调栈，怎样用并查集（Union-Find）解 LC 2334？什么时候选它？暴力解在什么规模下可以接受？

## A
**思路。** 把元素按值**从大到小**依次"点亮"。点亮 `nums[i]` 时，只和已点亮的左右邻居合并成连通块。这一刻已点亮的元素都 `>= nums[i]`，所以 `i` 所在连通块就是以 `nums[i]` 为最小值的最宽区间，块大小 `k` 就是宽度；检查 `nums[i] * k > threshold`。

```python
def valid_subarray_size(nums: list[int], threshold: int) -> int:
    n = len(nums)
    parent = list(range(n))
    size = [1] * n
    active = [False] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]          # 路径减半
            x = parent[x]
        return x

    for i in sorted(range(n), key=nums.__getitem__, reverse=True):   # 值从大到小依次"点亮"
        active[i] = True
        for j in (i - 1, i + 1):
            if 0 <= j < n and active[j]:
                a, b = find(i), find(j)
                if a != b:
                    parent[a] = b
                    size[b] += size[a]
        k = size[find(i)]                          # 此刻 i 所在连通块里的数都 >= nums[i]
        if nums[i] * k > threshold:
            return k
    return -1
```

运行：`[1,3,4,3,1], 6` → `3`；`[6,5,6,5,8], 7` → `1`（`8 > 7`，同样是合法答案）；`[1], 1` → `-1`；`[1], 5` → `-1`。

**复杂度。** 时间 `O(n log n)`（排序主导，并查集近似 `O(α(n))`）；空间 `O(n)`。

**怎么选。** 单调栈 `O(n)`、没有排序、代码更短，是首选。并查集版本的好处是思路更通用：凡是"按阈值从高到低逐步加入元素、问连通块大小"的题都能套（如 LC 1697 检查边长度限制的路径是否存在），如果面试官追问"离线回答很多个阈值"，这个框架更自然。暴力 `O(n^2)`（固定起点向右扩展并维护最小值）只在 `n` 到几千时可以接受，`n = 10^5` 会超时。

**Python 提醒**：`sorted(range(n), key=nums.__getitem__, reverse=True)` 对下标排序，比先排 `(值, 下标)` 元组更省内存；`reverse=True` 保持稳定排序，值相同时仍按原下标顺序，对结果没有影响。
