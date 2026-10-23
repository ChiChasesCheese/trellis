---
id: hl-cq-q38-followups
node: cpp-questions.i-low-latency
type: qa
step: 14
---
## Q
三个追问：无分支一定更好吗？`[[likely]]` 是什么？间接分支（虚调用、switch 表）怎么预测？

## A
- **无分支不一定更好**：分支可预测时，带分支的版本可能更快（跳过了工作）；无分支代码还会增加数据依赖。
- **`[[likely]]`**：C++20 属性，提示哪条路径更可能走；影响代码布局，不是直接影响预测硬件。
- **间接分支**：虚调用和 switch 表用间接分支预测器；多态程度很高（megamorphic）的调用点更容易预测失败。
