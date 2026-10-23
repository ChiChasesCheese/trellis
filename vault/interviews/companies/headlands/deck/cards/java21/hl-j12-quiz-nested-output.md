---
id: hl-j12-quiz-nested-output
node: java21.j12-scoped-values
type: qa
step: 21
---
## Q
下面程序输出什么？
```java
static final ScopedValue<Integer> X = ScopedValue.newInstance();
ScopedValue.where(X, 1).run(() -> {
    ScopedValue.where(X, 2).run(() -> System.out.print(X.get()));
    System.out.print(X.get());
});
System.out.print(X.isBound());
```

## A
输出 `21false`。

- 内层 `where(X, 2)` 遮蔽外层，先打印 `2`；
- 内层结束自动还原，外层打印 `1`；
- 整个块结束后绑定消失，`X.isBound()` 为 `false`。
