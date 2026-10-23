---
id: hl-j14-three-properties
node: java21.j14-stream-api
type: qa
step: 2
---
## Q
Stream 有哪三个必须记住的性质（懒、一次性、逐元素下推）？各带来什么后果？

## A
1. **懒（lazy）**：只写中间操作不执行任何东西，遇到终止操作才开始跑。所以 `Stream.of(1,2,3).peek(System.out::println)` 什么都不打印。
2. **一次性**：一个流只能终止一次，再用抛 `IllegalStateException: stream has already been operated upon or closed`。例如 `var s = list.stream(); s.count(); s.count();` 第二次就抛。
3. **逐元素下推**：不是「全部 filter 完再全部 map」，而是每个元素依次穿过整条流水线，所以 `findFirst()` 能提前停、`limit(3)` 能处理无限流。
