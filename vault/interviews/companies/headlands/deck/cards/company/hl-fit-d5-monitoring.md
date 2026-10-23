---
id: hl-fit-d5-monitoring
node: company.fit
type: qa
step: 17
---
## Q
JD 日常工作 "Develop and improve monitoring and proactive detection capabilities"，你用什么故事回答？强调什么？

## A
评级：**强**。

- 简历：on-call，建 transaction-tracing 与可观测性栈（Sentry、Datadog）。
- 自己建的每日健康检查"每笔 settled 交易都有费用"，抓到了静默 NULL 事故（ACH NULL）；还有异常检测器 + go/no-go。
- 强调"检查是对的，不能压掉"。
- 可补一句："a check that fires on missing data is better than a dashboard nobody opens."
