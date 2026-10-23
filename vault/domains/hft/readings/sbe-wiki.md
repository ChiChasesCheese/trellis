---
nodes: [protocols.sbe-mdp3, java.flyweight-sbe, java-at-hft.interop]
url: https://github.com/real-logic/simple-binary-encoding/wiki
---
# Simple Binary Encoding（SBE）设计说明

SBE 的设计原则：schema 生成编解码器、定长字段按顺序排列、flyweight 原地读写、不分配。

**读的时候提取：**
- 为什么 SBE 要求字段按顺序访问。
- flyweight 解码器如何做到零拷贝、零垃圾。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/real-logic/simple-binary-encoding/wiki)
%% trellis:end %%
