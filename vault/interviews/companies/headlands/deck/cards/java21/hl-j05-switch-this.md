---
id: hl-j05-switch-this
node: java21.j05-switch-expressions
type: qa
step: 22
---
## Q
枚举方法里怎么用 `switch (this)` 写 `Side.opposite()`？为什么不需要 `default`？

## A
```java
enum Side {
    BUY, SELL;
    Side opposite() { return switch (this) { case BUY -> SELL; case SELL -> BUY; }; }
}
```
枚举列全了所有常量，`switch` 表达式已穷尽，所以不需要 `default`。以后新增常量，编译器会在这里报错，提醒你补分支。
