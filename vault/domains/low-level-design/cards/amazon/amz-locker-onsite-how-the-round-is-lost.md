---
id: amz-locker-onsite-how-the-round-is-lost
node: amazon.amz-locker-onsite
type: qa
step: 6
tags: [grown]
---
## Q
在 Amazon 现场版快递柜里，这一轮最常见的丢分方式是什么？

## A
把时间花在附带的难点上：先写最近网点的地理算法或数据库表，单网点的主流程还没有写完整、没有手工推演过。另一个常见错误：把取件码当密码，按包裹计数错误次数；码是持有即凭证，只能按柜机限流。顺序应是：澄清、单网点主流程加失败路径、手工推演，然后才谈多网点、退货和持久化。
