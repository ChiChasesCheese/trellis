---
slug: find-the-distance-value-between-two-arrays
---
## Q
**LC 1385 两个数组间的距离值**｜Easy

统计 `arr1` 中有多少个 `x`，满足 `arr2` 里没有任何元素 `y` 使 `|x - y| <= d`。

## A
**一句话。** `arr2` 排序后二分：找第一个 `>= x - d` 的元素，它不存在或大于 `x + d`，`x` 就计数。

```python
def find_the_distance_value(arr1, arr2, d):
    arr2 = sorted(arr2)
    cnt = 0
    for x in arr1:
        i = bisect_left(arr2, x - d)  # [x-d, x+d] 内最小的候选
        if i == len(arr2) or arr2[i] > x + d:
            cnt += 1                   # 区间内没有元素
    return cnt
```

**复杂度。** 时间 `O((n + m) log m)`，空间 `O(m)`。

**易错点。**
- 用 `bisect_right(arr2, x - d)`：跳过恰好等于 `x - d` 的元素，`arr1=[3], arr2=[1], d=2` 得 `1`，应为 `0`。
- 只从 `x` 往右看：漏掉比 `x` 小的元素，`arr1=[5], arr2=[4,10], d=1` 得 `1`，应为 `0`。
- 忘了判断 `i == len(arr2)`：`x - d` 比所有元素都大时越界。

**追问。**
- 不排序怎么做？：双重循环 `O(nm)`，数据范围小时也够用。
- 两个数组都已有序？：双指针一次扫过，`O(n + m)`。

**同模式。** LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 475 供暖器、LC 658 找到 K 个最接近的元素、LC 2300 咒语和药水的成功对数
