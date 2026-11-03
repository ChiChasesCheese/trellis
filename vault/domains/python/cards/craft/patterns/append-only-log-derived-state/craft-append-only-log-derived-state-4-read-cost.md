---
id: craft-append-only-log-derived-state-4-read-cost
node: craft.patterns.append-only-log-derived-state
type: qa
step: 4
---
## Q
**只追加日志 + 派生状态 · 读要重放，怎么把读成本降下来**｜架构

人数追踪器只存「时间、变动」事件。查询「时刻 t 的人数」如果每次都从头累加，事件有 2 万条、查询有几百次时会很慢。怎么在不丢掉「事实只追加」的前提下让查询变快？

## A
**要点。** 写入时顺手维护前缀和（prefix sum）：第 i 个事件之后的人数存成 `counts[i]`；查询用二分（bisect）找到最后一个不晚于 t 的事件。日志仍然只追加，前缀和是随写入同步的派生索引，读从 O(n) 降到 O(log n)。

```python
def add(self, t: int, delta: int) -> None:
    assert not self.times or t >= self.times[-1]
    self.times.append(t)
    self.counts.append((self.counts[-1] if self.counts else 0) + delta)  # 前缀和随写入维护

def at(self, t: int) -> int:
    i = bisect.bisect_right(self.times, t)       # 最后一个 <= t 的事件
    return self.counts[i - 1] if i else 0
```

2 万个事件，300 次查询，与逐次重放对比（结果逐条断言相等）：

```
结果一致；前缀和+bisect 比逐次重放快约 1056 倍（300 次查询，2 万事件）
```

倍数随机器和数据变化，量级才是要点。

**代价。** 追加必须按时间有序（上面的 `assert`）；乱序到达就要在中间插入并重算后缀，或者先排序再批量构建。

**为什么一致性有保证。** 索引只在追加的那一处更新，没有别的写入口；随时可以重放日志核对。
