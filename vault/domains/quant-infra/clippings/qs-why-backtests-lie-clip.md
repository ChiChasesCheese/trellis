---
title: Why Backtests Lie
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/why-backtests-lie.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 为什么回测会撒谎

**大多数"看起来能赚钱"的策略是数据偏差或自我欺骗造成的幻觉。** 四类最常见的自欺,以及框架用**自动闸门**逐一堵住的机制——每个陷阱配一个本项目真实踩过的例子。

## 陷阱 1:幸存者偏差(Survivorship Bias)

**问题**:你用"今天还存在的公司"名单去回测历史 —— 但破产/退市的公司不在名单里,等于偷偷用了未来信息。

**真实例子**:我们想验证三个经典股票因子(BAB、残差动量、52 周高点)。第一轮用"当前还活着的大盘股"当 universe,全被拒。诊断发现:这些策略的 edge 本该来自**躲开/做空会爆掉的票**(雷曼、硅谷银行…),但这些死票根本不在名单里,所以横截面里"没有真正的输家",结论是假的。

**框架怎么堵**:
- `quant.data.universe.SP500Universe` 提供 **point-in-time(历史时点)成分股** —— 2008 年 9 月那天**实际**在 S&P 500 里的名单(含后来死掉的票)。
- `sp500_close_panel` 按每天实际成分掩码,跌出指数自动清仓(置 NaN),**捕捉退出时的真实亏损**。
- 数据审计的 `survivorship` 标记:如果"没有任何序列中途终止",就警告你 universe 有幸存者偏差。

> 我们重跑这三个因子(去偏差后)依然全 REJECT —— 但这次是**可信的拒绝**,而不是被偏差掩盖。

## 陷阱 2:前瞻偏差 / 偷看未来(Lookahead)

**问题**:策略在 t 时刻做决定时,不小心用到了 t 之后才知道的信息。最隐蔽的形式:用全样本算标准化、用复权数据(复权用了未来的拆股信息)、特征窗口跨过了训练/测试边界。

**为什么致命**:偷看未来的策略在回测里"神准",真实交易里一文不值 —— 因为现实中你拿不到未来。

**框架怎么堵**:
- **截断不变性闸门**(`truncation_invariance_gate`):框架**自己**把数据截断到 t、重算你的信号,跟全样本版对拍。**一旦信号因为"未来 bar 被删掉"而变化,直接判 FAIL。** 这是机制,不靠相信你的代码。**qs-owbg(2026-07-21)修复**:固定截 20 bar 对月频再平衡+ffill 的组合近乎失明——非再平衡日只是原样复制上一次决策,前视只有在"截断边界恰好落在最近一次再平衡的泄漏窗内"才可见,单一边界靠日历相位撞运气(审计复现:5 bar 前视仅 5/21 概率被抓)。修复把 `truncate` 按调用方已声明的 `holding`(再平衡/持有期)扫一整个周期、任一边界抓到即 FAIL——相位无关,21/21 稳定抓到;`holding=1`(默认,日频/未声明)字节级不变。
- **Purged + Embargoed walk-forward**:训练/测试切分时,剔除标签窗口跨界的样本,并在测试段前留禁运间隔(大小 = 策略声明的回看/持有期)。

## 陷阱 3:多重检验 / 参数挖掘(Multiple Testing)

**问题**:试得越多,光靠运气就越容易撞到一个"好看"的结果。

**直觉(抛硬币)**:一个人抛 10 次得 8 个正面挺稀奇;但 1000 个人各抛 10 次,几十个能得 8+ 正面纯靠运气。**参数扫描就是这个** —— 你试 50 组参数,哪怕底层是纯噪音,最好的那组也会有个像样的 Sharpe。只报"最优 Sharpe 1.2"却不说试了 50 次 = 自欺。

**真实例子**:我们做了 50+ 个策略实验,任何"winner"的真实显著性都被这些隐藏的试验稀释了。

**框架怎么堵**:
- **Deflated Sharpe 闸门**(Bailey-López de Prado):框架知道你扫了几组(N),用 N + 样本长度 + 收益的偏度/峰度,算出"真 Sharpe>0 的概率"。**扛不住对 N 次试验的 deflation 就 FAIL。** 我们的 demo 里,xs 动量的 Sharpe 0.54 在 10 次试验下 P(real)=0.59 < 0.95 → 被拒。
- **家族拥挤 warn**:查 ledger,如果同家族已经试过很多次,提示你额外打折。

## 陷阱 4:腐坏数据(Corrupt / Unadjusted Data)

**问题**:免费数据源有坏 tick —— 最常见是**未复权的拆股**,价格突然 ×10 或 ÷10,制造出离谱的"单日收益"。

**真实例子**:我们的 PIT 数据里有一只票单日打印 **+721229%**(7213 倍,未复权反向拆股)。两个 agent 各自不防,这个坏 tick **凭空制造了一个假的 +0.67 Sharpe** —— 只因他们碰巧手动 clip 了才没蒙混过关。

**框架怎么堵**:
- **构建期清洗**(`quant.data.artifacts.clean_panel`):识别 spike-and-reversal(暴涨又暴跌 = 数据 glitch 的指纹)并置 NaN,真实单向跳空(财报)保留。清洗在 artifact 构建期做一次、版本化,不靠每个 agent 自觉。
- **数据质量闸门**(`data_quality_gate`):兜底 —— 任何残留的 >100% 单日波动(基本不可能,真股票一天翻倍都罕见)直接 FAIL。我们 demo 里它一开始拦下一批,**诊断发现腐坏不是未复权拆股**(Yahoo 的 close 本就已拆股复权),而是**对退市股返回的垃圾数据**(把不同东西混在一个代码下,如 TIE 报 $30000、CFC 报 $126)。正解是稳健过滤:整列丢掉"反复 >100%"的垃圾票(`clean_panel` v2 的 `robust_v2`)。

**全库级体检已落地**(`data.health`):`audit_health()` 一次性跑完——跨源对账(同 symbol 双源收益 reconcile,发现复权口径不一致)、schema drift 探测(字段单位/缩放悄悄变)、自动化 lookahead detector(PIT 违规)、`market_data/` + 本地缓存 + fornax dataset 的定期巡检报告。`audit_bars`/`audit_universe` 覆盖单源单表(schema / OHLC / 样本量与最小可检测 Sharpe / 日历缺口 / staleness / outlier / regime 覆盖 / survivorship),FAIL 被 `run_experiment` 挡住。

## 一张表:四个陷阱 → 四道闸门

| 陷阱 | 自欺长这样 | 框架的闸门 |
|---|---|---|
| 幸存者偏差 | 用今天的名单跑历史 | PIT universe + survivorship 标记 |
| 前瞻偷看未来 | 回测神准、实盘崩 | 截断不变性 + purged/embargo |
| 多重检验 | 扫 50 组报最优 | Deflated Sharpe + 拥挤 warn |
| 腐坏数据 | 坏 tick 造假 alpha | 构建期清洗 + 数据质量闸门 |

## 核心心法

> **本框架的目标不是"找到赚钱策略",而是"严格地不骗自己"。**

每个策略都被一个强制关卡 `run_experiment` 挡着,自动跑完这四道闸门。任何一道 blocking 闸门没过 → verdict = REJECT。**一个诚实的"拒绝",比一个自欺的"通过"有价值得多。**

---

**下一步**:动手用闸门 → [跑一个实验](../guides/run-an-experiment.md);查词 → [术语表](../reference/glossary.md)。

## 相关页面

| 方向 | 页面 |
|---|---|
| 上游 | [0 · 研究总览](../quant/index.md) · [playbook](../playbook.md) |
| 下游 | [研究总账](../research-log.md) · [深入理解](../deep/index.md) |
| 同域 | [策略家族图谱](../reference/strategy-families.md) · [想法库](../ideas/index.md) |
| 验证 | [为什么回测会撒谎](why-backtests-lie.md) · [多重检验](multiple-testing.md) |

## 深入阅读 / 学习 / 拓展

- **站内:** [能力速查](../reference/capabilities.md) · [给 AI Agent](../for-agents.md)
- **源码:** 页内模块路径均在 `src/quant/`;先 `rg` 再写文档
- **注:** 前瞻/幸存者/成本陷阱总册
