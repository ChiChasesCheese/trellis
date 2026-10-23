---
id: hl-j03-no-default-sealed
node: java21.j03-pattern-switch
type: qa
step: 17
---
## Q
为什么对 `sealed` 层级的 `switch` 一般不要写 `default`？什么时候才写？

## A
```java
return switch (event) {
    case Trade t -> ...;
    case Rested r -> ...;
    default -> "?";          // 新增 Cancelled 时，这里不报错，悄悄走 default
};
```
写了 `default`，等于**关掉了穷尽检查**：新增变体时编译器不再报错，新类型悄悄落入 `default`，bug 要到运行时才发现。

没有 `default` 时，新增变体让所有漏处理的 `switch` 编译失败。只在**真想把剩下的都当一类**时才写 `default`。
