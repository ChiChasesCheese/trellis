---
id: hft-colocation-why
node: market-structure.colocation
type: qa
step: 1
---
## Q
主机托管（colocation）是什么？为什么 HFT 公司一定要把服务器放进交易所的机房，而不是放在自己的办公室？

## A
**主机托管：** 向交易所（或交易所所在的数据中心）租机柜，把自己的服务器放在撮合引擎的同一栋楼里，用一条很短的光纤连接。

**原因是光速。** 光在光纤里约每纳秒走 20 厘米，也就是每米约 5 ns。
- 机房内：几十米，单程约零点几微秒。
- 办公室在 50 公里外：单程约 250 µs，往返约 0.5 ms，是机房内的上千倍。

HFT 的竞争以微秒甚至纳秒计，起步就慢 0.5 ms 等于没有资格比赛。

常见的位置：Nasdaq 在新泽西的 Carteret，NYSE 在新泽西的 Mahwah，Cboe 在新泽西的 Secaucus，CME 在芝加哥郊区的 Aurora。所以地理位置是延迟的第一项，其余优化都排在后面。
