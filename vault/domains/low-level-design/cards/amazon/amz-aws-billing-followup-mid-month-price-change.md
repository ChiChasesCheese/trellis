---
id: amz-aws-billing-followup-mid-month-price-change
node: amazon.amz-aws-billing
type: qa
step: 7
tags: [grown]
---
## Q
在 AWS 账单服务里，面试官追问「月中调价」或「不同服务用不同币种」。该改哪里，哪里不动？

## A
新增 `PriceBook`：每个 (服务, 指标) 一串带生效时间的价格版本，`version_at` 用 `bisect_right` 取用量发生时刻生效的版本，每个版本带币种。账单按 (服务, 指标, 版本) 聚合，一个版本一行；`Invoice.totals` 按币种分别求和，`Money` 币种不同相加就抛错。费率类不动。例：10 月 16 日起 1 元涨到 2 元，10 日的 10 小时按 1 元、20 日的按 2 元，共 30 元。约定：阶梯在每个版本内重新计量。
