---
id: hl-j13-discard-result
node: java21.j13-unnamed-variables
type: qa
step: 13
---
## Q
`var _ = queue.offer(x);` 有什么风险？`_` 应该用来表达什么？

## A
`offer` 返回 `false` 表示队列满了，用 `var _` 丢弃返回值就是**吞错误**。

`_` 表达的是「我知道有这个值，但确实不重要」。不确定时就写 `if (!queue.offer(x)) ...` 处理失败。
