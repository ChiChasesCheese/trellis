---
id: hl-j14-peek-count
node: java21.j14-stream-api
type: qa
step: 17
---
## Q
为什么 `peek` 里的打印有时不执行？`peek` 该怎么用？

## A
`peek` 只用于**调试**，业务逻辑别放里面。不打印的原因：
- 没有终止操作，流水线是懒的；
- 被短路（如 `findFirst`、`limit`）；
- JDK 9 起 `count()` 若能直接从来源算出大小，会**跳过整条流水线**，`peek` 的副作用就不执行。

所以不能依赖 `peek` 的副作用。
