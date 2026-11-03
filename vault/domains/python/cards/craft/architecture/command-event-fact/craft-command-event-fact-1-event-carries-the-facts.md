---
id: craft-command-event-fact-1-event-carries-the-facts
node: craft.architecture.command-event-fact
type: qa
step: 1
---
## Q
**命令、事件与事实 · 通知订阅者时，传整个管理器，还是传一个事件对象**｜架构

分账系统新增支出后要通知订阅者（比如活动记录）。一种写法是把管理器本身递给订阅者，让它自己回头查；另一种是构造一个事件对象，里面写清楚发生了什么。订阅者稍后才处理消息，两种写法看到的内容有什么区别？

## A
**要点。** 事件是已经发生的事实：过去式命名、冻结、自带订阅者需要的全部信息。回头查询看到的是「现在」的状态，不是「事件发生那一刻」的状态；订阅者处理得越晚，两者差得越多，还可能读到另一个线程改了一半的数据。命令（`add_expense`）是祈使式的请求，可能失败；事件（`ExpenseAdded`）一旦发出就不能失败。

```python
@dataclass(frozen=True)
class ExpenseAdded:                     # 过去式：已经发生的事，冻结
    summary: str
    amount: int

class Manager:
    def __init__(self) -> None:
        self.total = 0
        self.subs_thin, self.subs_fat = [], []
    def add_expense(self, amount: int) -> None:                 # 命令：祈使式，可能失败
        if amount <= 0:
            raise ValueError("金额必须大于 0")
        self.total += amount
        for s in self.subs_thin:
            s(self)                         # 薄通知：递整个管理器，让订阅者回头查
        for s in self.subs_fat:
            s(ExpenseAdded(f"新增支出 {amount}", amount))   # 厚事件：发生了什么都在里面

m = Manager()
thin_view, fat_view = [], []
queue: list = []
m.subs_thin.append(lambda mgr: queue.append(mgr))               # 订阅者先排队，稍后处理
m.subs_fat.append(lambda e: fat_view.append(e.amount))

m.add_expense(30)
m.add_expense(50)                                              # 订阅者还没来得及处理第一条
for mgr in queue:
    thin_view.append(mgr.total)                                 # 回头查：看到的是「现在」，不是「当时」
print("回头查的订阅者看到的累计:", thin_view)
print("读事件的订阅者看到的每笔:", fat_view)
```

订阅者先把消息排进队列，连续加两笔支出（30、50）后才处理，实际输出：

```
回头查的订阅者看到的累计: [80, 80]
读事件的订阅者看到的每笔: [30, 50]
```

**为什么。** 回头查的订阅者两条消息都看到 80，第一条消息对应的 30 丢了；读事件的订阅者能还原每一笔。事件自带信息，在锁外通知也不会读到半成品。

**易错。** 事件里放的是订阅者必需的事实，不要塞整个内部对象（账本、用户表）：那样订阅者又能绕过锁去读写内部状态。
