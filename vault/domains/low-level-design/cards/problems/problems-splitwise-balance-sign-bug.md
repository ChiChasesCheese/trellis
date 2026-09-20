---
id: problems-splitwise-balance-sign-bug
node: problems.marketplaces.splitwise
type: qa
step: 8
tags: [grown]
---
## Q
分账（Splitwise）的账本每行存“hi 欠 lo 多少”，正值表示 hi 欠 lo。如果算每人净额时把符号写反（对 hi 加、对 lo 减），会出现什么现象？测试要怎么写才抓得住？

## A
不会抛任何异常，“谁欠谁多少”的列表一个字都不差（它读的是同一行的正负号），只有债务化简的结果会把每一笔建议转账的付款方和收款方整个对调——“Carol 该付 Alice 2000”变成“Alice 该付 Carol 2000”，在真实系统里是会赔钱的。防住它靠两条：符号方向只在记账那一处决定，别处一律经过它；测试断言 `(付款人, 收款人) -> 金额` 的完整映射，而不是只断言笔数或金额集合——只比金额的测试对这个 bug 完全是瞎的。
