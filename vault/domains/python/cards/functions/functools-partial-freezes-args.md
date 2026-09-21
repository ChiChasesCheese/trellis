---
id: functools-partial-freezes-args
node: functions.functools
type: qa
source: python-docs
---
## Q
`functools.partial(log, subsystem='server')` 这行代码做了什么？之后调用 `server_log('msg')` 实际执行的是什么？

## A
`partial(func, *args, **kwargs)` 返回一个新的可调用对象，把某些位置参数或关键字参数预先「冻结」在里面；这里 `subsystem='server'` 被固定住，产生的 `server_log` 相当于一个只需要传 `message` 的新函数。调用 `server_log('msg')` 时，实际执行的是 `log('msg', subsystem='server')`——调用时新传入的参数会拼接、或覆盖到预先固定的参数之后。
