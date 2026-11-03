---
id: craft-transition-table-state-machine-2-guards-vs-table
node: craft.patterns.transition-table-state-machine
type: qa
step: 2
---
## Q
**转移表状态机 · 余额不足、缺货为什么不放进转移表**｜模式

自动售货机里「已投币」状态下选择商品，表里写着（COIN_INSERTED, SELECT）→ DISPENSING。可是钱不够或缺货时不应该出货。能不能把「钱不够」也编成一个状态？

## A
**要点。** 不要。转移表只回答流程是否合法；金额、库存这类数据条件是守卫（guard），在转移之前检查，失败时状态原地不动。混进表里，状态数会随数据取值爆炸（钱不够、钱刚好、钱多、缺货……），而表应该是一个小而稳定的集合。

```python
class State(Enum):
    IDLE = auto(); COIN_INSERTED = auto(); DISPENSING = auto()

class Event(Enum):
    PAY = auto(); SELECT = auto()

TRANSITIONS = {
    (State.IDLE, Event.PAY): State.COIN_INSERTED,
    (State.COIN_INSERTED, Event.PAY): State.COIN_INSERTED,
    (State.COIN_INSERTED, Event.SELECT): State.DISPENSING,
}

class Machine:
    def __init__(self, price: dict[str, int], stock: dict[str, int]) -> None:
        self.state, self.credit, self.price, self.stock = State.IDLE, 0, price, stock

    def _go(self, event: Event) -> State:
        nxt = TRANSITIONS.get((self.state, event))
        if nxt is None:
            raise RuntimeError(f"{self.state.name} 下不能 {event.name}")   # 流程不合法
        return nxt

    def pay(self, cents: int) -> None:
        nxt = self._go(Event.PAY)
        self.credit += cents
        self.state = nxt

    def select(self, item: str) -> None:
        nxt = self._go(Event.SELECT)          # 1. 表：流程上能不能选
        if self.stock[item] == 0:             # 2. 守卫：缺货
            raise ValueError("缺货")
        if self.credit < self.price[item]:    # 2. 守卫：钱不够
            raise ValueError("余额不足")
        self.stock[item] -= 1                 # 3. 都过了才改状态
        self.credit -= self.price[item]
        self.state = nxt

m = Machine({"cola": 150}, {"cola": 3})
m.pay(100)
try:
    m.select("cola")
except ValueError as e:
    print("守卫拒绝:", e, "-> 状态仍是", m.state.name, "余额", m.credit)
m.pay(100)
m.select("cola")
print("成交 ->", m.state.name, "余额", m.credit, "库存", m.stock["cola"])
try:
    m.select("cola")
except RuntimeError as e:
    print("表拒绝:", e)
```

投 100 选 150 的可乐，再补投成交，再选一次，实际输出：

```
守卫拒绝: 余额不足 -> 状态仍是 COIN_INSERTED 余额 100
成交 -> DISPENSING 余额 50 库存 2
表拒绝: DISPENSING 下不能 SELECT
```

**为什么。** 守卫失败状态不动，用户可以继续补投币；这和先校验后提交是同一个想法，表的查询是校验段的第一步。

**易错。** 先改库存、后查表，查表失败时库存已经被扣了。
