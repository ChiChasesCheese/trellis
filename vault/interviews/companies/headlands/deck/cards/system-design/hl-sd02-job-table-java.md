---
id: hl-sd02-job-table-java
node: system-design.sd02-job-scheduler
type: qa
step: 18
---
## Q
Java 里怎么存 3×10⁸ 个任务才不被 GC 压垮？写出 `JobTable` 的字段，单写线程和时间源怎么用？

## A
每个任务不是一个对象，而是第 i 号槽位：几个并行数组（SoA）。3×10⁸ 个对象会压垮 GC；12 GB 的数组（或堆外 `MemorySegment`）只是一块内存，GC 不扫描 `long[]` / `int[]` 的内容。
```java
final class JobTable {
    final long[] fireAtMs;    // UTC epoch ms
    final int[]  state;       // SCHEDULED / DISPATCHING / FIRED / CANCELLED / DEAD
    final int[]  nextInSlot;  // 时间轮槽内双向链表，-1 表示空
    final int[]  prevInSlot;
    final long[] payloadOff;  // 指向磁盘 / 堆外的负载位置
    int freeHead;             // 空闲槽位链表，O(1) 分配释放，没有 new
    // id → slot：开放寻址 long→int 哈希表，避免 HashMap<Long,Integer> 装箱
}
```
- **单写线程**拥有所有数组，其他线程通过 MPSC 队列（JCTools `MpscArrayQueue` 或 Disruptor）提交命令，单写者原则，不需要锁；
- **时间源**：推进时间轮用 `System.nanoTime()`（单调，不受 NTP 回拨影响），与 `fireAt` 比较用校准后的墙上时钟；睡眠到**绝对**截止时间 `LockSupport.parkNanos(deadline - now)`，而不是 `Thread.sleep(10)` 累积漂移。
