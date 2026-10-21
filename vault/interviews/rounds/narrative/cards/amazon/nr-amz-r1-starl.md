---
id: nr-amz-r1-starl
node: amazon.outline
type: qa
step: 38
---
## Q
<p class="title">Quant-Stroller 研究平台<span class="meta">02 提纲</span></p>

STAR-L 提纲（60–90 秒）

## A
<span class="label">S</span>

- 个人项目，2026-06 至今：**多市场**量化研究平台，**Python**
- 约 **66K 行**、**470+ 测试文件**；美股、加密、A 股、外汇

<span class="label">T</span>

- 设计目标：新市场或数据商 = **薄适配器**，**策略代码零改动**
- 第二个目标：**抵抗过拟合**的纪律

<span class="label">A</span>

- 保持 **4 个窄 seam**：数据源、因子、策略、broker
- 建**双关卡**：**purged CV、Deflated Sharpe、PBO**，然后 **NautilusTrader 执行重放**
- **340+** 次实验记入 **append-only ledger**，每市场有成本模型
- 把一个中国小盘月度策略过了**两个关卡**
- 部署到**实盘模拟（paper-trading）**，带**事前风控**

<span class="label">R</span>

- 扣 **10 bps** 后 **excess Sharpe 1.39**；是 paper-trading，不是盈利证明

<span class="label">L</span>

- 用**流程**反驳自己的想法：ledger 显示我试了多少
- 没有通过**两个独立关卡**，什么都不上线

<div class="sources"><b>表达 · business English</b><br>• <b><i>design goal</i></b> — 设计目标<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“My design goal was zero strategy-code changes when a market is added.”</span><br>• <b><i>pre-trade risk check</i></b> — 下单前的风控检查<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The paper-trading loop runs pre-trade risk checks before every order.”</span><br>• <b><i>independent check</i></b> — 相互独立的校验<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Nothing ships without two independent checks, not one.”</span></div>
