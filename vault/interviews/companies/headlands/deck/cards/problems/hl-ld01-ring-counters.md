---
id: hl-ld01-ring-counters
node: problems.ld01-spsc-channel
type: qa
step: 3
---
## Q
环形缓冲区（ring buffer）怎么区分满和空？为什么 head/tail 用自由增长的计数，容量为什么取 2 的幂？

## A
数组队列 `poll` 要把 `buf[1..n-1]` 全往前挪 O(n)。环形：不挪元素挪**指针**，读指针 head 只往前走，到尾部绕回开头。

**经典陷阱**：`head`、`tail` 都存「数组下标」时，`head == tail` 既可能空也可能满。补救：永远空一个槽位；或另存 `size`（被两线程同时改，要原子操作）。**更好：`head`、`tail` 是只增不减的计数**（free-running），下标 = 计数对容量取模：
```
空  ⇔ tail - head == 0
满  ⇔ tail - head == capacity
元素个数 = tail - head
下标 = 计数 & mask
```
空和满天然不同，不浪费槽位，不需要 `size`。`long` 计数每纳秒加 1 要约 29 万年才溢出。

**容量 2 的幂**：`计数 % capacity` 要一次整数除法（几十个周期）；`capacity = 2^k` 时取模等价于只保留低 k 位，一次按位与：`capacity=8`，`mask=0b0111`，`13 & 7 = 5 = 13 % 8`。检查：`Integer.bitCount(capacity) == 1`（含 0 和负数；`Integer.MIN_VALUE` 的 bitCount 是 1，但先被 `capacity < 1` 拦下）。计数永远非负，所以与 `%` 结果一致。

```java
public boolean offer(long value) {
    if (tail - head == buf.length) return false;      // 满了不覆盖最旧元素
    buf[(int) (tail & mask)] = value;
    tail++;
    return true;
}
```
`poll` 在空队列上抛 `NoSuchElementException`；`size()` 的 `(int)` 强转安全（`tail - head ≤ capacity ≤ 2³⁰`）。SPSC 下自旋等待 `while (q.isEmpty()) Thread.onSpinWait(); q.poll();` 安全（只有消费者能让队列变空）。

手算容量 4：offer 10,20,30,40（tail=4，size 4，满）；offer 50 → false；poll → 10（head=1）；offer 50 → `buf[4&3=0]`（回绕，tail=5）；size 4。容量 8、head=13、tail=17：元素 4，offer 写 `buf[17&7=1]`，poll 读 `buf[13&7=5]`。
