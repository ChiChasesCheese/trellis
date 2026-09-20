---
nodes: [problems.marketplaces.splitwise, patterns.strategy, oop.values, quality.errors]
tags: [problem]
---
# Drill：分账（Splitwise）

一群朋友一起出门，谁都可能替别人垫付，分摊方式各不相同（有人只吃了一半、有人带了两个人）。
系统要随时答得出"谁欠谁多少"，最后还要用尽量少的转账把账结清。金额一律是整数最小货币单位
（分），全程不出现一个浮点数。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：用户、小组、记一笔**均分**的开销，以及一张回答"谁欠谁多少"的余额表。
  付款人不一定是参与人之一（替一桌你没吃的饭买单是合法的）。引用不存在的用户要有明确的
  失败路径。先想清楚余额到底存在哪一层，再动手写。
- 第 2 关（约 15 分钟）：四种拆分方式——均分／按精确金额／按百分比／按份额。**每种自己校验
  自己的输入**（精确金额之和等于总额、百分比之和等于 100、份额必须为正），并且每人份额
  **精确加总等于总额**。说清楚 100 分三个人均分时那多出来的 1 分归谁、依据是什么。
- 第 3 关（约 15 分钟）：从净额出发做债务化简，用两个堆做"最大债权人配最大债务人"的贪心；
  说出它保证什么（≤ n-1 笔）、不保证什么，并给一个它不是最优的反例。同时多个线程可以并发
  记账，账本不能被改到一半就被读走。
- 第 4 关（选做）：结算还款、活动日志、以及多币种或按小组隔离的余额。评分点不是"实现了没有"，
  而是**加它要不要回头改前三关的代码**——四种拆分策略、账本、开销，一行都不该动。

**怎么练**：把 `vault/domains/low-level-design/problems/splitwise/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/splitwise -q`。

**评分点**
- 余额存成"每一对用户一行净额"，并说得出为什么不选"每人一个净额"或"每次从流水现算"（[[problems-splitwise-pairwise-ledger]]）。
- 账本的键规范化成唯一一行，净额归零时整行删掉而不是留一个 0——容器必须会缩小（[[problems-splitwise-canonical-key-and-shrink]]）。
- 余数有主且规则可解释：`Fraction` 精确份额 + 最大余数法，并列时按参与人顺序（[[problems-splitwise-largest-remainder]]）。
- 说得出这道题的拆分策略为什么该写成类而不是普通函数，判据是"携带数据"和"共享代码"（[[problems-splitwise-split-class-not-function]]、[[patterns.strategy|策略模式与可替换算法（Strategy）]]）。
- 校验写在各个拆分策略自己身上，入口没有 `isinstance` 类型判断链；和金额无关的不变式在构造时就抛（[[problems-splitwise-validation-in-strategy]]）。
- 贪心化简讲得出 n-1 的上界、NP-hard 的下限，并当场给出一个贪心不是最优的反例（[[problems-splitwise-greedy-not-optimal]]）。
- 净额符号和账本行的符号严格对偶；测试断言的是"付款人→收款人→金额"的完整映射，不是只比金额（[[problems-splitwise-balance-sign-bug]]）。
- 锁放在事务边界（记账门面）而不是数据结构里，通知在锁外发，并说得出 GIL 为什么替代不了这把锁（[[problems-splitwise-lock-and-notify]]）。
- 已记录的开销不可变：份额构造时算好并冻结，撤销靠记一笔反向账而不是改历史（[[problems-splitwise-expense-immutable]]）。

**题解**：[[solution-splitwise]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
