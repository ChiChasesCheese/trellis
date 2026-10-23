---
id: hft-fragmentation-venues
node: market-structure.fragmentation
type: qa
step: 1
---
## Q
美国股票没有"唯一的交易所"：同一只股票（比如 AAPL）同时在很多地方交易。这些交易场所大致分哪几类？

## A
法规允许多个场所互相竞争，所以同一只股票同时有很多个订单簿。三类场所：

- **交易所**（exchange）：约十几家，分属 NYSE、Nasdaq、Cboe 三大集团，外加 IEX、MEMX 等。每家各有自己的撮合引擎和订单簿，公开显示报价。
- **暗池**（dark pool，法律上叫另类交易系统 ATS）：几十个，挂单不公开显示，成交后才上报。
- **批发商**（wholesaler）：如 Citadel Securities、Virtu，向券商买下散户订单直接成交，不进交易所。

在场外（暗池加批发商）成交的量，约占全部美股成交量的四成以上。后果：任一时刻，AAPL 在十几个订单簿里各有一个买一和卖一，要把它们拼起来才是全市场价格。
