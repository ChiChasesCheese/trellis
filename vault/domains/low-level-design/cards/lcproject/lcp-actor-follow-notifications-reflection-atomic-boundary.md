---
id: lcp-actor-follow-notifications-reflection-atomic-boundary
node: lcproject.lcp-actor-follow-notifications
type: qa
step: 3
tags: [作答]
---
## Q
关注演员与上新通知的服务里，一部新片入库后要给关注者发通知。如果入库成功、发通知前进程崩了，会出什么问题？哪几步必须一起成功或一起失败，哪些可以挪到这一步之外？

## A
**评分点**
- 说出边界是同一个临界区：判重与冲突检查、读取关注者算受众、写电影表、写收件箱，由同一把锁罩住
- 说出 follow、unfollow、inbox 也在同一把锁下，所以受众就是登记那一刻的关注者，结果等价于某个串行顺序
- 说出先算后写：在写任何东西之前完成冲突检查和受众计算，之后的写入不会失败，电影和通知要么都在要么都不在
- 说出校验放在边界之外、锁之前：非法输入根本进不了临界区，不会留下半截状态
- 说出把电影存下来但不发通知（或反过来）是要避免的：会导致重试被判成"重复"，通知却永远丢了

<details class="pt"><summary>参考答案</summary>

边界是一个临界区：在同一把锁里先判重和冲突，再读取关注者算出受众，然后写电影表、写收件箱。`follow`、`unfollow`、`inbox` 也拿这把锁，所以受众就是登记那一刻的关注者。冲突检查和受众计算都在写入之前，之后的写入不会失败，所以电影和通知要么都在要么都不在。校验在锁之外、状态之前完成。

</details>

**知识点：** 复合操作（Compound Actions）、线程安全结构的写法（Thread-Safe Structures）、同步原语（threading）
