---
id: fsm-flags-to-states-independent-flags
node: fsm.flags-to-states
type: qa
step: 4
---
## Q
表单字段有 `touched`（用户碰过）和 `valid`（值合法）。这两个布尔也要合并成一个状态枚举吗？

## A
**互相独立的维度保留成独立字段**

- **判断**：两个布尔的四种组合是否都合法、都有意义？都合法，就是两个独立的维度，不是互斥；
- **合并的代价**：做成四个状态的枚举，每条转移都要写四种情况，状态数是乘积，不是相加；
- **更好的拆法**：`touched` 是用户的行为历史，需要存；`valid` 完全由值推出，不存，用属性现算；
- **显示逻辑**：“要不要显示错误”是两者的函数：碰过且不合法。

```python
from dataclasses import dataclass

@dataclass
class Field:
    value: str = ""
    touched: bool = False
    @property
    def valid(self): return self.value.isascii() and self.value.isdigit()    # 派生
    @property
    def show_error(self): return self.touched and not self.valid

f = Field(); print(f.show_error)           # False：没碰过
f.touched = True; print(f.show_error)      # True：碰过且为空
f.value = "12"; print(f.show_error)        # False
```

<details class="pt"><summary>延伸</summary>

两个维度都在变化、而且各有自己的状态时（例如“连接状态”与“同步状态”），这就是并行状态（见“层次状态”），做法是两个独立的状态机并排，不做乘积。

</details>

**知识点：**把标志位改成状态（Flags to States）
