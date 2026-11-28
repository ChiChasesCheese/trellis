---
id: mlp-deepdive-impact-trust
node: deepdive.impact
type: qa
step: 4
---
## Q
**怎么证明结果可信、怎么用 AI**｜项目深挖

“How did you test it? How do you use AI tools, and how do you trust the code?”

## A
可信靠的是测试、对拍和闸门，不是读代码的感觉。

- **Quant-Stroller：** 470 多个测试文件；数据面用泄漏回放，策略层用 golden backtest（固定输入的回测结果与存档比对），执行层与 NautilusTrader 对拍。
- **Amex 管线：** 行级、批级、对账级三层；与 Amex 自己的汇总记录对账。
- **interchange 切换：** 把即将上线的生产查询当 `count(*)` 先跑一整天，验证和生产是同一份 SQL。
- **AI 工具：** 简历上写了用 Claude Code 做 review、测试生成和重构，把旧的 Ruby、Kotlin 业务逻辑迁到 Snowflake、Java，用全面测试保证行为一致。信任来自测试和行为对拍；schema pool 让多个智能体并行；钱相关代码每个 diff 自己读。

**英文答法。**
- I use Claude Code for **review, test generation and refactoring**; I moved legacy **Ruby and Kotlin** logic to **Snowflake and Java** with comprehensive tests ensuring **behavioural parity**.
- Trust comes from **tests and behavioural comparison**, not from reading the code and feeling good.
- I plan with the agent, **test-first each phase**, and put **CI and monitoring gates** around it; in money code I **read every diff myself**.
- I'm the **tech lead of a team of agents**, and I own every diff.

**追问。**
- **Why one SQL for validation and production?** There's no "validated one thing, shipped another".
