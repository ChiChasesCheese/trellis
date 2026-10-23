---
id: hl-j15-quiz-mul-widen
node: java21.j15-math-string-utils
type: qa
step: 23
---
## Q
`int a = 2_000_000_000; long x = a * 2;` 得到什么？怎么写才对？

## A
`-294967296`：`a * 2` 先按 `int` 乘（溢出）再扩展成 `long`。

正确：`long x = (long) a * 2;`，要检测溢出就写 `Math.multiplyExact((long) a, 2)`。
