---
id: amz-occupancy-tracker-stage1-enter-leave-in-code
node: amazon.amz-occupancy-tracker
type: qa
step: 3
tags: [grown]
---
## Q
在办公室人数追踪里，第 1 关的 `enter` 与 `leave` 核心逻辑怎么写？

## A
先校验，再追加；人数不存，由前缀和得出。最简版本（单区域）：

```python
def enter(self, person, ts):
    if person in self._inside:
        raise AlreadyInside(person)
    self._append(ts, +1)
    self._inside.add(person)

def _append(self, ts, delta):
    if self._times and ts < self._times[-1]:
        raise OutOfOrder(ts)
    self._times.append(ts)
    prev = self._counts[-1] if self._counts else 0
    self._counts.append(prev + delta)
```

`leave` 对称，不在楼里就抛 `NotInside`。校验在写入之前，失败不留脏数据。
