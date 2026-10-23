---
id: hl-j03-real-usage
node: java21.j03-pattern-switch
type: qa
step: 27
---
## Q
真实代码里模式匹配 `switch` 常见的写法有哪些？未命名模式 `_` 是什么、属于什么状态？

## A
- **订单校验**：`when` 守卫按"更具体的错误在前"排顺序；最后几行无守卫，让编译器验证 `sealed` 被穷尽。
- **渲染结果**：`case Malformed _ -> ...`、`case Ok(var chains) -> { ... yield lines; }`。
- **事件处理**：`switch` **语句**处理四种事件，无 `default`，同样要穷尽；带守卫的 `record` 模式如 `case Value(QueueMean.Mean(var n, var d)) when d == 1 -> n.toString();`。
- **15 种指令**的 `switch`，无 `default`。

**未命名模式 `_`**：不需要变量名时用 `_` 占位（如 `case Cancel _, Modify _ -> ...`），在 Java 21 里是**预览**特性。
