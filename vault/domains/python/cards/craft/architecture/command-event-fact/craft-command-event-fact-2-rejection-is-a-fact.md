---
id: craft-command-event-fact-2-rejection-is-a-fact
node: craft.architecture.command-event-fact
type: qa
step: 2
---
## Q
**命令、事件与事实 · 被拒绝的报单还要留下记录吗**｜架构

券商收到一张买单，资金不够，被拒绝了。命令失败了，是不是就当没发生过，不在订单表里留任何东西？

## A
**要点。** 命令可以失败，但失败本身是一条要留痕的事实：这张单在什么时间、被谁提交、因为什么被拒。券商的做法是先创建订单、登记进订单表，再检查资金，不够就把状态记为 `REJECTED` 然后抛异常。调用方得到异常，审计和客服能在订单表里查到这张被拒的单，对账时也不会出现「有人说下过单、系统里查无此单」。

```python
# 简化示意：只保留「先入表、再检查」的骨架；真实的 Brokerage.place_order 还要冻结、撮合、结算
class Status(Enum):
    OPEN = "open"
    REJECTED = "rejected"

@dataclass
class Order:
    id: str
    qty: int
    status: Status = Status.OPEN

class InsufficientFunds(Exception): ...

class Brokerage:
    def __init__(self, cash: int) -> None:
        self.cash, self.orders = cash, {}
    def place_order(self, oid: str, qty: int, price: int) -> Order:
        order = Order(oid, qty)
        self.orders[oid] = order                       # 先留痕
        if qty * price > self.cash:
            order.status = Status.REJECTED             # 被拒的报单也是一条事实
            raise InsufficientFunds(f"{oid} 需要 {qty * price}，只有 {self.cash}")
        self.cash -= qty * price
        return order

b = Brokerage(100)
b.place_order("O1", 5, 10)
try:
    b.place_order("O2", 10, 10)
except InsufficientFunds as e:
    print("抛出:", e)
print("留痕:", {k: v.status.value for k, v in b.orders.items()})
```

现金 100，先下一张 5 股 × 10 的单，再下一张 10 股 × 10 的单，实际输出：

```
抛出: O2 需要 100，只有 50
留痕: {'O1': 'open', 'O2': 'rejected'}
```

**为什么。** 「抛异常」告诉当前调用方失败了，「留痕」告诉将来的所有人发生过什么，两件事缺一不可。若只抛异常不留痕，失败只存在于一次调用栈里，调用栈一退出就没了。

**代价。** 被拒的单也占存储，需要有保留期；留痕本身不能再失败，所以放在能失败的检查之前（先写后查）。
