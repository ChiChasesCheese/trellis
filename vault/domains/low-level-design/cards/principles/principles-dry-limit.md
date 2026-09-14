---
id: principles-dry-limit
node: principles.simplicity
type: qa
---
## Q
Two modules contain near-identical 10-line blocks. When is extracting a shared helper the WRONG move?

## A
When the duplication is **accidental**: the blocks look alike today but encode different business knowledge that will change for different reasons. The merged helper then sprouts flags and branches per caller — the wrong abstraction.

DRY deduplicates *knowledge*, not text. Heuristics: "duplication is cheaper than the wrong abstraction" (Sandi Metz); wait for the rule of three before extracting.

## Q zh
什么时候应该因为代码重复而不是因为不是 DRY 而违反 DRY 原则？

## A zh
两个代码片段看起来相似，但：
- 它们由于不同的原因而改变（它们有不同的 "为什么")
- 它们会在不同的时间演变成不同的方向
- 将它们提取到单个位置会创建一个虚假的抽象，实际上约束了它们各自的演变

一个常见的例子：两个不同的验证规则可能从相同的条件开始，但由于业务需求，它们最终会分支出去。"湿" 代码在这里会更好。
