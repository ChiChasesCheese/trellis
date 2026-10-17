---
id: amz-round-logical-and-maintainable-scoring
node: amazon.amz-round
type: qa
step: 2
tags: [grown]
---
## Q
Amazon 官方把 LLD 这一轮对应的考察项叫「Logical and Maintainable」，它具体给哪四件事打分？

## A
官方原文的四个要点：(1) 职责分离——按类和方法把解法拆成清晰的逻辑组件，不写「什么都干」的大函数；(2) 命名——变量、方法、类的名字能让没读过代码的人看懂并调试；(3) 可扩展——需求变化时逻辑能演进；(4) 测试名要描述业务与技术需求，且测试代码与名字一致。总之它考「别人接手能不能改」，不是考算法技巧。
