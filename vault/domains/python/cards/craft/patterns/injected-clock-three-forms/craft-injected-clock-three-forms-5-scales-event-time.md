---
id: craft-injected-clock-three-forms-5-scales-event-time
node: craft.patterns.injected-clock-three-forms
type: qa
step: 5
---
## Q
**注入时钟 · 从假时钟到事件时间重放**｜模式

LeetCode 的日志限流器把时间戳作为参数传入，LLD 限流器注入 Clock。到了流式系统里，同样的想法叫什么？为什么在日志重放时必须用记录里的时间，而不是机器的当前时间？

## A
**要点。** 叫事件时间（event time）：用事件里携带的时间戳，而不是处理它那一刻的机器时间（处理时间，processing time）。事件时间让同一份日志无论重放多快、重放多少遍，结果都一样；处理时间的结果取决于你的重放速度。

```python
def count_in_window(events, window, now_of):
    q = deque()
    for ts, _ in events:
        now = now_of(ts)                  # 事件时间: now = ts；处理时间: 读墙上时钟
        q.append(ts)
        while q and q[0] <= now - window:
            q.popleft()
        out.append(len(q))
```

同一份日志（时间戳 100、101、105、111），窗口 10 秒，快速重放：

```
事件时间重放 1: [1, 2, 3, 2]
事件时间重放 2: [1, 2, 3, 2]
处理时间重放  : [1, 2, 3, 4]
```

**尺度对照。** 一个函数的参数 `timestamp` → 对象的 `clock` → 流处理里的 event time 与水位线（watermark）→ 分布式测试（如 Jepsen）需要可控时钟来制造时钟漂移。

**易错。** 事件时间要求时间戳可信且大体有序；迟到的事件要靠水位线决定还收不收。

**信号。** 想复现一个只在特定时间出现的 bug，或需要对账、回放；就先问：时间是不是输入。
