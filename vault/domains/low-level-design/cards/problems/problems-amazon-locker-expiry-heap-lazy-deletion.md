---
id: problems-amazon-locker-expiry-heap-lazy-deletion
node: problems.machines.amazon-locker
type: qa
step: 5
tags: [grown]
---
## Q
快递柜（Amazon Locker）的「三天没人取就回收」，为什么不用 `threading.Timer` 也不用后台线程定期全表扫？正确做法的坑在哪？

## A
每个授权一个定时器：一个网点上千个码就是上千个句柄，取件后忘了取消就是泄漏，而且测试只能真等，或把期限调成 0.1 秒再 `sleep`。后台线程定期全表扫：每次 O(码表大小)，更根本的问题是**逻辑里出现了真实时间**，这段代码从此只能靠 `sleep` 测。

正确做法是**显式的 `expire_due()` + 注入时钟 + 到期小顶堆**：时间只从 `self._clock()` 进来（测试里是可手动推进的假时钟），谁来驱动扫描是部署问题；堆让扫描只看堆顶，代价 O(k log n)。

坑是**惰性删除**（lazy deletion）：包裹被提前取走时只删了码表，堆里那条记录还在。弹出时必须识别并丢弃：

```python
while self._deadlines and self._deadlines[0][0] <= now:
    _, code = heapq.heappop(self._deadlines)
    grant = self._grants.get(code)
    if grant is None or not grant.is_expired(now):
        continue
    events.append(self._expire(grant, now))
```

漏掉那两行 `continue`，堆就是一个功能全对、跑一个月才爆的内存泄漏。
