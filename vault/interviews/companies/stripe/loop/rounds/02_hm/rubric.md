# HM 轮 —— 自评表

> 依据：`loop/LOOP_GUIDE.md` §2、`loop/raw/hr_hm_behavioral.md` §HM 轮 3–4 节。
> 每位面试官提交 **1–4 分**书面反馈（Leon Consulting）；Hiring Committee 4–7 天开会；
> **"一个 lukewarm 即拒"**——真实案例：L3 候选人 recruiter/技术轮全 strong hire，仅 1 轮
> lean-no（还不是 HM 轮）就被 C-level 否决（Blind pGMZbjds）；L4 候选人技术全过，
> **在 behavioral 用了技术术语**被 candidate review 拒（Blind kt6bwgwv）。

## 用法

1. `python3 loop/mock.py bq hm -n 3 -m 3` 抽 3 题，每题限时 3 分钟讲完一个 STAR-L 故事
   （用 `stories.md` 里准备好的六个故事对应）。
2. 讲完立刻按下面 6 个维度打分，不要等全部讲完再回忆——HM 轮真实反馈就是逐题记录的。
3. 任何维度 ≤2 分，视为这道题需要重讲。

## 评分维度（来源：codinginterview.com 6 维度 + ophyai/TechPrep 补充）

### 1. Clarity of communication（表达清晰度）
> "crisp, concise explanations"（codinginterview.com）；HM 会不断打断换问题，故事必须能被打断后续接（Blind wexjj3xy）。

| 分数 | 长什么样 |
|---|---|
| **1 分** | 讲了 2 分钟还没到 Action 段；被打断后接不上刚才讲到哪。 |
| **2 分** | 结构存在但啰嗦，关键信息被埋在细节里。 |
| **3 分** | STAR-L 五段清楚，3 分钟内讲完；被打断后能大致续上。 |
| **4 分** | 90 秒版和 3 分钟版都能流畅切换；被打断后立刻能从任意一步（比如直接跳到 Result）续接。 |

### 2. Rigorous thinking（严谨思维 / trade-off）
> "reasoning behind decisions, not just what happened"（Dataford/TechPrep）；"argue from first principles"（compatibility 页）。

| 分数 | 长什么样 |
|---|---|
| **1 分** | 只讲"做了什么"，没有"为什么这样做、放弃了什么方案"。 |
| **2 分** | 提到有别的方案，但说不清楚放弃的具体理由。 |
| **3 分** | 至少讲清 1 个被放弃的 alternative 及理由。 |
| **4 分** | 讲清 2 个以上 alternative，并且能说出当时用什么数据/原则做的取舍。 |

### 3. Ownership and accountability（端到端负责）
> "founder-like mindset"（codinginterview.com）；"end-to-end accountability"（官方原文）。

| 分数 | 长什么样 |
|---|---|
| **1 分** | 故事里"我"和"我们"混用，分不清个人贡献；或范围停在"我负责的那部分"。 |
| **2 分** | 个人贡献清楚，但止步于交付，不涉及后续运维/结果追踪。 |
| **3 分** | 从需求到上线全程在场，出问题时提到"我"去处理。 |
| **4 分** | 3 分基础上，还主动做了本不在职责范围内、但影响结果的事。 |

### 4. User-centered thinking（用户导向）
> "consider downstream impact on users and developers"（Exponent Guide）；"how another engineer would use your code"（TechPrep）。

| 分数 | 长什么样 |
|---|---|
| **1 分** | Result 段完全是技术指标（延迟/吞吐），没提到对人（商户/开发者/同事）的影响。 |
| **2 分** | 提到了用户，但是笼统的一句话（"用户体验更好了"）。 |
| **3 分** | 有具体的用户群体和影响描述。 |
| **4 分** | 讲清楚"我为了用户牺牲了什么"（deadline/自己方案/舒适度），显示这是真实权衡不是套话。 |

### 5. Collaboration and humility（协作与谦逊）
> "debate without ego"（Exponent）；"seek feedback or get defensive"（Medium diyaag 摘要）。**少术语**（Blind kt6bwgwv 真实反例）。

| 分数 | 长什么样 |
|---|---|
| **1 分** | 讲冲突故事时把对方描述成不讲理/技术差；堆砌术语让非本专业面试官听不懂。 |
| **2 分** | 语气中立，但没提到自己主动求反馈或改变立场的证据。 |
| **3 分** | 能公正转述对方立场，并提到自己因反馈调整过做法。 |
| **4 分** | 3 分基础上，语言对非技术听众友好（HM 未必是同技术栈），无堆砌术语。 |

### 6. Learning mindset（学习意愿）
> "embrace unfamiliar challenges and grow"（Exponent）。

| 分数 | 长什么样 |
|---|---|
| **1 分** | 说"没有什么要改的"，或找不到自己的责任。 |
| **2 分** | 承认了失误，但教训停留在"下次会更小心"这种空泛表述。 |
| **3 分** | 教训具体（比如"之后我在设计阶段加了一步 xxx"）。 |
| **4 分** | 教训具体，且能说出**后来在哪个场景真的用上了**这个教训（形成闭环）。 |

## 打分表（每轮练习填一次）

| 日期 | 抽到的题 | 清晰度 | Rigor | Ownership | 用户导向 | 协作谦逊 | 学习 | 最低分 |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |
| | | | | | | | | |
| | | | | | | | | |

**判定规则**：取 6 个维度的**最低分**作为整题判定分——对应真实机制"一个 lukewarm 即拒"。
连续 3 次练习里，同一个维度反复拿最低分，说明这不是某道题的问题，是某个故事本身有结构性缺口，
回 `stories.md` 的覆盖矩阵里查这条原则对应哪个故事槽位，重写骨架。
