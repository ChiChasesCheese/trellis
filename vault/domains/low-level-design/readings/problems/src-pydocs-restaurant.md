---
nodes: [problems.booking.restaurant]
url: https://docs.python.org/3/library/dataclasses.html
---
# dataclasses — Data Classes

值得读：官方文档对 `frozen=True`、`slots=True` 的语义说明，是本文 `MenuItem`、
`Reservation`、`WaitlistEntry`、`SeatingResult` 这几个不可变记录类型的直接依据——
`frozen=True` 禁止属性被重新赋值，`slots=True` 省掉每个实例的 `__dict__`，两者合在一起
既表达了"这是一份不该被改的快照"，也避免了误加一个没有声明过的属性。
