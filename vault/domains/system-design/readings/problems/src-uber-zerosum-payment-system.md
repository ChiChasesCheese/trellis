---
nodes: [problems.commerce.payment-system]
url: https://www.uber.com/us/en/blog/ubers-payments-platform/
---
# Zero-Sum by Design: 10 Years of Uber's Payments Platform

值得读：Uber 官方工程博客披露了其内部支付平台 Gulfstream 的账本设计——把每笔资金移动
建模为不可变的 "Money Order",要求一次移动里的全部记账条目之和必须为零,一笔已写入的
order 不能以任何形式被修改,调整只能通过新开一笔 order 完成,余额用强一致存储按实体
维护。与本题解不同的地方在于：本题解没有采用 Uber 这里"每个实体一行强一致余额"的具体
存储选型,而是把余额做成从追加写账本条目推导出的快照 + 增量重放(参见 Stripe 和 Square
的披露),原因是本设计假设的规模(年 12 亿笔)还不需要 Uber 那种超过十亿级实体、要求
余额行本身强一致更新的极端场景。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.uber.com/us/en/blog/ubers-payments-platform/)

## Archived copy
![[src-uber-zerosum-payment-system-clip]]
%% trellis:end %%
