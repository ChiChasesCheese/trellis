---
id: hl-j04-no-for-destructure
node: java21.j04-record-patterns
type: qa
step: 4
---
## Q
Java 21 里能不能在增强 `for` 里解构，如 `for (Point(var x, var y) : points)`？

## A
**不能。** Java 20 预览过，Java 21 正式版**删除**了；在 `--release 21` 下是语法错误。

Java 21 只能在 `instanceof` 和 `switch` 的 `case` 里用 record 模式。遍历时先取元素，再对元素做 `instanceof Point(var x, var y)` 或 `switch`。
