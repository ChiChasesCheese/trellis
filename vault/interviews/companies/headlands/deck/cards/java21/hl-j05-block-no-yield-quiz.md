---
id: hl-j05-block-no-yield-quiz
node: java21.j05-switch-expressions
type: qa
step: 28
---
## Q
`case 1 -> { System.out.println("x"); }` 出现在 `switch` 表达式里为什么编译失败？怎么改？

## A
块执行完既没有 `yield` 也没有 `throw`，表达式没有值，报 `switch rule completes without providing a value`。

改成：
```java
case 1 -> { System.out.println("x"); yield 0; }
```
（`yield` 的值类型要与其他分支兼容。）
