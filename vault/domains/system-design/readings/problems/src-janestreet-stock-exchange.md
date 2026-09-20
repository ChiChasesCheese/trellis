---
nodes: [problems.commerce.stock-exchange]
url: https://blog.janestreet.com/how-to-build-an-exchange/
---
# How to Build an Exchange — Jane Street Blog

值得读：Jane Street 公开分享的内部撮合引擎 JX 设计——单一活跃撮合引擎搭配一个被动副本
通过可靠组播（reliable multicast）监听全部输出，故障时近乎瞬时接管，思路和 LMAX 的日志
重放模式同构但表述角度不同（组播 vs 日志复制）。本题「深入探讨」第 2 节把两者并列作为
"确定性重放优于对内部状态做共识协商"这一思路的两个独立真实印证。

%% trellis:begin %%
## Source
[Open the original ↗](https://blog.janestreet.com/how-to-build-an-exchange/)
%% trellis:end %%
