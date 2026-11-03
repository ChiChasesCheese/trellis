---
id: craft-lock-hierarchy-and-reentrancy-5-service-call-graph
node: craft.architecture.lock-hierarchy-and-reentrancy
type: qa
step: 5
---
## Q
**调用方向与可重入 · 微服务之间为什么调用图也要无环**｜架构

服务 A 同步调用服务 B，B 在处理里又同步调用 A，每个服务的线程池只有少量线程。没有任何一把「锁」，为什么还会死锁？这和进程内的锁序是什么关系？

## A
**要点。** 线程池里的工作线程就是一种有限资源，和锁同类：A 的唯一线程在等 B 的答案，B 的唯一线程在等 A 的答案，A 的线程被占着，B 对 A 的请求只能排队，两边都等不到。这和锁序环是同一个结构：依赖图里有环加上资源有限，就可能互相等待。对策也相同：调用图保持无环（分层，只允许上层调下层），必须反向时改为异步事件，不同步等待。

```python
A = ThreadPoolExecutor(max_workers=1)          # 服务 A：只有一个工作线程
B = ThreadPoolExecutor(max_workers=1)          # 服务 B

def b_handler() -> str:
    return A.submit(lambda: "A 的答案").result(timeout=0.5)     # B 同步回调 A

def a_handler() -> str:
    return B.submit(b_handler).result(timeout=0.5)              # A 同步调用 B

try:
    print(A.submit(a_handler).result(timeout=2))
except TimeoutError:
    print("A 等 B，B 等 A：谁都等不到，只剩超时")

# 无环：A 调 B，B 只返回结果，不回头调 A
def b_handler_pure() -> str:
    return "B 的答案"                                            # 无环：B 只返回结果
def a_handler_ok() -> str:
    return B.submit(b_handler_pure).result(timeout=0.5)
print(A.submit(a_handler_ok).result(timeout=2))
A.shutdown(wait=False, cancel_futures=True); B.shutdown(wait=False, cancel_futures=True)
```

先跑 `A.submit(a_handler)`，再跑 `A.submit(a_handler_ok)`（各等 2 秒），实际输出：

```
A 等 B，B 等 A：谁都等不到，只剩超时
B 的答案
```

**为什么。** 超时让这个示例只是报错而不是永远卡住；生产里没有超时的同步调用链才是永久卡死。线程池越大、请求越少，越不容易触发，所以这种问题常常只在流量高峰才暴露。

**信号。** 画服务调用图时出现环，或者发现「回调上游」的接口：改成分层，或把反向通知改成事件。
