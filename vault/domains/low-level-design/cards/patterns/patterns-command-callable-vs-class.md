---
id: patterns-command-callable-vs-class
node: patterns.command
type: qa
step: 2
---
## Q
Python 里什么时候一个 Command 只需要一个 callable（比如 `functools.partial`），什么时候必须写成类？

## A
如果调用只需要"执行一次、不用撤销、不用排队等待"，一个绑好参数的函数——`functools.partial(transfer, src, dst, amount)`——就是一个完整的 Command，不需要类。一旦要支持撤销（需要同时携带 `undo()` 和执行时产生的上下文，比如转账前的余额）、要放进队列反复检查状态、或者要序列化保存以便重放，就需要一个类：类能把"执行后的状态"和两个相关方法（`execute` / `undo`）绑在一起，一个裸函数做不到这一点。
