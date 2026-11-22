---
id: tc-uncertainty
node: t01.answering-under-uncertainty
type: qa
step: 1
tags: [惯用说法]
---
## Q
**Answering under uncertainty · 不确定时怎么答**｜惯用说法 · 必会

面试官问："How many QPS would this service need to handle?" 题目没给数据，你也没有确切答案。怎么既回答，又让对方知道哪些是假设？

## A
**可以这么说：**
- "I don't have the exact number, but I'd assume around 5,000 QPS at peak. Does that sound reasonable?"
- "My working assumption is that reads dominate, about ten to one."
- "I'm fairly confident about the storage estimate, less so about the traffic."
- "If that assumption is wrong, the design changes in one place: the cache sizing."
- "I'm not sure. My best guess is X, and I'd verify it by Y."

**别这么说：**
- "I don't know." 然后沉默。
- 把猜测说成事实："It's definitely 5,000." 之后被推翻会很难堪。

**语气：** 三步：给一个具体的估计 → 说明这是假设和你的把握 → 指出它错了会影响什么。对方听到的是有条理的工程判断，而不是猜。

**出处：** 惯用说法，非引用
