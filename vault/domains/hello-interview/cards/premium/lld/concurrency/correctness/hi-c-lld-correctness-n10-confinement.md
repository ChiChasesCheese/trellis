---
id: hi-c-lld-correctness-n10-confinement
node: lld.concurrency.correctness.notes
type: qa
step: 10
---
## Q
**并发正确性 · 线程封闭（Shared Nothing）**｜摘要 · 必会

线程封闭怎么消除同步？有什么真实例子，代价是什么？

## A
- **思路：** 数据只被一个线程访问就不可能有竞态；把数据分区，每线程拥有自己的一份（线程一管 A 到 M 区，线程二管 N 到 Z 区）
- **真实系统：** Dragonfly 按键空间分到各线程，Akka 把状态封闭在 actor 里，数据库连接池借出的连接同一时刻只归一个线程使用
- **代价：** 同步复杂度换成架构复杂度；跨分区操作仍需协调，热点分区导致不均，必须严格执行否则竞态回来
- **面试里：** 多数题过度；被追问扩展性时提
