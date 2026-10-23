---
id: hl-j08-lambda-var
node: java21.j08-var
type: qa
step: 16
---
## Q
`BiFunction<Long, Long, Long> add = (var x, var y) -> x + y;` 里 `var` 的唯一用处是什么？

## A
`var` 在 lambda 形参里的**唯一用处**是能给形参加注解，例如 `(@NonNull var x, @NonNull var y) -> ...`。

条件：所有形参要么全 `var`、要么全不 `var`。除此之外，`(x, y) -> x + y` 的隐式类型写法效果相同，不需要 `var`。
