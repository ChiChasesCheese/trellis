---
id: tc-non-technical
node: t03.non-technical-audiences
type: qa
step: 1
tags: [原则]
---
## Q
**Non-technical audiences · 类比与后果**｜原则 · 必会

支付服务出了三十分钟的故障，客服主管问你："到底发生了什么？我要怎么告诉客户？" 你想回答"数据库连接池被耗尽了"。这样可以吗？

## A
**原则：** 对不懂技术的人，讲**结果和后果**，不讲机制。他需要的是"客户看到了什么、影响多大、什么时候恢复、他能对客户说什么"，而不是系统内部怎么坏的。机制要讲，也只用一个贴近生活的**类比**，且只给一个。

**怎么做：**
1. 先说用户可见的现象："For 30 minutes, some customers couldn't complete payments."
2. 再说范围和现状：多少人受影响，现在是否恢复。
3. 说他能做什么：给客户的口径、补偿的依据。
4. 非要解释原因时，用一个类比，用完就收："Too many people tried to go through one door at once."
5. 去掉术语和内部缩写，用简单的词，避免只在某种文化里才懂的说法。

**常见错法：**
- **用术语解释术语：** "连接池耗尽"又要再解释。
- **类比太多或太深：** 听的人记住了类比，忘了结论。
- **只讲原因不讲影响：** 他最关心的问题没有答案。

**改写示例：**
- Before: "The connection pool was exhausted because of a retry storm."
- After: "Between 2:10 and 2:40, about 8 percent of payments failed, and customers could retry successfully afterward. The cause was a traffic spike we didn't handle well. It's fixed, and here is what we're doing so it doesn't recur."

**出处：** Google Technical Writing One《Audience》（匹配词汇、知识的诅咒、用简单词汇、避免习语）；类比与后果的做法由规则推导
