---
id: hft-cpp-spsc-seqlock-no-cas
node: cpp.spsc-seqlock
type: qa
step: 1
---
## Q
单生产者单消费者（SPSC）环形缓冲区为什么只用两个原子下标就能无锁工作，甚至不需要 CAS（compare-and-swap，比较并交换）？

## A
关键是**每个变量只有一个写者**：
- `tail`（下一个写入位置）只由生产者修改；
- `head`（下一个读取位置）只由消费者修改。

没有两个线程争着改同一个变量，就不需要 CAS 来仲裁。协作靠 acquire/release 配对：
- 生产者先把数据写进槽位，再用 **release** 更新 `tail`，等于“发布”；
- 消费者用 **acquire** 读 `tail`，看到新值就保证能看到槽位里的数据；
- 消费者读完后 release 更新 `head`，生产者 acquire 读它，才知道槽位已空出。

容量取 2 的幂，下标用 `counter & (N-1)` 代替取模。计数器只增不减（无符号回绕无碍），元素数 = `tail - head`。

例：N = 8，`head = 5`，`tail = 7`，队列里 2 个元素；下一个写入槽位是 `7 & 7 = 7`，满的条件是 `tail - head == 8`。
