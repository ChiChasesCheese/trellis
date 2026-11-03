---
id: craft-single-flight-coalescing-4-wait-or-report-in-flight
node: craft.patterns.single-flight-coalescing
type: qa
step: 4
---
## Q
**单飞合并 · 重复请求到达时，是等第一个做完，还是立刻回「正在处理」**｜模式

通知服务按去重键防止同一封信发两遍。第二个请求到达时，第一个还在发送中。可以让第二个线程阻塞到第一个完成并返回同一个结果（缓存单飞和转账的做法），也可以立刻返回一个「重复，处理中」的占位结果。各自适合什么场景？

## A
**要点。** 阻塞等待：调用方要的是**结果本身**（缓存的值、转账是否成功），合并给它的是同一份结果，调用方感知不到有重复。立即返回占位：调用方要的只是**不要再发一遍**，没有必要让一个工作线程为了别人的发送占着不动；占位结果就是「别重复，第一份我已经在处理」。

```python
def claim(self, key):
    """第一次见到这个 key 返回 None（占坑成功）；重复则返回上一次记下的结果。"""
    now = self._clock()
    with self._lock:                         # 检查 + 占坑在同一把锁里
        entry = self._entries.get(key)
        if entry is not None and now - entry[0] <= self._ttl:
            return entry[1] if entry[1] is not None else _PENDING   # 结果还没出来 → 占位
        if len(self._entries) >= self._capacity:
            self._purge_locked(now)
        self._entries[key] = (now, None)     # None = 发送中
        return None
```

**为什么。** 「先 `if key in store`、再 `store[key] = ...`」是检查再行动的竞态：两个线程都能通过检查，同一封信发了两遍，所以整段在一个临界区里，这也是两种做法共同要守的底线。区别只在冲突方之后做什么：等待，要有一个唤醒机制（`Event`）和超时；占位，什么都不需要，但调用方必须会处理「处理中」这个返回。

**代价。** 等待会占住线程，慢后端下线程池可能被一个热点耗尽；占位把不确定性推给调用方（稍后再查，或按幂等再试一次）。去重表本身也要有上限和过期（TTL + 容量），否则 key 越攒越多。

**信号。** 看调用方能不能接受「还没好」。能 → 占位。不能（例如缓存读要立刻拿到值）→ 等待。
