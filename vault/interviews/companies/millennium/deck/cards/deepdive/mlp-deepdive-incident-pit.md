---
id: mlp-deepdive-incident-pit
node: deepdive.incidents
type: qa
step: 1
---
## Q
**Quant-Stroller 最难的问题：前视泄漏**｜项目深挖

“What was the hardest engineering challenge in this project?”

## A
最难的是 point-in-time 面板：回测里任何一天用到的数据，必须是当天真的已知的数据，不能偷看未来。

- **问题：** 5,500 只股票的 A 股全集，有幸存者偏差（只看到活下来的公司）和财报重述（数据商事后修改过去的数字）。如果取“最新值”，回测会悄悄用上未来信息，结果好看但不真实。
- **做法：** 用数据商快照日期做 as-of 连接（as-of join，取某时刻已知的最近一条），而不是取最新值。
- **校验：** 随机抽一个日期回放，检查没有未来的数据混进来。这就是泄漏回放校验。
- **另一层防线：** 策略要过统计闸门（净化交叉验证、deflated Sharpe、PBO）和执行闸门，才能进纸面交易；340 多个实验写进只追加的账本。

**英文答法。**
- The hardest problem was the **point-in-time panel**: a **5,500-stock A-share universe** with **survivorship and restatement** issues.
- I used an **as-of join over vendor snapshot dates** instead of "latest value".
- To prove it, a validation **replays a random date** and checks that **nothing from the future leaked in**.

**追问。**
- **How did you test it?** 470-plus test files; the leakage replay on the data plane, golden backtests on the strategy layer, and execution cross-checks against NautilusTrader.
- **Async in the project?** Data pulls use asyncio with a semaphore; training uses multiprocessing; I don't mix them.
