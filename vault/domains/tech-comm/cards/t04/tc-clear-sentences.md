---
id: tc-clear-sentences
node: t04.active-voice-clear-sentences
type: qa
step: 2
tags: [原则]
---
## Q
**Clear sentences · 强动词**｜原则 · 必会

你写的一句话是："There is a cache that is used to store the results of recent queries, and a warning occurs if it is nearly full." 读起来很累。怎么改成一句顺口的话？

## A
**原则：** 句子的力量在**动词**。用具体动词，去掉 "there is / there are" 和 occur、happen 这类弱动词；少用主观形容词，把它换成可量化的事实。

**怎么做：**
1. 把 "There is X that does Y" 改成 "X does Y"。
2. 把 be、occur、happen 换成精确动词（issue、reject、drop）。
3. 把 "blazingly fast"、"very easy" 换成数字或事实。
4. 技术文档是教人，不是推销：营销腔留给别处。

**常见错法：**
- **名词化：** "perform an analysis of" 不如 "analyze"。
- **堆形容词副词：** "extremely fast" 不给读者任何信息。
- **弱动词加被动：** "A warning occurs" 谁发出的？

**改写示例：**
- Before: "There is a cache that stores recent query results."
- After: "A cache stores recent query results."
- Before: "A warning occurs if the disk is nearly full."
- After: "The system issues a warning when the disk is nearly full."
- Before: "This update makes search blazingly quick."
- After: "This update cuts search time from 4 seconds to 1 second."

<details class="pt" markdown="1"><summary>出处</summary>

Google Technical Writing One《Clear sentences》（developers.google.com/tech-writing/one/clear-sentences）；改写例句为演示用

</details>
