---
id: craft-error-boundaries-and-failure-taxonomy-6-compensation-and-http
node: craft.architecture.error-boundaries-and-failure-taxonomy
type: qa
step: 6
---
## Q
**错误边界与失败分类 · 补偿动作自己也失败了，该吞还是该报；系统层面这套分类叫什么**｜架构

下单流程是一串步骤（预留库存 → 扣款 → 发货），某步失败就先补偿失败的那一步本身、再倒序补偿已完成的步骤。若「发货」失败，回滚「扣款」时退款接口又超时了，这个二次失败该怎么办？放大到服务之间，状态码和重试策略如何对应这套分类？

## A
**要点。** 补偿失败不能吞：它意味着系统里留下了需要人工处理的残留（钱扣了没退）。订单的 Saga 失败时抛出的 `SagaFailure` 带着三样东西：失败的步骤、原始异常、补偿阶段失败的列表，调用方一次拿全。服务之间同理，失败要分「可重试」（429、503、gRPC 的 UNAVAILABLE）和「不可重试」（400 请求错、409 冲突），重试用尽进死信并告警。

```python
class Residue(Exception):
    def __init__(self, step, cause, errors):
        super().__init__(f"步骤「{step}」失败：{cause}")
        self.errors = errors

def run(steps):                              # steps: [(名字, 动作, 补偿)]
    done = []
    for name, act, undo in steps:
        try:
            act()
        except Exception as exc:
            errors = []
            # 失败的这一步排在最前（动作不是原子的），再倒序补偿已完成的
            for n, u in [(name, undo), *reversed(done)]:
                try:
                    u()
                except Exception as ce:
                    errors.append((n, str(ce)))   # 不吞：这是需要人工处理的残留
            raise Residue(name, exc, tuple(errors)) from exc
        done.append((name, undo))

def ok(): pass
def refund_timeout(): raise TimeoutError("退款接口超时")
def no_stock(): raise RuntimeError("仓库无货")

try:
    run([("预留库存", ok, ok), ("扣款", ok, refund_timeout), ("发货", no_stock, ok)])
except Residue as r:
    print(r)
    print("补偿也失败了:", list(r.errors))
```

三步：预留库存、扣款（补偿会超时）、发货（动作失败）。失败的「发货」自己的补偿排在最前，再倒序补偿「扣款」「预留库存」；退款超时被收进 `errors`，没有掩盖原始异常。实际输出：

```
步骤「发货」失败：仓库无货
补偿也失败了: [('扣款', '退款接口超时')]
```

**为什么。** 重试只对瞬时错误有用：对 400 重试一百次还是 400，只会放大流量。分类写进枚举，重试循环就只看一个布尔：

```python
class Failure(Enum):
    INVALID = (400, False)           # 请求本身错，重试没用
    RATE_LIMITED = (429, True)       # 稍后重试
    UNAVAILABLE = (503, True)        # 瞬时故障，退避重试
    def __init__(self, http, retryable):
        self.http, self.retryable = http, retryable

def call_with_retry(outcomes, max_attempts=3):    # outcomes: 每次尝试的结果，None 表示成功
    for attempt, o in enumerate(outcomes, start=1):
        if o is None:
            return f"第 {attempt} 次成功"
        if not o.retryable:
            return f"第 {attempt} 次 {o.http} 不重试，直接报给调用方"
        if attempt == max_attempts:
            return f"重试 {attempt} 次用尽 -> 死信 + 告警"

U, R, I = Failure.UNAVAILABLE, Failure.RATE_LIMITED, Failure.INVALID
for outcomes in ([U, R, None], [I, None], [U, U, U, None]):
    print(call_with_retry(outcomes))
```

三组结果依次是：先 503、再 429、第三次成功；一开始就是 400；连续三次 503，第四次本来会成功但已用尽次数。实际输出：

```
第 3 次成功
第 1 次 400 不重试，直接报给调用方
重试 3 次用尽 -> 死信 + 告警
```

**代价。** 补偿要幂等，这样在不确定「对方到底做成没有」时可以放心调用：对没扣过款的单子退款应是无操作；做不到就只能人工兜底。
