---
id: tc-precise-words
node: t04.precise-words
type: qa
step: 1
tags: [原则]
---
## Q
**Precise words · 一词一义**｜原则 · 必会

一份运行手册里，同一个组件一会儿叫 "worker"，一会儿叫 "agent"，一会儿叫 "runner"；还写着 "may cause some delay"。新同事问："这是三个东西吗？延迟多久？" 怎么改？

## A
**原则：** 一个概念只用一个名字，每个名字只指一个概念。换名字会让读者以为你换了东西。含糊的词（可能、一些、很快）换成能被检验的说法。

**怎么做：**
1. 给每个组件选一个名字，全文只用它；需要简称时先定义，之后只用简称。
2. 新术语第一次出现就定义，或给链接；术语多就放术语表。
3. 把 "some"、"may"、"soon" 换成数字、条件或范围。
4. 不确定时直接写不确定："We haven't measured this."
5. 避免只有一种文化才懂的习语，读者里有不少是第二语言读者。

**常见错法：**
- **同义词替换求"文笔好"：** 技术文档里这是在制造歧义。
- **把"可能"当保险：** 每句都 may，读者无从判断。
- **一个词两种意思：** 例如 "service" 既指进程又指团队。

**改写示例：**
- Before: "The worker pulls jobs from the queue. If the agent fails, some jobs may be delayed."
- After: "The worker pulls jobs from the queue. If a worker fails, its jobs wait up to 30 seconds before another worker takes them."

**出处：** Google Technical Writing One《Words》（developers.google.com/tech-writing/one/words：定义术语、一致使用术语）；《Audience》（避免习语）
