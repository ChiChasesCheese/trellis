---
id: craft-command-event-fact-4-frozen-envelope
node: craft.architecture.command-event-fact
type: qa
step: 4
---
## Q
**命令、事件与事实 · 通知的信封为什么冻结、重试为什么造新的**｜架构

通知服务把一次请求「物化」成交给短信、邮件渠道的信封：地址、标题、正文都已经渲染好。渠道发送失败要重试。信封应该可变（改 `attempt`），还是冻结后每次重试造一个新的？幂等键又怎么取？

## A
**要点。** 信封是事实：这一次、在这个渠道上、要发出的就是这些内容。它冻结，并且带齐渠道需要的一切（地址、标题、正文），这样渠道不必回头问服务，也就不必和服务争锁。重试用 `replace(envelope, attempt=n)` 造新的，旧的还留在历史里；幂等的粒度取「一次请求 × 一个渠道」：邮件成功、短信失败，重发短信时邮件不会再发。

```python
@dataclass(frozen=True, slots=True)
class Envelope:
    notification_id: str
    channel: str
    address: str
    title: str
    body: str
    attempt: int = 1
    @property
    def idempotency_key(self) -> str:
        return f"{self.notification_id}|{self.channel}"      # 一次请求 × 一个渠道

e1 = Envelope("n1", "sms", "+86-138", "验证码", "你的验证码是 123456")
e2 = replace(e1, attempt=2)                                   # 重试：造新的，不改旧的
print(e1.attempt, e2.attempt, e1.idempotency_key == e2.idempotency_key)
try:
    e1.attempt = 5
except FrozenInstanceError:
    print("信封改不动：provider 手里的就是发送当时的样子")
email = replace(e1, channel="email")
print("同一请求不同渠道，幂等键不同:", e1.idempotency_key != email.idempotency_key)
```

`e1` 是第 1 次尝试的短信信封，`email = replace(e1, channel="email")`，实际输出：

```
1 2 True
信封改不动：provider 手里的就是发送当时的样子
同一请求不同渠道，幂等键不同: True
```

**为什么。** 第一行说明 `e1.attempt` 仍是 1、`e2.attempt` 是 2，两次尝试的幂等键相同，所以接收方可以去重。第二行是对 `e1.attempt = 5` 抛的 `FrozenInstanceError`：渠道手里的对象不会在它发送途中被别的线程改掉。

**代价。** 每次重试多一个对象，但对象很小；比起可变信封的竞态（重试线程改了 attempt，发送线程还在读），冻结更便宜。
