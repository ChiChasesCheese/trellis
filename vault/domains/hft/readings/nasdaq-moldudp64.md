---
nodes: [protocols.moldudp64, protocols.gap-recovery]
url: https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/moldudp64.pdf
---
# MoldUDP64 规范

给 UDP 组播行情加会话和序列号的轻量协议，以及向重传服务器请求缺口的方式。

**读的时候提取：**
- 下行包头：session、sequence number、message count。
- 心跳包与结束包的格式。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/moldudp64.pdf)

## Archived copy
![[nasdaq-moldudp64-clip]]
%% trellis:end %%
