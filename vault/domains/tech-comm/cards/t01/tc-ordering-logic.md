---
id: tc-ordering-logic
node: t01.ordering-logic-time-structural-degree-order
type: qa
step: 1
tags: [原则]
---
## Q
**Ordering logic · 三种排序**｜原则 · 追问

你要讲"系统有三个问题"，又要讲"迁移分三步"，还要讲"团队分四个部门要做什么"。每一组里的顺序该按什么排？

## A
**原则：** 一组并列要点之所以能成组，必有一种逻辑；这种逻辑决定了顺序。只有三种：

| 来源 | 顺序 | 例子 |
|---|---|---|
| 一件事的**步骤**（原因到结果） | Time order：按先后 | 迁移三步：备份、同步、切换 |
| 把整体**拆成部分** | Structural order：按结构部位 | 前端、网关、存储，沿着请求路径讲 |
| 把**同类的东西**归在一起 | Degree order：按程度排序 | 三个风险，按影响从大到小 |

**怎么做：**
1. 先问：这组要点是怎么来的（步骤、部分、还是同类）？
2. 按对应顺序排；找不到顺序，说明分组有问题。
3. 步骤组的概括是"做完这些的效果"；同类组的概括是"它们共同的特征"。

**常见错法：**
- **随手排序：** 听的人看不出逻辑。
- **把三种混在一起：** 一条是步骤，一条是风险，一条是部门。
- **同类组不按程度：** 最重要的放在最后一条。

**示例：** "Three risks, in order of impact: data loss, downtime, and cost overrun. Data loss first, because it can't be undone."

<details class="pt" markdown="1"><summary>出处</summary>

Minto p. 97–112（Ch.6 Imposing Logical Order：Time Order / Structural Order / Degree Order）

</details>
