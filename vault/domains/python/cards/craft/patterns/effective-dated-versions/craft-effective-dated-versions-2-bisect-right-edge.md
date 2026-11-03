---
id: craft-effective-dated-versions-2-bisect-right-edge
node: craft.patterns.effective-dated-versions
type: qa
step: 2
---
## Q
**生效时间版本 · 为什么是 bisect_right，而且「个数」就是版本号**｜模式

版本表 `starts = [100, 200, 300]`，规则是「ts 恰好等于某版本的生效时间时，属于该（新）版本」。用 `bisect_left` 还是 `bisect_right`？返回值怎么变成要用的版本？

## A
**要点。** `bisect_right(starts, ts)` 返回「生效时间 `<= ts` 的版本个数」：因为版本号从 1 开始、且按生效时间排序，这个个数恰好就是当前生效版本的编号（1 起），取列表时下标是 `v - 1`；`v == 0` 表示 ts 比第一个版本还早，没有规则可用。`bisect_left` 返回的是「严格小于 ts 的个数」，在 ts 恰好等于生效时间时少算一个，把新版本生效的那一秒算成旧版本。

```python
from bisect import bisect_left, bisect_right

starts = [100, 200, 300]                       # 版本 1,2,3 的生效时间（含）
for ts in (99, 100, 199, 200, 300):
    v = bisect_right(starts, ts)               # 个数 = 版本号（1 起），0 = 还没有版本
    print(f"ts={ts:3}  right={v}  left={bisect_left(starts, ts)}")
```

实际输出：

```
ts= 99  right=0  left=0
ts=100  right=1  left=0
ts=199  right=1  left=1
ts=200  right=2  left=1
ts=300  right=3  left=2
```

**为什么。** 区间是**左闭右开**（half-open）：版本 i 管 `[starts[i], starts[i+1])`。生效时间那一刻属于新版本，是业务约定（「从 200 秒起」），代码要和约定一致。边界上错一秒，刚好在价格切换的那笔交易就会被收错，而且平时的测试几乎不会碰到边界。

**易错。** ①`bisect_right` 返回个数，不是下标，别直接拿来当下标；②`v == 0` 时 `versions[v - 1]` 是 `versions[-1]`，Python 的负下标会悄悄取到最后一个版本，得到毫无察觉的错误结果，所以必须先判断 0。

**对照。** LeetCode 的 Time Based Key-Value Store 用的是同一行：`i = bisect_right(timestamps, t)`，`i == 0` 返回空串，否则取 `values[i - 1]`。
