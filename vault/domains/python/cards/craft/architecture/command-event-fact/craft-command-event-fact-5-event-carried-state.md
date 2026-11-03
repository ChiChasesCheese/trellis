---
id: craft-command-event-fact-5-event-carried-state
node: craft.architecture.command-event-fact
type: qa
step: 5
---
## Q
**命令、事件与事实 · 事件驱动架构里命令和事件的语义差别**｜架构

服务之间用消息通信：「取款」是发给账户服务的请求，「已取款」是账户服务广播出去的通知。两者都是消息，在命名、失败处理、幂等上各有什么不同？事件要带多少信息才不需要消费者回头查询？

## A
**要点。** 命令（`Withdraw`）发给一个处理者，用祈使式命名，可以被拒绝，要带发起方生成的幂等键，重试返回第一次的结果。事件（`Withdrawn`）广播给任意多消费者，用过去式命名，不能被拒绝，只能被忽略；消费者靠事件自带的状态更新自己（事件携带状态转移，event-carried state transfer），按 `event_id` 去重，因为投递至少一次。

```python
@dataclass(frozen=True)
class Command:                    # 祈使：发给一个处理者，可以被拒绝
    name: str
    key: str                      # 幂等键：由发起方生成
    amount: int

@dataclass(frozen=True)
class Event:                      # 过去式：广播给任意多消费者，不能被拒绝，只能被忽略
    event_id: str
    name: str
    account: str
    new_balance: int              # 事件携带状态（event-carried state transfer）

class Account:
    def __init__(self) -> None:
        self.balance, self.done = 100, {}
    def handle(self, cmd: Command) -> Event | str:
        if cmd.key in self.done:
            return self.done[cmd.key]                   # 命令重试：返回第一次的结果
        if cmd.amount > self.balance:
            result = "rejected: insufficient"           # 命令可以被拒绝，拒绝也是结果
        else:
            self.balance -= cmd.amount
            result = Event(f"ev-{cmd.key}", "Withdrawn", "A", self.balance)
        self.done[cmd.key] = result
        return result

class ReadModel:                  # 消费者：靠事件自带的状态更新，不回头调用账户服务
    def __init__(self) -> None:
        self.seen, self.balance = set(), None
    def on_event(self, e: Event) -> None:
        if e.event_id in self.seen:
            return                                        # 至少一次投递：按 event_id 去重
        self.seen.add(e.event_id)
        self.balance = e.new_balance                    # 靠事件自带的状态更新，不回头查

acct, rm = Account(), ReadModel()
r1 = acct.handle(Command("Withdraw", "k1", 30))
r1_retry = acct.handle(Command("Withdraw", "k1", 30))     # 客户端超时重试
r2 = acct.handle(Command("Withdraw", "k2", 500))
for ev in (r1, r1_retry):                                 # 同一个事件被投递了两次
    rm.on_event(ev)
print("命令重试同一结果:", r1 is r1_retry, "| 超额命令:", r2)
print("读模型余额:", rm.balance, "| 账户余额:", acct.balance)
```

余额 100，取 30（重试一次，同一个键），再取 500，把同一个事件投递两次给读模型，实际输出：

```
命令重试同一结果: True | 超额命令: rejected: insufficient
读模型余额: 70 | 账户余额: 70
```

**为什么。** 事件只带「变了什么」（金额 30）也可以，但消费者要从自己保存的旧状态算新状态，漏一条、乱序就错；带上新余额让消费者直接覆盖，漏了中间几条也能追上，代价是消息更大、耦合到账户的数据结构，而且乱序到达时旧事件会覆盖新状态，所以事件还要带版本号，消费者只接受更大的版本。

**易错。** 事件的字段是契约：加字段要向后兼容，删字段会弄坏不知情的消费者。
