---
id: tlc-sliding-window-maximum-2-code
node: b.sliding-window-maximum
type: qa
step: 2
---
## Q
**LC 239 滑动窗口最大值**｜写出 Python 实现

整数数组 `nums`（长度 `1..10^5`，值 `-10^4..10^4`）和窗口大小 `k`（`1..len(nums)`）。返回长度为 `k` 的窗口依次滑过数组时，每个位置的窗口最大值。要求 `O(n)`。

## A
**思路。** 用双端队列 `window` 存下标，保证它对应的值从队首到队尾严格递减。处理第 `i` 个数 `x`：先把队尾所有值不大于 `x` 的下标弹掉，再把 `i` 放进队尾；如果队首下标已经 `<= i - k`（滑出窗口），从队首弹出；一旦 `i >= k - 1`（窗口满了），队首下标对应的值就是当前窗口的最大值。

```python
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    window: deque[int] = deque()       # 存下标；对应的值从队首到队尾严格递减
    ans: list[int] = []
    for i, x in enumerate(nums):
        while window and nums[window[-1]] <= x:
            window.pop()               # 比 x 小（或相等）且更靠左的数，永远没有机会当最大值
        window.append(i)
        if window[0] <= i - k:         # 队首已经滑出窗口
            window.popleft()
        if i >= k - 1:                 # 窗口满了才记录
            ans.append(nums[window[0]])
    return ans
```

运行：`nums=[1,3,-1,-3,5,3,6,7], k=3` → `[3, 3, 5, 5, 6, 7]`，`nums=[1], k=1` → `[1]`，`nums=[3,2,2,1,3], k=2（有重复值）` → `[3, 2, 2, 3]`，`nums=[5,1,1,1], k=2` → `[5, 1, 1]`，`nums=[4,3,2,1], k=4（窗口等于整个数组）` → `[4]`，`nums=[7,7,7], k=1` → `[7, 7, 7]`。

**复杂度。** 时间 `O(n)`：每个下标入队一次、出队至多一次（摊还），循环体内的 `while` 总共弹出不超过 `n` 次；空间 `O(k)`：队列至多存 `k` 个下标（输出数组另计）。

**写法要点。** `collections.deque` 的两端 `append` / `pop` / `popleft` 都是 `O(1)`，列表的 `pop(0)` 是 `O(n)`；队列里存**下标**而不是值：下标既能取值，又能判断是否过期；`while window and nums[window[-1]] <= x` 先判空再取队尾；`window[0] <= i - k` 用 `if` 就够，因为每步最多一个元素过期（窗口每次右移一格）；输出放在 `i >= k - 1` 之后，避免窗口未满时输出。
