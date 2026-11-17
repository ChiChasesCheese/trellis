---
id: fsm-testing-exhaustive-matrix
node: fsm.testing
type: qa
step: 1
---
## Q
状态机的测试，只测几条正常路径够吗？怎么保证每一个（状态，事件）组合都有明确的期望？

## A
**穷举状态和事件的笛卡尔积，每格要么合法要么拒绝**

- **每格一个期望**：合法的写目标状态，非法的写“拒绝”；
- **漏格即失败**：期望表缺一格就报错；新增状态或事件时，测试逼你把新行填满，不会悄悄漏掉；
- **期望由你写**：表是按合同手写的，不要从实现的表里复制，否则测的是自己；
- **规模**：几个状态乘几个事件是几十个格子，一次参数化就能跑完。

```python
from itertools import product

TABLE = {("pending", "disburse"): "active", ("active", "settle"): "repaid"}
def fire(s, e):
    if (s, e) not in TABLE: raise ValueError((s, e))
    return TABLE[(s, e)]

STATES, EVENTS = ["pending", "active", "repaid"], ["disburse", "settle"]
WANT = {("pending", "disburse"): "active", ("pending", "settle"): None,
        ("active", "disburse"): None, ("active", "settle"): "repaid",
        ("repaid", "disburse"): None, ("repaid", "settle"): None}      # None = 拒绝

assert set(WANT) == set(product(STATES, EVENTS)), "期望表缺格"
for (s, e), want in WANT.items():
    try: got = fire(s, e)
    except ValueError: got = None
    assert got == want, (s, e, got, want)
print(len(WANT), "cells ok")                         # 6 cells ok
```

**知识点：**状态机的穷尽测试（Exhaustive Testing）
