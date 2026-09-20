---
nodes: [problems.commerce.e-commerce]
url: https://github.com/donnemartin/system-design-primer
tags: [reference-repo]
---
# The System Design Primer

值得读：MIT 协议的开源社区仓库（非商业课程），系统整理了缓存、分片、消息队列等
通用构件各自的基础权衡，但没有专门针对电商场景给出方案。本题解和它的差异在于：本文
把这些通用构件按目录/购物车/结账/库存/订单五个不同一致性域的具体需求重新组合（哪个
域用哪种存储、哪种一致性保证），而不是停留在"缓存能加速读、队列能解耦写"这一层通用
结论。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/donnemartin/system-design-primer)

## Archived copy
![[system-design-primer-clip]]
%% trellis:end %%
