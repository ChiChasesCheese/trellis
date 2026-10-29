---
id: tlc-array-partition-i-4-followup
node: a.array-partition-i
type: qa
step: 4
---
## Q
**LC 561 数组拆分 I**｜追问

面试官接着问：（1）能做到 `O(n)` 吗？（2）如果每组是 `k` 个数，最大化各组最小值之和？（3）如果改成最小化各对**较大者**之和？

## A
1. **`O(n)`**：值域只有 `[-10^4, 10^4]`，共 `20001` 种值，用计数排序（counting sort）。按值从小到大扫，用 `take` 记下当前元素在排序后是否落在偶数下标：值 `v` 出现 `c` 次时，其中落在偶数位的有 `(c + take) // 2` 个；`c` 为奇数时奇偶性翻转。

```python
def array_pair_sum_counting(nums: list[int]) -> int:
    OFFSET = 10**4
    count = [0] * (2 * OFFSET + 1)          # 值域 [-10^4, 10^4] 平移到 [0, 2·10^4]
    for x in nums:
        count[x + OFFSET] += 1
    total, take = 0, True                   # take：当前元素是否落在排序后的偶数下标
    for v, c in enumerate(count):
        if c:
            total += (v - OFFSET) * ((c + take) // 2)   # 这 c 个相同值里有几个落在偶数位
            take = take ^ (c % 2 == 1)                  # c 为奇数时奇偶性翻转
    return total
```

`[1,4,3,2]` → `4`，`[6,2,6,5,1,2]` → `9`。时间 `O(n + R)`，`R = 20001`。
2. **每组 `k` 个**：同样的交换论证，排序后连续 `k` 个一组，答案 `sum(sorted(nums)[::k])`。
3. **最小化较大者之和**：对称地，最大的 `x_2n` 一定被计入，让它和 `x_2n-1` 同组，「吞掉」次大值；仍是排序后相邻配对，答案 `sum(sorted(nums)[1::2])`。

**Python 提醒**：`bool` 是 `int` 的子类，`(c + take) // 2` 里 `True` 当 `1` 用；`take ^ (c % 2 == 1)` 两个 `bool` 异或仍得到 `bool`。
