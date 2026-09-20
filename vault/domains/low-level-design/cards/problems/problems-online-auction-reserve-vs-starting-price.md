---
id: problems-online-auction-reserve-vs-starting-price
node: problems.marketplaces.online-auction
type: qa
step: 4
tags: [grown]
---
## Q
在线拍卖里，起拍价（starting price）和底价（reserve price）是同一回事吗？它们分别控制什么，在代理出价（proxy bidding）算法里各自出现在哪一步？

## A
**不是同一回事，必须是两个独立字段。**

- **起拍价**：第一次出价的下限，**公开**。它只出现一次——`minimum_bid()` 在还没有领先者时返回它，作为第一位出价者必须达到的门槛。
- **底价**：低于这个数卖家宁可不卖，通常**不公开**。它出现在结算与代理出价两处：拍卖到点时，"成交"还是"流拍"取决于最终价是否达到底价（`sold = leader is not None and price >= reserve_price`）；而只要领先者的上限已经够到底价，代理出价就会把当前价直接抬到底价，因为卖家反正会接受这个数，没有理由让价格停在底价以下。

把两者合成一个字段的后果：要么起拍价被迫等于底价（暴露了卖家的心理价位），要么底价被迫公开（丧失了它"不公开"的作用）。

流拍也因此**只用一个状态** `UNSOLD`：没人出价、和出价了但没到底价，原因不同，但系统行为完全一样（没有赢家、不收款），原因由"有没有领先者"自己说明，不需要拆成两个状态。
