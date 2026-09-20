---
id: problems-online-auction-leader-raises-own-max
node: problems.marketplaces.online-auction
type: qa
step: 2
tags: [grown]
---
## Q
在线拍卖的代理出价（proxy bidding）设计里，如果**当前领先者自己**提高出价上限（比如从 150 提到 210），当前价该不该跟着涨？为什么把他当成一个新挑战者走常规分支是错的？

## A
**不该涨（除非中途有人插过手）**，而且必须给领先者单开一条路，不能走常规的 `M > L` 分支。

天真的实现会把领先者提价当成新挑战者：`min(210, 旧上限 + 一档)`，于是他自己把自己的价顶上去了——**没有人应该和自己竞价**，这是本题最经典的 bug。

正确处理：

```python
if bidder_id == self._leader:
    if maximum <= self._leader_max:
        raise BidTooLowError(...)
    self._leader_max = maximum
    # 价格不动，也不发"价格变化"事件
```

只改上限，价格一动不动。校验门槛也不一样：领先者加价的门槛是「必须超过自己现有的上限」，而不是「必须达到现价加一档」——后者对他毫无意义，因为现价本来就是他在付。
