---
id: hl-hc13-freelist-naive
node: problems.hc13-fixed-memory-pool
type: qa
step: 3
---
## Q
空闲链表（free list）为什么比 `boolean[] inUse` 扫描更好？最笨解法错在哪，为什么随机借还测试测不出？

## A
最笨：`boolean[] inUse`，`allocate` 从头扫找第一个空的 O(capacity)；`free` 检查越界和 `!inUse[block]`。正确，重复归还、越界都能检测。**错在**：池接近满、空位散落在数组中间时要扫过前面所有被借走的块。

为什么易被漏测：50/50 随机借还时池里平均只有几百块在用，前几百格之后就是空位，扫描很快（300 万次只要 125 ms）。所以测试把池填满再 150 万次「换掉随机一块」：`capacity = 65536` 时朴素版每步约 3.9 µs、共约 6 秒，超 2 秒预算；链表版约 11 ms。**教训：测性能要测最坏的形状。**

「第二笨」：`ArrayDeque<Integer>` 当空闲栈 O(1)，但 `Integer` 是装箱对象，借还一次就 `new` 一个——**池子本身在制造垃圾**。

**空闲链表**：把「还没被借走的块」串成链，借 = 摘链头，还 = 挂链头，都 O(1)。关键一招是把链表指针藏在块自己里面（**侵入式**，intrusive）：空闲块不存数据，位置可存「下一个空闲块是谁」。`int[] next` + `int head`：
- capacity=4 初始 `next = [1,2,3,-1]`，`head = 0`；
- `allocate`：`b = head; head = next[b]`，返回 b；
- `free(b)`：`next[b] = head; head = b`。
构造 O(capacity)，空间 `4 × capacity` 字节。

手算（capacity 3）：`allocate`→0、`allocate`→1、`free(0)`、`allocate`→0（刚还的最先借走，LIFO）、`allocate`→2、`allocate`→-1（池满是正常状态）。
