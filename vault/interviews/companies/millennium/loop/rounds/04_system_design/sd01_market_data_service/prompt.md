# Market / Price Data Service（多经理对冲基金的行情数据服务）

我们是一家 multi-manager 对冲基金，几十个独立的 trading pod 各自跑自己的策略，还有一个中央的 risk 团队要把所有 pod 的仓位汇总起来算整体风险。所有这些团队都依赖同一份行情数据：每天收盘后有几个数据供应商（vendor）扔一批 end-of-day 的价格文件过来，盘中还有另外几个供应商推 streaming 的实时报价。现在这套东西还是每个 pod 各自写脚本去接不同供应商的数据，我们想把它收拢成一个统一的 price data service。

需求大概是这样：

1. **采集**：EOD 价格是文件形式（供应商每天收盘后落一批文件），盘中价格是流式的；供应商不止一家，同一个 symbol 可能被多家供应商同时报价。
2. **存储要支持"point-in-time"**：pod 和 risk 系统经常需要问"这个 symbol 在过去某个时间点的价格是多少"，这个查询**绝对不能看到未来的数据**——risk 团队拿这个做历史回溯和归因，如果 as-of 查询意外读到了"事后才收到的修正值"，算出来的风险归因就是错的。同时，供应商经常会**迟到地推送修正**（比如收盘价发出去之后又发现算错了，第二天改一个价格重新发一次），这些修正不能覆盖历史，原始值和修正值都要能查到。
3. **对外服务**：几百个 trading pod 要能查"这个 symbol 现在最新价格是多少"，也要能查 as-of 历史价格；中央 risk 系统要能对某个历史时刻做一致的价格快照查询。
4. **衍生数据**：从原始 tick/价格流上要能算出 OHLC 和 VWAP 这类聚合 bar。
5. **多币种**：不同 symbol 计价货币不同，最终要统一换算成基准货币（base currency），这个换算本身要跟价格的时间点对齐，不能用"当前"汇率去换算"历史"价格。
6. **推送**：价格更新要能主动推给订阅的下游（pod、risk 系统），而不是让所有人自己轮询。

请设计这个系统。

---

**面试环境说明**：Millennium 的 System Design 题在候选人报告里集中出现在**后期轮次**——onsite/final 阶段是 3–4 小时 back-to-back、约 5 位面试官（coding、SD、项目深挖、behavioral 各一场，每场约 45 min），或者像一手案例那样是"5 轮技术电面"里的一轮（R5，45–60 min，时长口径两种都有报告）。白板工具未证实——LEaD 目前确认的是 R1 用 Webex + HackerRank，但 HackerRank 面向 live coding，SD 轮是否复用同一工具、还是口头 + 共享白板，没有一手报告点名；按"口头描述 + 简单手绘框图"准备即可。面试官风格：官方明确"talk through code live"和"how to know what's true in an unfamiliar system"这类考点，一手报告里也有"面试官几乎不给反馈"的案例——预期是自己主动推进设计、主动提出规模假设，不能指望被追问式引导。

**题目原始报告与来源**（置信度综合见下；company-wide catalog `catalog/CATALOG.md` `sd01` 行）：

- **"price data design problem"** —— LeetCode Discuss 7423863（2025-12-19，Quant Developer – Python，5 轮技术流程的 R5，重开的技术轮）：一手报告只给出题名，没有还原具体接口和约束，本文件的接口、数据模型和 failure mode 是围绕题名做的合理展开，标 **(reconstructed)**。**置信度：高**（一手、可读全文，但内容单薄）。
- TechPrep 2026 Millennium 指南列出的 SD 题型池——"research data pipelines"、"real-time risk monitors"、"signal evaluation systems"——这三个题型都指向"给交易/风控系统喂数据"这一类设计，和"price data design problem"同源，互相印证这是一个题族而非孤例。**置信度：低-中**（聚合站转述，不可读全文）。
- QuantVault 的 Millennium OA 题库捕获里出现过 **"multi-currency PnL"** 的设计/编码题面——印证多币种换算是这家公司反复考的角度，本题把它并入 SD 版本的"多币种"需求。**置信度：中**。
- **mlp.com 官方技术页**提到 Millennium 每天处理 **900K+ 份数据文件**——这是本题"EOD 文件 + 多供应商"这个设定的规模量级出处，用来支撑面试时的规模估算（吞吐、并发供应商数量）。**置信度：高（官方）**。
- 本题没有独立于 `pc09`（Table A 编码题 "Price data store"：写入/最新价/as-of/区间聚合/多币种换算）的一手 SD 版接口描述——两者是同一题族在不同轮次的两种形态：pc09 考"单机/单进程能不能把这套逻辑写对"，本题（sd01）考"这套逻辑要撑住几百个 pod + 多供应商 + 推送，该怎么拆分成一个分布式系统"。

除以上四条明确来源外，题目里的具体接口签名、数据模型细节、failure mode 展开均为 **(reconstructed)**，按题族的常见考法与 Millennium 自身业务形态（多 pod、多供应商、多币种）合理推演。
