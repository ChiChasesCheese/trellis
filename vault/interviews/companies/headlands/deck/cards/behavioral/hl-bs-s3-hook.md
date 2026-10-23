---
id: hl-bs-s3-hook
node: behavioral.stories
type: qa
step: 16
---
## Q
无报错 bug 故事 S3 的钩子句是什么？用来回答哪些问题？有哪些数字？

## A
钩子："**My hardest bug threw no error: rows that should exist were simply missing.**"

用于：**hardest bug**、**on-call**、**how do you test**、**修一类问题**。

数字：约 **200 个商户**；成交量量级约 **$10M/天**（是**交易额，不是费用额**）；**4 个**测试漏洞原因；**2 个重载 → 1 个函数**；按"promote 后天数"分桶，**每桶覆盖率都是 0%**。
