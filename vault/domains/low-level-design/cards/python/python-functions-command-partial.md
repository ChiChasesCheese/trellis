---
id: python-functions-command-partial
node: python.first-class-functions
type: qa
step: 3
tags: [grown]
---
## Q
`functools.partial` 在实现“命令模式（Command）”时解决了什么问题？

## A
Command 模式要把“一次调用加它的参数”打包成一个可以延迟执行、可以存进撤销栈的对象。`functools.partial(func, *args, **kwargs)` 恰好把函数和它的部分/全部参数绑定成一个新的可调用对象——不用手写一个只存 `func` 和参数、只有一个 `execute()` 方法的 `Command` 类。
```python
from functools import partial

undo_stack = []
def move(entity, dx, dy):
    entity.x += dx; entity.y += dy

cmd = partial(move, player, 1, 0)
undo_stack.append(partial(move, player, -1, 0))  # 撤销动作
cmd()
```
