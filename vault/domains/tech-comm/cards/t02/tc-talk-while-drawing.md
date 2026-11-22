---
id: tc-talk-while-drawing
node: t02.talk-while-drawing
type: qa
step: 1
tags: [原则]
---
## Q
**Talk while drawing · 边画边讲**｜原则 · 必会

你画一个缓存模块用了四十秒，这四十秒里你一句话没说，面试官看着你的背影。这样有什么问题？怎么改？

## A
**原则：** 画图的同时一直在讲：**说你在画什么、它负责什么、为什么放在这里**。沉默时对方没法评价你的思路，也插不进话。

**怎么做：**
1. 落笔前先说一句："I'll add a cache here, to take read load off the database."
2. 每画一个框，点名它的**职责**，一句话，不超过一句。
3. 尽量侧身站，让对方看得见白板和你的脸（线上就是别一直盯着工具栏）。
4. 想到以后再处理的复杂点，口头加一句"later"，白板上记个小标记，然后继续："Noted, I'll come back to cache invalidation."
5. 讲完一块停一下，给对方留插话的位置。

**常见错法：**
- **沉默地画：** 对方只能猜你想什么。
- **背对对方讲：** 声音被白板吞掉，对方也看不到你的表情。
- **把每一块都当场讲透：** 主路径还没成形就陷进细节。

**改写示例：**
- Before: (silent for 40 seconds, then) "OK, so this is the cache."
- After: "I'm adding a cache between the service and the database. Its job is to serve hot reads, so the database only sees misses. I'll note that invalidation is a risk and come back to it."

<details class="pt" markdown="1"><summary>出处</summary>

hellointerview.com/learn/system-design/in-a-hurry/delivery（talking through your thought process；simple verbal callout and written note, then move on）

</details>
