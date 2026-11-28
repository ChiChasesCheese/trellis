---
id: hi-c-lld-design-principles-x07-name-principles
node: lld.in-a-hurry.design-principles.exam
type: qa
step: 7
---
## Q
**设计原则 · 被问用了哪些原则**｜考点 · 必会

设计结束，面试官问"你用到了哪些设计原则？"。怎么回答才加分？

## A
- **别报缩写表：** 面试官要的是应用，不是背诵
- **拿具体决定对应：** "计费规则放在 `Ticket` 里是因为它持有时间，规则跟着状态走；预留了策略抽出的位置，但现在只有一种规则所以没建（YAGNI）"
- **说出取舍：** 哪条原则被让步，为什么
- **一两个就够：** 讲最有分量的决定
