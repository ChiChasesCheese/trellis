---
id: hl-hc13-java21-features
node: problems.hc13-fixed-memory-pool
type: qa
step: 16
---
## Q
这个池用到哪些 Java 21 特性？各自比旧写法好在哪，什么时候不该用？

## A
- **record**：`Order(long id, long px, int qty, int side)` + `Order.ZERO`；旧写法类 + 4 字段 + 构造器 + 访问器 + `equals/hashCode/toString` 约 30 行易漏改；一行，`equals` 逐字段，可直接比较 `new Order(1,2,3,4)` 和 `pool.get(h)`。
- **record 模式**：`put(long, Order)` 里 `case Order(long id, long px, int qty, int side) -> ...` 一次解构四个字段，组件个数 / 类型由编译器检查；只用一个字段时直接 `o.px()` 更清楚。
- **switch 表达式**：`freeOrThrow` 里 `RuntimeException failure = switch (free(block)) {...}`；旧写法 switch 语句 + 每分支赋值 + `break`（漏 `break` 就 fall through）；每分支一个值，对 enum 穷尽，新加 `FreeResult` 值这里编译不过。
- **`var`**：右边已写类型时（`var pool = new IndexPool(3)`）；右边看不出类型时（`var x = foo()`）不该用。
- **虚拟线程**：`Executors.newVirtualThreadPerTaskExecutor()` 开 2000 个并发任务；旧的线程池要调参，2000 个平台线程吃大量内存；自旋型任务不该用（占住载体线程），这里任务短小不阻塞。
- **`VarHandle` / `LongAdder`**：`findVarHandle` 对 long head CAS；`arrayElementVarHandle(int[].class)` 对 gens / next 做 CAS / opaque / release；`LongAdder` 计数。旧写法 `AtomicReferenceFieldUpdater` / `Unsafe` / 每槽位一个 `AtomicInteger`（capacity 个对象）。
- **FFM**：`Arena` / `MemorySegment` / `StructLayout` / `SequenceLayout`，JDK 21 预览（`--enable-preview`），JDK 22 转正，API 名字会变。

C++ 差异：`Arena` 对应 `std::aligned_alloc` + `alignas` 的 `struct`；`MemoryLayout` + `VarHandle` 对应普通结构体成员 + `static_assert(offsetof)`；`LongAdder` 对应单个 `atomic<int>`（relaxed，标准库没有分片计数器）；没有虚拟线程，压测用多批短命 `std::jthread`；`IllegalStateException` 对应自定义 `StateError`（`std::logic_error` 子类）、`PoolClosed`；C++ 里「new 慢」是因为分配器的锁 / 碎片 / 系统调用，而不是 GC。
