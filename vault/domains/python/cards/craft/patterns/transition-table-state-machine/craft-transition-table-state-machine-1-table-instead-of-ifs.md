---
id: craft-transition-table-state-machine-1-table-instead-of-ifs
node: craft.patterns.transition-table-state-machine
type: qa
step: 1
---
## Q
**转移表状态机 · 为什么把「哪个状态能去哪」写成数据**｜模式

订单有 NEW、PAID、SHIPPED、CANCELLED 几个状态，事件有付款、发货、取消。常见的写法是每个方法里各写一段 `if self.status == ...`。方法一多，规则散在各处，改一个状态要翻遍所有方法。有更好的组织方式吗？怎么保证没漏掉任何组合？

## A
**要点。** 把规则写成一张表：键是（当前状态，事件），值是新状态。表里没有的组合一律非法。新增状态只改表，每个方法不再重写 `if`，整张表能被穷举测试盖满。

```python
class S(Enum):
    NEW = auto(); PAID = auto(); SHIPPED = auto(); CANCELLED = auto()

class E(Enum):
    PAY = auto(); SHIP = auto(); CANCEL = auto()

TRANSITIONS: dict[tuple[S, E], S] = {      # 表里没有的组合一律非法
    (S.NEW, E.PAY): S.PAID,
    (S.NEW, E.CANCEL): S.CANCELLED,
    (S.PAID, E.SHIP): S.SHIPPED,
    (S.PAID, E.CANCEL): S.CANCELLED,
}

class IllegalTransition(Exception): ...

class Order:
    def __init__(self) -> None:
        self.state = S.NEW

    def fire(self, event: E) -> None:
        try:
            nxt = TRANSITIONS[(self.state, event)]
        except KeyError:                        # 绝不静默忽略
            raise IllegalTransition(f"{self.state.name} 不能 {event.name}") from None
        self.state = nxt

# 穷举测试：所有 (状态, 事件) 组合，行为必须与表一致
legal = illegal = 0
for s, e in product(S, E):
    o = Order(); o.state = s
    try:
        o.fire(e)
        assert TRANSITIONS[(s, e)] is o.state
        legal += 1
    except IllegalTransition:
        assert (s, e) not in TRANSITIONS and o.state is s    # 非法时状态原地不动
        illegal += 1
print(f"{len(S)}x{len(E)}={legal + illegal} 个组合：合法 {legal}，非法 {illegal}")
```

4 个状态 × 3 个事件的穷举测试，实际输出：

```
4x3=12 个组合：合法 4，非法 8
```

**为什么。** 非法转移必须抛异常。静默忽略会让「已发货的订单被取消」变成日志里看不见的 bug。

**代价。** 表只回答「流程上合不合法」，不回答「余额够不够」。后者是守卫，见下一张卡。
