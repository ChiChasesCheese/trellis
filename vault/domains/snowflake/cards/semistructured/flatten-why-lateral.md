---
id: flatten-why-lateral
node: semistructured.flatten-lateral-joins
type: qa
tags: [grown]
---
## Q
为什么 `FLATTEN` 需要放在 `LATERAL` 连接里，而不能像普通表一样独立地出现在 FROM 子句中与 `orders` 做连接？

## A
普通连接两侧彼此独立，右侧无法引用左侧当前行的列。`FLATTEN` 的输入恰恰是左表每一行里的数组（如 `o.v:items`），必须逐行计算。`LATERAL`（横向连接）允许右侧的表函数引用左侧 FROM 项的列，对左表每一行调用一次 FLATTEN，再把产生的行与这一行拼接起来。在 Snowflake 中，`, LATERAL FLATTEN(...)` 和 `, TABLE(FLATTEN(...))` 都表达这种逐行关联。
