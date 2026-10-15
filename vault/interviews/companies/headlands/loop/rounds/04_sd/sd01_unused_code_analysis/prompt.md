# sd01 · 无用代码分析（Unused-code / Dead-code Analysis）

> 轮次：系统设计 / 开放式（FastPrep 标 System design，无阶段标签；Glassdoor 称是**首轮视频面**里的口述题）· 置信度：**中**（2 个独立来源，均无逐字题面）
> 来源：FastPrep「Design Distributed Unused-Code Analysis」（lastSeen 2023-06-28，`catalog/raw/github_repos.md` §3.1.D）·
> Glassdoor RVW98042384（`catalog/raw/forums.md` G3，日期未显示）：
> 「The first round of the interview was conducted via video call. … how I would identify and remove unused code from a company's codebase.」/ Question 1：「removing unused or dead code in a large company's codebase」，评论称该题**偏窄、HFT 公司很少删代码**。
> CATALOG Table C `sd01`，FO Q7（`forums.md` §2）。

## 题面

**逐字能确定的两句**（英文原文）：

1. 「how I would identify and remove unused code from a company's codebase」（Glassdoor，口述）
2. 「Analyze a fixed company-wide code snapshot and produce explainable unused-code candidates…」（FastPrep 摘要，被截断）

**本 kit 补全的版本 (reconstructed)**：

> 公司有一个大型代码仓库（多个语言，以 Java 为主）。设计一个系统，对**某一时刻的固定代码快照**做分析，产出「可能没用的代码」的**候选清单**，并让每个候选**可解释**（为什么认为它没用，证据是什么）。然后说明怎么把候选变成**安全的删除**。需要在一个公司规模的仓库上跑得完，并能随代码变化持续运行。

「固定快照」这个词很关键（**推断**）：它把题目限定为**批处理分析**（离线、确定性、可复现），而不是在线服务。「可解释的候选」意味着输出不是一个布尔值，而是**带证据的判断 + 置信度**；「候选」意味着系统不负责自动删除，**人审 + 安全流程**在回路里。

## 面试官大概会这样推进 (reconstructed)

| 阶段 | 面试官说 / 问 | 你要做的 |
|---|---|---|
| 开场 | 「怎么找出并删掉大代码库里没用的代码？」 | 先别画图：问「没用」的定义、语言、有没有构建系统、删错的代价 |
| 5 分钟 | 「静态分析能做到什么，做不到什么？」 | 引出：可达性（reachability）、反射 / 依赖注入 / 序列化 / 公共 API、动态证据 |
| 15 分钟 | 「公司有一亿行代码，怎么跑？」 | 估算：索引阶段可以并行到数百核；图本身一台机器放得下 |
| 25 分钟 | 「怎么证明某个候选真的可以删？误报怎么办？」 | 置信度分层、证据、生产运行数据、软删除、回测 |
| 35 分钟 | 「谁来删？怎么说服代码主人？」 | PR 机器人、按 owner 拆分、指标、文化（交易公司的 Chesterton's fence） |
| 45 分钟 | 「增量运行？多语言？」 | 增量索引、构建缓存、跨语言边 |

## 开场必问的澄清问题（及你可以采用的假设）

| 问题 | 为什么问 | 若没答案，假设 |
|---|---|---|
| 「没用」指什么？静态不可达？生产里从未执行？还是两者？ | 静态和动态的结论不同，成本和风险也不同 | 两者都做，**分层**报告：静态不可达为主，动态证据加权 |
| 什么语言？构建系统？ | 决定分析在源码还是字节码上做 | Java 为主（Maven/Gradle 或 Bazel），少量 C++ / Python / 脚本 |
| 规模？ | 决定要不要分布式 | 2×10⁷ 行（假设），并说明方案对 10⁸ 行同样成立 |
| 删除是自动的还是人审？ | 决定对误报的容忍度 | 只产候选，人审后删除 |
| 误报（删了还在用的代码）和漏报（留着死代码）哪个更贵？ | 决定阈值 | 误报贵得多：宁可漏报（尤其是交易系统里的熔断 / 灾备路径） |
| 有没有生产运行数据（类加载日志、JFR、覆盖率）？ | 动态证据来源 | 能拿到类加载日志，方法级需要 agent |
| 有没有对外发布的库 / 公共 API？ | 公共符号的消费者可能在快照之外 | 有少量；标为「开放世界」，需额外检查 |
| 产出给谁、什么形式？ | 可解释性的读者 | 代码 owner（CODEOWNERS）；PR + 报告页面 |

## 约束与不变量（写在白板上）

* **不变量 1**：报告为「无用」的符号，必须附一条**见证（witness）**：要么是「从所有根出发都到不了它」的证明摘要，要么是「它的所有引用者本身都不可达」。
* **不变量 2**：分析覆盖不完整时（缺模块、构建失败、索引失败）**不报告**依赖于缺失部分的结论（fail closed）。
* **不变量 3**：同一快照、同一版本的分析器，输出逐字节相同（确定性），方便复核与回归。
* **非目标**：自动改写代码；运行时热卸载；证明程序等价（不可判定）。

## 评分入口

见 [rubric.md](rubric.md)。参考答案：[model_answer.md](model_answer.md)。追问：[followups.md](followups.md)。

总体方法：[../00_how_to_run.md](../00_how_to_run.md)。
