---
id: tc-rule-of-three
node: t01.rule-of-three
type: qa
step: 1
tags: [原则]
---
## Q
**Rule of three · 并列项数量**｜原则 · 必会

你准备了"七个原因"说明为什么要迁移数据库，开讲后发现听的人眼神已经飘了。该怎么改？

## A
**原则：** 听的人短时间能记住的并列项很有限（Minto 引 Miller：约七个，有人只有五个；三个最容易记）。超过四五个，就要**先分组再说**，让他只记住组。

**怎么做：**
1. 并列要点超过三四个，就先归类，每类起一个有信息量的名字。
2. 上层只说类别（三个以内），细节放到各类下面。
3. 每组内部要有**排序依据**：按步骤的时间先后、按系统的结构部位、或按重要程度（Minto 的三种 logical order：time、structural、degree）。
4. 说不出为什么是这个顺序，说明分组本身有问题。

**常见错法：**
- **为凑三个而硬拆或硬合：** Minto 讲的是数量上限和分组，并没有"必须三点"的规矩。真有两点就说两点。
- **只数不分组：** "七个原因"读者一个也记不住。
- **顺序随意：** 最弱的理由放第一，最强的反而被忽略。

**改写示例：**
- Before: "There are seven reasons: cost, licensing, replication lag, schema changes, tooling, hiring, and vendor support."
- After: "There are three reasons: it costs less to run (cost, licensing), it is easier to operate (replication, schema changes, tooling), and it is easier to staff (hiring, vendor support). Let me start with the biggest, cost."

<details class="pt" markdown="1"><summary>出处</summary>

Minto p. 17–24（Ch.1 The Magical Number Seven）；p. 33–48（Ch.2 The Horizontal Relationship）；p. 97–112（Ch.6 Imposing Logical Order）

</details>
