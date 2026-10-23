---
id: hl-sdrun-determinism-breakers
node: system-design.how-to-run
type: qa
step: 23
---
## Q
破坏状态机决定性（determinism）的常见东西有哪些？各怎么避免？

## A
- 读墙上时钟（`System.currentTimeMillis`）→ 业务时间用事件里的时间戳 / 可注入时钟；
- `HashMap` 遍历顺序 → 用有序结构或数组；
- 浮点运算顺序不同 → 用定点整数；
- 多线程竞争、依赖线程调度的并发 → 单写者；
- `Random` 无种子 → 固定种子；
- GC / 内存地址（`identityHashCode`）→ 不依赖。
