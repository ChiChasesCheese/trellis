---
nodes: [problems.marketplaces.splitwise]
url: https://github.com/abhaypaswan/lld-python/tree/main/problems/splitwise
---
# lld-python — splitwise

值得读：自由来源里唯一原生 Python、带 pytest 的实现，和本文出发点一致——金额一律是整数
最小货币单位（明确写了 "There is no float money anywhere in this design"），`User` 是 frozen
dataclass，`Split` 是抽象基类加 `EqualSplit`/`ExactSplit`/`PercentageSplit`/`ShareSplit` 四个
子类，并且把"一百块三个人分，那一分钱归谁"点名为这道题的分水岭。
不同之处：它的余额是 `ExpenseManager` 里一张 `dict[User, int]` 的每人净额，所以化简很顺，
但答不出"A 和 B 之间还差多少"这个 Splitwise 的主界面问题；本文改成按用户对存净额，并在
"关键设计决策"里逐项对比了这两种表示的代价。它的观察者是一个带 `on_expense_added` /
`on_settlement` 两个方法的接口，本文改成单一的自描述事件加可调用对象。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/abhaypaswan/lld-python/tree/main/problems/splitwise)

## Archived copy
![[src-abhaypaswan-splitwise-clip]]
%% trellis:end %%
