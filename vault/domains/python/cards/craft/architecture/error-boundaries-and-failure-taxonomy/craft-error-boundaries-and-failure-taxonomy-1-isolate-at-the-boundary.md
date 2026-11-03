---
id: craft-error-boundaries-and-failure-taxonomy-1-isolate-at-the-boundary
node: craft.architecture.error-boundaries-and-failure-taxonomy
type: qa
step: 1
---
## Q
**错误边界与失败分类 · 一个订阅者出错，凭什么不能影响别的订阅者**｜架构

紧急通知系统把一条火警依次发给多个订阅者的处理函数。订阅者 A 的函数有 bug 抛了异常。如果发布者直接循环调用，后面的订阅者 B 会怎样？异常该由谁处理、处理之后什么信息必须留下来？

## A
**要点。** 在两个模块的边界上隔离别人的故障，边界内保留自己的失败原因。发布者调用订阅者代码，就是调用不受自己控制的代码：用 `try/except Exception` 包住每一次调用，失败换成一条死信记录（DeadLetter：哪个订阅者、哪条消息、什么错误），继续发给下一个。吞掉异常的同时，必须留下计数、死信或日志，否则故障就消失了，没人知道。

```python
def good(msg: str) -> None: print("  订阅者 B 收到", msg)
def bad(msg: str) -> None: raise ValueError("订阅者 A 自己的 bug")

@dataclass(frozen=True)
class DeadLetter:
    handler: str
    msg: str
    error: str

def publish_naive(msg: str, handlers) -> None:
    for h in handlers:
        h(msg)                                  # A 抛了，B 永远收不到

def publish(msg: str, handlers, dead: list[DeadLetter]) -> None:
    for h in handlers:
        try:
            h(msg)
        except Exception as exc:                # 边界：隔离别人的故障
            dead.append(DeadLetter(h.__name__, msg, f"{type(exc).__name__}: {exc}"))   # 留下原因

try:
    publish_naive("火警", [bad, good])
except ValueError as e:
    print("朴素版：B 没收到，异常冲到发布者:", e)

dead: list[DeadLetter] = []
publish("火警", [bad, good], dead)
print("隔离版死信:", dead)
```

`bad` 抛 `ValueError`，`good` 打印收到，两种发布方式各发一次「火警」，实际输出：

```
朴素版：B 没收到，异常冲到发布者: 订阅者 A 自己的 bug
  订阅者 B 收到 火警
隔离版死信: [DeadLetter(handler='bad', msg='火警', error='ValueError: 订阅者 A 自己的 bug')]
```

**为什么。** 朴素版有两层伤害：B 收不到火警，发布者自己的调用栈还被订阅者的 bug 带走。文件监听器的回调同样如此：回调抛异常只记进失败列表，不影响其他回调。

**代价。** 吞异常最大的风险是静默：只有计数没有人看，等于没处理。死信要有出口（告警、重放），否则只是换了个地方丢。
