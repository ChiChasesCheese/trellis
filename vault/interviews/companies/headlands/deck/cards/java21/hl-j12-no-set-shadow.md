---
id: hl-j12-no-set-shadow
node: java21.j12-scoped-values
type: qa
step: 10
---
## Q
`ScopedValue` 为什么没有 `set`？想「改值」怎么办？嵌套绑定同一个 key 会怎样？

## A
**`ScopedValue` 不可变，没有 `set`。** 想改值只能用新值开一个内层 `where(...).run(...)`：内层看到新值，出来自动还原。这直接消灭「可变、随处可改」的毛病：某范围内值是什么，从缩进结构就看得出。

嵌套是**遮蔽**（shadow）而不是覆盖：

```java
where(USER, "alice").run(() -> {
    where(USER, "admin").run(() -> { /* USER = admin */ });
    /* 回到这里 USER = alice */
});
```
对比 `ThreadLocal` 要自己写 `old = get(); try { set(x) } finally { set(old) }`。
