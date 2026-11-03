---
id: craft-event-wait-and-handoff-5-scales-long-poll
node: craft.idioms.event-wait-and-handoff
type: qa
step: 5
---
## Q
**Event 的等待与交接 · 从线程里的 `wait` 到长轮询与带截止时间的 await**｜写法

进程内，等待者在 `Event` 上等领跑者的结果。客户端和服务端隔着网络，一个请求不能无限挂着。同样的「等结果」要怎么搬过去？

## A
**要点。** 骨架没变：服务端对每个键保存一个事件和结果，先存结果再唤醒。变的是**等待要有上限**：服务端最多挂住请求 `hold` 秒，没结果就返回「还没好」（HTTP 202 / 204）；客户端带着**同一个幂等键**再来，直到拿到结果或总预算用完。客户端的总预算同样是绝对截止时间，每一轮只用剩余时间。

```python
# 长轮询 / 等待结果：服务端最多挂住请求 hold 秒，没结果就让客户端带着同一个键再来
class Server:
    def __init__(self) -> None:
        self.results: dict[str, str] = {}
        self.events: dict[str, threading.Event] = {}
        self.mu = threading.Lock()

    def submit(self, key: str, work_time: float) -> None:
        with self.mu:
            ev = self.events.setdefault(key, threading.Event())
        def run():
            time.sleep(work_time)
            self.results[key] = f"receipt-{key}"     # 先存结果
            ev.set()                                 # 后唤醒
        threading.Thread(target=run).start()

    def poll(self, key: str, hold: float) -> str | None:
        with self.mu:
            ev = self.events.setdefault(key, threading.Event())
        if ev.wait(hold):
            return self.results[key]
        return None                                  # 对应 HTTP 202/204: 还没好

def client_await(server: Server, key: str, total: float, hold: float = 0.2):
    deadline = time.monotonic() + total              # 客户端总预算：绝对截止时间
    attempts = 0
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(f"{key} 在 {total} 秒内没有结果")
        attempts += 1
        r = server.poll(key, min(hold, remaining))   # 每轮最多挂 hold，且不超过剩余预算
        if r is not None:
            return r, attempts

s = Server()
s.submit("k1", work_time=0.5)
r, n = client_await(s, "k1", total=2.0)
print("拿到结果:", r, "| 多于一次轮询:", n > 1)
s.submit("k2", work_time=1.0)
try:
    client_await(s, "k2", total=0.5)
except TimeoutError as e:
    print("预算用尽:", e)
```

实际输出：

```
拿到结果: receipt-k1 | 多于一次轮询: True
预算用尽: k2 在 0.5 秒内没有结果
```

**变化。** 进程内等待者和领跑者同生共死；跨网络，服务端可能在两次轮询之间重启，所以结果必须能按键重新查到（持久化），事件只是加速唤醒的手段，不是真相来源。每一轮的挂起时间要比中间代理的超时短，否则请求会被中间层切断，客户端无法区分「没结果」与「断线」。

**代价。** 长轮询每个等待者占一个连接；等待者很多时改用推送（WebSocket、Webhook）或让客户端用退避重试代替。

**信号。** 一个操作耗时不确定、调用方要拿结果、重试不能重复执行（配合幂等键）。
