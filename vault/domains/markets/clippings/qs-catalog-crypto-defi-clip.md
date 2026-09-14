---
title: 'Family 12: Crypto & DeFi'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/catalog/12-crypto-defi.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 家族 12:加密与 DeFi(Crypto & DeFi)

> **核心概念(从零讲)**:**加密是最年轻、散户最多、最不拥挤的市场 —— 经典异象在这里又强又新鲜,而且有传统市场没有的全新结构性套利。** 它 24/7 交易、有永续合约/资金费率/链上透明数据这些独特机制。**为什么存在(行为 + 结构 + 新机制)**:散户主导 → 行为偏差更强(动量、反转都更猛);市场新、参与者杂 → 结构性套利(交易所间价差、现货-期货基差)还没被磨平。**谁在另一边亏**:追涨杀跌的散户、不同平台间的定价摩擦。

> ⚠️ **加密在本仓库只作"交叉验证",不作主锚点** —— 它历史短(DSR 难过)、2021-25 的牛市 beta 会让任何多头偏向"看着很赚"(其实是搭了火箭,不是 alpha)。**用市场中性(L/S、资金费 carry)剥掉 beta 才看得清真信号。**

## 方向清单

94. **横截面动量(crypto)** — 一篮子币里买强卖弱,市场中性。**教**:动量在散户市场更强、L/S 剥离 beta。**状态**:本项目实测 L/S Sharpe 0.72,**DSR FAIL**(短样本)—— 有信号但不够稳。
95. **资金费率 carry(funding rate arb)** — 永续资金费持续为正时,做空永续 + 做多现货,收资金费,delta 中性。**教**:永续合约、资金费率机制、最干净的 crypto carry。**谁亏**:付资金费的杠杆多头。**坑**:费率可瞬间转负、平台风险。
96. **现货-期货基差(basis trade)** — 期货溢价(contango)时,做多现货 + 做空期货,锁定基差收敛。**教**:基差、期现套利、年化基差收益。
97. **跨交易所套利(CEX-CEX)** — 同一币在不同交易所的价差。**教**:跨市场套利、为什么价差存在(转账延迟、提现限制)。**门槛**:延迟、库存、提现摩擦。
98. **DEX-CEX 套利 / AMM 套利** — 去中心化交易所(AMM 定价)和中心化交易所的价差。**教**:AMM、恒定乘积做市、滑点。
99. **链上信号** — 用链上数据(交易所流入流出、巨鲸地址、稳定币供给、活跃地址)预测价格。**教**:链上透明性 = 独特数据、on-chain 分析。**数据**:链上(部分免费)。
100. **流动性提供 / LP 收益(DeFi)** — 给 AMM 池提供流动性收手续费,管理**无常损失**。**教**:LP、无常损失(impermanent loss)、收益 vs 风险。**坑**:无常损失常吃掉手续费收益。
101. **质押 / 收益 carry(staking)** — 质押 PoS 代币收质押收益(crypto 版的"无风险"利率)。**教**:质押、PoS、加密原生收益率。
102. **MEV / 清算** — 抢跑、三明治、清算机器人(链上的微观结构套利)。**教**:MEV、链上订单排序、为什么这是 crypto 的 HFT。**门槛**:技术 + 基础设施极高。

## 共同的坑

- **牛市 beta 幻觉**:2021-25 任何沾多头的策略都"看着很赚",那是搭了火箭不是 alpha。**必须看市场中性(L/S、carry)的 Sharpe**,且对 BTC 买入持有做基准。
- **历史短 + 极端波动**:样本少 → DSR 难过;肥尾极重 → 风险管理是生死线。
- **平台 / 智能合约风险**:交易所暴雷(FTX)、合约漏洞、提现冻结 —— 这些"运营风险"是传统市场没有的,且会让"无风险套利"瞬间归零。
- **成本 + 摩擦**:转账延迟、gas 费、提现限制让很多"纸面套利"无法成交。

延伸:[多空·中性·自融资](../concepts/long-short-and-neutral.md) · [Carry(套息)](03-carry.md)(资金费 carry 的母家族) · 实时来源 `quant scout --source github`。

## 相关页面

| 方向 | 页面 |
|---|---|
| 上游 | [catalog 总览](index.md) · [策略风格光谱](../deep/strategy-styles.md) |
| 下游 | [想法库](../ideas/index.md) · [playbook](../playbook.md) |
| 同域 | [策略家族图谱](../reference/strategy-families.md) · [alpha 从哪来](../deep/where-alpha-comes-from.md) |
| ADR / concepts | [交易 101](../concepts/trading-101.md) · [为什么回测会撒谎](../concepts/why-backtests-lie.md) |

## 深入阅读 / 学习 / 拓展

- **站内:** [深入理解](../deep/index.md) · [跑一个实验](../guides/run-an-experiment.md)
- **增长纪律:** 新方向 → 本页加一行 + [`ideas/_template.md`](../ideas/_template.md);探针 `quant scout`
