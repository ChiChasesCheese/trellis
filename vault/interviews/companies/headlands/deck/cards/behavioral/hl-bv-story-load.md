---
id: hl-bv-story-load
node: behavioral.value-matrix
type: qa
step: 9
---
## Q
Headlands 的故事覆盖矩阵里，哪些故事承担的主答案（P）最多？"过载"（>4）说明什么风险？

## A
故事负载（P / S）：
- **S3**（无报错 bug）：P = 4，S = 3
- **S7**（schema pool）：P = 4，S = 3
- **S6**（异常检测器 go/no-go）：P = 3，S = 3
- **S8**（Terraform 7 分钟）：P = 3，S = 2
- **R1**（个人研究平台）：P = 3，S = 4

某个故事当主答案超过 4 个，说明对它**过度依赖**：同一场面试里不能把同一个故事讲两次，所以靠它覆盖越多价值，越容易在另一个问题上无故事可用。S3、S7 各是 4 个价值的主答案，是上限。
