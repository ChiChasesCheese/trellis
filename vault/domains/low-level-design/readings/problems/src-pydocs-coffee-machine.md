---
nodes: [problems.machines.coffee-machine]
url: https://docs.python.org/3/library/threading.html
---
# threading — Python 标准库

值得读：这道题的全部技术依据都在这一页。两件事最该读清楚。其一是 `Lock` 和 `RLock` 的区别：
`RLock` 允许同一个线程重入，因此它能让"订阅者在回调里反过来调用机器"不再死锁——但那不是
修复，是把一个当场可见的错误换成一个安静的吞吐塌方（订阅者从此在持锁状态下运行）。本题解
因此故意用不可重入的 `Lock`，让这类错误立刻暴露，并把事件投递挪到锁外。其二是 `Barrier`：
它让"恰好 N 个线程同时到齐"成为一个可以断言的事实，于是并发测试不必靠 `sleep` 赌时序——
本题解用它同时验证了"不超卖"和"并发度恰好等于出口数"两条不变式。
