---
id: hft-order-types-tif
node: microstructure.order-types
type: qa
step: 2
---
## Q
订单的有效期（time in force，TIF）有哪几种常见设置？IOC 和 FOK 有什么区别？

## A
TIF 规定订单能存活多久：
- **DAY**：当天有效，收盘仍未成交就自动取消。
- **GTC**（good till cancel）：一直有效，直到你撤销。
- **IOC**（immediate or cancel）：立刻能成交多少就成交多少，**剩下的立即取消**，不会挂在簿上。
- **FOK**（fill or kill）：必须**全部**立刻成交，否则整张单取消。

例子：想买 1000 股，限价 100.02。卖一 100.01 有 400 股，卖二 100.02 有 300 股。IOC 成交 700 股、取消 300 股；FOK 发现只有 700 股 < 1000，一股也不买，整单取消。

HFT 常用 IOC：只吃掉当前看到的量，不留挂单，避免挂单过期后被别人吃掉。
