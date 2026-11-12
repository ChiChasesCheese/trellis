---
slug: car-fleet
---
## Q
**LC 853 车队**｜Medium

单行道上的车开往 `target`，不能超车，追上前车后以其速度并排行驶，成为一个车队。求到达终点的车队数。

## A
**一句话。** 按位置从近到远排序，算各自到达时间，比前面所有车队都晚的车自成新车队。

```python
def car_fleet(target, position, speed):
    fleets = 0
    latest = 0.0                  # 目前最晚的到达时间
    cars = sorted(zip(position, speed), reverse=True)
    for pos, spd in cars:
        arrive = (target - pos) / spd
        if arrive > latest:       # 严格大于：追不上前面的车队
            fleets += 1
            latest = arrive
    return fleets
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 直接数不同的到达时间：示例 1 的无阻挡时间 `1,1,12,7,3` 去重得 `4`，应为 `3`。
- 比较写成 `>=`：终点才追上也是同一车队，`(12,[10,8],[2,4])` 得 `2`，应为 `1`。
- 从远到近扫：示例 1 得 `1`，应为 `3`。

**追问。**
- 浮点比较会出错吗？：题目范围内不会；保险可交叉相乘 `(t-p1)*s2 > (t-p2)*s1`。
- 想免排序？：位置 `< target <= 10^6`，用位置下标的桶，`O(n + target)`。

**同模式。** LC 739 每日温度、LC 496 下一个更大元素 I、LC 84 柱状图中最大的矩形、LC 735 小行星碰撞
