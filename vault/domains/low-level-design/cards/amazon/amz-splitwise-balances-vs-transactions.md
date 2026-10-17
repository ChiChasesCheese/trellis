---
id: amz-splitwise-balances-vs-transactions
node: amazon.amz-splitwise
type: qa
step: 4
tags: [grown]
---
## Q
在分账设计里，应该存每一笔交易，还是只存两两余额？查询「A 欠 B 多少」怎么做到 O(1)？

## A
两样都存，职责不同：交易流水只追加，用来审计和撤销；两两净余额 `dict[(a, b)] → 分` 用来回答查询。键要规范化——总是把 id 较小的放前面，正数表示前者欠后者——否则 (A,B) 和 (B,A) 各存一份会互相抵消不掉。每笔支出只更新「付款人 × 每个参与者」那几条余额，查询是一次字典读取。
