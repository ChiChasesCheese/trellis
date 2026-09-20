---
nodes: [problems.booking.restaurant]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/restaurant-management-system.md
---
# Designing Restaurant Management System

值得读：最流行的免费题面，把预订、点单、库存、支付、员工、报表几大块的需求列得很全，
适合用来核对自己有没有漏项。它的参考实现用单例（Singleton）管理 `Restaurant`，订单状态是
整单一个枚举字段而不是每道菜各自的状态机，也完全没有拆账——这三处正是本文与它分道扬镳、
把篇幅重新分配到课程门禁和拆账上的地方。仓库使用 GPL-3.0 许可，可以直接引用。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/restaurant-management-system.md)
%% trellis:end %%
