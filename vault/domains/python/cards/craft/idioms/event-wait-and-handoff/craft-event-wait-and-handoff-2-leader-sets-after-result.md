---
id: craft-event-wait-and-handoff-2-leader-sets-after-result
node: craft.idioms.event-wait-and-handoff
type: qa
step: 2
---
## Q
**Event 的等待与交接 · 领跑者为什么先写结果、后 `set()`，并且在 `finally` 里无条件 set**｜写法

缓存键过期，十个线程同时来读。只让第一个（领跑者）回源，其余在 `Event` 上等它。领跑者什么时候 `set()` 才对？如果回源抛了异常，等待者会怎样？

## A
**要点。** 这是结果交接（handoff）：领跑者产生结果，等待者拿结果。两条规则：（1）**先写结果、后 `set()`**：`set()` 之后等待者立刻醒来读结果，写在后面它们会读到空；（2）**成败都要 `set()`**，放在 `finally` 里，否则领跑者异常退出后，等待者永远等下去。等待者醒来不假定一定有结果，而是回到循环重新判断：命中就返回，没命中就重新竞争当新领跑者。

```python
class Cache:
    def __init__(self) -> None:
        self.data: dict[str, str] = {}
        self.inflight: dict[str, threading.Event] = {}
        self.mu = threading.Lock()
        self.loads = 0

    def get_or_load(self, key, loader, *, set_first=False, use_finally=True):
        while True:
            if key in self.data:
                return self.data[key]
            with self.mu:
                waiter = self.inflight.get(key)
                leader = waiter is None
                if leader:
                    waiter = self.inflight[key] = threading.Event()
            if not leader:
                if not waiter.wait(1.0):
                    return "<等了 1 秒仍无结果>"
                continue                    # 被唤醒后回到循环重新判断，不假定一定有结果
            if use_finally:
                try:
                    value = loader()
                    self.data[key] = value  # 先写结果
                    self.loads += 1
                    return value
                finally:
                    with self.mu:
                        done = self.inflight.pop(key)
                    done.set()              # 后唤醒，成败都唤醒
            value = loader()                # 不安全版：loader 抛异常就不会 set
            self.data[key] = value
            self.inflight.pop(key).set()
            return value


def run(loader, **kw):
    c = Cache(); out = []
    def w():
        try:
            out.append(c.get_or_load("k", loader, **kw))
        except RuntimeError as e:
            out.append(f"领跑者收到异常: {e}")
    ts = [threading.Thread(target=w) for _ in range(3)]
    for t in ts: t.start(); time.sleep(0.02)
    for t in ts: t.join()
    return c, sorted(out)

def slow_ok():
    time.sleep(0.2); return "value"
c, out = run(slow_ok)
print("三个并发请求 回源次数:", c.loads, "结果:", out)

def make_flaky():
    calls = []
    def f():
        time.sleep(0.2)
        if not calls:
            calls.append(1); raise RuntimeError("回源失败")
        return "value"
    return f
c, out = run(make_flaky())
print("成败都 set: ", out)
c, out = run(make_flaky(), use_finally=False)
print("失败不 set: ", out)
```

实际输出：

```
三个并发请求 回源次数: 1 结果: ['value', 'value', 'value']
成败都 set:  ['value', 'value', '领跑者收到异常: 回源失败']
失败不 set:  ['<等了 1 秒仍无结果>', '<等了 1 秒仍无结果>', '领跑者收到异常: 回源失败']
```

**为什么。** 领跑者失败，异常只给它自己的调用方；等待者收到的是「可以重试了」的信号，由其中一个成为新领跑者。把领跑者的异常转发给所有等待者是另一种设计（共享失败），代价是一次瞬时故障会让一批请求一起失败。

**易错。** 不要把 `set()` 放在 `except` 里，会漏掉 `KeyboardInterrupt` 等非 `Exception` 的退出；`finally` 里先把 `inflight` 表项摘掉再 `set()`，否则后来者拿到的是已完成的旧事件。
