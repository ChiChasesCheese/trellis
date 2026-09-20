---
nodes: [problems.marketplaces.online-shopping]
url: https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/007-order-management
---
# machine-coding-interview-questions — Order Management

值得读：把同一道题收窄成"订单管理"，并且抓住的核心和本题解一致——"这道题只有一个会动的
部件：订单的状态"，而且明确写着"即使不用正式的状态对象，你也需要一张清晰的转移表"。
它还配了五种语言的参考实现、一份 `spec.yaml` 和一份按 Part 1/2/3 分关的题面，分关的粒度
值得借鉴。
不同之处：它把 State 模式推荐为默认答案，本题解拒绝了——订单在各个状态下没有行为差异，
只有"允许往哪走"的许可差异，用一张表比五个类更好读也更好用；它的金额是 `double`，本题解
一律用整数最小货币单位；它不涉及支付、库存、履约之间的补偿，也没有库存预留与过期。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/007-order-management)

## Archived copy
![[src-jkaus324-online-shopping-clip]]
%% trellis:end %%
