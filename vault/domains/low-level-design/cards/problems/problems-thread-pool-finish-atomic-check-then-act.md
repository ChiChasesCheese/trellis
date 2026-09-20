---
id: problems-thread-pool-finish-atomic-check-then-act
node: problems.components.thread-pool
type: qa
step: 5
tags: [grown]
---
## Q
线程池的 `Future` 完成时要『设置完成标志』并『取出回调列表逐个调用』。如果 `add_done_callback` 和这个完成过程并发执行，什么写法会导致回调被静静地漏掉？

## A
如果『判断是否已完成』和『取出回调列表并清空』不是同一次加锁下的原子操作，就会漏：假设完成方先在锁内取出旧列表、清空 `self._callbacks`，但要等释放锁之后才去设置完成标志——这时另一个线程调用 `add_done_callback`，它检查完成标志还是 `False`，于是把回调追加进**这个刚被清空的新列表**；完成方随后设置标志、只遍历它先前取出的那份旧列表，永远不会看到后来追加的这个回调，它就这样凭空消失。正确写法是把『设置完成标志』和『取出并清空回调列表』放进同一次加锁里，这样 `add_done_callback` 的检查要么完整发生在这次加锁之前（能追加进即将被取出的列表）、要么完整发生在之后（读到的完成标志已经是 `True`，直接同步调用），不存在夹在中间的第三种情况——这是一次典型的 check-then-act 竞态，和 `self._served += 1` 不是原子操作是同一类问题的另一个变体。
