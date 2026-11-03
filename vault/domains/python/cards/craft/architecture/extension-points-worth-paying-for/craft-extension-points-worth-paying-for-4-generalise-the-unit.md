---
id: craft-extension-points-worth-paying-for-4-generalise-the-unit
node: craft.architecture.extension-points-worth-paying-for
type: qa
step: 4
---
## Q
**值得付费的扩展点 · 叫车系统里拼车是怎么在不改状态机的前提下加进来的**｜架构

叫车系统前几关是一位乘客一趟行程，有一个状态机（已请求 → 行程中 → 已完成）。第 4 关要支持拼车：同一辆车同时载两位乘客，各自上下车点不同、各自结算。是再造一个拼车模型，还是改造原来的行程？

## A
**要点。** 把「一位乘客的那一段」抽成 `RideLeg`（乘客、占几个座、上下车点、各自的费率），行程是一组腿的列表。一个人的行程是一条腿，拼车是两条腿，同一种东西；状态机只关心行程整体的状态，不认人数，所以一行不改。要预先付的费用，就是第 1 关把乘客相关的信息放在一个小对象里，而不是平铺在行程上。

```python
class State(Enum):
    REQUESTED = 1; ONGOING = 2; DONE = 3
ALLOWED = {State.REQUESTED: {State.ONGOING}, State.ONGOING: {State.DONE}, State.DONE: set()}

@dataclass(frozen=True)
class RideLeg:                      # 一位乘客的那一段
    rider: str
    seats: int
    km: int

@dataclass
class Trip:
    legs: list[RideLeg] = field(default_factory=list)
    state: State = State.REQUESTED
    def transition_to(self, s: State) -> None:       # 状态机：只认行程，不认人数
        if s not in ALLOWED[self.state]:
            raise ValueError(f"{self.state.name} -> {s.name}")
        self.state = s
    def fares(self) -> dict[str, int]:
        return {leg.rider: 10 + 2 * leg.km for leg in self.legs}

solo = Trip([RideLeg("甲", 1, 8)])
pool = Trip([RideLeg("甲", 1, 8), RideLeg("乙", 2, 5)])    # 第 4 关：拼车只是多一条腿
for t in (solo, pool):
    t.transition_to(State.ONGOING); t.transition_to(State.DONE)
    print(len(t.legs), "条腿", t.state.name, t.fares())
```

一人行程和两人拼车各走一遍「行程中 → 已完成」，实际输出：

```
1 条腿 DONE {'甲': 26}
2 条腿 DONE {'甲': 26, '乙': 20}
```

**为什么。** 相比之下，另造一个 `PoolTrip` 类，要复制状态机、重做并发与取消逻辑，两套模型之后永远要同步改。把「单位」选对（腿，不是行程），后续的变体就只是数量变化。

**信号。** 需求里出现「同一个东西可以有多个」（多乘客、多收件人、多币种），先问：现在这个类里哪些字段其实是「每个参与者一份」，把它们提出来。
