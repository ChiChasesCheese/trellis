---
id: hl-ld01-spsc-code
node: problems.ld01-spsc-channel
type: qa
step: 7
---
## Q
写出 `SpscLongRing` 的 `offer` 和 `poll`（cached index + release/acquire），并说明每一步为什么安全。

## A
```java
public boolean offer(long value) {
    long t = tail;                                  // 自己独占写，普通读
    if (t - cachedHead == buf.length) {             // 按旧快照看是满的 → 才读真正的 head
        cachedHead = (long) HEAD.getAcquire(this);
        if (t - cachedHead == buf.length) return false;
    }
    buf[(int) (t & mask)] = value;                  // ① 数据
    TAIL.setRelease(this, t + 1);                   // ② 发布
    return true;
}
public long poll() {
    long h = head;
    if (h == cachedTail) {
        cachedTail = (long) TAIL.getAcquire(this);
        if (h == cachedTail) throw new NoSuchElementException("ring is empty");
    }
    long v = buf[(int) (h & mask)];                 // ④
    HEAD.setRelease(this, h + 1);                   // ⑤ 读完才归还
    return v;
}
```
- `tail` 只有生产者写，读自己的字段用普通读；
- 旧 `head ≤ 真 head`，旧值只高估占用：说不满则真不满；说满才刷新，不会产生错误的「有空位」结论；
- `HEAD.getAcquire` 看到新 head 就保证消费者在 release head 之前的读（`buf[old]`）已完成，可覆盖该槽位；
- ⑤ 的 release 保证 ④ 的读发生在生产者看到新 head 之前；
- `size()` 用 `Math.clamp(t - h, 0, buf.length)`（Java 21）夹到 `[0, capacity]`：先读 head 再读 tail，期间两者都可能前进，差值理论上可能略超范围；
- `VarHandle` 经 `MethodHandles.lookup().findVarHandle(ConsumerFields.class, "head", long.class)` 取得，对**非 volatile 的普通字段**做 release/acquire 访问；
- `SpscLongRing.isFull` 覆盖接口 default 方法，只读 tail 与 head，不依赖近似的 `size()`；`LongQueue.isFull()` 是 default 方法的实际理由：填充继承链占了 `extends`，公共行为只能放接口。

SPSC 测试：两线程 1000 万条 `long` < 2 s（实测 184 ms，约 5500 万条/秒）；不得有消费者读到上一轮留下的旧值（把 `setRelease` 改成普通写在 ARM 上立刻出错）。

步骤递进：不加任何东西 → 可见性（JIT 提循环外）和顺序都错；`volatile` 对；release/acquire 去掉全栅栏；cached index 少读对方行；填充防伪共享。
