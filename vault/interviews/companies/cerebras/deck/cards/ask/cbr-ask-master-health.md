---
id: cbr-ask-master-health
node: ask.hm
type: qa
step: 3
---
## Q
反问招聘经理：怎么问 master 分支现在有多健康？

## A
- **问法**："How healthy is master today — roughly how often is it green, and how long does a red failure stay unowned?"
- **为什么问**：职位要"improve master and release-branch stability"，这个数字就是你的起点。
- **好答案**：有数字，哪怕不好看，并且知道主要原因。
- **坏答案**：没人知道。连度量都没有，第一个月的工作是建度量。
- **相关的好问题**："What's a recent failure that crossed layers, and how long did it take to find the owner?"——听排查工具成熟不成熟。
