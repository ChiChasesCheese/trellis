---
id: patterns-observer-notify-lock
node: patterns.observer
type: qa
step: 3
---
## Q
在持有锁（lock）的情况下调用观察者的回调，为什么危险？

## A
回调是外部代码，你不知道它会做什么——如果某个订阅者的回调反过来又调用了 subject 的方法（比如收到通知时又去订阅或退订），而这个方法恰好要抢同一把 `threading.Lock`，就会在同一线程里死锁（`Lock` 不可重入），或者在遍历订阅者列表的过程中列表被回调偷偷修改而出错。安全的做法：持锁时只更新内部状态、把订阅者列表拷贝一份，出锁之后再逐个调用回调。
