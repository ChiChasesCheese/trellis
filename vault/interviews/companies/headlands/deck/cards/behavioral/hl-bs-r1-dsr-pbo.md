---
id: hl-bs-r1-dsr-pbo
node: behavioral.stories
type: qa
step: 5
---
## Q
Deflated Sharpe 和 PBO 各防什么问题？为什么这要求账本必须诚实？

## A
- **Deflated Sharpe**：试得越多，最好的那个越可能只是**运气**；它按**试验次数**给 Sharpe 打折。
- **PBO**（probability of backtest overfitting）：样本内的赢家在样本外**排到中位数以下**的概率。

所以账本必须**诚实**：Deflated Sharpe 需要知道你**一共试了多少次**，只记赢家会让折扣算错。"下次会怎么不同"：【待补：下次会怎么做不同】。
