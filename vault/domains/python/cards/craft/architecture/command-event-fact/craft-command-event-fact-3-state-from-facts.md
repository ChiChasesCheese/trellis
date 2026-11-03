---
id: craft-command-event-fact-3-state-from-facts
node: craft.architecture.command-event-fact
type: qa
step: 3
---
## Q
**命令、事件与事实 · 为什么存「发放」和「扣费」这些事实，而不存余额**｜架构

额度系统收到一批发放和扣费。直接存一个可变的余额字段，看似最简单。后来发现有一笔发放被晚报了（t=2 发生，t=4 才到达），或者要查「t=3 时的余额」。存余额字段怎么应对？存事实呢？

## A
**要点。** 事实（发放、扣费）是追加进来的、不可变的记录；状态（余额、各额度包还剩多少）是对事实的计算结果，随用随算。事实被补录进来，状态自然跟着变，不需要回滚旧结果，也不需要写一套「修正余额」的逻辑；历史时点的状态只是只取到那个时间为止的事实。

```python
@dataclass(frozen=True)
class Grant:
    id: str
    amount: int
    at: int

@dataclass(frozen=True)
class Charge:
    id: str
    amount: int
    at: int

grants = {"g1": Grant("g1", 100, 1)}
charges = {"c1": Charge("c1", 30, 2), "c2": Charge("c2", 50, 3)}

def balance_as_of(t: int) -> int:                  # 余额不存，现算：事实 -> 状态
    return (sum(g.amount for g in grants.values() if g.at <= t)
            - sum(c.amount for c in charges.values() if c.at <= t))

print("t=2:", balance_as_of(2), "| t=3:", balance_as_of(3))
grants["g2"] = Grant("g2", 40, 2)      # 迟到的事实：t=2 就发了额度
print("补录 g2 后 t=2:", balance_as_of(2), "| t=3:", balance_as_of(3), "（不需要回滚任何旧结果）")
```

实际输出：

```
t=2: 70 | t=3: 20
补录 g2 后 t=2: 110 | t=3: 60 （不需要回滚任何旧结果）
```

**为什么。** 配送结算同理：配送员的取餐、到店、送达是四种生命周期事件，工资不存，每次现算；事后更正某个时间，只改那条事实。事实按键存在字典里（`dict[id, Grant]`），补录或更正同一个 id 是一次覆盖，重复投递天然幂等。

**代价。** 每次读都要重算，事实多了开销大；要么缓存派生状态并能从事实重建，要么给事实做快照（见真相与派生缓存）。
