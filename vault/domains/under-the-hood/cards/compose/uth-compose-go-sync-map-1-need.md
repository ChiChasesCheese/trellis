---
id: uth-compose-go-sync-map-1-need
node: compose.go-sync-map
type: qa
step: 1
---
## Q
**读多写少的并发 map**｜Go · sync.Map 旧实现（1.25 及以前）

一张被很多 goroutine 共享、读远多于写的 map，为什么加锁的普通 map 不够好？

## A
**背景。** goroutine 是 Go 的轻量线程。普通 `map` 不是并发安全的：一边读一边写，运行时直接报 `fatal error: concurrent map read and map write` 并崩溃。直接的办法是配一把锁。`Mutex` 让所有读者排队；`RWMutex` 允许多个读者并行，但每次 `RLock` 仍要原子地修改同一个计数器，多个核反复抢同一个内存位置。

| 操作 | 要求 |
|---|---|
| `Load(k)` | key 已存在时不加锁 |
| `Store(k, v)` 改已有 key | 不加锁，原子换值 |
| `Store(k, v)` 加新 key | 可以加锁，但读者不能崩溃 |
| `Delete(k)` | 并发安全 |
| `Range(f)` | 遍历 |

**为什么。** 一张表加一把锁，读也要排队；完全不加锁，写新 key 要改 map 的内部结构，读者同时读就会崩溃。折中是两张表：读者只看一张"发布之后永不改结构"的表，写者在锁里改另一张。

**对应 LeetCode：** 无直接对应的题
