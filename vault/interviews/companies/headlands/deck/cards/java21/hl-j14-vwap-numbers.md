---
id: hl-j14-vwap-numbers
node: java21.j14-stream-api
type: qa
step: 16
---
## Q
5 笔成交：AAPL 18950×100、18960×300、18940×10；MSFT 41000×50、41010×150。总体 VWAP 与 AAPL 的 VWAP 各是多少？为什么乘法要用 `Math.multiplyExact`？

## A
VWAP（成交量加权平均价）= 总名义金额 / 总数量。
- 总名义金额 = 18950×100 + 18960×300 + 41000×50 + 41010×150 + 18940×10 = 15 973 900，除以总数量 610 = **26186.72…**。
- AAPL = (1 895 000 + 5 688 000 + 189 400) / 410 = **18957.07…**（MSFT = 41007.5）。

用 `Math.multiplyExact` 是因为价格乘数量溢出时宁可抛异常，也不要悄悄变成负数。`LongSummaryStatistics`：count=5、sum=610、min=10、max=300、average=122。
