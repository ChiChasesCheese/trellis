---
id: method-testability-signals
node: method.evaluation
type: qa
---
## Q
A grader skims your code for "testable" in about 30 seconds. What are they actually looking at?

## A
Whether they could exercise one rule **without constructing the world**:

- Does the fee/allocation logic take its inputs as parameters, or does it reach into a fully-built `ParkingLot`?
- Any `new Collaborator()`, `Singleton.getInstance()`, or `LocalDateTime.now()` **inside** logic? Each is an unsubstitutable dependency — an injected `Clock` is the standard tell that you've met this before.
- Are the interesting rules pure functions of their arguments, with I/O and mutation pushed to the edges?

"I wrote tests" is weaker evidence than a constructor that lets them.


## Q zh
一个评分者用 30 秒的时间浏览你的代码"可测试"。他们实际上看的是什么?

## A zh
他们是否能**不构建世界**的情况下练习一个规则:

- 费用/分配逻辑是参数作为其输入，还是到达一个完全构建的 `ParkingLot`?
- 任何 `new Collaborator()`、`Singleton.getInstance()` 或 `LocalDateTime.now()` **内部**逻辑? 每一个是一个不可替代的依赖 — 一个注入的 `Clock` 是标准的迹象你已经遇见过这个。
- 是否有趣的规则是它们的参数的纯函数，I/O 和突变推到边缘?

"我写了测试"比让他们的构造函数弱。
