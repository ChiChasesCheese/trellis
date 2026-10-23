---
id: hl-cq-cs11-layout
node: cpp-questions.cheatsheet
type: qa
step: 11
---
## Q
一句话背诵：结构体布局规则——填充、成员顺序的效果、`alignas(64)`、空类大小。

## A
- 成员按对齐加填充，**大的放前面**（同样四个字段 24 → 16 字节）。
- `alignas(64)` 让对象独占一条缓存行。
- `sizeof(空类)` = 1。
