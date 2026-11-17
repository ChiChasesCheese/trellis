---
id: fsm-guards-actions-enter-hooks
node: fsm.guards-actions
type: qa
step: 3
---
## Q
预订可以被用户取消，也可以因为过期被系统取消，两条路径都要把名额还回去。这段“还名额”的代码该放在哪里？

## A
**放在进入状态的钩子里，所有路径共用**

- **进入钩子（on enter）**：每次转移落在某个状态，都会执行一遍；
- **放在转移的动作里的后果**：新增一条通向 `cancelled` 的路径（比如管理员取消）时，忘了加释放名额，名额永远少一个；
- **退出钩子（on exit）**：离开状态时做的清理，同理；
- **顺序的约定**：常见约定是退出旧状态、执行转移动作、进入新状态；用之前，确认你的实现采用什么顺序；
- **钩子只放“进入这个状态必然要做”的事**，和具体事件有关的事仍放在转移动作里。

```python
TABLE = {("active", "cancel"): "cancelled", ("active", "expire"): "cancelled"}

def release(ctx): ctx["free"] += 1
ON_ENTER = {"cancelled": release}

def fire(state, event, ctx):
    dst = TABLE[(state, event)]
    ON_ENTER.get(dst, lambda c: None)(ctx)       # 进入 cancelled：无论哪条路径
    return dst

for event in ("cancel", "expire"):
    ctx = {"free": 0}; fire("active", event, ctx); print(event, ctx)
# cancel {'free': 1} / expire {'free': 1}
```

**知识点：**守卫、动作和进出钩子（Guards, Actions, Hooks）
