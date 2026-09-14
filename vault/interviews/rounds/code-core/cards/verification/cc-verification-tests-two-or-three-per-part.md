---
id: cc-verification-tests-two-or-three-per-part
node: verification.tests
type: qa
---
## Q
Time is short. How many of your own tests per part, and which ones specifically?

## A
**Two or three per part, chosen to differ in *kind*, not in data.**

- One that exercises the part's **new** rule at its boundary ([[cc-verification-edge-exact-threshold-triple]]).
- One **degenerate** shape — empty or single record ([[cc-verification-edge-empty-and-single]]).
- One that re-runs an **earlier** part's example through the current code, so an extension that broke a previous part fails now instead of at submission.

Three tests of the same kind with different numbers cost the same minutes and cover one shape. Keep them as data — a list of `(input_lines, expected_lines)` — so adding a fourth is one line and re-running everything after an edit is one call ([[cc-verification-tests-table-driven]]).

## Q zh
时间紧。每个 part 你自己写几个测试？具体是哪几个？

## A zh
**每个 part 两到三个，按*种类*而非数据来挑。**

- 一个在边界上检验该 part **新增**规则的（[[cc-verification-edge-exact-threshold-triple]]）。
- 一个**退化**形态 —— 空输入或单条记录（[[cc-verification-edge-empty-and-single]]）。
- 一个把**更早**那个 part 的样例重新跑一遍当前代码的，这样扩展破坏了前面的 part 会当场失败，而不是等到提交时。

三个同类但数字不同的测试花掉同样的分钟，却只覆盖一种形态。把它们存成数据 —— 一个 `(input_lines, expected_lines)` 的列表 —— 加第四个就是一行，改完之后重跑全部就是一次调用（[[cc-verification-tests-table-driven]]）。
