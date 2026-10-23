---
id: hl-j02-binary-compat
node: java21.j02-sealed
type: qa
step: 20
---
## Q
给 `sealed` 类型的 `permits` 加一项，对已有的 `switch` 在"重新编译"和"不重编译直接运行"两种情况下分别有什么后果？

## A
- **重新编译**：旧 `switch` 因为没处理新变体而报编译错误——这正是目的。
- **不重编译**直接跑旧 class：旧 `switch` 遇到新变体会抛 **`MatchException`**（模式匹配 `switch` 里的运行时兜底异常）。

所以在公共 API 里给 `sealed` 类型加变体是**不兼容变更**。
