---
id: tc-diagram-anti-patterns
node: t02.diagram-anti-patterns
type: qa
step: 1
tags: [原则]
---
## Q
**Diagram anti-patterns · 架构图常见错法**｜原则 · 追问

同事给你看一张架构图：二十几个框，箭头密密麻麻，有的双向有的单向，颜色五种，没有说明。你看了三分钟，不知道它想说什么。该怎么改？

## A
**原则：** 一张图要有一个**要点**（takeaway），其他东西都要为它服务。Google 的经验法则：一张图的信息量不超过一段话，或不超过约五条要点就能解释清楚。

| 反模式 | 怎么改 |
|---|---|
| 箭头没有含义（请求？事件？依赖？） | 箭头旁标内容；一种箭头只表示一种关系 |
| 一个框一个组件，二十几个框 | 拆成"总图"加"每个子系统一张图" |
| 没有边界 | 用方框圈出 trust boundary、团队或部署边界 |
| 所有元素一样重要 | 用颜色或粗线突出焦点，其他变淡 |
| 颜色多、对比弱 | 限制颜色；保证文字清晰可读 |
| 双向箭头 | 请求和返回分开画 |

**怎么做：**
1. 先写**图注**（caption），一句话说这张图要读者记住什么，再画图。
2. 画完问：能否再简化？要不要拆成两张？
3. 把重点之外的东西调淡。

**常见错法：**
- **想一张图讲完所有事。**
- **图注只写"系统架构图"：** 没有要点。

<details class="pt" markdown="1"><summary>出处</summary>

Google Technical Writing Two《Illustrating》（developers.google.com/tech-writing/two/illustrations）

</details>
