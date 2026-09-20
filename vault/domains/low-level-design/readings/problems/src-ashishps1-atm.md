---
nodes: [problems.machines.atm]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/atm.md
---
# awesome-low-level-design — Designing an ATM System

值得读：六种语言（含 Python）并排给出同一份设计，实体切法是 `Card` / `Account` /
`Transaction`（抽象基类 + `WithdrawalTransaction`、`DepositTransaction` 两个子类）/
`BankingService` / `CashDispenser` / `ATM`，可以用来核对自己有没有漏掉实体。本题解在两处
明确不同：没有排队、撤销、重放需求时，`Transaction` 继承体系只是把三个五行的方法各写成一个
类，本文改用三个方法加一条不可变流水（`JournalEntry`）；它的 `CashDispenser` 只回答"够不够"，
而本文把"取不出来"拆成金额不可表示、库存凑不出、张数超过送钞上限三种，因为它们给客户的
下一步建议完全不同。它对"先扣账还是先吐钞"没有展开，那恰是本文花篇幅最多的地方。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/atm.md)
%% trellis:end %%
