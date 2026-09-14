---
title: Parameters, Hyperparameter Optimization, and the Edge of Overfitting
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/parameters-and-hyperopt.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 参数、超参优化,与过拟合的边界

几乎所有 retail 框架都鼓励、而本仓库**刻意不做到底**的事:把参数扫到峰值。拿 freqtrade 的 `hyperopt` 当靶子(设计精良的参数优化机 = 最标准的过拟合机器),理解它为何危险,才理解本仓库的纪律:**单因子不扫到峰值,把试过次数诚实记进 `n_trials`,让 [Deflated Sharpe](../reference/metrics.md) 折掉运气,宁可诚实 REJECT。** 配合 [多重检验](../concepts/multiple-testing.md) · [验证方法论](../reference/validation-methodology.md)。

---

## 1. 什么是超参(hyperparameter)

一个策略里有两类数。一类是**数据决定的**(比如回归出来的因子载荷);另一类是**你拍脑袋定的**——这类就是**超参**:

- 动量的**回看窗口** lookback(20 日?60 日?252 日?);
- 反转的 Bollinger **带宽** $k$(2 倍标准差?2.5 倍?);
- 横截面的 **top-k**(做多前 10% 还是前 20%);
- 进出场**阈值**(RSI < 30 才买?< 25?);
- 再平衡频率、止损位、持有期……

把每个超参的可取范围摆在一起,就张成一个**参数空间(parameter space)**。3 个参数、每个 10 个取值,空间就有 $10^3=1000$ 个点。**超参优化(hyperparameter optimization)就是在这个空间里搜一个让某个目标最大的点。** 听起来天经地义——可正是这一步,埋着量化里最贵的陷阱。

---

## 2. freqtrade 的 hyperopt 怎么做(客观介绍)

[freqtrade](https://www.freqtrade.io/en/stable/hyperopt/) 是流行的开源加密交易框架,它的 `hyperopt` 子命令是教科书式的超参优化实现。三个部件:

### 2.1 参数空间:声明式的可优化参数

策略里把超参声明成特殊对象,框架就知道哪些数该搜、搜什么范围:

```python
from freqtrade.strategy import (
    IntParameter, DecimalParameter, CategoricalParameter, BooleanParameter,
)

class MyStrategy(IStrategy):
    buy_rsi     = IntParameter(20, 40, default=30, space="buy")          # 整数 20..40
    buy_adx     = DecimalParameter(20, 40, decimals=1, default=30.1, space="buy")  # 1 位小数
    buy_trigger = CategoricalParameter(["bb_lower", "macd_cross"], default="bb_lower", space="buy")
    buy_enabled = BooleanParameter(default=True, space="buy")            # = Categorical([True, False])
```

- **`IntParameter` / `DecimalParameter` / `RealParameter`**:整数 / 限定小数位的浮点 / 无限精度浮点(`Real` 张成近乎无穷的空间,几乎不用)。
- **`CategoricalParameter` / `BooleanParameter`**:离散选项 / 真假开关。
- 运行时用 `.value` 取当前被搜到的值(`if dataframe['rsi'] < self.buy_rsi.value`);用 `.range` 在 `populate_indicators` 里一次性预算所有候选窗口的指标。
- 参数按 `space=` 归到 **buy / sell / roi / stoploss / trailing / protection** 几个空间,可以只搜其中几个(`--spaces roi stoploss`)。

### 2.2 loss 函数:你要最大化什么

hyperopt 不会自己知道"好"长什么样,你得选一个**目标(loss,越小越好,框架内部取负)**:

| loss 函数 | 优化目标 |
|---|---|
| `SharpeHyperOptLoss` / `...Daily` | 交易级 / 日级 Sharpe |
| `SortinoHyperOptLoss` / `...Daily` | Sortino(只罚下行波动) |
| `CalmarHyperOptLoss` | Calmar(收益 / 最大回撤) |
| `MaxDrawDownHyperOptLoss` | 最小化回撤 |
| `OnlyProfitHyperOptLoss` | 只看总利润 |
| `MultiMetricHyperOptLoss` | 利润 + 回撤 + 盈利因子 + 频率的混合 |

### 2.3 epochs + 贝叶斯优化器

```bash
freqtrade hyperopt --strategy MyStrategy --spaces buy sell \
  --hyperopt-loss SharpeHyperOptLoss -e 500
```

`-e 500` 跑 500 个 **epoch**:每个 epoch = 选一组参数、整段回测、算 loss。开头若干轮(约 30)是**随机撒点**热身,之后切到**贝叶斯优化**(基于 Optuna / scikit-optimize 的代理模型),用已经评估过的点拟合一个"参数→loss"的响应曲面,**专挑曲面上最有希望的区域继续试**——这比网格暴扫高效得多,几百个 epoch 就能逼近峰值。

**这套东西本身是好工程。** 它把"手动调参"自动化、可复现(`--random-state`)、还高效。问题不在工具,在**用它的人把那个峰值当成了真实的 edge**。

---

## 3. 为什么 hyperopt 是"过拟合机器"

把上面那句话拆开:**hyperopt 的全部本事,就是在参数空间里找一个让回测目标最大的点。** 而回测目标(比如 Sharpe)= **真实 edge + 这一段历史的运气噪音**。优化器没法区分两者,它**两个一起最大化**——于是它系统性地挑出那个"运气噪音恰好最大"的点。

### 抛硬币直觉

一个人抛 10 次得 8 个正面挺稀奇;但**让 1000 个人各抛 10 次,几十个能得 8+ 正面纯靠运气**。参数扫描就是这第二种场景:你试 500 组参数,**哪怕底层是纯噪音**,这 500 个回测 Sharpe 里"最好的那个"也会有个像样的数。只报"最优 Sharpe 1.4"却不说试了 500 次 = 自欺。这就是 **in-sample 峰值在样本外崩**的机理:你挑的是噪音的尖峰,样本一换,尖峰塌掉。

### 数学:试得越多,显著性门槛越高

这不是定性吐槽,是可以**算出来**的。设单次试验的 Sharpe 估计在零假设下(真 edge=0)有标准差 $\sqrt{\operatorname{Var}(SR)}$。试 $N$ 次,取最大,那个**期望最大 Sharpe** 是(Bailey–López de Prado):

$$
SR^*_N=\sqrt{\operatorname{Var}(SR)}\;\Big[(1-\gamma)\,\Phi^{-1}\!\big(1-\tfrac1N\big)+\gamma\,\Phi^{-1}\!\big(1-\tfrac1{Ne}\big)\Big]
$$

$\gamma\approx0.5772$ 是 Euler 常数,$\Phi^{-1}$ 是正态分位数。**$SR^*_N$ 随 $N$ 单调上升**——你试的次数越多,"纯靠运气就能达到的 Sharpe"越高,于是**判定你是真 edge 所需的门槛也越高**。本仓库把它实现在 `quant/experiment/stats.py::expected_max_sharpe`。

真正的显著性指标是 **Deflated Sharpe Ratio(DSR)**:把上面的 $SR^*_N$ 当基准,代进 Probabilistic Sharpe:

$$
\mathrm{DSR}=\Phi\!\left(\frac{(\widehat{SR}-SR^*_N)\sqrt{N_{\text{obs}}-1}}{\sqrt{1-\gamma_3\widehat{SR}+\frac{\gamma_4-1}{4}\widehat{SR}^2}}\right)
$$

$N_{\text{obs}}$ 是样本期数,$\gamma_3,\gamma_4$ 是收益的偏度/峰度(肥尾会进一步压低可信度)。直觉:**$\widehat{SR}$ 必须显著地超过"试 $N$ 次本就能撞到的水平",才算真。** freqtrade 的输出里没有这一项——它只给你那个未折扣的峰值。

---

## 4. 我们的立场:不扫到峰值,而是诚实记账

理解了第 3 节,我们的纪律就顺理成章。**我们不反对超参,我们反对的是"扫到峰值、只报峰值、假装没扫过"。** 具体四条:

1. **单因子不把参数扫到峰值。** 一个因子(动量、反转、BAB)我们用**一个有经济学理由的默认参数**(比如动量 12-1、Bollinger $k=2$),而不是开 500 epoch 去逼一个让 Sharpe 最大的 lookback。理由就是第 3 节:那个峰值的一大半是运气,样本外必缩水。

2. **`n_trials` 诚实反映"到底试了几次"。** 这是整套纪律的良心所在。`deflated_sharpe_gate(returns, n_trials)` 里的 `n_trials` **不是装饰**——它是 $SR^*_N$ 公式里的 $N$。你扫了 10 组就填 10,扫了 500 组就填 500。**填得越大,门槛 $SR^*_N$ 越高,过线越难。** 这把"多重检验"从一个容易被忽略的良心问题,变成了一个**机制问题**:harness 把真实搜索规模当 `n_trials` 传进去,你想偷偷扫一遍再假装只试了一次,数学不允许。

3. **Deflated Sharpe 自动折扣。** `deflated_sharpe_gate`(`quant/experiment/gates.py`)默认要求 $P(\text{real}\mid N\text{ trials})\ge 0.95$,否则判 **FAIL**。它不看你嘴上说的,看 DSR 算出来的概率。

4. **宁可诚实 REJECT。** 本仓库做了 ~10 个诚实实验,**几乎全部 REJECT**,正是因为 DSR 把"试了几次"算了进去。Demo 里横截面动量毛 Sharpe **0.54**,在 **10 次试验**下 $P(\text{real})=0.59 < 0.95$ → 被拒。注意:**它不是因为 Sharpe 太低被拒,是因为"0.54 撑不住对 10 次试验的 deflation"被拒。** 换 freqtrade 那套,你只会看到"最优 Sharpe 0.54",然后上线亏钱。

### 实证:我们没有为了过线而调参

这一点在仓库历史里有据可查,不是口号:

- **加宽 universe**(经典股票因子第一轮用"今天还活着的大盘股",全被拒)→ 我们的修法是换成 [point-in-time 成分股](../concepts/why-backtests-lie.md)(含退市死票),**重跑后依然全 REJECT**。我们没有去搜一个能让它过线的参数组合,而是接受"去偏差后的可信拒绝"。
- **fan-out 多个因子/标的**:每多试一个,就多记一次 `n_trials` / 触发 `crowding_warn`,**门槛随之抬高**——我们让多重检验**惩罚自己**,而不是从 fan-out 里挑个最好的当 headline(那是事后赢家偏差,验证方法论第 8 条硬性禁止)。

> 一句话对照:**freqtrade 问"哪组参数让回测最好看";我们问"在我试过这么多次之后,这个结果还有多少是真的"。** 前者最大化样本内峰值,后者最大化"不骗自己"。

---

## 5. 怎么"对"地用超参(如果非搜不可)

超参优化不是原罪,**前提是你把搜索的代价如实计入显著性**。要搜,就守这五条:

1. **样本外是神圣的(purged + embargo)。** 所有调参只在 in-sample 做;留一段**从没碰过**的 OOS 做最终检验。用 `purged_embargo_split`:剔除标签窗口跨界的样本,测试段前留禁运间隔(= 策略声明的 $\max(\text{lookback},\text{holding})$),防边界泄漏。见[验证方法论](../reference/validation-methodology.md)第 2 节。

2. **参数稳定性:邻近参数 Sharpe 不能腰斩。** 试 ≥3 组邻近参数,最优 vs 邻近偏离 ≤ 30%。**lookback 从 20 改到 25 就 Sharpe 减半 = 你挑了个运气尖峰,样本外必崩。** 真 edge 应该是参数曲面上的一片**高原**,不是一根针。

3. **嵌套交叉验证(nested CV)。** 内层 CV 调参、外层 CV 评估,**评估层永远不参与选参**——否则你又把"挑最优"的运气漏进了业绩里。

4. **把搜索次数计进 DSR。** 这是和 freqtrade 最本质的区别:无论你跑了 500 epoch 还是手调了 8 次,**那个数字必须进 `n_trials`**。贝叶斯优化"高效逼近峰值"反而更危险——它专挑噪音尖峰,等价试验数往往比名义 epoch 还高。

5. **regime 分解 + 2× 成本存活。** 别只看全样本一个数:分 2008 / 2020 / 2022 看,2× 成本下重跑仍要存活。一个靠在某段历史调出来的峰值,通常一换 regime 或一翻倍成本就归零。

---

## 6. 对照表:freqtrade hyperopt vs 我们的纪律

| 维度 | freqtrade hyperopt | 本仓库的纪律 |
|---|---|---|
| **核心动作** | 在参数空间搜让 loss 最大的点 | 用有理由的默认参数,不扫到峰值 |
| **目标函数** | `SharpeHyperOptLoss` 等(未折扣) | Deflated Sharpe(对 $N$ 次试验折扣后) |
| **优化器** | 贝叶斯(Optuna/skopt)高效逼近峰值 | 不优化到峰值;搜了就把次数计进 `n_trials` |
| **试验次数怎么处理** | 跑几百 epoch,只报最优那一个 | `n_trials` = 真实搜索规模,$N$↑ → 门槛 $SR^*_N$↑ |
| **样本外** | 靠用户自觉留 timerange | `run_experiment` 强制 purged/embargo OOS |
| **多重检验** | 不显式建模 | `deflated_sharpe_gate` + `crowding_warn` 机制化 |
| **典型结局** | 漂亮的样本内峰值,样本外缩水 | 大多诚实 REJECT,但拒绝是可信的 |
| **哲学** | "哪组参数让回测最好看" | "试了这么多次后,这个结果还有多少是真的" |

---

> **核心心法(重申):本框架的目标不是"找到赚钱策略",而是"严格地不骗自己"。** hyperopt 是一台把"自欺"自动化、规模化的精密机器——快、可复现、还好看。我们刻意不把它用到底,因为我们要的不是样本内最高那根针,而是**扣掉运气之后还站得住的高原**。一个诚实的 REJECT,比一个扫出来的"通过"值钱得多。

---

**延伸**:[为什么回测会撒谎 · 陷阱 3 多重检验](../concepts/why-backtests-lie.md) · [验证方法论 · 第 5/7 条](../reference/validation-methodology.md) · [指标 · Deflated Sharpe](../reference/metrics.md) · 代码 `quant/experiment/gates.py`、`quant/experiment/stats.py`。

## 相关页面

| 方向 | 页面 |
|---|---|
| 上游 | [信号工程](signal-engineering.md) · [成本与价格](costs-and-prices.md) |
| 下游 | [跑一个实验](../guides/run-an-experiment.md) · [验证方法论](../reference/validation-methodology.md) |
| 同域 | [多重检验](../concepts/multiple-testing.md) · [为什么回测会撒谎](../concepts/why-backtests-lie.md) |
| ADR / concepts | [实验框架](../reference/experiment-framework.md) |

## 深入阅读 / 学习 / 拓展

- **站内:** [因子风险](factor-risk-and-idiosyncratic-alpha.md) · [高维因子择时](high-dim-factor-timing.md)
- **源码:** [`experiment/gates.py`](https://github.com/ChiChasesCheese/Quant-Stroller/blob/main/src/quant/experiment/gates.py) · Bailey & López de Prado DSR/PBO
