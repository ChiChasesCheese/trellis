---
id: craft-append-only-log-derived-state-5-scales-event-sourcing
node: craft.patterns.append-only-log-derived-state
type: qa
step: 5
---
## Q
**只追加日志 + 派生状态 · 从快照数组到事件溯源和 Kafka**｜架构

LeetCode 的快照数组、LLD 的账本、分布式的事件溯源（event sourcing）看起来是三件事，它们共享什么结构？放大到多台机器时什么变了？

## A
**要点。** 都是「追加事实 + 在其上读出视图」。快照数组每格存 (版本, 值) 的追加列表，`snap()` 什么也不复制，只把版本号加一；读时对版本二分。

```python
def set(self, i, v):
    h = self.hist[i]
    if h[-1][0] == self.snap_id: h[-1] = (self.snap_id, v)   # 同一版本内覆盖
    else:                        h.append((self.snap_id, v)) # 新版本：追加事实

def get(self, i, snap_id):
    h = self.hist[i]
    j = bisect.bisect_right(h, (snap_id, float("inf"))) - 1  # 最后一个版本 <= snap_id
    return h[j][1]
```

写 5，快照，再写 6，实际输出：

```
5 6 （快照 0 里是 5，之后写入的 6 不影响它）
```

**尺度对照。** 数组格子里的追加列表 → 账本的 journal（加冲正、对账）→ Kafka 的日志（分区内有序、按 offset 读）加物化视图（CQRS：写走日志，读走派生视图，视图可以丢掉重建）。

**变化。** 单机的「同一把锁里更新索引」变成「消费者异步更新视图」：视图落后日志一点，读到的是旧值（最终一致）；重放要幂等，用 offset 或事件 ID 去重。

**信号。** 需要「历史某时刻的值」「可审计」「出错能重算」。代价是读路径多一层派生，以及日志无限增长要靠快照加压缩。
