---
id: mlp-coding-pc06-solve
node: coding.pc06
step: 1
type: qa
---
## Q
**接雨水与盛水最多的容器：题与解**｜编程轮

同一轮里连着出现两题。一，`heights[i]` 是竖线高度，选两条线与 x 轴围成容器，求能装水的最大面积（LC 11）。二，同样的柱子并排站成一排，下雨后一共能积多少水（LC 42）。

## A
**一句话思路。** 两题都用两端往中间收的双指针。容器题：每次移动较矮的一侧，因为移动较高的一侧宽度变小、高度仍被矮的卡住，面积不可能变大。接雨水：一根柱子头上的水是 `min(左边最高, 右边最高) - 自身高度`；先写两个数组的版本，再压成双指针，哪边的历史最大值小，就结算哪一边。

```python
def max_container_area(h):
    l, r, best = 0, len(h) - 1, 0
    while l < r:
        best = max(best, min(h[l], h[r]) * (r - l))
        if h[l] <= h[r]:
            l += 1            # 矮的一侧限制了面积，只有移动它才可能变大
        else:
            r -= 1
    return best

def trap_arrays(h):           # 先写这个：容易推出来
    n = len(h)
    left, right = [0] * n, [0] * n
    run = 0
    for i in range(n):
        run = max(run, h[i])
        left[i] = run         # 到 i 为止左边最高
    run = 0
    for i in range(n - 1, -1, -1):
        run = max(run, h[i])
        right[i] = run        # 从 i 起右边最高
    return sum(min(left[i], right[i]) - h[i] for i in range(n))

def trap_two_pointer(h):      # 再压成 O(1) 空间
    l, r, lmax, rmax, water = 0, len(h) - 1, 0, 0, 0
    while l < r:
        if h[l] <= h[r]:      # 右边必有不矮于 h[l] 的柱子，左侧水位只由 lmax 决定
            lmax = max(lmax, h[l])
            water += lmax - h[l]
            l += 1
        else:
            rmax = max(rmax, h[r])
            water += rmax - h[r]
            r -= 1
    return water

print(max_container_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))                      # 49
print(trap_arrays([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]),
      trap_two_pointer([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))               # 6 6
```

**复杂度。** 容器题和双指针接雨水都是 O(n) 时间、O(1) 空间；两个数组的版本 O(n) 空间。

**边写边讲。**
- "For the container I always move the **shorter** wall, since moving the taller one can't increase the area."
- "Water above a bar is **min of the max on each side** minus its height; I'll do arrays first, then reduce to two pointers."
- "I process the side with the **smaller running max**, because the other side is guaranteed to have a wall at least that tall."
