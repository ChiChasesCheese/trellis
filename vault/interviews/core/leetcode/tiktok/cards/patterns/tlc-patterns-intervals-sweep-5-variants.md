---
id: tlc-patterns-intervals-sweep-5-variants
node: patterns.intervals-sweep
type: qa
step: 5
---
## Q
**区间与扫描线｜变形：两个区间表求交、跳跃游戏的可达范围、稀疏坐标上的覆盖计数**

除了合并和会议室，区间题还有哪些常见形态？各自的扫描方式是什么？

## A
1. **两个已排序的区间表求交集**（双指针，每次推进右端点更小的那个）：

```python
def interval_intersection(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    i = j = 0
    res: list[list[int]] = []
    while i < len(a) and j < len(b):
        lo, hi = max(a[i][0], b[j][0]), min(a[i][1], b[j][1])
        if lo <= hi:
            res.append([lo, hi])           # 有交集
        if a[i][1] < b[j][1]:
            i += 1                         # 右端点更小的先结束，推进它
        else:
            j += 1
    return res
print(interval_intersection([[0,2],[5,10],[13,23],[24,25]], [[1,5],[8,12],[15,24],[25,26]]))
# [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]
```

2. **可达范围是区间（LC 55 跳跃游戏）**：维护「当前能到达的最远下标」`far`；若某个下标 `i > far`，说明走不到：

```python
def can_jump(nums: list[int]) -> bool:
    far = 0
    for i, x in enumerate(nums):
        if i > far:
            return False
        far = max(far, i + x)
    return True
print(can_jump([2,3,1,1,4]), can_jump([3,2,1,0,4]))   # True False
```

   LC 45 跳跃游戏 II 是同一个思路加「分层」：当前这一跳能到的区间 `[lo, hi]`，扫完这一层就跳数 +1。

3. **稀疏大坐标上的覆盖计数（LC 2021）**：用字典记录差分，只对出现过的端点排序，累加得到每个端点之后的覆盖数；见前缀和与差分一组。

4. **资源调度（LC 253、2402）**：排序 + 堆，见堆一组；区别是 LC 2402 需要知道**哪个房间**，所以要用「房间号堆 + 结束时间堆」。

5. **选最多互不重叠区间 / 最少箭射爆气球**：按**右端点**排序，贪心选结束最早的；与合并按左端点排序不同。
