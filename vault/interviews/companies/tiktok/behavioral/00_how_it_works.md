# HM 面和项目深挖怎么运作（教程）

- TikTok 的行为类问题有两处：**每一场技术面开头的简历拷问**（10–45 分钟），以及 **HM（用人经理）面**（45–90 分钟）。两处问的是同一件事：你做过的项目，你的判断，你的深度。
- HM 面还决定**级别和进哪个组**。它是淘汰轮，不是寒暄。
- 一个常见的组合：项目讲解 → 行为题 → 一道编码 → 剩 30 分钟时一个高层设计（支付系统被问到过不止一次）。要带着「这一小时随时会变」的心理准备。

## 1. 面试官在找什么

| 他们看重的 | 你的回答里应该出现 |
|---|---|
| **ownership**（范围、决策、指标是你的） | 「我」做的动作；团队的部分明确划线；你拍板的那一个决策 |
| **深度** | 为什么选这个架构，指标证明了什么，重来会改什么；被追问到下一层时说得出 |
| **强度与可持续** | 事故值班、紧时间的交付，你怎么处理；不抱怨 |
| **直接和数据** | 暴露问题，用数字下结论，不用「managing up」 |
| **AI 使用** | 具体例子，你怎么验证 AI 写的东西 |

- 级别由 HM 对简历的解读决定：**范围越大的决策越清楚地是你的，级别越高**。
- 高级别的项目深挖会变成**对抗式**：每个架构选择、每个成功指标都被挑战。目的是看你有没有想过替代方案，不是要你认错。

## 2. 时间怎么分

| 阶段 | 时间 | 你要做的 |
|---|---|---|
| 简历拷问（每场技术面开头） | 10–45 分钟 | 每个项目 90 秒内讲完 L1，停，等追问；超过 15 分钟主动说「我们先做题，细节之后再展开可以吗」 |
| 一个行为故事 | 60–90 秒，最长 2 分钟 | 钩子放最前，60 秒内出现「我的决定」，数字说得出口 |
| 项目深挖（HM 面） | 每个项目约 30 分钟 | 用 [[deep_dive]] 的 12 个问题轮着答 |
| 一道编码（HM 面里偶尔有） | 约 20 分钟 | 光板、自己造用例 |
| 高层设计（HM 面里偶尔有） | 剩 30 分钟时开始 | 先估算和幂等 / 对账，UI 和集成细节放最后 |

- 项目讲解先说**为什么这个问题重要**（钱、客户、风险），再说你做了什么。
- 数字放在句子里：22M 笔 Amex 交易、13.7M 行 / >99.9% 一致、约 200 个商户。
- 每个故事结尾带一句 **what I would change**：资深面试官一定会问。

## 3. 追问的形状：三层

| 层 | 问什么 | 你的答案 |
|---|---|---|
| L1 | 发生了什么，你做了什么，你那一份 | 顺序 + 「我」 |
| L2 | 为什么：机制、选型、替代方案 | 一句因果：「因为 X，所以选 Y，代价是 Z」 |
| L3 | 下一层：规模放大 10 倍呢？坏了呢？你怎么知道对？ | 边界 + 怎么测 |

- L3 是对抗式追问的主要形状。答案模板：**说最深已知层 → 说边界 → 说怎么查**，不编。
- 例（Amex 管线）：L1「文件怎么进来？」→ 每天一个定宽文件，`COPY INTO` 进暂存表。L2「怎么不重复？」→ 三层幂等：文件加载历史、`MERGE` 键、错误日志。L3「如果每天是一千倍的数据？」→ 我会先测每个阶段的耗时和每秒行数；单表 `MERGE` 的瓶颈在哪里我没有测过，我会先看查询剖析。

## 4. 项目介绍的骨架（90 秒）

- **背景与规模**：系统做什么、一个数字、为什么重要。
- **我的范围**：我拥有什么，我继承了什么，哪些是队友的。
- **关键决策**：两个选项，我选了哪个，**因为……**，代价是……
- **正确性 / 指标**：怎么知道它是对的（对账、一致率、监控）。
- **失败与改进**：生产里出过什么问题；重来我会改什么。
- 说完停，让面试官选下一层。

## 5. 常见失败

- **自相矛盾**：面试官抓住同一条流程追问，先提出一个方案，下一句又推翻。方案不确定时先说「我有两个选项，各自的代价是……」，再选一个，之后不改口。
- **团队式叙述**：全程说 we。动作用 I，团队的部分显式划线。
- **一堆名词没有机制**：每个名词后跟一个「因为……」。
- **数字没出处**：只用故事里有的数字；不知道就说量级，不编。
- **项目拷问吞掉编码时间**：见第 2 节。
- **夸大**：「快了 N 倍」没有测过就不说。
- **不会装会**：被问到没做过的层，说 「I know it to X; below that I'd measure or read the docs.」
- **没有失败**：面试官要听一次真的出过的事。

## 6. 语言

- 面试默认英文；HM 如果在中国或新加坡，可能先问「你会说中文吗」然后换成普通话，有时不会先问。
- 两种语言都准备：S1、S5 各练一个中文 90 秒口述。技术名词用英文原词（idempotent、`MERGE`、reconciliation），因为团队内部就这么说。
- 【待补：你更舒服的语言，和被切换语言时的第一句话】

## 7. 同一题的 mid 与 senior 版（项目：Amex 结算管线）

**Mid**
> I built a pipeline that loads Amex settlement files into Snowflake, parses them and calculates fees. It processes about 22 million transactions.

- 缺：为什么这样设计、怎么保证对、出过什么问题、重来改什么。

**Senior（约 90 秒）**
> Amex is a closed-loop network: instead of near-real-time settlement views, it sends one fixed-width file a day, so we can't book a transaction until the file confirms it settled. I inherited a stub with one table and owned the pipeline end to end for eighteen months. A scheduled task loads the file into a staging table; six append-only streams, one per record type, each with its own offset, feed six procedures that merge on a composite key; two validation functions run a full outer join against pending transactions and send every mismatch to an error log instead of dropping it; a downstream task with two upstream dependencies calculates the fee in one transaction. Every stage is idempotent — file load history, merge keys, the error log — so at-least-once plus idempotent writes is effectively once. About twenty-two million transactions in half a year. Correctness has three layers: row, batch, and reconciliation against Amex's own summary record, and a mismatch halts the task and pages on-call. The part I'd change: the six parsers repeat one offset table; I'd move offsets into a config table with one generic parser.

- 多了：机制、取舍、三层正确性、边界、改进。

## 自测

**1. 简历拷问拖长了，怎么办？**
<details><summary>答案</summary>超过 15 分钟主动说：「细节我之后可以展开，我们先做题可以吗？」否则编码只剩不到 20 分钟。</details>

**2. 对抗式追问的三层？**
<details><summary>答案</summary>L1 发生了什么；L2 为什么（机制、选型、替代方案）；L3 下一层（放大 10 倍、坏了、怎么知道对），答案是最深已知层 → 边界 → 怎么查。</details>

**3. 追问同一条流程时先提方案、后来自己推翻，为什么致命？**
<details><summary>答案</summary>面试官评的是你对这个流程的掌握是否稳定。有两个选项时，先说各自的代价，再选一个，之后不改口。</details>

**4. 一个项目介绍的骨架？**
<details><summary>答案</summary>背景与规模 → 我的范围 → 关键决策（因为……代价是……）→ 怎么知道对 → 失败与改进。</details>

**5. 22M 笔交易的平均速率是多少？**
<details><summary>答案</summary>半年约 183 天，约 12 万笔 / 天，平均每秒约 1.4 笔。这是低 QPS、高正确性要求的系统，不要把它讲成「高吞吐」。</details>
