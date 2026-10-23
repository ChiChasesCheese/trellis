---
id: hl-hc13-memory-order
node: problems.hc13-fixed-memory-pool
type: qa
step: 12
---
## Q
`ConcurrentPool` 里每个访问点该用什么内存序（acquire / release / opaque / CAS）？为什么「读到过期数据没关系」？

## A
| 位置 | 访问方式 | 为什么 |
|---|---|---|
| 读 `head` | `getAcquire` | 要看到别的线程 push 之前对 `next[i]`、`gens[i]` 的写 |
| `head` 的 CAS | `compareAndSet`（volatile 语义，含 release） | push 时发布 `next[i]` 和版本号；pop 成功要成为全序的一环 |
| `next[i]` 读写 | `getOpaque` / `setOpaque` | 读到旧值没关系——`head` 的 tag 已变，CAS 会失败；只需不撕裂、不被编译器缓存 |
| `gens[i]` 的 CAS（free） | `compareAndSet` | 并发 double-free 的仲裁点 |
| `gens[i]` 在 allocate 里的写 | `setRelease` | 弹出成功后槽位归本线程所有；发布版本号给之后的 `isLive` |
| `inUse` 计数器 | `LongAdder` | 纯统计，不参与正确性；分散热点 |

思想：「**读到过期数据没关系，只要最后用 CAS 校验**」——只在「CAS 的对象能反映过期」时成立，所以 tag 不能省。

`VarHandle` 用法：`findVarHandle` 对普通 `long head` 字段做 CAS；`arrayElementVarHandle(int[].class)` 对普通 `int[]` 元素做 CAS / opaque / release，不需要每槽位一个原子对象（对比 `AtomicIntegerArray` 或每槽位一个 `AtomicInteger` 要 capacity 个对象）。

C++ 对应：`std::atomic` + 显式 `std::memory_order`，同一套内存模型，`opaque` ≈ `relaxed`。`next_` 必须是 `vector<atomic<uint32_t>>` + `relaxed`：普通数组元素被并发读写是数据竞争（UB）。内存序全写 `relaxed` 则 `next_` 的值没有被发布，popper 可能读到未初始化的链接；全写 `seq_cst` 不会错但慢——先对再快。`tag` 和 `head` 放进同一个 64 位原子；共享内存做 IPC 时原子变量要求 `is_always_lock_free`。

Java 的 `Arena.ofShared()` 的 segment 允许别的线程访问。`available()` 并发进行中可以是近似值，所有线程静止后必须精确。
