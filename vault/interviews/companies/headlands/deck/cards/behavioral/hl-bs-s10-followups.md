---
id: hl-bs-s10-followups
node: behavioral.stories
type: qa
step: 52
---
## Q
被追问 S10：谓词错在哪？一句话根因？延迟是竞态吗？别人怎么信任你的数字？是什么触发你重读谓词？
What was wrong with the predicate? Root cause in one sentence? Is the lag a race? How do others trust it?

## A
- **What was wrong?** 没检查**手续费创建时计划是否已存在**。
- **Root cause in one sentence?** 这条路径**复制了信用记录的历史计划 id**，而不是**在收费时点解析**。
- **Is the lag a race?** 同形：两个写入方，**读取方的时间**决定答案；修法是**在事件时间点解析**。
- **How do others trust it?** 每个结论都有一条**查询**；逻辑里**没有写死国家**，所以先排除"美国特例"。
- **What triggered the re-read?** 【待补：是什么让你重审了谓词】
