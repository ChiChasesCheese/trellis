---
id: fsm-flags-to-states-impossible-combos
node: fsm.flags-to-states
type: qa
step: 1
---
## Q
贷款类里有三个布尔字段 `is_pending`、`is_active`、`is_repaid`。为什么这是一个设计问题？改成什么？

## A
**互斥的布尔字段，是一个伪装起来的枚举**

- **组合数**：三个布尔有 8 种取值，业务上只有 3 种合法，其余 5 种（一个都没有，或同时是已放款又已还清）是“不可能的状态”；
- **谁来保证它不出现**：每个修改处都要同时改三个字段，漏改一个就产生非法组合，而且不会报错；
- **改成枚举**：一个字段，只有合法值；不可能的状态在类型上就不能表示；
- **判断标准**：几个布尔字段永远至多有一个为真，就是同一个维度，应该合并。

```python
from itertools import product

LEGAL = {(True, False, False): "pending", (False, True, False): "active",
         (False, False, True): "repaid"}                 # (is_pending, is_active, is_repaid)
combos = list(product([False, True], repeat=3))
print(len(combos), len(LEGAL))                           # 8 3

flags = [True, False, False]                             # pending
flags[1] = True                                          # 放款时漏了把 pending 清掉
print(tuple(flags) in LEGAL)                             # False：没人报错，状态已经坏了
```

**知识点：**把标志位改成状态（Flags to States）
