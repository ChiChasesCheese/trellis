---
id: hi-c-lld-correctness-x04-swap-deadlock
node: lld.concurrency.correctness.exam
type: qa
step: 4
---
## Q
**并发正确性 · 换座死锁**｜考点 · 必会

细粒度锁下，Alice 换 7A 与 12B，Bob 换 12B 与 7A，会怎样？涉及三把或更多锁时怎么办？

## A
- **结果：** 双方各持一把锁等对方的一把，死锁
- **修法：** 按全局统一顺序加锁（比如座位 id 按字符串排序后依次获取，"12B" 在 "7A" 之前），两人都先抢 12B，一个等另一个
- **更多锁：** 同样先排序再依次获取；用 `ExitStack` 管理多把锁的释放
- **前提：** 排序键要稳定且唯一；锁放在不同容器里时，顺序约定要写进文档
