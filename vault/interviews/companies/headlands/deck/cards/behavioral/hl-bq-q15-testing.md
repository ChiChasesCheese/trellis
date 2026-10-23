---
id: hl-bq-q15-testing
node: behavioral.question-bank
type: qa
step: 31
---
## Q
你怎么做测试？（60 秒）
How do you test?

## A
故事：S3 + S5 + R1。

- **测输出，不只测路径**：我们的测试断言的是**路由**，从没断言**手续费**；**fixture** 和真实群体不一致。
- **用你要发布的东西来验证**：字段级对比（**>99.9%**）之后，我把**生产查询本身**当作 count 来跑（**+0.224%**）。
- **测试保护结果**：我的回测平台有 **470+ 个测试文件**和策略的**两道门**。
- 一句话："A check that fires on **missing data** beats a dashboard nobody opens."
