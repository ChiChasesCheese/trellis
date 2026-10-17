---
nodes: [amazon.amz-discount-engine]
url: https://www.1point3acres.com/bbs/thread-1191754-1-1.html
tags: [no-archive]
---
# 一亩三分地 thread-1191754：Amazon VO 一轮 OOD（2026-10-02）
值得读：一位候选人记下的 Amazon OOD 一轮：折扣基类带 `isEligible` / `apply`，三种折扣各自实现，PriceEngine 遍历购物车行、累加折扣后从原价扣除，BUY_X_GET_Y 靠“赠品数量 × 单价”折成减免。帖子部分内容需登录才可见，只能看到这些主干。与本题解的分歧：它的遍历是“每行 × 每个折扣”，没有给满减留位置；本题解把整车折扣拆成第二层，并让 `apply` 接收剩余价格，避免叠加时多减。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.1point3acres.com/bbs/thread-1191754-1-1.html)
%% trellis:end %%
