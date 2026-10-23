---
id: hl-j07-no-interpolation
node: java21.j07-text-blocks
type: qa
step: 19
---
## Q
文本块里怎么嵌入变量？`.formatted` 要注意什么？它和 Java 21 预览的 String Templates 是什么关系？

## A
文本块没有 `${x}`。插值用 `.formatted(x)`、`+` 或 `String.format`。`.formatted` 里的 `%` 要写成 `%%`（JSON 里的百分号要注意）。

**不要和 String Templates（`STR."..."`）混淆**：那是 Java 21 的预览特性，JDK 23 已撤回；文本块是稳定特性，不依赖它。
