---
id: hl-j16-longadder-vs-atomic
node: java21.j16-concurrency-primitives
type: qa
step: 20
---
## Q
`AtomicLong` 与 `LongAdder` 怎么选？什么时候不能用 `LongAdder`？

## A
| | `AtomicLong` | `LongAdder` |
|---|---|---|
| 适合 | 要**精确当前值**并参与决策：序号发号、`compareAndSet`、限额检查 | 只写不频繁读的**统计量**：成交笔数、字节数、命中数 |
| 读 | `get()` O(1)，精确 | `sum()` 要遍历 Cell，不是原子快照 |
| 高竞争写 | 差（重试 + 缓存行抖动） | 好（分散） |
| 内存 | 8 字节 | 高竞争下有多个 Cell，更大 |

`LongAdder.sum()` 不是快照：别拿它做「达到阈值就触发」的精确判断，也别拿它发序号。
