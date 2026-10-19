---
id: nr-amz-r1-starl
node: amazon.r1
type: qa
step: 2
---
## Q
【R1 · Quant-Stroller（个人项目：反过拟合的研究平台）】STAR-L 提纲（60–90 秒）

## A
**S**

- 个人项目，2026-06 至今：**多市场**量化研究平台，**Python**
- 约 **66K 行**、**470+ 测试文件**；美股、加密、A 股、外汇

**T**

- 设计目标：新市场或数据商 = **薄适配器**，**策略代码零改动**
- 第二个目标：**抵抗过拟合**的纪律

**A**

- 保持 **4 个窄 seam**：数据源、因子、策略、broker
- 建**双关卡**：**purged CV、Deflated Sharpe、PBO**，然后 **NautilusTrader 执行重放**
- **340+** 次实验记入 **append-only ledger**，每市场有成本模型
- 把一个中国小盘月度策略过了**两个关卡**
- 部署到**实盘模拟（paper-trading）**，带**事前风控**

**R**

- 扣 **10 bps** 后 **excess Sharpe 1.39**；是 paper-trading，不是盈利证明

**L**

- 用**流程**反驳自己的想法：ledger 显示我试了多少
- 没有通过**两个独立关卡**，什么都不上线
