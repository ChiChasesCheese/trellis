---
id: fsm-testing-mutate-table
node: fsm.testing
type: qa
step: 4
---
## Q
穷举测试全绿了。怎么确认它真的拦得住转移表里的错？

## A
**改坏转移表，穷举测试必须变红**

- **三类改坏**：删一行（合法转移变成拒绝）、改一个目标状态、多加一行（非法转移变成合法）；
- **每类各一次**：测试应当对每一种都变红；仍然绿说明那一格没有期望；
- **和期望表的关系**：期望表按合同手写，被测的表是实现，两份独立；
- **成本**：改坏一次是一行代码，跑一次是毫秒。

```python
from itertools import product

S, E = ["pending", "active", "repaid"], ["disburse", "repay"]
WANT = {("pending", "disburse"): "active", ("active", "repay"): "repaid"}   # 其余应被拒绝

def killed(table):                                    # 穷举比较：有差异就算被测试抓住
    return any(table.get(c) != WANT.get(c) for c in product(S, E))

TABLE = {("pending", "disburse"): "active", ("active", "repay"): "repaid"}
mutants = {"drop": {k: v for k, v in TABLE.items() if k[0] != "active"},
           "retarget": {**TABLE, ("pending", "disburse"): "repaid"},
           "extra": {**TABLE, ("repaid", "disburse"): "active"}}
print(killed(TABLE), {n: killed(t) for n, t in mutants.items()})
# False {'drop': True, 'retarget': True, 'extra': True}
```

**知识点：**状态机的穷尽测试（Exhaustive Testing）
