---
nodes: [problems.marketplaces.splitwise]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/splitwise.md
---
# awesome-low-level-design — Splitwise

值得读：需求清单写得很全（建组、加开销、三种拆分、结算、交易历史、并发一致性），六种语言
并排给同一份设计，适合拿来对照"面试官心里那张需求表"有没有漏项；`Split` 抽象基类加
`EqualSplit`/`PercentSplit`/`ExactSplit` 的骨架和本文一致。
不同之处：这份是本文的反面参照系。它把 `SplitwiseService` 写成 Singleton；余额存在每个
`User` 对象里的一张"我和别人"的映射（同一对关系在两个人身上各存一份，必须同时更新，漏一处
就永久对不上）；金额用浮点数；并发靠 `ConcurrentHashMap` 这类并发容器，而不是界定事务边界。
本文在"关键设计决策""常见错误"两节逐条说明了为什么不这样做。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/splitwise.md)
%% trellis:end %%
