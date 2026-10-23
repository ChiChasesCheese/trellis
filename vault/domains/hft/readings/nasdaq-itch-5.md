---
nodes: [protocols.itch-model, protocols.itch-messages, protocols.binary-encoding, orderbook.building]
url: https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf
---
# Nasdaq TotalView-ITCH 5.0 规范

Nasdaq 逐笔行情协议的官方规范：数据类型、每种消息的字节布局。

**读的时候提取：**
- Add Order / Executed / Cancel / Delete / Replace 消息的字段。
- 价格是 4 位小数的整数、时间戳是午夜起的纳秒数、所有整数大端。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf)

## Archived copy
![[nasdaq-itch-5-clip]]
%% trellis:end %%
