---
id: hl-hc13-handle-pack
node: problems.hc13-fixed-memory-pool
type: qa
step: 6
---
## Q
怎么把 `(int generation, int index)` 打包进一个 `long` handle？为什么 `index` 要 `& 0xFFFFFFFFL`，`free` 的判定顺序是什么？

## A
```java
public static long handle(int index, int generation) {
    return ((long) generation << 32) | (index & 0xFFFFFFFFL);
}
public static int indexOf(long handle) { return (int) handle; }                    // 取低 32 位
public static int generationOf(long handle) { return (int) (handle >>> 32); }     // 无符号右移，不关心符号
```
布局：高 32 位 `generation`，低 32 位 `index`。handle 在方法间传、当 map key，最好是**一个**基本类型值而不 `new` 对象。

**符号扩展**：`index` 为负（最高位 1）转 `long` 时高 32 位全填 1，污染 generation 成 `0xFFFFFFFF`。`& 0xFFFFFFFFL` 先当无符号数处理，高 32 位清零。很多人写成 `((long) generation << 32) | index` 就是错的。C++ 用 `uint64_t`，索引 / 版本号都是 `uint32_t`，无符号扩宽补零，类型本身防错；`static_cast<uint64_t>(-1)` 符号扩展成全 1 会冲掉版本号。

`GenPool.free`：
```java
int index = indexOf(handle), g = generationOf(handle);
if (index < 0 || index >= gens.length || (g & 1) == 0) return FreeResult.INVALID;   // 越界，或偶数版本号 = 从没发过
if (gens[index] != g) return FreeResult.DOUBLE_FREE;                                // 奇数但已过期
gens[index] = g + 1;                                                                 // 奇 → 偶
next[index] = head; head = index; available++;
return FreeResult.FREED;
```
`allocate`：`int g = ++gens[index]`（偶→奇），返回 `handle(index, g)`。`index < 0` 必须检查：低 32 位当 `int` 是负数（如 `0x0000_0001_8000_0000`），否则 `gens[index]` 抛异常。`0L` 和 `NONE (-1)` 永远无效。不再需要 `ALLOCATED` 哨兵：奇偶就是状态，`next[]` 只在空闲链表里有意义。

样例：`GenPool(1)`：`a = allocate()` = `0x0000_0001_0000_0000`（index 0，generation 1）；`free(a)`→FREED；`b = allocate()` = `0x0000_0003_0000_0000`（同槽位 generation 3）；`free(a)`→DOUBLE_FREE；`isLive(b)`→true。`new GenPool(1, -2)` 版本号从 `0xFFFFFFFE` 起，分配得 -1，归还后回绕为 0。构造 `initialGeneration` 必须是偶数。
