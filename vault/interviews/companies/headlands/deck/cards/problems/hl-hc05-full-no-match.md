---
id: hl-hc05-full-no-match
node: problems.hc05-market-order-book
type: qa
step: 16
---
## Q
`TickBook.limit` 在池满时为什么返回 `FULL` 且不撮合，而不是先撮合再拒绝剩余部分？

## A
先撮合再发现没地方挂，成交已经发生（回调已通知），「拒绝」语义就不干净了。池满时对可能完全成交的单误拒是保守的，但简单、可预测、状态不会被改一半。这是有界内存系统常见的**背压**（back-pressure）策略。

同样的原则用在：
- Part 2 的溢出检查放在撮合之前（原子拒绝）；
- 所有会抛异常的检查放在修改之前（强异常保证）；
- C++ 的 `bad_alloc` 之后的一致性：先分配后提交，或在热路径上完全不分配（`TickBook`）。

测试：对拍（differential testing）——同一串随机命令喂给 `TickBook` 和明显正确的 `OrderBook`，逐步比较成交序列、最优价、每档数量；再加一个暴力模型当裁判。
