---
slug: angle-between-hands-of-a-clock
---
## Q
**LC 1344 时钟指针的夹角**｜Medium

给定 `hour` 和 `minutes`，返回时针与分针构成的较小角的度数。

## A
**一句话。** 分针 `6 * minutes` 度，时针 `30 * (hour % 12) + 0.5 * minutes` 度，取 `min(diff, 360 - diff)`。

```python
def angle_clock(hour, minutes):
    minute_angle = minutes * 6
    # 时针每小时 30 度，加上本小时内随分钟走的部分
    hour_angle = (hour % 12) * 30 + minutes * 0.5
    diff = abs(hour_angle - minute_angle)
    return min(diff, 360 - diff)
```

**复杂度。** 时间 `O(1)`，空间 `O(1)`。

**易错点。**
- 时针忽略分钟偏移：`(3, 30)` 得 `90`，应为 `75`。
- 不取较小角：`(1, 50)` 得 `245`，应为 `115`。
- 用整数除法算半度：`(3, 15)` 得 `7`，应为 `7.5`。

**追问。**
- 一天中两针重合几次？：`22` 次，约每 `12/11` 小时一次。

**同模式。** LC 836 矩形重叠、LC 223 矩形面积、LC 1360 日期之间隔几天、LC 1507 转变日期格式
