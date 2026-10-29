---
id: tlc-car-fleet-2-code
node: b.car-fleet
type: qa
step: 2
---
## Q
**LC 853 车队**｜Medium · 字节高频｜写出 Python 实现

目的地在 `target`（`0 < target <= 10^6`），`n` 辆车（`1 <= n <= 10^5`）的位置 `position`（`0 <= position[i] < target`，互不相同）和速度 `speed`（`0 < speed[i] <= 10^6`）。车不能超车，追上后以较慢车的速度并排行驶，并排的车算一个车队。返回到达 `target` 的车队数。

## A
**思路。** `sorted(zip(position, speed), reverse=True)` 让离终点最近的车排最前。逐辆算无阻挡的到达时间 `(target - pos) / spd`；它严格大于目前最大的到达时间 `latest`，说明追不上前面的车队，车队数加一并更新 `latest`；否则被吞并，什么都不做。

```python
def car_fleet(target: int, position: list[int], speed: list[int]) -> int:
    fleets = 0
    latest = 0.0                       # 目前所有车队里最晚到终点的时间
    for pos, spd in sorted(zip(position, speed), reverse=True):    # 从离终点最近的车开始
        arrive = (target - pos) / spd  # 这辆车不受阻挡时的到达时间
        if arrive > latest:            # 比前面所有车队都晚：追不上，自成新车队
            fleets += 1
            latest = arrive
    return fleets
```

运行：`car_fleet(12, [10,8,0,5,3], [2,4,1,1,3])` → `3`，`car_fleet(10, [3], [3])` → `1`，`car_fleet(100, [0,2,4], [4,2,1])` → `1`；十万辆车随机输入也立刻返回。

**复杂度。** 时间 `O(n log n)`：排序；扫描 `O(n)`。空间 `O(n)`：排序后的元组列表。

**写法要点。** `zip(position, speed)` 把两个数组按车绑成元组，一起排序；`reverse=True` 按元组第一项（位置）从大到小，位置互不相同，所以速度不会参与比较；`for pos, spd in ...` 直接拆包；用一个变量 `latest` 代替单调栈，因为栈里只有栈顶会被比较；除法 `/` 在 Python 3 里是真除法，结果是 `float`。
