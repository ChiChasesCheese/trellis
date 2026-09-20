---
id: problems-auction-proxy-bid-increment-table-worked-example
node: problems.commerce.auction
type: qa
step: 3
tags: [grown]
---
## Q
Using eBay's published bid-increment table (e.g. a $0.50 increment applies in the $5.00–$24.99 price band, a $2.50 increment in the $100.00–$249.99 band), if the current display price is $19.99 (meaning the current leader's private maximum bid is $20.50) and a new bidder enters a proxy maximum of $45.02, what is the new display price and why is it not $45.02?

## A
The new maximum ($45.02) exceeds the current leader's maximum ($20.50), so the new bidder becomes the leader. But proxy bidding only raises the display price as far as needed to beat the previous leader by one increment, not to the new leader's own ceiling: the increment applicable at $20.50 (the $5.00–$24.99 band) is $0.50, so the new display price is min($45.02, $20.50 + $0.50) = $21.00. The new leader's true ceiling of $45.02 stays private and is only revealed incrementally if someone else bids higher.

## Q zh
用 eBay 公开的价位递增表（例如 5.00–24.99 美元区间对应 0.50 美元的递增单位，100.00–249.99 美元区间对应 2.50 美元），如果当前展示价是 19.99 美元（即当前领先者的私密出价上限是 20.50 美元），一个新出价者提交了 45.02 美元的代理出价上限，新的展示价是多少？为什么不是 45.02 美元？

## A zh
新上限（45.02 美元）超过了当前领先者的上限（20.50 美元），所以新出价者成为领先者。但代理出价只会把展示价提高到刚好压过前一位领先者一个递增单位的程度，而不是直接跳到新领先者自己的上限：20.50 美元所在的区间（5.00–24.99 美元）对应的递增单位是 0.50 美元，所以新的展示价是 min(45.02, 20.50+0.50) = 21.00 美元。新领先者真正的 45.02 美元上限仍然保密，只有在别人出价更高时才会被逐步揭示。
