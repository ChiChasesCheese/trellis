---
id: tc-know-your-audience
node: t03.know-your-audience
type: qa
step: 1
tags: [原则]
---
## Q
**Know your audience · 听众三问**｜原则 · 必会

你要把"数据库升级到新大版本"的方案讲给三类人：同组工程师、产品经理、总监。你先回答自己什么问题，才能决定内容？

## A
**原则：** 好的文档或发言 = 听众完成任务所需的知识，减去**他们已经有的知识**。动笔之前先答三问：

| 问题 | 它决定什么 |
|---|---|
| 他们已经知道什么？ | 哪些可以省，哪些要补 |
| 他们要根据你讲的做什么决定？ | 哪些内容必须放最前 |
| 他们最关心什么？ | 用什么角度讲同一件事 |

**怎么做：**
1. 先按角色粗分（工程师、PM、管理者），再想"他们离这个主题有多近"：刚参与过的人和三个月没碰的人差别很大。
2. 写下读完（听完）之后，他们应该**知道什么、能做什么**。
3. 术语和缩写按最不熟的那位来定义。
4. 避免只有一个文化圈才懂的说法（如 "a piece of cake"），读者很多是用第二语言或翻译工具读。

**常见错法：**
- **知识的诅咒：** 专家忘了新手不知道什么，直接用内部缩写。
- **一份材料给所有人：** 结果谁都不满意。
- **只讲你想讲的：** 不管听众要做什么决定。

**示例：** 同一件事。给工程师："Upgrade needs a 20-minute read-only window; here is the rollback plan." 给总监："We need approval for one maintenance window; risk is low, rollback is tested."

<details class="pt" markdown="1"><summary>出处</summary>

Google Technical Writing One《Audience》（developers.google.com/tech-writing/one/audience）；Minto p. 57–64（Ch.4：Situation 即读者已知）

</details>
