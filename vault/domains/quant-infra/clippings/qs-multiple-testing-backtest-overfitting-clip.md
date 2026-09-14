---
title: 'Why ''It Worked on the Test Set'' Isn''t Enough: Multiple Testing and Backtest
  Overfitting'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/multiple-testing.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 为什么"测试集效果好"不够:多重检验与回测过拟合

量化研究最根本的自欺不是"单个策略过拟合训练集",而是**"试了很多个,挑了表现最好的那个"**。为什么 train/test split 防不住、学术怎么证明、框架怎么实现、以及**为什么高失败率是设计而非 bug**。

## 1. 核心问题:从一堆里挑最好的 = 挑运气

假设你有 N 个**毫无真实 skill** 的策略(纯随机)。每个的真 Sharpe 是 0,但样本里的 Sharpe 会在 0 附近抖动。你挑出**样本 Sharpe 最高**的那个——它的 Sharpe 不是 0,而是这 N 个噪声里的最大值。

关键数学事实(Bailey & López de Prado):**零 skill 下,期望的最大 Sharpe 随试验数增长**,近似

$$ \mathbb{E}[\max SR_N] \approx \sigma_{SR}\Big[(1-\gamma)\,Z^{-1}\!\big(1-\tfrac1N\big) + \gamma\,Z^{-1}\!\big(1-\tfrac1{N e}\big)\Big] $$

(γ = Euler-Mascheroni,σ_SR ≈ √(1/年数) 是 Sharpe 估计的噪声)。**试得越多,这个"纯运气门槛"越高。** 所以:

> **一个回测 / 样本外 Sharpe,在不知道你试了多少次(N)的情况下,统计上不可解读。**

## 2. 为什么 train/test split 不够

| 它管的 | 它不管的 |
|---|---|
| **单个**策略在没见过的数据上还成立吗(防 in-sample 拟合)| 我挑出来这个,是不是 N 次尝试里最幸运的一次(多重检验)|

致命点:**测试集只在"一生用一次、非自适应"时才干净。** 你拿 44 个策略都去测试集上比一遍、挑测试集 Sharpe 最高的——**你就是在过拟合测试集**,它变成了第二个训练集。

这不是比喻,是被严格证明的:**Dwork et al. (2015), "The reusable holdout," _Science_** 证明,**自适应地反复查询留出集**(看一眼→改→再看,正是研究者真实在做的)会泄漏信息、让留出集失去统计效力。你光看了一眼 scoreboard 上的 44 个,就已经"碰"过它了。

**唯一真正干净的"测试集" = 搜索时还不存在的数据**(forward / 出设计期)。现有数据怎么切都可污染;真正没碰过的未来数据才是金标准——这就是为什么我们对 FX value 反复强调 forward 验证、并专门测了"发表后(≥2013)有没有衰减"。

**这跟前视(lookahead)是两回事,别混:** 多重检验管的是"试了几次、挑了最好那个"——就算每次都严格因果、零泄漏,试得多了照样能刷出假 Sharpe。真正的前视(信号用到了不该看见的未来数据)由另一道机制闸 `truncation_invariance_gate` 独立堵——见
[实验框架 · truncation_invariance_gate](../reference/experiment-framework.md) 与
[为什么回测会撒谎 · 陷阱 2](why-backtests-lie.md)。两道闸都是 `run_experiment` 的强制收口点,缺一不可(qs-owbg,2026-07-21:该闸对月频再平衡组合曾有 76% 的检测盲区,已修复为按 `holding` 扫描整个再平衡周期)。

## 3. 学术支撑(可引用)

**核心("好回测不知道 N 就没意义"):**

- **Bailey, Borwein, López de Prado, Zhu (2014), "Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance," _Notices of the AMS_ 61(5).** —— 证明零 skill 下期望最大 Sharpe 随 √(log N) 增长;推导"最小回测长度";直言大量发表的回测很可能是假阳性。
- **Bailey & López de Prado (2014), "The Deflated Sharpe Ratio," _Journal of Portfolio Management_ 40(5).** —— 把上面做成可计算的 haircut(= 我们的 `deflated_sharpe` 闸门)。
- **Bailey, Borwein, López de Prado, Zhu (2017), "The Probability of Backtest Overfitting," _Journal of Computational Finance_.** —— PBO / CSCV:量化"样本内最优在样本外跑输中位数的概率"。

**测试集重用会失效(直接回答"测试集不够"):**

- **Dwork, Feldman, Hardt, Pitassi, Reingold, Roth (2015), "The reusable holdout: Preserving validity in adaptive data analysis," _Science_ 349.**

**整个因子文献本身被多重检验污染:**

- **Harvey, Liu, Zhu (2016), "...and the Cross-Section of Expected Returns," _RFS_ 29(1).** —— 全行业试了上千因子,"新因子"的 t 门槛应是 ~3.0 而非 2.0。
- **Harvey & Liu (2015), "Backtesting," _JPM_**;**Harvey & Liu (2021), "Lucky Factors," _JFE_.**

**最早的实证打脸(数据窥探):**

- **Sullivan, Timmermann, White (1999), "Data-Snooping, Technical Trading Rule Performance, and the Bootstrap," _Journal of Finance_.** —— 把"试了几千条规则"算进去,技术交易规则的超额收益基本消失。
- **White (2000), "A Reality Check for Data Snooping," _Econometrica_ 68(5)**;**Hansen (2005) SPA test.**

**教科书:** López de Prado (2018), _Advances in Financial Machine Learning_, Wiley(DSR、purged/embargo CV、CSCV/PBO 的系统化)。

## 4. 我们框架怎么实现这套文献

我们不是发明,是**直接实现 López de Prado / Harvey-Liu 这条线**:

| 文献机制 | 我们的实现 |
|---|---|
| Deflated Sharpe(按 N 的期望最大值折扣,**序统计**视角)| `experiment/gates.py::deflated_sharpe_gate` + `experiment/stats.py::expected_max_sharpe`(就是上面的公式;返回的 `GateResult` 类型住在 `quant.core.audit`,qs-5aq)|
| **Harvey-Liu Sharpe 折价(按 N 校正 p 值,**逐检验**视角)** | `experiment/stats.py::haircut_sharpe` —— 把观测 Sharpe 的 t 值转单边 p、Bonferroni 放大 N 倍、再反解"幸存"的 Sharpe。Harvey-Liu 的题眼:折价是**非线性**的 —— 强信号几乎不掉、边缘信号几乎被砍光(`haircut_ratio`∈[0,1]),民间"砍一半"的规则是错的。和 Deflated Sharpe 是同一件事的两个角度(期望最大值 vs 逐检验 p 校正)。|
| Purged + embargo CV | `experiment/splits.py::purged_embargo_split`(防时序泄漏的单条 walk-forward OOS 折)|
| **Combinatorial Purged CV(CPCV,AFML ch.12)** | `experiment/splits.py::combinatorial_purged_split` —— N 组里每选 k 组当测试集(`C(N,k)` 种),各自 purge+embargo;`reconstruct_cpcv_paths` 把每个切分的 OOS 片段拼回 `C(N-1,k-1)` 条**全样本回测路径**,于是 OOS 指标(如 Sharpe)成了一个**分布**(PBO/DSR 想要的就是这个分布,而不是一个脆弱的点估计)。`n_backtest_paths(N,k)` 给路径数。|
| PBO / CSCV(回测过拟合概率)| `experiment/overfitting.py::probability_of_backtest_overfitting`(对整个 sweep 测"IS 最优在 OOS 是否反转")|
| 可见的分母(试了多少)| `experiment/ledger.py::scoreboard`(`quant scoreboard` / 文档站 [研究记分板(自动)](../live/scoreboard.md))—— 把"开了几枪"摊开 |
| **诚实总报告(一站式前门)** | `stats.honesty_report` → `HonestyReport`:一次跑完整套(naive vs Lo 年化 Sharpe / PSR / MinTRL 需多少年 / Harvey-Liu 折价 / `significant` 总判决)。`research/grinold_pipeline_e2e.py` 手动跑的那套,封装成一个调用 |
| 最小业绩记录长度(MinTRL,Bailey-LdP)| `stats.minimum_track_record_length` —— PSR 按样本长度反演:这个 Sharpe 要多少观测才对基准统计显著(含 skew/kurt);和 minBTL 互补(那个是多重检验角度,这个是单策略显著性) |
| Sharpe 年化的序列相关修正(Lo 2002)| `stats.sharpe_annualization_factor` / `lo_annualized_sharpe` —— naive `√q` 年化假设 iid;正自相关的策略真年化 Sharpe **更低**(`η(q)=q/√(q+2Σ(q-k)ρ_k)`),又一处回测高估自己的地方 |
| 反推门槛(三条腿)| `stats.breakeven_sharpe`(过闸门需多少 Sharpe)/ `stats.max_trials`(一个 Sharpe 能扛几次试错)/ `stats.minimum_gate_length`(**本仓闸门**对样本长度的精确反解:这个 Sharpe 在这么多次搜索后需要多长记录才能过闸)|
| ⚠️ minBTL ≠ 本仓闸门要求 | `stats.minimum_backtest_length` 是 Bailey & López de Prado 2014 的经验闭式 `(E[max SR_N]/sr)²`,假定 trial 离散度为 1 且**从不计算 PSR**,因此把本仓 `deflated_sharpe_gate` 的真实要求**低估 2.4×(386 trials)到 17×(1 trial)**。问「这个 Sharpe 算不算过拟合的期望值」用 minBTL;问「我们这道闸会不会认」用 `minimum_gate_length`。后者解的是**不动点**:expected-max benchmark 由 `√(ppy/n_obs)` 构成,加长记录同时降门槛并锐化估计——**加长样本买两次证据** |
| 校准的前提:日历要对 | `probabilistic_sharpe_ratio` 建立在**每根 bar 的** Sharpe 上,所以 `periods_per_year` 必须是调用方 bar 的日历。传错会把 `z` 重缩放 `√(ppy_真/ppy_用)`,闸门不是变松变紧而是**失去校准**:硬编码 252 曾让 1min(ppy≈98280)把真 P=0.56 报成 **0.999**,多重检验 haircut 实质失效(qs-jniu)。**一个只会输出 0 或 1 的闸门没有判别力** |
| **尾部主张也要付账(qs-32gd)** | `gates.tail_gain_gate` —— 降险 overlay 按**尾部**判而非 ΔSharpe(因为 ΔSharpe 0.18 要 **320 年**才能建立,而回撤改善又大又可复现)。它**不是**一道更松的闸:零假设是「同一敞口计划、**没有真实择时**」(循环位移),经验 p 再过一遍 **Bonferroni**。结果:23.7 年上对**一次预注册**假设显著(p 0.018–0.025),而在现有 overlay 家族已花掉的 **6+ 次**搜索下**不显著**(0.108–0.153)。**已经被搜索过的东西不能靠换一条判据重新变成 PASS** —— 加上「必须 `overlay_claim="tail"` 事先声明、不能答错后切换」,两条一起才让它是闸而不是软门 |
| 真正的样本外 | 强调 forward / 出设计期验证(见 [FX value](../ideas/fx-value.md) 的 holdout)|

每个进入 `run_experiment` 的想法都必须把"试了几次"作为 `n_trials` 传进 DSR 闸门——**门槛随搜索规模机械抬高,不靠自觉**。

**Overlay 例外(净增益,非 vs 零):**`stack="overlay"` 且传入裸 `benchmark=` 时,blocking 闸切到
`overlay_net_gain_gate`(ΔSharpe / 记录 ΔMaxDD)。原因:overlay 声称的是「相对未叠加层的净增益」,
不是「相对现金的绝对 edge」——用 DSR-vs-零会让「基准本身就正 Sharpe + 风控抹平曲线」假 PASS。
见 [实验框架 · overlay 净增益闸](../reference/experiment-framework.md) 与 PR #347。**这不等于
overlay 逃过多重检验**:2026-07-21 对抗审计发现该切换曾是完整绕过(`overlay_net_gain_gate`
不接 `n_trials`,`dsr_prob` 写 NaN);qs-ctdi(#471)修复后,`overlay_net_gain_gate` 对
excess-over-benchmark 收益流套用与 `deflated_sharpe_gate` 相同的 n_trials 折扣——ΔSharpe 门槛
和多重检验门槛都要过。同一票也把 `n_trials >= grid_size` 地板从「只在 walk-forward
(`reestimate!='none'`)生效」扩到「只要声明了 `param_grid` 就生效」(冻结路径此前可无限制
声明任意 `n_trials`)。

**`realized_beta_gate` 不是多重检验机制,别混:**2026-07-22(qs-d847)新增到同一
`experiment/gates.py` 的 `realized_beta_gate` 答的是另一个正交问题——横截面多空账本对
EW 市场的因果滚动实现 beta 是否在声明的中性阈值内(v0.4 教训:美元中性 ≠ beta 中性,qs-jms
的负 Sharpe 100% 来自未对冲的空头 beta)。它**不消耗、不折扣 `n_trials`**,WARN 也**不**
计入 blocking 判决(与本页上面讲的 DSR/PBO/CPCV 是两条独立的闸)。细节见
[实验框架 · realized_beta_gate](../reference/experiment-framework.md)。

**`borrow_availability_gate` 同样不是多重检验机制:**2026-08-16(qs-e0dc)加进同一
`experiment/gates.py` 的这道闸答的是**可执行性**,不是多重性——空头腿在每根 bar 上真的
借得到券吗。`MarketStructure` 早就能答「这个市场可不可以做空」,其 `short_requires_borrow`
甚至点明了机制(要从别人那里借入标的),但没有任何东西验证借入存在,于是 book 可以在
根本填不上的腿上被打分。它**不消耗、不折扣 `n_trials`**;它 blocking,但判据是覆盖率而非
显著性。触发它的实测:外部 A 股多空模型 **52.5% 的空头持仓在持有当月不在融券标的名单内**,
仅修正可得性就把 Sharpe 2.04 压到 1.12。细节见
[实验框架 · borrow_availability_gate](../reference/experiment-framework.md)。

**为什么两者要分清:** 一个策略可以完全过多重检验(信号是真的、n_trials 付足了)却依然
**不可交易**。上一节量化的是「记账值多少 Sharpe」,这道闸量化的是「这条腿有多少能真的成交」
——两个数都要报,任何一个单独看都会给出错的部署结论。

### N 跨轮累计:已落地(2026-07-04),原理与用法

跨多轮研究同一个方向时,如果每轮只被"本轮试验数"折扣,历史试验就被遗忘,闸门系统性偏松——像重考 10 次只报最好那次还声称"一考即过"。现在 **N 默认跨轮累计**,机制:

1. **`run_experiment` 默认回读 ledger**:`effective_n = 本次 n_trials + ledger.family_history()` 里该 family 的历史累计(排除自身 exp_id,重跑不自我膨胀);`use_ledger_trials=False` 退回局部计数(学术对照用)。
2. **存储语义**:每行记 `n_trials_effective`(写入时的全量计费),历史累计取该列 **max**(而非 sum)——对重跑、对共享同一预注册预算的 sweep 网格都幂等;老账本(无该列)回退为 sum(局部 `n_trials`)。`sweep()` 开跑前取一次 prior,每格点统一计 `grid + prior`。
3. **`trials_sr_std` 用实测分布**:该方向历史 ≥3 次后,`deflated_sharpe_gate` 用**实测 Sharpe 标准差与解析零假设的较大者**(`max(realized, sqrt(ppy/n_obs))`)——DSR 原论文的 trial-dispersion 口径;实测离散度只能提高门槛、不能低于解析零假设;gate detail 的 `trials_sr_std_source` 标注用了哪个。
4. **可见性**:`scoreboard`(CLI `quant scoreboard` / web 控制台记分板页,legacy Streamlit 同名 tab)新增 `cum_trials` + `dsr_prob` 列——每个方向的累计 N 与最佳 run 的 P(real) 一眼可见。

**留待进阶(ONC)**:150 个格点里很多参数组合收益高度相关,字面 N=150 会过度惩罚;López de Prado 建议对试验收益的相关矩阵聚类估**有效独立 N**。当前实现取保守侧(宁可多罚)。Harvey & Liu 甚至主张把文献中他人试过的因子也计入基线(其 t 值门槛 ≈3.0 即由此来);"自己试过的全算上"是本仓库已实现的底线。

### 计价的基准:选择 vs 合成(qs-ijga,2026-08-16)

上面那条 ONC 讲的是「相关的试验能不能少罚」。**这里讲的是另一件正交的事:有些东西根本
不该被计成试验。**

DSR 折扣的数学对象是 `max over N trials` —— 惩罚存在的理由是**从 N 个结果里挑了最好的
那一个**。所以 N 是「比较了多少个**结果**」,不是「喂进去多少个**输入**」。同一批 154 个
因子有两种 campaign,代价截然不同:

| | 有没有 `max` 操作 | 诚实价码 |
| --- | --- | --- |
| **选择**:154 个因子逐个测,报最好的 | 有,在 154 个结果上 | `battery.charge_batch(154)` = 154 |
| **合成**:154 个因子作为**特征**进同一个模型,跑一次,报这一个结果 | **没有** | 合成器自己的**超参网格** |

仓内此前只能表达第一种(`run_batch(candidates: list[Candidate])` 的 API 形状即假定了选择),
于是所有大规模因子工作都被迫按选择计价。后果有账可查:`tabat_cn` 家族 39 行**全部 REJECT
且全部死在 `gate_deflated_sharpe`**,`n_trials_effective` 随家族历史从 154 累积到 **2310**
—— 同一个因子仅仅因为跑得晚就更难过闸,而因子质量没变。

**这值多少?** 反解本仓闸门(`dsr_prob >= 0.95`)得到「过闸所需的最低年化 Sharpe」
(`research/charge_sweep.py --analytic`;高斯 + 解析零假设):

| charge | n=2500(~10y 日频) | n=1500(~6y 日频) |
| ---: | ---: | ---: |
| **1**(合成,无可调参) | **0.688** | **0.888** |
| 20 | 1.126 | 1.455 |
| **154**(ta 池现状) | **1.374** | **1.775** |
| **2310**(累积后) | **1.630** | **2.106** |

即 **0.69–1.22 个 Sharpe**。解析近似已对账:n=1500 / charge=154 算出 `dsr_prob` 0.0761,
ledger 实测 0.0766。**这也解释了我们自己的历史**:唯一 confirmed 的 zz1000 微盘 sleeve
超额 Sharpe 1.39,恰好擦过 charge=154 的门槛 1.374 —— 是这个门槛在筛。

落地在 `experiment/battery.py`:`charge_synthesis` / `SynthesisSpec` / `resolve_charge` /
`synthesis_provenance`。**没有碰 DSR 数学,也没动 `_dsr_prob_detail` 的 never-loosen guard**
—— 即便打开相关性折扣(ONC 那条路),154 次选择依然该付 154,两者不冲突。

合成是**最容易作弊**的地方,所以三道栅栏缺一不可(均有测试钉住):

1. **价码由超参网格派生**,没有 trials 旋钮(对齐 qs-ctdi 的反洗单契约);
2. **产出多于一个结果的 campaign 一律拒绝** —— 比较候选就是选择,无论每个候选吃进多少特征;
3. **特征集必须预先声明 sha** —— 看过单因子回测再挑因子并没有消除那 154 次选择,
   只是把它搬进了特征选择,那种情况仍按 `charge_batch` 或叠 `external_search` 计。

**反面教材**(2026-08 复核外部项目 `A-Share-Neural-Alpha-Long-Short`):报 `n_trials=1`,
而其训练轮数由 20 个候选、**看着完整回测期业绩**人工挑定(`epoch_selection_lineage_mode
= same_period_retrospective_epoch_search`)。我们复跑该网格,净 Sharpe 跨度 **−0.38 → +0.75**。
**条件 2 是所有人都在偷的那一项。**

**但记账修正不造 alpha。** 同一批 ta 池聚合后过闸(等权、PIT 定向、grid=1)得 Sharpe
**−0.310**,charge 从 146 降到 1 连符号都不改。判据在跑之前就写进脚本 docstring:
「若 charge=1 仍不过闸,那就是因子的问题」。详见 `research/dsr_charge_basis.md`。

## 5. 为什么高失败率是设计的一部分(不是方向错)

这是关键的心态校正:**如果门槛正确地把 N 算进去了,那么大多数东西_必然_失败。**

我们的 `quant scoreboard` 实测:**90 次运行、44 个 family → 只有 1 个过全闸门(2%)**,42 个全死于 `deflated_sharpe`。顶部 quality_roe(0.79)、bab(0.65)看着不错的,都被多重检验折扣掉。

- **2% 的通过率不是"我们很差",是"闸门在工作"。** 真正该恐慌的是**高通过率**——那意味着门槛太松、你在自欺。
- 真实世界的 base rate 就是这样:Harvey-Liu-Zhu 统计的上千个已发表因子,扣掉多重检验后**大半站不住**。我们一个免费数据的小框架捞到 1 个 borderline 真 lead,**完全符合甚至好于**这个 base rate。
- **找到能赚钱的策略本来就该极其罕见。** 如果它不罕见,要么市场不有效(它不是),要么你在骗自己(大多数人是)。

**所以:方向正确,高失败率不可避免——而且高失败率正是诚实的标志。** 我们框架最值钱的不是任何单一策略,是**它机械地保证你不会把那 42 个噪声当成发现**。

### 一个 DSR 抓不到的表兄:实验从没评分过自己的主题(qs-qqk)

多重检验管的是「你试了太多次,最好那次是运气」。还有一种更朴素的自欺,DSR 完全看不见:
**实验根本没测过它声称在测的东西。** `purged_embargo_split` 的测试折按设计只铺序列后半段,
所以 2004→2026 的面板 OOS 实为 2015→2026 —— 一个自称「2008 危机 alpha」的研究可以跑到底、
拿到漂亮的 DSR,而 2008 从头到尾在训练半区。压力表里那行 `n/a` 看起来和「数据里没这段」
一模一样。

`scoring_coverage_gate`(`quant.experiment.gates`)把它变成硬闸:危机/顶部类研究用
`run_experiment(..., target_events=[...])` **声明**目标事件,落在训练半区就 FAIL。
`oos_start` / `oos_end` 无条件入 ledger,报告再也没法拿面板跨度冒充评分跨度。
详见[验证方法论 §6.1](../reference/validation-methodology.md#61-qs-qqk)。

> 延伸:[验证方法论](../reference/validation-methodology.md) · [为什么回测会撒谎](why-backtests-lie.md) · [G10 FX value 的六向验证](../ideas/fx-value.md)。

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
- **注:** DSR/PBO 心智
