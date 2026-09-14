---
id: patterns-command-when
node: patterns.behavioral
type: qa
---
## Q
Command turns a method call into an object. Name the three capabilities you buy that a plain call can't give, and the LLD problems where each shows up.

## A
Reifying `execute()` (plus receiver and args) as an object lets you:

- **Queue / schedule / log** invocations — thread-pool tasks, job queues, write-ahead logs, request replay.
- **Undo/redo** — each command carries `undo()` (or a memento); a history stack replays or reverts (text editor, drawing app).
- **Compose and parameterize** — macro commands, binding the same button to different actions, transactional batches.

Cost: one class (or lambda) per action. In languages with first-class functions, a bare lambda *is* a command — reach for the full pattern only when you need undo state or metadata alongside the action.

## Q zh
Command 把一个方法调用变成对象。列出三个你得到的能力是普通调用无法给的，以及每个出现在 LLD 问题中的位置。

## A zh
把 `execute()`（加上接收者和参数）具体化为对象让你能：

- **排队 / 调度 / 记录**调用——线程池任务、作业队列、预写日志、请求重放。
- **撤销/重做**——每个命令携带 `undo()`（或备忘录）；历史栈可以回放或恢复（文本编辑器、绘图应用）。
- **组合和参数化**——宏命令、将同一按钮绑定到不同动作、事务批处理。
