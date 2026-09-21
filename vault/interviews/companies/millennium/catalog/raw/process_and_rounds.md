# 流程、轮次、通过线、时间线（全公司 + LEaD 专属）

> 采集日期：2026-09-21。置信度同 `coding_first_round.md`。**LEaD 专属证据只有 4 条**（§1），其余是 Millennium SWE 通用流程（§2），只能类推。

## 1. LEaD 专属证据

| # | 事实 | 来源 | 置信度 |
|---|---|---|---|
| L1 | 第一轮 = **45 min，一位 SWE，Webex + HackerRank live coding**；无 OA、无 Caliper 提及 | Chi 邮件 2026-09-21（`inbox.md`） | 高 |
| L2 | **Miami 2026-02 一位候选人：3 轮，"mostly behavioral with no technical questions"，每轮很快回音** | Glassdoor Millennium 面经页（搜索摘要；Miami + 2026-02 + 早期职业 = 极可能 LEaD 或 FDE） | 中 |
| L3 | "The LEaD program starts with a **90 min video interview**" | Blind 摘要（日期不明） | 中低 |
| L4 | LEaD = 2–5 YOE、Miami only、"relatively new"；TC ≈ 同 YOE 的 MSFT；一例 new-grad Miami 轮岗（AI/ML/LLM 项目）offer ≈ **$210K TC** | Blind "Millenium LEaD program" + Blind 摘要 | 中 |
| L5 | 官方：cohort 制、12–18 个月、结束后进四个技术分部之一；负责人 Steve Johnson | mlp.com（`official_lead.md`） | 高 |
| L6 | 官方 JD：C++/Python/Java、Pandas/NumPy、FastAPI/Boost/Spring Boot、LLM 产品经验优先、ML/data pipeline、messaging、Docker/K8s、AWS/GCP | JD 镜像 | 高 |

**推断的 LEaD 流程**（L1 + L2 + 通用流程）：简历筛（批处理拒信 13:0x UTC）→ **R1 45 min SWE 技术 + 简历（HackerRank）** → R2/R3 更多人（HM / 技术 leader，可能偏 behavioral 与项目）→ 决定。**L2 的"全 behavioral"与 L1 的"live coding"并不矛盾**：L2 可能是 FDE 或 2026-02 的另一 req；也可能 LEaD 后续轮次确实偏 behavioral/项目。备考按"R1 必写代码，后续轮项目 + 行为 + 可能 SD"准备。

## 2. Millennium SWE 通用流程（类推用）

| 阶段 | 形式 | 证据 |
|---|---|---|
| Recruiter/HM screen | ~30 min：背景、为什么金融、薪资预期、是否理解 pod 结构 | TechPrep（低-中）；1p3a 1078136（PM 岗 HR 面：经历、策略、业绩、搬迁意愿） |
| OA | HackerRank：75 min/2 题（Blind）· 2 h/5 题（1p3a 1079245）· 3 h/4–6 题（QuantVault、1p3a 855488）· 4 h（1p3a 918431）· 180 min（Senior SWE，1p3a 668645）；**intern 2026：5 题 = 3 选择 + 1 industrial + 2 算法**；PracHub："multi-file Python repository tasks"；可能另有 Caliper/Criteria 测评 | 多源；**LEaD 本次无 OA** |
| 技术电面 | 45–60 min × 1–2；Webex + HackerRank/CodePad；"15 min 背景 + 30 min 一题"（1p3a 1090775）；"30 of 45 min on resume"（Blind） | 高-中 |
| 第二轮 | **三场 45 min 技术面（HackerRank）**（Blind 2hkyh25n） | 中 |
| Onsite / final | 3–4 h back-to-back，约 5 人：coding、SD、项目深挖、behavioral；pod 岗见 PM；**skip-level manager phone**；Bangalore 一轮纯项目讨论 | Blind、TechPrep、LC Discuss |
| 决定 | "decision typically 1–3 weeks"（SEO）；一手：R4 后 2 天自动拒信（LC 7423863）；Glassdoor Miami：每轮很快回音；**offer 后被 ghost / 重开一轮再拒的一手案例** | 中 |
| 端到端 | 6–10 周（TechPrep，低）；LEaD：投递 8/14 → 邀约 9/21 = **38 天到第一轮** | 高（自己的数据） |
| NDA / 其它 | 未见 NDA 报道；HackerRank 面试产品含 AI 助手与"监控候选人与 AI 的交互"（hackerrank.com 产品页）——**面试中是否允许 AI 以邀请为准，默认不用** | 中 |

## 3. 评什么（三源交叉）

- 官方：abstract reasoning + creativity · ownership & initiative · teamwork · **talk through code live** · fundamentals · handle feedback · industry trends（`official_lead.md` §4）。
- 一手：R3 允许查语法（看思路不看背诵）· 少一个括号没给 debug 时间就挂（**代码要一遍写对，写完自己走一遍样例**）· "面试官几乎不给反馈"（自己推进）· "问最喜欢的数据结构与取舍"（口头基本功）· "how to know what's true in an unfamiliar system"（LEaD 轮岗特别看这个）。
- 文化："挺卷、强调 autonomy 与 personal accountability"（1p3a 1158922）；pod 制 → "各团队自己选工具"（CIO 引语）。

## 4. 矛盾与未知

1. **45 min vs 90 min**：本次邀约 45 min（高）；Blind 说 LEaD 首轮 90 min（低）。以邀约为准；90 min 可能是旧格式或含 HR 段。
2. **写代码 vs 全 behavioral**：邀约明说 HackerRank live coding；Glassdoor Miami 2026-02 说全 behavioral。**准备两手：一题实用编码 + 项目深讲。**
3. **LC 风格 vs 实用题**：两种一手都有（LC 42/11/974 vs 分组聚合/分页拉取/装饰器）。QD-Python 岗偏 LC + Python 内功；SWE 岗偏实用。LEaD JD 偏数据/ML → 实用题概率更高，但 LC medium 必须不掉链。
4. **语言**：邀约未限；JD C++/Python/Java 任一；Miami equities algo 用 Java。**用 Python**，但 Java 基础题（HashMap 冲突、集合框架）要能口答。
5. **后续轮次数**：3 轮（Glassdoor Miami）/ 第二轮三场技术（Blind，非 LEaD）。未知；面完 R1 问 recruiter。
6. **未能抓取正文**：Blind 全部、Glassdoor 全部、1p3a 正文（含 951597 intern timeline、1124751、1158922）、LeetCode 6020524、levels.fyi 页面本体、LinkedIn。

## 5. 时间线与动作

- 邀约 2026-09-21 20:04 UTC；eightfold 自选时间。**建议选 3–4 天后**（把 pc01–pc10 过一遍 + Python 内功卡 + 项目口播），不要拖过一周（LEaD cohort 名额有限，"heard back quickly at every round"）。
- 回复 recruiter 时问：语言是否有限制；live coding 侧重（算法 vs 实际场景）；后续轮次的结构与时间线。
