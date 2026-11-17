---
id: fluency-time-decimal-rounding
node: fluency.time-numbers
type: qa
step: 6
---
## Q
需求写“按四舍五入保留两位”，代码用 `round(x, 2)`。为什么 `round(2.5)` 是 2，`round(0.125, 2)` 是 0.12？要真正的四舍五入，该用 `Decimal` 的哪个舍入模式？

## A
**`round` 是半数取偶；要四舍五入用 Decimal**

- **`round` 平局取偶（half-even，银行家舍入）**：恰好在中点时取偶数那一边，`round(0.5)=0`、`round(1.5)=2`、`round(2.5)=2`；大量数据里上下偏差互相抵消；
- **`float` 的中点往往不是真中点**：`2.675` 在二进制里略小于 2.675，`round(2.675, 2)` 得 `2.67`；“四舍五入”的预期被浮点表示吃掉；
- **`Decimal` 精确表示十进制**：从字符串构造 `Decimal("0.125")`，用 `quantize` 指定舍入模式；常用的有 `ROUND_HALF_UP`（平局远离 0，财务常说的四舍五入）、`ROUND_HALF_EVEN`（默认）、`ROUND_DOWN`（向 0 截断）、`ROUND_FLOOR`；
- **别从 `float` 构造**：`Decimal(0.1)` 保存的是 `0.1000000000000000055…`；要么传字符串，要么 `Decimal(str(x))`；
- **只在边界舍入一次**：中间步骤保持精确（整数分或 `Decimal`），最后一步才舍入；每一步各舍一次，误差会累加。

```python
from decimal import Decimal, ROUND_HALF_UP
cent = Decimal("0.01")

x = Decimal("0.125")
print(x.quantize(cent))                          # 0.12：默认半数取偶
print(x.quantize(cent, rounding=ROUND_HALF_UP))  # 0.13：财务意义的四舍五入
print(round(2.5), round(0.125, 2))               # 2 0.12
print(Decimal(0.1) == Decimal("0.1"))            # False：浮点的 0.1 不是十进制的 0.1
```

<details class="pt"><summary>延伸</summary>

舍入模式是合同的一部分：税、手续费、汇率各自有规定。同一笔账在不同模块用了不同模式，对账时差的就是这 1 分。

</details>

**知识点：**时间与数字（Time & Numbers）
