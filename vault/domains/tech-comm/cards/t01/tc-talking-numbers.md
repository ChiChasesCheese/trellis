---
id: tc-talking-numbers
node: t01.talking-about-numbers
type: qa
step: 1
tags: [惯用说法]
---
## Q
**Talking about numbers · 量级与基线**｜惯用说法 · 追问

你想告诉评审人"新方案把延迟降到了 87.3 毫秒"。听的人拿不到判断依据。怎么让数字有意义？

## A
**可以这么说：**
- "p99 latency went from about 400 milliseconds to under 100, so roughly four times faster."
- "That's on the order of a few thousand requests a second, not millions."
- "For context, the old system handled around 200 a second."
- "It's about 20 percent of our infrastructure bill, so it's worth optimizing."
- "Let me round that to 90 milliseconds. The exact figure doesn't change the conclusion."

**别这么说：**
- "It's 87.3 milliseconds." （没有基线，也没有意义）
- "It improved a lot." （不给任何数字）

**规则：** 数字要带三样东西：**基线**（对比什么）、**量级**（几个数量级）、**四舍五入**到不改变结论的精度。比较时说清是百分比还是倍数，起点和终点各是多少。

**出处：** 惯用说法，非引用；与 Numbers in English 互补（那里讲读法）
