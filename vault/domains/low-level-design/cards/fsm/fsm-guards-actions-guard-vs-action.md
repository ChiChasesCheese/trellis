---
id: fsm-guards-actions-guard-vs-action
node: fsm.guards-actions
type: qa
step: 1
---
## Q
“连续出现第 3 次才算确认并产生开始事件”这种规则，在状态机里放在哪里？守卫（guard）和动作（action）怎么分？

## A
**守卫只读判断，动作才写入**

- **守卫**：一个返回布尔值的纯函数，决定这条转移能不能发生，不改任何东西；
- **动作**：转移发生时执行的副作用：记日志、发事件、更新计数；
- **同一（状态，事件）可以有几条候选**：按顺序试，第一条守卫通过的生效；
- **守卫没通过就不执行动作**：所以动作里的写入，不用担心“检查没通过也被执行了”；
- **没有一条适用**：抛错，不是悄悄落空。

```python
RULES = {("seen", "tick"): [                       # (目标, 守卫, 动作)，按顺序试
    ("confirmed", lambda c: c["n"] + 1 >= 3, lambda c: c["out"].append("start")),
    ("seen", lambda c: True, lambda c: c.__setitem__("n", c["n"] + 1)),
]}

def fire(state, event, ctx):
    for dst, guard, action in RULES[(state, event)]:
        if guard(ctx): action(ctx); return dst     # 守卫只读；通过了才执行动作
    raise ValueError("no transition")

ctx, s = {"n": 0, "out": []}, "seen"
for _ in range(3): s = fire(s, "tick", ctx)
print(s, ctx)                                      # confirmed {'n': 2, 'out': ['start']}
```

**知识点：**守卫、动作和进出钩子（Guards, Actions, Hooks）
