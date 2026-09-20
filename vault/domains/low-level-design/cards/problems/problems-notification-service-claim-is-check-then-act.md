---
id: problems-notification-service-claim-is-check-then-act
node: problems.components.notification-service
type: qa
step: 9
tags: [grown]
---
## Q
通知服务的去重表写成 `if key not in seen: seen.add(key); send()`。这段代码在多线程下会出什么事？为什么单线程测试永远发现不了？正确写法是什么？

## A
这是典型的**检查—然后—行动（check-then-act）竞态**：两个线程可以同时通过 `key not in seen` 这一步，于是同一封信发了两遍。单线程里两次调用天然串行，所以永远测不出来；上了线就在『调用方超时重发』的那一瞬间双发。

GIL 帮不上忙：字典的单个操作是原子的，但『查了再写』是两个操作，中间可以被切换。正确写法是把检查和占坑放进同一把锁，做成一个原子的 `claim`：

```python
with self._lock:
    entry = self._entries.get(key)
    if entry is not None and now - entry[0] <= self._ttl:
        return entry[1]          # 重复：返回上次的结果
    self._entries[key] = (now, None)
    return None                  # 占坑成功
```

测法：八条线程加栅栏同时提交同一个 id，断言只有一条得到『已入队』、渠道只被调用一次。
