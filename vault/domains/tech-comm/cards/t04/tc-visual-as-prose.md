---
id: tc-visual-as-prose
node: t04.writing-out-a-visual-as-prose
type: qa
step: 1
tags: [原则]
---
## Q
**Writing out a visual as prose · 把图写成文字**｜原则 · 追问

文档里要描述一个三层架构，但这次不能放图（邮件、屏幕阅读器、文本评论）。你写道："一个关键的改进领域是提升系统各层的处理效率与协同。" 读者没有任何画面。怎么写？

## A
**原则：** 读者读句子时会在脑里**建一幅画**，每读一个词往里加东西。让文字帮他建图：**先给整体的轮廓，再按顺序往里放细节**；每句话都要有可以"看到"的东西。

**怎么做：**
1. 先想象你画的图是什么样；写第一句，让读者先有轮廓："The system has three layers, stacked from the user down to storage."
2. 然后按图的顺序逐个放：先上、后中、再下，不要跳。
3. 每放一个，说它**和上一个的关系**："The gateway sits above the services and forwards each request."
4. 抽象的名词换成具体的东西和动作。
5. 写完把它画出来，看画得出来吗；画不出来，就是还抽象。

**常见错法：**
- **抽象名词堆叠：** "提升协同与效率"，读者没有东西可抓。
- **细节先于轮廓：** 读者没有地方放它。
- **顺序跳跃：** 先讲底层，再讲顶层，又回头。

**改写示例：**
- Before: "A key area for improvement is better coordination across layers."
- After: "Requests enter through the gateway, pass to one of three services, and end in a shared database. Two of the three services each query the database separately; those two queries are the ones to merge."

**出处：** Minto p. 225–232（Ch.12 Logic in Imagery：Create the Image / Copy the Image in Words）
