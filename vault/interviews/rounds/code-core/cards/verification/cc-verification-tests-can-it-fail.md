---
id: cc-verification-tests-can-it-fail
node: verification.tests
type: qa
---
## Q
You add four tests and all four pass immediately. What is the one check you run before believing them?

## A
**Prove a test can fail.** Run the suite against an empty stub, or break the function on purpose, and confirm it goes red.

- Common vacuous tests: asserting on an empty result when the function returns `[]` for *everything*; comparing a value with itself through a shared helper; asserting only `is not None`.
- A test whose expected value came from your own implementation's output tests that the code has not changed, not that it is correct. Expectations must come from the statement, from hand computation, or from an independent oracle ([[cc-verification-invariant-brute-force-oracle]]).
- One deliberate mutation per part costs about 20 seconds and is the only evidence your suite is not decorative.

## Q zh
你加了四个测试，四个立刻全过。在相信它们之前，你要做的那一项检查是什么？

## A zh
**证明测试有能力失败。** 拿一个空桩跑一遍套件，或者故意把函数改坏，确认它会变红。

- 常见的空转测试：函数对*任何输入*都返回 `[]`，你却在断言空结果；通过同一个辅助函数把值和它自己比；只断言 `is not None`。
- 期望值取自你自己实现输出的测试，测的是「代码没变」，不是「代码正确」。期望值必须来自题面、手算、或一个独立的 oracle（[[cc-verification-invariant-brute-force-oracle]]）。
- 每个 part 故意改坏一次约花 20 秒，而这是你的测试套件不是装饰品的唯一证据。
