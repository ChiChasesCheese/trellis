---
id: hl-ld01-java21-features
node: problems.ld01-spsc-channel
type: qa
step: 14
---
## Q
SPSC 通道实现用到哪些 Java 21 特性？各自比旧写法好在哪？

## A
- **`VarHandle`**：`SpscLongRing` 的 `HEAD/TAIL`（普通字段 + `setRelease/getAcquire`）；`MessageRing` 的 `memorySegmentViewVarHandle`。旧写法：全 `volatile`（过强）、`AtomicLong`（布局难控）、`sun.misc.Unsafe`（私有 API）。好处：对普通字段选访问强度，release/acquire 恰是 SPSC 所需，字段布局自己控制，填充才有意义。
- **FFM**（`MemorySegment`、`Arena`、`FileChannel.map(mode, off, size, Arena)`）：`MappedByteBuffer` 是 `int` 索引（≤ 2 GiB）、无确定性取消映射、原子访问要 `Unsafe`；FFM `long` 大小、`Arena.close()` 确定性取消映射、`VarHandle` 原子访问映射内存。JDK 21 预览，22 转正。
- **`Math.clamp`**（Java 21）：`size()`、`bytesPending()` 用 `Math.clamp(t - h, 0, capacity)`，代替嵌套两层易写反的 `Math.max(0, Math.min(x, capacity))`；`clamp(long, int, int)` 返回 `int` 省强转。
- **接口 `default` 方法**：`LongQueue.isFull()`；实际理由：填充继承链占了 `extends`，公共行为只能放接口，实现类可覆盖。
- **switch 表达式**：子进程入口 `String err = switch (mode) { case "consume" -> …; case "produce" -> …; default -> … };` 每分支产生值；字符串 switch 不能穷尽所以必须有 `default`。
- **`var`**：`var ring = MessageRing.init(…)`。

其他用到的 API：`Integer.bitCount`、`Thread.onSpinWait()`、`ProcessHandle.current().info().command()`、`Process.waitFor(超时)`、`destroyForcibly()`、`MemorySegment.copy(byte[]/segment 互拷)`、`Arena.ofShared()`（允许别的线程访问）。
