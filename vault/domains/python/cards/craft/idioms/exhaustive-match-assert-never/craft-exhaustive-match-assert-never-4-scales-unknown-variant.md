---
id: craft-exhaustive-match-assert-never-4-scales-unknown-variant
node: craft.idioms.exhaustive-match-assert-never
type: qa
step: 4
---
## Q
**穷尽性检查 · 从 `assert_never` 到协议演进时遇到未知事件类型**｜写法

进程内，枚举新增了成员，类型检查器能指出漏处理的地方。放到分布式里，生产者先上线了新事件类型，消费者还是旧版本。消费者收到一个它不认识的事件，应该忽略、崩溃，还是别的？

## A
**要点。** 进程内的穷尽性靠编译期检查，因为所有代码在同一次构建里。跨服务时不存在这样的检查点：生产者和消费者独立发布，新类型一定会在某一刻先到达旧消费者。所以消费者必须**显式处理「不认识」这个分支**，而不是静默丢弃：记入死信队列（dead-letter queue）、报警，让人决定是升级消费者还是忽略。多余的**字段**则可以放心忽略（向前兼容）；缺少**必填字段**或**未知类型**才是该显式失败的。

```python
@dataclass(frozen=True)
class Paid: order: str
@dataclass(frozen=True)
class Refunded: order: str; amount: int

KNOWN = {"paid": Paid, "refunded": Refunded}
dead_letters: list[str] = []

def decode(raw: str):
    msg = json.loads(raw)
    cls = KNOWN.get(msg["type"])
    if cls is None:                                  # 生产者先发布了新类型
        dead_letters.append(raw)                     # 显式失败: 进死信, 报警, 不静默丢
        return None
    fields = {k: v for k, v in msg.items() if k != "type" and k in cls.__dataclass_fields__}
    return cls(**fields)                             # 未知的多余字段可以忽略, 缺必填字段会报错

print(decode('{"type": "paid", "order": "o1", "coupon": "x"}'))
print(decode('{"type": "chargeback", "order": "o1"}'))
print("死信:", dead_letters)
```

实际输出：

```
Paid(order='o1')
None
死信: ['{"type": "chargeback", "order": "o1"}']
```

**变化。** `assert_never` 的位置从 `match` 的最后一个分支，变成了「未知类型」的死信处理。目的相同：新情况出现时有人知道。区别在于它不是崩溃：崩溃会让整条消息流卡在这一条上，死信让流继续、问题可追。

**代价。** 死信队列需要有人看，不监控的死信和静默丢弃没有区别；先发布消费者、后发布生产者，是消除这个问题最便宜的发布顺序。

**信号。** 一个枚举或联合类型会在多个代码位置被分派，或者跨服务传递类型标签。
