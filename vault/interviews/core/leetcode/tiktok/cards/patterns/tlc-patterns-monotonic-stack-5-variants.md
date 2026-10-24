---
id: tlc-patterns-monotonic-stack-5-variants
node: patterns.monotonic-stack
type: qa
step: 5
---
## Q
**单调栈与单调队列｜变形：滑动窗口最大值、小行星碰撞、以每个元素为最小值的区间**

单调队列怎样处理窗口过期？小行星碰撞为什么也是栈？LC 2334 怎样用「最近更小」得到答案？

## A
**单调队列（LC 239）**：队列存下标，值从队首到队尾递减；队首永远是窗口最大值。

```python
from collections import deque
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    dq: deque[int] = deque()
    res: list[int] = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()                       # 比 x 小且更早的，永远不会再成为最大值
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()                   # 队首已滑出窗口
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res
print(max_sliding_window([1,3,-1,-3,5,3,6,7], 3))   # [3, 3, 5, 5, 6, 7]
```

**小行星碰撞（LC 735）**：只有栈顶向右（`> 0`）、新元素向左（`< 0`）才会碰撞；栈里留下的就是存活者。

```python
def asteroid_collision(asteroids: list[int]) -> list[int]:
    st: list[int] = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and st and st[-1] > 0:
            if st[-1] < -a:
                st.pop()                   # 栈顶爆炸，继续碰撞
            elif st[-1] == -a:
                st.pop(); alive = False    # 同归于尽
            else:
                alive = False              # 新来的爆炸
        if alive:
            st.append(a)
    return st
print(asteroid_collision([5,10,-5]), asteroid_collision([8,-8]), asteroid_collision([10,2,-5]))   # [5, 10] [] [10]
```

**LC 2334**：对每个 `nums[i]`，求以它为最小值的最长区间长度 `k = right[i] - left[i] - 1`（`left` 为左边严格更小的位置，`right` 为右边更小或相等的位置）；若 `nums[i] * k > threshold`，则存在合法子数组，返回 `k`。
- 例：`[1,3,4,3,1], threshold=6`，下标 3 的 `3`：左边严格更小的是下标 0，右边更小或相等的是下标 4，区间长 `3`，`3 * 3 = 9 > 6` → 返回 `3`。

**LC 42 接雨水**：栈里存递减的墙，遇到更高的墙 `h` 就弹出一个凹槽底部，宽度 `i - 新栈顶 - 1`，高度差 `min(新栈顶高, h) - 底部高`，累加。
