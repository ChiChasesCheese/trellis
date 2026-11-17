---
id: fluency-time-integer-cents
node: fluency.time-numbers
type: qa
step: 5
---
## Q
商品价 `19.99`，要按 `2500` 基点（25%）算折扣，再把总额按比例分给几个收款方。为什么金额要存成整数分、先乘后整除？零头去哪里？

## A
**金额存整数分，先乘后整除**

- **`float` 存不准十进制小数**：`19.99 * 100` 是 `1998.9999…`，`int()` 得到 1998 分；每次运算都带着这种误差，累计后对不上账；
- **整数分精确**：加减乘都精确，比较用 `==`；解析输入时直接按字符串或 `Decimal` 转成分，不经过 `float`；
- **先乘后整除**：`amount * bps // 10000`；先除成小数再乘，`12/10000*2500` 会在小数上先丢精度，截断后差 1；
- **取整方向要写进合同**：`//` 是向下取整，`round` 平局取偶（`round(2.5)` 是 2），两者对同一笔金额可能差 1 分，规则要一致；
- **零头不凭空消失**：按比例分摊后，各份之和可能少几分；约定零头留在“剩余”或给最后一方，让各份之和等于总额（守恒）。

```python
def share(amount: int, bps: int) -> int:
    return amount * bps // 10000          # 整数分，向下取整

total = 1001
a = share(total, 2500)                    # 250
b = share(total, 7500)                    # 750
print(a, b, total - a - b)                # 250 750 1：零头 1 分留在剩余
print(int(19.99 * 100))                   # 1998：float 少了 1 分
print(int(12 / 10000 * 2500), share(12, 2500))   # 2 3：先除后乘 vs 先乘后除
```

<details class="pt"><summary>延伸</summary>

整数分的上界要写进校验：Python 的 `int` 不会溢出，但传给 JSON 另一端（JavaScript）的整数超过 2**53 就失去精度，传给 32 位或 64 位存储的整数超界会被拒绝。

</details>

**知识点：**时间与数字（Time & Numbers）
