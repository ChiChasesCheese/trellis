---
id: hl-hc13-complexity
node: problems.hc13-fixed-memory-pool
type: qa
step: 14
---
## Q
四个池的时间 / 空间复杂度和实测量级是多少？测试的性能边界怎么设？

## A
| 操作 | 时间 | 空间 |
|---|---|---|
| `IndexPool.allocate/free` | O(1) | 4 × capacity 字节 |
| `GenPool.allocate/free` | O(1) | 8 × capacity 字节 |
| `OffHeapOrderPool` 各操作 | O(1) | 32 × capacity 字节堆外，一次分配 |
| `ConcurrentPool.allocate/free` | O(1) 期望；争用下 CAS 重试无界（lock-free，不是 wait-free） | 8 × capacity 字节 |

量级（12 核）：`IndexPool` 近满换块 150 万次 11 ms、随机 300 万次 40 ms；`GenPool` 10 / 27 ms；`OffHeapOrderPool` 100 万记录 62 ms；`ConcurrentPool` 4 线程 × 5 万轮 × 16 次借还 450 ms。O(n) 扫描版：近满换块约 3.9 µs/步 → 150 万步约 6 s；50/50 随机负载只要 125 ms。

构造 `new IndexPool(1 << 20)` O(capacity) 可以；所有操作 O(1)，不能为了找空闲块去扫数组。

**性能测试要点**：300 万次随机借还 < 2 s；**池几乎一直是满的**时 150 万次「换掉随机一块」< 2 s（O(n) 扫描空位的写法死在这里）；100 万记录的堆外池 < 2 s；4 线程各 5 万轮 × 16 次借还 < 2 s。

**边界清单**：容量 `0`、负数、`MAX_CAPACITY + 1`、`capacity == 1`；编号 `-1`、`capacity`、`Integer.MIN_VALUE / MAX_VALUE`；打包：版本号为负（高位 1）、下标 `Integer.MAX_VALUE`、忘了 `& 0xFFFFFFFFL`；handle：`0L`、`-1L`、版本号偶数、低 32 位当 int 是负数、`Long.MIN/MAX`；状态：池满后再分配、重复归还三次、归还从没分配过的块、归还后又重新分配同一槽位（ABA）；回绕：`new GenPool(1, -2)`；并发：小池 + 8 线程反复借还不能出现两个主人、三个线程同时 `free` 同一批 handle、跨线程借 / 还、大量虚拟线程（2000 个各 200 轮）。

相关变体：把编号换成 `ByteBuffer.slice()`（容量 int、无 close）；块大小可变（slab / buddy allocator）；`acquire()` 阻塞等待 `release()` 唤醒（`Semaphore` + 栈的阻塞版，语义与非阻塞不同）；C++ 追问 placement new / alignment / `std::pmr`。
