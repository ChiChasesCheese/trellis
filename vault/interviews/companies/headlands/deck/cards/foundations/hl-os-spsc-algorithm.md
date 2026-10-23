---
id: hl-os-spsc-algorithm
node: foundations.os-processes-threads-ipc
type: qa
step: 25
---
## Q
SPSC 环形缓冲的算法是什么？为什么用只增不减的序号而不是回绕的下标？

## A
`head` 和 `tail` 都是一直增加的序号（long），槽位是 `序号 & mask`。元素个数 = `tail − head`；空：`tail == head`；满：`tail − head == N`。

生产者 `offer(v)`：
1. `t = tail`（我是唯一写者，直接读）；`t − head == N` 则满，返回 false；
2. ① 先写数据 `slot[t & mask] = v`；
3. ② 再发布 `tail = t + 1`（release 写）。

消费者 `poll()`：
1. `h = head`；`h == tail`（acquire 读）则空；
2. ③ 读数据 `slot[h & mask]`；
3. ④ 释放槽位 `head = h + 1`（release 写）。

用序号的原因：若存回绕下标（0..N−1），`head == tail` 既可能是空也可能是满，需多留一个空槽或加计数器；只增序号一眼区分。64 位序号每秒 10 亿条也要几百年才溢出。
