---
id: classify-quasi-identifier-risk
node: security.data-classification-and-tagging
type: qa
tags: [grown]
---
## Q
一张表去掉了姓名和身份证号，只保留邮编、出生日期和性别。为什么数据分类（data classification）仍会把这些列标为准标识符（quasi-identifier），需要保护？

## A
准标识符单独看不能识别个人，但几列组合起来往往可以唯一定位到一个人（邮编 + 出生日期 + 性别就能重识别出很大比例的人）。所以只删直接标识符（identifier）并不等于匿名化。把它们标为 QUASI_IDENTIFIER，是为了提醒治理团队对这些列也施加脱敏、泛化或聚合限制，而不是因为它们本身敏感。
