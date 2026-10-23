---
id: hl-j08-int-overflow-trap
node: java21.j08-var
type: qa
step: 15
---
## Q
下面代码输出什么？这展示了 `var` 的什么陷阱？

```java
var px = 3_000_000;
var qty = 3_000;
var wrong = px * qty;
var right = (long) px * qty;
System.out.println(wrong + " vs " + right);
```

## A
输出 **`410065408 vs 9000000000`**。

`px` 和 `qty` 都是 `int` 字面量，`int * int` 溢出后才赋给 `wrong`。陷阱：**类型不再写在左边，数字字面量悄悄是 `int`，乘法溢出没人发现。**

写成 `long notional = px * qty;` 也是同样的 bug（右边仍是 `int` 乘法后才转 `long`），但显式类型更容易让 reviewer 问"为什么右边没转 `long`"。
