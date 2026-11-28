---
id: hi-pt-dasher-payout-7-pairwise-midpoint
node: qb.lld.dasher-payout.points
type: qa
step: 7
---
## Q
**配送员报酬计算 · 切段取中点**｜追问 · 出自：配送员报酬计算 › 深入 6

把一段时间按事件点和高峰窗口边界切成若干小段后，怎么遍历相邻点，又怎么判断每个小段属于哪个窗口？

## A
**遍历。** `itertools.pairwise(sorted(points))`，比 `zip(xs, xs[1:])` 少一次切片拷贝，意图更直。

**判断。** 取小段中点 `mid = a + (b - a) / 2`，看 `mid.time()` 落在哪个窗口：边界属左属右都不用操心。逐分钟循环既慢，秒级精度又不准。

```python
mid = a + (b - a) / 2
peak = next((w.multiplier for w in peaks if w.covers(mid.time())), Decimal(1))
```
