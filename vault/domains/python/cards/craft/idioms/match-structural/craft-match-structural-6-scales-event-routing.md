---
id: craft-match-structural-6-scales-event-routing
node: craft.idioms.match-structural
type: qa
step: 6
---
## Q
**结构化模式匹配 · 从语法树求值到按事件类型路由**｜写法

LeetCode 的表达式求值按节点类型分派，LLD 的表格引擎也是。放到系统层面，「按事件种类分派到处理器」有两种常见写法：一个集中的 `match`，或者一张订阅表。怎么选？

## A
**要点。** 同一个问题：给定一个有形状的数据，调用对应的处理逻辑。`match` 是**集中分派**：所有种类在一个函数里，加一种就改这个函数，缺一种在代码里一眼可见。订阅表（registry）是**分散分派**：处理器自己登记它关心的事件类型，调度代码不变，同一事件可以有多个独立的处理器。

```python
@dataclass(frozen=True)
class Paid: order: str
@dataclass(frozen=True)
class Shipped: order: str; carrier: str
@dataclass(frozen=True)
class Refunded: order: str; amount: int

# 1) match：集中在一处，漏了哪种事件一眼可见；新增类型要改这里
def handle_match(e):
    match e:
        case Paid(o): return f"开票 {o}"
        case Shipped(o, c): return f"通知 {o} 由 {c} 配送"
        case Refunded(o, a): return f"退款 {o} {a}"

# 2) 订阅表：处理器自己注册，新增事件类型不改调度代码
HANDLERS: dict[type, list] = {}
def on(cls):
    def deco(fn):
        HANDLERS.setdefault(cls, []).append(fn); return fn
    return deco
def dispatch(e):
    return [h(e) for h in HANDLERS.get(type(e), [])]

@on(Paid)
def invoice(e): return f"开票 {e.order}"
@on(Paid)
def audit(e): return f"审计 {e.order}"          # 同一事件可以有多个独立的处理器

print(handle_match(Shipped("o1", "SF")))
print(dispatch(Paid("o1")))
print(dispatch(Refunded("o1", 5)), "<- 没人订阅: 静默丢弃, 需要显式处理")
```

实际输出：

```
通知 o1 由 SF 配送
['开票 o1', '审计 o1']
[] <- 没人订阅: 静默丢弃, 需要显式处理
```

**选择依据。** 事件种类固定、一个事件由一个地方负责处理、想让漏处理变得显眼：`match`（配合 `assert_never`）。种类会持续增加、不同团队各自处理同一个事件、处理器可以插拔：订阅表。消息系统（Kafka 主题 + 消费者组）是订阅表放大到分布式的样子。

**代价。** 订阅表的问题是「没人订阅」时事件被静默丢弃，要显式决定：报警、记入死信、还是忽略。`match` 的代价是调度函数成为所有人都要改的热点，改动冲突和耦合都集中在它身上。

**信号。** 看到 `if event.type == "..." elif ...` 一长串，先问：种类是封闭的还是开放的。
