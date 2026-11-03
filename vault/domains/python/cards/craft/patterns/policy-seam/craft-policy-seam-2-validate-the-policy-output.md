---
id: craft-policy-seam-2-validate-the-policy-output
node: craft.patterns.policy-seam
type: qa
step: 2
---
## Q
**策略接缝 · 接缝两侧各自负责什么：给策略什么、对它的返回值信不信**｜架构

送餐机器人餐厅里，「哪台空闲机器人接这张单」是可替换的策略。策略函数拿到的应该是真正的机器人对象，还是别的东西？如果有人写的策略返回了一个不在候选里的编号，引擎该怎么办？

## A
**要点。** 接缝要窄、方向要明确。引擎给策略一份只读快照（`RobotView`，frozen dataclass），策略只能返回一个编号，没法直接改机器人，也没法拿到未来可能会误用的内部引用。引擎再把策略的返回值当成「不可信输入」校验：不在候选里就抛 `PolicyError`，而不是默默派出一个不可用的机器人。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class RobotView:                 # 只读快照：策略改不了真机器人
    id: int; battery: int

class PolicyError(RuntimeError): ...

def most_battery(candidates):
    best = max(candidates, key=lambda r: (r.battery, -r.id), default=None)   # 同电量取编号小的
    return None if best is None else best.id

def rogue(candidates): return 99                       # 一个写错的策略

def dispatch(candidates, policy):
    chosen = policy(candidates)
    if chosen is None: return None                     # 没人可派
    if chosen not in {c.id for c in candidates}:       # 引擎不信任策略的返回值
        raise PolicyError(f"策略选了不可用的机器人 {chosen}")
    return chosen

cands = [RobotView(1, 40), RobotView(2, 90), RobotView(3, 90)]
print("most_battery ->", dispatch(cands, most_battery))
try: dispatch(cands, rogue)
except PolicyError as e: print(e)
```

实际输出（`most_battery` 取电量最多、同电量取小编号；`rogue` 永远返回 99）：

```
most_battery -> 2
策略选了不可用的机器人 99
```

**为什么。** 策略是别人（或以后的你）写的代码，它出 bug 的方式是返回错误的值，而不是抛异常。引擎若直接信任，错误会推迟到「一个根本在充电的机器人被派去送餐」那一刻才露面，离原因很远。在接缝处校验，错误紧挨着肇事的策略。

**代价。** 每次分派多一次集合构建；候选很多时要预先建好，或者让策略返回候选对象本身而不是编号。

**易错。** 给策略传可变的内部对象是最常见的泄漏：策略顺手改了一个字段，核心的不变量就被绕过了。
