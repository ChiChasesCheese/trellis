---
slug: minimum-number-of-taps-to-open-to-water-a-garden
---
## Q
**LC 1326 灌溉花园的最少水龙头数目**｜Hard

花园为 `[0, n]`，点 `i` 的水龙头打开可灌溉 `[i - ranges[i], i + ranges[i]]`。求灌溉整个花园的最少水龙头数，不可能返回 `-1`。

## A
**一句话。** 预处理每个左端点能到的最远右端，再像跳跃游戏 II 一样，到边界时选能伸最远的。

```python
def min_taps(n, ranges):
    reach = [0] * (n + 1)          # reach[l]：左端为 l 的最远右端
    for i, r in enumerate(ranges):
        l = max(0, i - r)          # 截到 0，负下标会写到尾部
        reach[l] = max(reach[l], i + r)
    taps = end = far = 0
    for i in range(n):             # 依次覆盖单位区间 [i, i+1]
        far = max(far, reach[i])
        if i == end:               # 已选的到头了：必须再开一个
            if far <= i:
                return -1
            taps += 1
            end = far
    return taps
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 左端点不截断：`i - r < 0` 时 `reach[-3]` 写到数组尾部，`(5, [3,4,1,1,0,0])` 得 `-1`，应为 `1`。
- 把覆盖当成覆盖点：`(1, [0,0])` 每个龙头只盖一个点，线段 `[0,1]` 没盖住，应为 `-1`。
- 循环写成 `range(n + 1)`：单位区间 `[n, n+1]` 不存在，会误判有缝。

**追问。**
- 为什么贪心对？：到 `end` 时所有左端 `<= end` 的龙头都可接上，选最远的一定不差。
- 换成区间覆盖（LC 1024）？：同样先按左端点预处理，再贪心跳。

**同模式。** LC 45 跳跃游戏 II、LC 1024 视频拼接、LC 452 用最少数量的箭引爆气球、LC 435 无重叠区间
