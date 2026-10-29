---
id: tlc-largest-perimeter-triangle-2-code
node: a.largest-perimeter-triangle
type: qa
step: 2
---
## Q
**LC 976 三角形的最大周长**｜写出 Python 实现

正数数组（长度 `3..10^4`，元素 `1..10^6`）里选三条边组成面积不为零的三角形，求最大周长，组不成返回 `0`。要求 `O(n log n)`。

## A
**思路。** 降序排序，用 `zip` 一次拿到相邻三元组 `a >= b >= c`；第一个满足 `b + c > a` 的三元组周长就是答案，都不满足返回 0。

```python
def largest_perimeter(nums: list[int]) -> int:
    nums = sorted(nums, reverse=True)                 # 从大到小；不改动调用方的列表
    for a, b, c in zip(nums, nums[1:], nums[2:]):     # 相邻三元组，a >= b >= c
        if b + c > a:                                 # 两条短边之和大于最长边即可
            return a + b + c
    return 0
```

运行：`[2,1,2]` → `5`，`[1,2,1,10]` → `0`，`[2,3,4,10]` → `9`，`[3,6,2,3]` → `8`，`[1,2,3]` → `0`。

**复杂度。** 时间 `O(n log n)`：排序；扫描 `O(n)`。空间 `O(n)`：`sorted` 返回新列表，三个切片也各复制一份。

**写法要点。** `sorted(..., reverse=True)` 不改动调用方的列表；`zip(nums, nums[1:], nums[2:])` 是「滑动三元组」的惯用法，长度按最短的切片自动截断，不会越界；找到就 `return`，循环自然结束说明没有解，返回 0。
