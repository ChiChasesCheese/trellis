---
id: problems-online-auction-callable-watcher-not-abc
node: problems.marketplaces.online-auction
type: qa
step: 7
tags: [grown]
---
## Q
在线拍卖要在出价、延期、结束时通知订阅者，这是观察者模式（Observer）的标准场景。Java 题解通常写一个 `AuctionObserver` 接口加 `on_update` 方法。Python 里该怎么做？观察者事件的内容该带什么？

## A
**不需要抽象基类。** 观察者只有一个方法，那它就是一个普通函数：关注者的类型直接声明成 `Callable[[AuctionEvent], None]`，`print`、`list.append`、一个闭包、一个实现了 `__call__` 的类，全都直接可用，不需要继承任何东西。抽象基类的价值在"多个方法要一起实现"或要用 `isinstance` 分派，这里两者都没有。

真正值得花心思、且和用不用基类无关的是两处：

1. **事件自带内容**：`AuctionEvent` 带齐现价、领先者、被顶掉的人、结束时间和状态。`on_update(auction, "你被超越了")` 这种签名会把订阅者推回去读 `auction` 的实时状态——那等于绕过锁读一份正在变化的数据。
2. **退订的手段要和订阅一起交出去**：`watch()` 返回一个 `unwatch` 闭包，关注者表才会缩小；拍卖一结束，整张表当场清空，因为之后不会再有任何事件。没有这两条，关注者表就是一个只增不减的内存泄漏。
