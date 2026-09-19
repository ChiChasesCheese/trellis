---
id: kafka-streams-joinwindows-asymmetric-before
node: streams.streams-api
type: qa
step: 6
source: kafka-2e
---
## Q
示例里用 `JoinWindows.of(Duration.ofSeconds(1)).before(Duration.ofSeconds(0))` 来连接搜索事件流和点击事件流，为什么不直接用一个对称的「搜索前后各1秒」的窗口，而要额外调用 `before(0秒)` 来收窄它？

## A
`JoinWindows.of(Duration.ofSeconds(1))` 默认构造的是一个对称窗口，即搜索事件前1秒到后1秒之间的点击事件都会被匹配进来；但业务逻辑上，只有发生在搜索**之后**的点击才可能是「用户看到搜索结果后点击」，发生在搜索之前的点击和这次搜索毫无关系，只是巧合地落在了时间窗口内。调用 `.before(Duration.ofSeconds(0))` 把「搜索之前」这部分窗口收窄为0，相当于把对称窗口改造成一个只往后延伸1秒的单向窗口，确保只匹配发生在搜索事件之后（而非之前）的点击事件，避免把无关的点击错误地关联到某次搜索上。
