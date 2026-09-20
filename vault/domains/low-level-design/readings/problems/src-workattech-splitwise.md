---
nodes: [problems.marketplaces.splitwise]
url: https://workat.tech/machine-coding/editorial/how-to-design-splitwise-machine-coding-ayvnfo1tfst6/
tags: [no-archive]
---
# workat.tech — How to design Splitwise (machine coding)

值得读：面向机考的 Java 编辑部题解，把"需求怎么一关一关加码、每一关该交付什么"的节奏讲得
很清楚，本文的分关划分参考了它；它也明确指出输入输出格式和命令行驱动（Driver）在机考里
本身就是评分项。
不同之处：余额用 `Map<String, Map<String, Double>>` 的双向嵌套表，同一对关系存两处、金额是
`Double`；均分的余数直接塞给参与人列表里的第一个人（`splitAmount + (amount - splitAmount * n)`），
没有给出规则依据；债务化简被标为可选需求并跳过了。它还按拆分方式给 `Expense` 分出
`EqualExpense`/`ExactExpense`/`PercentExpense` 三个子类——本文认为开销和拆分方式是正交的两个
维度，应该组合而不是继承。
