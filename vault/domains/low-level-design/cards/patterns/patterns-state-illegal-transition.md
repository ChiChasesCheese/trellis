---
id: patterns-state-illegal-transition
node: patterns.state
type: qa
step: 5
---
## Q
只用 `if`/`elif` 手写状态机，最容易在哪里出错？

## A
最容易漏掉的是"这个状态下不该发生的事件"——比如出货过程中又收到一次投币事件，手写分支往往默认沿用最后一个 `elif` 的逻辑而不是显式拒绝，悄悄破坏了不变量（比如多扣一次钱却没有多出一件货）。显式的转移表或 State 类天然会在查不到 `(state, event)` 组合时报错，而不是被动地默认处理。
