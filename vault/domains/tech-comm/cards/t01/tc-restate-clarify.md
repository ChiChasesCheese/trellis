---
id: tc-restate-clarify
node: t01.restate-clarify
type: qa
step: 1
tags: [原则]
---
## Q
**Restate & clarify · 防答非所问**｜原则 · 必会

面试官说："Design a system to handle notifications." 你立刻想到消息队列，开始画图。这里最可能出什么问题？先做什么？

## A
**原则：** 题目永远比你听到的模糊。先用自己的话**复述一遍**，再问几个会**改变设计**的问题，得到确认后才动手。这样"答非所问"在前两分钟就被发现，而不是在第三十分钟。

**怎么做：**
1. 复述：用一句话说出你理解的目标和范围，请对方确认。
2. 问会改变方案的问题（规模、延迟要求、一致性、谁是用户），不问对设计没影响的细节。
3. 把得到的约束写在白板角落，后面的取舍都回指它。
4. 问题控制在三个左右，其余写成假设："I'll assume X; tell me if that's wrong."

**常见错法：**
- **不问就画：** 方案很漂亮，但解的是另一道题。
- **问一长串清单：** 像在审问对方，也浪费时间。
- **复述原题照读：** 没有加进自己的理解，对方无法判断你有没有懂。

**改写示例：**
- Before: (draws a Kafka cluster in silence)
- After: "So we're building a system that sends push and email notifications to users. Before I start, three quick questions: roughly how many notifications per day, does order matter, and is delivery best-effort or guaranteed?"

<details class="pt" markdown="1"><summary>出处</summary>

Tech Interview Handbook（techinterviewhandbook.org/coding-interview，把"提澄清问题、讲清思路"列为面试评分项）；具体做法由规则推导，非引用

</details>
