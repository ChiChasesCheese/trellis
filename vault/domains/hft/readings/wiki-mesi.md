---
nodes: [machine.coherence, machine.false-sharing]
url: https://en.wikipedia.org/wiki/MESI_protocol
---
# MESI 缓存一致性协议

Modified / Exclusive / Shared / Invalid 四种状态和它们之间的转换。

**读的时候提取：**
- 写一个 Shared 行为什么要先让其他核失效。
- 这种失效流量如何变成伪共享的代价。

%% trellis:begin %%
## Source
[Open the original ↗](https://en.wikipedia.org/wiki/MESI_protocol)

## Archived copy
![[wiki-mesi-clip]]
%% trellis:end %%
