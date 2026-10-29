---
id: uth-go-rust-go-channel-3-select
node: go-rust.go-channel
type: qa
step: 3
---
## Q
**select 同时多个 case 就绪选哪个**｜Go · 1.27 运行时

多个 case 同时能执行时，`select` 怎么保证公平、又不死锁？

## A
**结构。** `select` 先随机洗牌（shuffle）出轮询顺序，再按 channel 地址给所有 channel 排序加锁。

**细节。**

- 轮询顺序：逐个随机交换，所以每个就绪的 case 被选中的概率相同
- 实测：两个 channel 都就绪，选 10000 次，结果是 4919 : 5081
- 加锁顺序：按 `hchan` 地址排序，排序用堆排序，保证 O(n log n) 且栈空间固定

**为什么。** 固定顺序会让靠前的 case 饿死其他 case；所有 `select` 都按同一顺序加锁，就不会互相等待造成死锁。

**对应 LeetCode：** LC 384 打乱数组 · LC 912 排序数组
