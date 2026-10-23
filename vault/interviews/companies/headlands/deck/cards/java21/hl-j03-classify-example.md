---
id: hl-j03-classify-example
node: java21.j03-pattern-switch
type: qa
step: 20
---
## Q
`classify(Signal s)` 里对 `Tick` 写了 `when t.qty() == 0`、`when t.px() > 100_000` 两个守卫分支，最后又写了一个无守卫的 `case Tick t`。最后一行有什么作用？

## A
```java
case Tick t when t.qty() == 0 -> "empty tick";
case Tick t when t.px() > 100_000 -> "expensive tick";
case Tick t -> "tick " + t.px() + "x" + t.qty();     // 兜底：不带 when
```
最后一个 `case Tick t` **没有守卫**，起两个作用：
1. **兜底**：前两个条件都不满足时的默认处理；
2. **让编译器相信 `Tick` 被完整覆盖**：带守卫的分支不算覆盖，没有这一行就不穷尽。

例：`Tick(1,0)` → `empty tick`；`Tick(200000,5)` → `expensive tick`；`Tick(100,3)` → `tick 100x3`。
