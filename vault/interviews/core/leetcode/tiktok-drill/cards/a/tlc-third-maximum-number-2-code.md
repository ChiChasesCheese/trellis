---
id: tlc-third-maximum-number-2-code
node: a.third-maximum-number
type: qa
step: 2
---
## Q
**LC 414 第三大的数**｜写出 Python 实现

数组 `nums`（`1 <= 长度 <= 10^4`，值在 `[-2^31, 2^31 - 1]`）：返回不同数字中第三大的数，不存在则返回最大值。要求 `O(n)`。

## A
**思路。** 维护降序列表 `top`，保存至今最大的至多 3 个不同值。新数已在 `top` 里就跳过；否则加入、排序、截断到 3 个。结束时长度为 3 返回 `top[2]`，否则 `top[0]`。

```python
def third_max(nums: list[int]) -> int:
    top: list[int] = []                        # 目前见过的最大的至多 3 个不同的值，降序
    for x in nums:
        if x in top:                           # 重复的数不占名次
            continue
        top.append(x)
        top.sort(reverse=True)                 # 最多 4 个元素，排序是 O(1)
        del top[3:]                            # 只留前 3 名
    return top[2] if len(top) == 3 else top[0]
```

运行：`[3,2,1]` → `1`，`[1,2]` → `2`，`[2,2,3,1]` → `1`，`[1]` → `1`，`[5,2,2]` → `5`，`[1,2,-2147483648]` → `-2147483648`。

**复杂度。** 时间 `O(n)`：`x in top` 和排序都作用在至多 4 个元素上；空间 `O(1)`。

**写法要点。** 用一个短列表代替三个变量，没有「空位」哨兵，`-2^31` 问题自然消失；`del top[3:]` 原地截断，越界切片不报错，长度不足 3 时什么都不做；这个写法把 `3` 换成 `k` 就是第 `k` 大（`k` 小时可用，`k` 大时换堆）。
