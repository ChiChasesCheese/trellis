---
id: method-self-verification
node: method.evaluation
type: qa
---
## Q
Why should you run and verify your own code before the interviewer asks — and how, when no test framework is set up?

## A
Rubrics explicitly score self-verification: a bug you catch is a plus signal; the same bug caught by the interviewer is a minus. Cheap method without a framework:

- a `main()` driver that exercises the happy path plus one edge case (full lot, invalid unpark)
- state the expected output **before** running, then run

Predict-then-run demonstrates you reason about the code rather than poke at it.


## Q zh
为什么在面试官问之前你应该运行和验证你自己的代码 — 以及怎样，当没有测试框架被设置?

## A zh
标准明确评分自我验证: 你抓住的一个 bug 是加号信号；相同的 bug 被面试官抓住是减号。没有框架的便宜方法:

- 一个 `main()` 驱动练习快乐路径加上一个边界情况（满的停车场、无效取泊）
- 在运行之前说明预期的输出，然后运行

预测-然后-运行演示你推理代码而不是戳它。
