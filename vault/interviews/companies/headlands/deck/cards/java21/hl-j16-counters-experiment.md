---
id: hl-j16-counters-experiment
node: java21.j16-concurrency-primitives
type: qa
step: 21
---
## Q
计数器四种写法（`int++` 不保护、`synchronized`、`AtomicLong`、`LongAdder`）每线程加 200 万次，随线程数增加表现如何？

## A
粗糙计时（ms，只看趋势）：

| 线程数 | `int++` | `synchronized` | `AtomicLong` | `LongAdder` |
|---|---|---|---|---|
| 1 | 2 | 6 | 2 | 6 |
| 2 | 3，值 2095019（期望 4000000） | 252 | 33 | 7 |
| 8 | 5，值 2074320（期望 16000000） | 573 | 123 | 9 |

- `int++` 最快但**值错得离谱**，丢更新；不正确的快没有意义。
- 单线程差不多；线程多了 `synchronized` 掉到数百 ms（锁竞争 + 阻塞/唤醒），`AtomicLong` 其次（CAS 重试 + 缓存行抖动），`LongAdder` **几乎不随线程数增长**。
- 8 线程时 `LongAdder` 比 `AtomicLong` 快 10 倍以上，比 `synchronized` 快 60 倍以上。
