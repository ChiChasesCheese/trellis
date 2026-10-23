---
id: hl-hc13-concurrent-free
node: problems.hc13-fixed-memory-pool
type: qa
step: 11
---
## Q
并发下两个线程同时 `free` 同一个 handle 怎么保证只有一个赢？`ConcurrentPool` 的 `allocate`/`free` 核心代码怎么写？

## A
单线程 `free` 是「检查版本 → 改版本 → 压栈」三步，两线程同时 `free` 同一 handle，都通过检查、都压栈 → 同一槽位进空闲链表两次。**想法**：把「检查 + 改版本」合成**一次 CAS** `CAS(gens[i], g, g + 1)`：成功的线程拥有「归还这个槽位」的权利，失败的看到版本已变 → `DOUBLE_FREE`。**偶 / 奇约定在此派上用场**：版本号本身就是状态（奇 = 在用），一次 CAS 完成「状态检查 + 切换」，不需另一个标志位。验证：换成「先读后写」，并发 double-free 压力测试全面失败（成功归还 2110 > 2000）。

```java
public long allocate() {
    while (true) {
        long h = (long) HEAD.getAcquire(this);
        int index = indexOf(h);
        if (index == EMPTY) return NONE;
        int below = (int) NEXTS.getOpaque(next, index);
        if (HEAD.compareAndSet(this, h, pack(tagOf(h) + 1, below))) {
            int g = (int) GENS.get(gens, index) + 1;
            GENS.setRelease(gens, index, g);          // 成功弹出，槽位归本线程所有
            inUse.increment();
            return GenPool.handle(index, g);
        }
        Thread.onSpinWait();
    }
}
public FreeResult free(long handle) {
    ... // 越界 / 偶数版本 → INVALID
    if (!GENS.compareAndSet(gens, index, g, g + 1)) return FreeResult.DOUBLE_FREE;   // 唯一赢家
    inUse.decrement();
    while (true) {
        long h = (long) HEAD.getAcquire(this);
        NEXTS.setOpaque(next, index, indexOf(h));
        if (HEAD.compareAndSet(this, h, pack(tagOf(h) + 1, index))) return FreeResult.FREED;
        Thread.onSpinWait();
    }
}
```
要点：读到的 `next[index]` 可能已过期，没关系，CAS 会验证（改它的 push 同时改了 head 的 tag）；赢者独占「把槽位压回栈」的权利，之后的压栈循环只与别线程的 push/pop 竞争 head；颠倒顺序（先压栈再 CAS 版本）会让同一槽位被压两次、成环、发给两个线程。`available()` 是 `capacity - inUse.sum()`，并发时近似，静止后精确；任意线程可 allocate、任意线程可 free。
