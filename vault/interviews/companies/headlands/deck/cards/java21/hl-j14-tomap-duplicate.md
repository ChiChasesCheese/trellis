---
id: hl-j14-tomap-duplicate
node: java21.j14-stream-api
type: qa
step: 19
---
## Q
`Collectors.toMap` 遇到重复 key 会怎样？怎么处理？

## A
抛 `IllegalStateException`（Duplicate key），这是 Stream 里最常见的运行时错误之一。

处理重复要写第三个参数（合并函数）：

```java
Collectors.toMap(Trade::symbol, Trade::qty, (a, b) -> a)    // 重复时保留前一个
Collectors.toMap(Trade::symbol, Trade::qty, Long::sum)      // 重复时累加
```
