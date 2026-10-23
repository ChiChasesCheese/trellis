---
id: hl-hc07-longtickermap
node: problems.hc07-ticker-hash-map
type: qa
step: 11
---
## Q
`LongTickerMap` 怎么实现零分配？`locateForInsert` 为什么返回 `~位置`，哈希为什么不能用 `key & mask`？

## A
`long[] slots` 交错布局（`slots[2i]=key`, `slots[2i+1]=value`），`0` = 空，`-1` = 墓碑（合法 key > 0，不会混淆），64 位 Fibonacci 哈希取高位，比较用 `==`。key 必须 > 0，否则 `IllegalArgumentException`；`put` 返回 `boolean`（`true` = 新 key）；`get(k, ifAbsent)`；`add` 溢出抛 `ArithmeticException` 且不改值。

```java
private int home(long key) { return (int) ((key * 0x9E3779B97F4A7C15L) >>> shift); }
private int locateForInsert(long key) {          // 找到返回 >=0；找不到返回 ~(应该插入的位置)
    int i = home(key), firstTomb = -1;
    while (true) {
        long k = slots[2 * i];
        if (k == key) return i;
        if (k == EMPTY) return ~(firstTomb >= 0 ? firstTomb : i);
        if (k == TOMB && firstTomb < 0) firstTomb = i;
        i = (i + 1) & mask;
    }
}
```
- 「`~位置`」编码：负数 = 没找到，取反是该插入的位置，**一个 `int` 同时带回两样**，避免分配结果对象；
- `add`：`int i = locateForInsert(key)`，`i >= 0` 就 `addExact`，否则 `insertNew(key, delta, ~i)`——只哈希、探测一次；
- 稳态下无 `new`、装箱、lambda 捕获——零分配。测试用 `ThreadMXBean.getThreadAllocatedBytes`：预热后 160 万次 `add` 分配 < 256 KB，对照 `HashMap<String,Long>.merge` > 8 MB；
- **哈希不能写 `key & mask`**：低位全是补的 0，几乎所有 key 落同一格；测试用 17576 个三字母代码要求最长探测距离 ≤ 64。
