---
nodes: [problems.media.google-docs]
url: https://svn.apache.org/repos/asf/incubator/wave/whitepapers/operational-transform/operational-transform.html
tags: [engineering-blog]
---
# Google Wave Operational Transformation

值得读：Google Wave 项目公开的操作转换（OT）算法白皮书，详细说明了转换函数如何处理插入/
删除/属性变更的流式组合、客户端必须等待服务器确认才能发送下一批操作的控制回路，以及
wavelet 上操作组合（composition）如何减少等待确认期间需要转换的操作数。这是本题解里唯一
直接来自 Google 一手技术资料的来源，本题解「深入探讨」第 2 节的服务器权威控制回路设计直接
采纳了这篇白皮书的架构。

%% trellis:begin %%
## Source
[Open the original ↗](https://svn.apache.org/repos/asf/incubator/wave/whitepapers/operational-transform/operational-transform.html)
%% trellis:end %%
