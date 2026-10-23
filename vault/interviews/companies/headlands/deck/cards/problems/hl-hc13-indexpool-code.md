---
id: hl-hc13-indexpool-code
node: problems.hc13-fixed-memory-pool
type: qa
step: 4
---
## Q
写出 `IndexPool` 的构造、`allocate`、`free`，以及用 `ALLOCATED = -2` 检测重复归还的做法。

## A
```java
public IndexPool(int capacity) {
    if (capacity < 1 || capacity > MAX_CAPACITY) throw new IllegalArgumentException("capacity: " + capacity);
    next = new int[capacity];
    for (int i = 0; i < capacity - 1; i++) next[i] = i + 1;
    next[capacity - 1] = NONE;
    head = 0; available = capacity;
}
public int allocate() {
    int block = head;
    if (block == NONE) return NONE;        // 池满不抛异常
    head = next[block];
    next[block] = ALLOCATED;               // -2：一个数字同时承担「链表指针」和「是否在用」
    available--;
    return block;
}
public FreeResult free(int block) {
    if (block < 0 || block >= next.length) return FreeResult.INVALID;   // 先查范围再查状态
    if (next[block] != ALLOCATED) return FreeResult.DOUBLE_FREE;
    next[block] = head; head = block; available++;
    return FreeResult.FREED;
}
```
- 只有 `next[]` 时 `free(3)` 调两次，第二次 `next[3] = head; head = 3` 把 3 挂在自己后面成环，之后 `allocate` 永远返回 3；重复归还**不能**把块插进链表两次（否则同一块被分配给两个人）。
- 不另开 `boolean[]`：空闲块 `next` ≥ -1，在用块 -2，空闲和在用互斥。「不在用」含「已还过」和「从没借过」，统一 `DOUBLE_FREE`。
- 先查范围再查状态，否则越界直接抛 `ArrayIndexOutOfBoundsException`。
- `MAX_CAPACITY = 1 << 28` 避免 `new int[...]` 吃掉 1 GiB 以上，超出明确报错而非 `OutOfMemoryError`。
- `freeOrThrow`：`RuntimeException failure = switch (free(block)) { case FREED -> null; case DOUBLE_FREE -> new IllegalStateException(...); case INVALID -> new IllegalArgumentException(...); };`——switch 表达式对 enum 穷尽，漏写编译报错；`FreeResult` 用 `enum` 而非 `int` 常量，新增结果时所有 switch 编译失败。

样例：`IndexPool(2)`：`allocate`→0、→1、→-1；`free(0)`→FREED；`free(0)`→DOUBLE_FREE；`free(7)`→INVALID；`allocate`→0。`IndexPool(4)`：`allocate×3`=0,1,2，`free(1)`=FREED，`allocate`=1，`free(1)`=FREED，`free(1)`=DOUBLE_FREE。
