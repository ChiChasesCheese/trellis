---
id: hl-j15-widen-first
node: java21.j15-math-string-utils
type: qa
step: 14
---
## Q
`int a = 2_000_000_000, b = 2; long wrong = a * b;` 得到什么？怎么写才对？为什么说 Exact 只保护它自己那一次运算？

## A
`wrong = -294967296`：`a * b` 先按 `int` 相乘（已经溢出了），再扩展成 `long`。

```java
long right = (long) a * b;                      // 先扩展再乘
long safe  = Math.multiplyExact((long) a, b);   // 想要溢出检测用这个
```
Exact 只保护它自己那一次运算；表达式里别处先溢出了，它救不了。要在乘之前把操作数扩宽到 `long`，再用 `multiplyExact`。
