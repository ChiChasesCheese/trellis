---
id: hl-j03-validate-example
node: java21.j03-pattern-switch
type: qa
step: 21
---
## Q
订单校验 `validate(Command cmd, Set<Long> knownIds)` 怎么用带守卫的 `switch` 写？守卫和无守卫的分支各起什么作用，好处是什么？

## A
```java
return switch (cmd) {
    case Limit l when l.id() <= 0 -> "INVALID_ID";
    case Limit l when l.price() <= 0 -> "INVALID_PRICE";
    case Limit l when l.qty() <= 0 -> "INVALID_QTY";
    case Market m when m.id() <= 0 -> "INVALID_ID";
    ...
    case Limit l -> knownIds.contains(l.id()) ? "DUPLICATE_ID" : null;
    case Market m -> knownIds.contains(m.id()) ? "DUPLICATE_ID" : null;
    case Cancel c -> knownIds.contains(c.id()) ? null : "UNKNOWN_ID";
};
```
- 带守卫的是参数校验，无守卫的是状态检查，并让编译器验证 `sealed` 被覆盖。
- **校验顺序就是代码顺序**（id → price → quantity → 状态）。
- 新增 `Modify` 命令，`switch` 立刻编译失败；没有 `instanceof` / 强转 / 嵌套 `if`。
