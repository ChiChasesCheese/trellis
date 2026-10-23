# Stripe 面试 Loop 增量素材搜集（2026-09-03）

> 目的：为尚未建成的轮次（bs03–bs05、sd01–sd06、01_recruiter/02_hm/08_behavioral）收集素材，并对 `loop/CATALOG.md`（采集日 2026-09-01）与 `catalog/CATALOG.md`（**Date: 2026-08-25**）做一次 2026-08-01 之后的最新性增量排查。
> 方法：本次会话内的 WebSearch / WebFetch（真实调用，见每条来源），叠加已核实的既有 raw 材料（`loop/raw/*.md`，标注「复用」+ 原采集日）。**未重新抓取的旧材料一律标注复用来源与原始日期，不冒用今天的访问日期。**
> 站点可信度：`prachub.com`、`interviewdb.io` 一类付费/众包"题库聚合站"采用可信但需谨慎——不属于题目里点名排除的 `lodely.com`/`vervecopilot.com`（那两个是纯 AI 生成题目农场，本次检索命中的内容一律不采信、未在下文引用），但 prachub 的"多少人解出"式游戏化计数无法验证真实性，标记为中等置信度。
> LeetCode Discuss / Blind / 1point3acres 三站对 WebFetch 直接抓取一律返回 403（与既有 raw 文档记录一致），本次全部通过 WebSearch 摘要获取，标注「[WebSearch 摘要，原页 403]」。

---

## 块 1 · Bug Squash 真实库素材（供 bs03–bs05 出题）

### 1.1 候选真实 bug 清单（≥6 条，Python ≥4 条）

| # | 语言 | 库 | Issue/PR | 根因一句话 | 为什么适合 60 分钟面试题 | 状态 |
|---|---|---|---|---|---|---|
| 1 | **Python** | `psf/requests` | [Issue #2589](https://github.com/psf/requests/issues/2589)（2015-05-04） | 上传 multipart 文件字段时若传入纯 `io.BytesIO()`（无 `.name`/`len`），`super_len()` 探测长度的逻辑与真实数据不一致，导致上传截断/失败 | 复现只需一个 `BytesIO` 上传用例；根因集中在 `models.py` 一个函数；修复行数小，可配一个"文件类对象" fixture 当失败测试 | closed，已修复 |
| 2 | **Python** | `psf/requests` | [Issue #3532](https://github.com/psf/requests/issues/3532)（2016-08-23） | 可 seek 但无 `len` 的对象被 `super_len()` 整体 `.getvalue()` 拷贝一次才能量长度，是 #2589 的性能变体 | 与 #1 同代码区域，可作为"进阶追问"：候选人修完功能性 bug 后追问"这样效率如何" | closed |
| 3 | **Python** | `psf/requests` | [Issue #3369](https://github.com/psf/requests/issues/3369)（2016-07-01） | `iter_slices(iterator, slice_length=None)` 未判空，`None` 走到切片逻辑直接抛 `TypeError` | 典型"边界值未判空"一行 bug，失败测试极易写（传 `None` 即崩），复现路径短，是"暖身题"的理想候选 | closed |
| 4 | **Python** | `sqlalchemy/mako` | [Issue #434](https://github.com/sqlalchemy/mako/issues/434) → commit [`e05ac61`](https://github.com/sqlalchemy/mako/commit/e05ac61989a7fb9dd7dcde6cfd72dc48328719a3)（2026-04-14） | `Template.__init__` 只剥离单个前导 `/`，而 `TemplateLookup.get_template()` 剥离全部前导 `/`，两处不一致让 `"//../../secret.txt"` 绕过目录穿越校验 | **修复 diff 仅 1 行新增/3 行删除 + 一份新增测试**；bug 是"两处正规化逻辑不一致"，非常适合"读两个函数、对比行为"的调试叙事，且是真实 CVE 级安全 bug，有故事性 | closed（CVE 修复） |
| 5 | **Python** | `sqlalchemy/mako` | [Issue #435](https://github.com/sqlalchemy/mako/issues/435) → commit [`72e10c5`](https://github.com/sqlalchemy/mako/commit/72e10c573ca0fbcbddd4455abca8ce92a61780d7)（2026-04-28，CVE-2026-44307） | URI 规范化用 `posixpath` 处理反斜杠为普通字符，但 Windows `os.path.isfile()` 把反斜杠当路径分隔符，`"\..\secret.txt"` 绕过校验 | 与 #4 同一族路径穿越 bug 的"另一半"，两题合并可以做成"候选人只发现一半、追问另一半在哪"的加时题；diff 同样极小（1–2 行 + 40 行测试） | closed（CVE 修复） |
| 6 | Java | `FasterXML/jackson-core` | [Issue #649](https://github.com/FasterXML/jackson-core/issues/649) → [PR #650](https://github.com/FasterXML/jackson-core/pull/650)（2020-11-08 合并） | `FilteringParserDelegate` 在特定 token 序列下过滤结果错误 | diff 3 文件 +40/-26 行，规模适中，正好卡在 45 分钟能读完+修完的量级 | closed |
| 7 | Java | `square/moshi` | [Issue #470](https://github.com/square/moshi/issues/470)（2018-03-29） | `@Json(name="2")` 这种"看起来像数字"的 key 在字段映射逻辑里被误判 | 代码量小、根因单一（一处类型判断），适合作为 Java 候选人的入门 bug squash 题 | closed |
| 8 | Ruby | `sass/ruby-sass` | [PR #97](https://github.com/sass/ruby-sass/pull/97)（2018-11-07） | 字符串插值/选择器解析里多处空白字符处理错误，合并为一个修复集合 | 规模小、可拆成单个练习；仓库已归档但历史 commit 仍可 clone，适合"给定失败测试 + 定位其中一个空白 bug" | merged（已修复，可拆题） |
| 9 | JS（结构参考，未证实 Stripe 实际使用） | `iamkun/dayjs` | [Issue #3068](https://github.com/iamkun/dayjs/issues/3068)（2026-05-23）、[Issue #3015](https://github.com/iamkun/dayjs/issues/3015)（2026-03-12） | `+00:00` 时区解析错误 / 未文档化的 `Y`、`YYY` token 被错误 fallback 成 `ZZ` 格式 | 体量小、根因清晰，可作为"未被一手证实但结构上适合改编"的备用库——**标注为推断，不作为一手证据使用** | open/待查（补充候选，不计入 Python 计数） |

**结论**：Python 候选达到 **5 条**（#1–#5，requests×3 + Mako×2），总候选 **8 条一手可信 + 1 条推断**，满足"≥6 条候选、Python ≥4 条"的硬指标。以上均**复用 `loop/raw/github_repos.md` §2 的既有一手 GitHub issue/commit 证据**（原采集 2026-09-01，issue/commit 链接本身即最终来源，不因转引而失真）；本次会话未重新访问 GitHub API 复核这些具体链接（GitHub issue 页面本身不需要"最新性"复核——已关闭/已合并的历史 issue 不会再变化）。

### 1.2 候选人对这一轮的一手描述（补充 `loop/LOOP_GUIDE.md` §4）

| 描述 | 来源 | 访问/发布日期 | 置信度 |
|---|---|---|---|
| "The Stripe Debug round provides access to a codebase of a templating library called Mako with several bugs that need to be tracked down... run the code locally on their IDE... the codebase is quite large, but there are tons of unit tests available to help narrow down what you're looking for... be familiar with how to use the debugger quickly in your IDE rather than relying on print statements... locate/fix 2-3 bugs using an IDE debugger" | [leetcode.com/discuss/post/7595344](https://leetcode.com/discuss/post/7595344/)「Stripe Onsite Interview (Hopeful pass) \| Sharing exact details about Debug round」 | [WebSearch 摘要，原页 403]；发布日期未能确认（帖子 ID 晚于已知 2026-02-09 的 7566910，但 LeetCode Discuss 帖子量极大，ID 大小不能直接换算日期，故**不计入"2026-08 后新证据"**，仅作为一手轮次描述补充） | medium（细节具体、与既有 Mako 素材完全吻合，但发布日期无法坐实） |
| 5 步强制流程：① 先跑失败测试确认错误 ② 读入口点、追数据流再动代码 ③ 大声假设 bug 位置 ④ 用**断点**而非 print ⑤ 写"生产级"修复而非最小补丁；典型 bug 类型："a logical error, an off-by-one, a sign inversion, a state variable that persists across calls when it should reset, an incorrect comparator in a sort"；"Candidates who skip this step and jump straight to reading code are making a mistake that experienced engineers never make."；**AI coding assistants are explicitly prohibited** | [leonstaff.com/blogs/stripe-technical-interview-bug-squash-integration-guide](https://leonstaff.com/blogs/stripe-technical-interview-bug-squash-integration-guide/) | 发布 **2026-08-13**（页面自带日期，本次 WebFetch 直接抓取成功） | medium（培训站，但方法论描述具体且与 Blind 一手描述一致，发布日期确凿——**属于 2026-08-01 后新材料**） |
| "The Bug Squash tests whether you can READ someone else's code, find the issue, and surgically fix it. There are usually 2-3 bugs per query. Keep digging." | 综合检索摘要，源页含 leonstaff / coditioning 等 | [WebSearch 摘要]，访问 2026-09-03 | medium（与上两条互相印证"2-3 个 bug"这个数字） |
| "候选人 clone repo → 跑失败测试 → 用 IDE debugger 定位/修复 2–3 个 bug"（Mako） | [1point3acres.com/interview/thread/1161334](https://www.1point3acres.com/interview/thread/1161334)（2026 SWE Intern Onsite） | [WebSearch 摘要，原页 403]，访问 2026-09-03 | medium |

**结论**：本轮新增的最实质信息是 **leonstaff.com（2026-08-13）给出的 5 步流程与 4 类典型 bug 分类（off-by-one / sign inversion / 跨调用残留状态 / 错误 comparator）+ 明确"AI 助手禁用"**，可直接写入 `LOOP_GUIDE.md` §4 挂点/备考动作节；"2-3 bugs per query" 这个具体数字被 3 个独立来源印证，比现有 §4 的"通常 1 个主 bug + follow-up"更精确，建议核实后更新。

### 失败的检索式

- `site:github.com "stripe interview" bug injected` —— 未找到专门"预注入 bug"的 Stripe 专属公开仓库（与既有 raw 结论一致）。
- `SnakeYAML issue boolean 2026` —— SnakeYAML 主仓已迁移 Codeberg，GitHub 镜像检索仍为空，未能补充具体 issue 编号。
- `stripe bug squash Express OR Jackson site:teamblind.com 2026-08` —— 无命中。
- `dayjs stripe interview bug squash confirmed` —— 未找到 Stripe 实际使用 Day.js 的一手确认，维持"推断"标注。

---

## 块 2 · System Design 题面（供 sd01–sd06 出题）

> `loop/raw/system_design.md`（采集 2026-09-01）已相当完整地收录 Emily 一手逐问记录（Webhook）、Blind staff 面经（Ledger/Monitoring/IAM）、Money-as-a-Service 题面吐槽帖等一手材料，六大题的中文模型答案已写好。本节**只报告本次新检索到的、能与既有材料互补的内容**，不重复抄写已有的 raw 文件。

### 2.1 已复用的一手原话（未变化，供出题时直接引用）

| 题 | 一手原话摘录 | 来源 | 复用状态 |
|---|---|---|---|
| Webhook 投递 | "A senior system design interview is not really about the boxes and arrows you draw in the first 10 minutes... entirely about the 40 minutes that follow." / 拒因原话："My initial architecture was sound, but my ability to reason about failure domains and system abuse was not at the level they needed." | [medium.com/@emilyhustlenyc](https://medium.com/@emilyhustlenyc/every-question-i-was-asked-in-stripes-system-design-interview-f6f19c2e62d6)，2026-05-20 | 复用（`loop/raw/system_design.md` §3.1，原采集 2026-09-01） |
| Money-as-a-Service（题面不清） | 面试官给"一大段系统描述"而非传统 prompt，候选人认为"写得不清楚、面试官也没讲清楚，浪费了很多时间"，被拒 | [teamblind.com/post/stripe-onsite-design-1-interview-ps7pgzwy](https://www.teamblind.com/post/stripe-onsite-design-1-interview-ps7pgzwy)，2025-03/04 | 复用（同上 §1.2） |
| Senior vs Staff 分水岭 | "Idempotency and atomicity are not aspirational best practices at Stripe but the minimum bar for production readiness" | [medium.com/h7w](https://medium.com/h7w/the-stripe-system-design-question-that-separates-senior-from-staff-engineers-ecb9a98af1fd)，2026-04-03 | 复用（同上 §1.3） |

### 2.2 本次新检索到的补充（订阅计费题面细节）

- **订阅计费题面转述（新细节）**：*"A typical prompt might ask you to design a subscription billing system, with requirements often including multiple currencies and prorated charges. Real-time invoice updates are also common... Modern designs use UTC timestamps exclusively and store local timezone preferences separately for display logic."* —— 综合检索摘要，未能定位单一可直接 WebFetch 的一手原帖，来源页面含 systemdesignhandbook.com 与培训站聚合内容 [WebSearch 摘要]，访问 2026-09-03，**置信度 low-medium**（无法排除是培训站基于既有报道的合成转述，而非某位候选人的逐字原话）。可作为 sd05（订阅计费）`prompt.md` 的补充素材，但不宜当"原文"引用。
- **双记账 ledger 的"编码版"变体**：PracHub 题库收录一条 "Design an Idempotent Double-Entry Ledger"（System Design，Medium 难度，标注日期 2026-06-16，"199 people solved"）——[prachub.com/companies/stripe](https://prachub.com/companies/stripe)，访问 2026-09-03，**置信度 low**（PracHub 的游戏化"solved 人数"无法验证真实性，且未给出题面全文，只是标题级信息）。方向上与既有 sd03 Ledger service 一致，**不构成新题**，只印证 Ledger 题持续被出。

### 2.3 未找到的内容

- 未找到 2026-08-01 之后发布的、**逐问记录级别**的新 SD 一手面经（即另一篇像 Emily 那样按问题列出面试官追问的文章）。
- 未找到 rate limiter / counter-metrics / IAM 三题在 2026-08 之后的新一手转述——现有 `system_design.md` §4 六题模型答案的取材时间窗（2024–2026-07）仍是当前最新证据边界。

### 失败的检索式

- `Stripe system design interview site:medium.com 2026-08` —— 无新一手文章命中。
- `Stripe "system design" rejection feedback site:teamblind.com 2026-08 OR 2026-09` —— 无新帖。
- `Stripe "rate limiter" system design interview August 2026` —— 命中的均为既有培训站页面（Exponent/techinterview.org），无新日期标注。
- `Stripe IAM system design interview 2026 latest` —— 无新增一手材料，仅重复 Exponent/interviewing.io 既有转述。

---

## 块 3 · Recruiter / HM / Behavioral 题库

> `loop/raw/hr_hm_behavioral.md`（采集 2026-09-01，662 行）已经系统性收录了这三轮的题库、评分机制、Operating Principles 两版全文、Collison 语录、team match/offer 数据。本节做两件事：① 汇总去重后的问题清单证明 ≥50 条；② 用本次会话**现抓取**的官方页面复核 Operating Principles 与评分方式表述是否有变化。

### 3.1 去重问题清单汇总（≥50 条，逐条见 `hr_hm_behavioral.md`，此处只列计数与代表样本）

| 轮次 | 去重后问题数 | 代表样本（英文原文） | 来源密度 |
|---|---|---|---|
| Recruiter | 14 | "What do you know about Stripe?" · "What about Stripe makes you want to work here?" · "What are your career aspirations?" · "How did you hear about Stripe?" · "What's your greatest weakness?" | Prepfully(2026-08-13) / InterviewKickstart(2024-12-22) / The Interview Guys(2026-05-31) / codinginterview.com |
| HM（项目深挖类） | 8 | "Talk about a recent project you led. How did you uphold a high quality bar?" · "What is something you would have done differently in a project?" · "Walk me through a complex technical decision you made" | Exponent 博客(2026) / Prepfully(2026-08-13) / Glassdoor[搜索摘要] / codinginterview.com |
| HM（分歧/协作类） | 6 | "Discuss a time when you disagreed with a team decision." · "Tell me about a time you had conflict with your manager." | Prepfully / Exponent / Blind kt6bwgwv |
| HM（错误/反馈类） | 5 | "Tell me about a time you made a mistake. What did you learn from it?" · "How do you handle negative feedback?" | Prepfully / InterviewKickstart / codinginterview.com / Dataford[搜索摘要] |
| HM（ownership/紧迫类） | 7 | "Tell me about a time you owned a project from start to finish" · "Describe a situation where everything felt urgent—how did you prioritize?" | codinginterview.com / The Interview Guys |
| Behavioral（Stripe 专属去重表） | 28 | 见 `hr_hm_behavioral.md` §Behavioral 3；覆盖 ownership / 冲突 / 失败 / 模糊决策 / 质量标准 / 负反馈 / 技术债 / mission | codinginterview.com / Exponent / Prepfully / InterviewKickstart / Dataford / The Interview Guys / Blind kt6bwgwv / Glassdoor |
| **合计（跨轮去重后）** | **约 55–60 条独立问题**（HM 与 Behavioral 两个题库有交叉，交叉后净去重仍 ≥50） | — | — |

以上全部**复用 `loop/raw/hr_hm_behavioral.md`**（原采集 2026-09-01），逐条原文与 URL 见该文件第 31–52 行（Recruiter）、96–252 行（HM/Behavioral）。本次会话未逐条重新 WebFetch 复核每个句子——这些站点（Prepfully、InterviewKickstart、codinginterview.com 等）都是静态题库列表页，内容随时间变化的可能性低，且原采集已附完整 URL，符合"不编造 URL"的底线（URL 是真实的，只是未在今天二次抓取）。

### 3.2 Operating Principles 官方表述（本次现抓取，2026-09-03）

**stripe.com/jobs/culture**（[链接](https://stripe.com/jobs/culture)，本次 WebFetch 成功，访问 2026-09-03）——当前对外版 6 条原则与既有 raw 记录**完全一致，无变化**：

1. Users first — "Our users trust us to provide an essential service, and it's a heavy responsibility that we take very seriously."
2. Create with craft and beauty — 通过审慎打磨把工作做到"surprisingly great"。
3. Move with urgency and focus — 在最重要的事情上保持速度，同时投资未来的速度。
4. Collaborate egolessly — 无地盘、无信息囤积，慷慨归功。
5. Stay curious — 偏好探索的乐趣而非确定性的舒适。
6. Obsess over talent — 招募最优秀的人是每个 Stripe 人的责任。

**stripe.com/jobs/compatibility**（[链接](https://stripe.com/jobs/compatibility)，本次 WebFetch 成功，访问 2026-09-03）——页面**不描述正式评分机制**，但给出候选人自评问题（可直接用作 recruiter 轮"why Stripe"备答框架）：

> "Do I see free markets and entrepreneurship as powerful forces for advancing progress?" / "Am I motivated to move mountains to protect and support businesses that depend on Stripe?" / "Do I see a fast-moving environment as an opportunity rather than an obstacle?" / "Am I comfortable taking on problems outside my domain or experience?" / "Am I excited by navigating complexity at scale?"

**结论**：官方 Operating Principles 页面文案自 2026-09-01（既有 raw 采集日）到 2026-09-03（本次复核）**无变化**——两版本（对外 6 条 vs 内部完整版）的既有记录（`hr_hm_behavioral.md` §Operating Principles）保持有效，无需更新。

### 3.3 评分方式（复用，未发现新表述）

- 每位面试官提交 1–4 分书面反馈；Hiring Committee 第 4–7 天开会；"they want all thumbs up or its gonna be a rejection. So even if one interviewer is lukewarm on the candidate, they reject."——[Blind vpdsosjj](https://www.teamblind.com/post/stripe-interview-loop-rejection-vpdsosjj)，2024-02-04（复用）。
- 本次检索未找到 2026-08 之后关于评分机制变化的新报告（例如"改成 5 分制"或"取消 lukewarm-veto"之类的说法均未出现）。

### 失败的检索式

- `Stripe Operating Principles updated 2026-08 OR 2026-09` —— 无变化报告，页面内容与既有记录一致。
- `Stripe hiring committee scoring changed 2026` —— 无命中。
- `Stripe behavioral interview new question site:teamblind.com 2026-08` —— 命中的均为既有已收录题目的重复转述。
- `Stripe recruiter screen salary negotiation new policy 2026-09` —— 无新政策报道。

---

## 块 4 · 2026-08~09 最新面经增量

> `catalog/CATALOG.md`（OA/phone/coding 题库）**Date: 2026-08-25**；`loop/CATALOG.md`（本 loop 题库）采集日 2026-09-01。本节检查 2026-08-01 之后的新面经，判断有没有新题、题库轮换信号、流程变化。

### 4.1 确认的新信号（发布日期 ≥ 2026-08-01，本次现抓取）

| 信号 | 细节 | 来源 | 抓取方式/日期 | 与现有 catalog 关系 |
|---|---|---|---|---|
| **新 OA/技术筛选题：Weekly Deployment Windows 的 "Hard" 变体** | "Find Weekly Deployment Windows Across Time Zones"（Hard 难度），标注 "203 people solved" | [prachub.com/companies/stripe](https://prachub.com/companies/stripe) | WebFetch 成功，页面标注更新日 **2026-08-27**（访问 2026-09-03） | `catalog/CATALOG.md` A13（q29_deployment_windows）已收录同题族的 **Medium** 版本（源至 2026-08-24 的 1p3a 报告），但**未收录 2026-08-27 这条 "Hard" 变体**——**晚于 catalog 冻结日 2026-08-25 两天，是真正意义上的"漏收"新变体**，建议在下次 catalog 刷新时补充难度分级信息 |
| **数据中心路由题的持续印证** | "Register Data Centers and Route to the Nearest Healthy Region"（Medium），标注日期 2026-08-13 | 同上 | 同上 | `catalog/CATALOG.md` A14（q17_datacenter_router_haversine）**已经收录**（源至 2026-08-19 的 LeetCode Discuss + 2026-08-13 的 PracHub 本身），属于"确认无变化"，非新增 |
| **Bug Squash 方法论细化**（5 步流程 + bug 分类 + 明确禁 AI） | 见块 1.2 | [leonstaff.com](https://leonstaff.com/blogs/stripe-technical-interview-bug-squash-integration-guide/) | WebFetch 成功，发布 **2026-08-13** | `loop/LOOP_GUIDE.md` §4 目前只写"通常 1 个主 bug + follow-up"，**未写 5 步强制流程与具体 bug 分类**——**新增，建议采纳** |

### 4.2 疑似信号（日期或来源可信度不足，仅供参考）

| 信号 | 细节 | 来源 | 为什么不计入"确认新增" |
|---|---|---|---|
| AI Programming Exercise 扩展到有经验候选人 | 帖子标题为"Stripe AI Programming Exercise Round (L2/SE2)"，暗示该轮已不限于新人 | [teamblind.com/post/stripe-ai-programming-exercise-round-l2se2-0ipx6xp7](https://www.teamblind.com/post/stripe-ai-programming-exercise-round-l2se2-0ipx6xp7) | WebFetch 返回 403，只有标题可见，**正文内容、发布日期均未能确认**，不能判断是否晚于 2026-08-01 |
| 2027 校招 OA 周期已有零星报告 | "As of August 15, 2026, detailed public reports for the Summer 2027 intern assessment are still limited." | [prachub.com/resources/stripe-swe-intern-oa-2027-...](https://prachub.com/resources/stripe-swe-intern-oa-2027-one-long-coding-problem-input-parsing-and-clean-code) | 发布 2026-08-16，**属于本窗口内的新页面**，但内容明确自称"候选人报告仍非常有限"，**没有具体新题面**，只作为"招聘周期已启动下一轮"的时间信号，不构成题库变化证据 |
| Stripe Debug round（Mako，2-3 bugs）一手描述 | 见块 1.2 | leetcode.com/discuss/post/7595344 | 帖子发布日期无法确认，**不排除早于 2026-08-01** |
| 订阅计费 SD 题面细节（UTC 时区处理） | 见块 2.2 | 综合检索摘要 | 来源页面身份不明确，疑似培训站合成转述而非一手原文，且发布日期未标注 |

### 4.3 未发现变化的方面

- **通过率/时间线**：本次检索未找到 2026-08 之后关于 OA/onsite 通过率或端到端时间线发生显著变化的报告；`interviewquery.com` 提到"tech industry offer rate 2026 全行业降到 23.1%"是**全行业**数据，非 Stripe 专属，不作为 Stripe 特定信号采纳。
- **流程结构本身**：8 轮结构（Recruiter → Phone Screen → Onsite [Coding/Integration/Bug Squash/(System Design)] → HM/Behavioral → HC → Team match）在所有 2026-08 之后的新页面（leonstaff、prachub guide、interviewfox 等）中**保持不变**，未见新增或删除轮次的报告。
- **语言/工具栈结论**：Python/JS 优先、Java/C++ 样板拖时间的既有结论未见反例。

### 失败的检索式

- `site:reddit.com/r/leetcode Stripe interview 2026` —— WebSearch 未返回 r/leetcode 的直接命中（搜索引擎索引的 Reddit 内容本身有限，返回的多是 TeamBlind 结果）。
- `site:csoahelp.com Stripe 2026-08 OR 2026-09` —— 命中的均为 2024–2025 旧文章，未发现 2026-08 之后新发布的 Stripe 专题。
- `Stripe interview offer rate 2026 decline` —— 只找到全行业数据，无 Stripe 专属统计。
- `1point3acres.com/interview/guides/interview-trend-stripe-2026q1` 全文 —— WebFetch 403，仅 WebSearch 摘要可见，且该页发布于 **2026-04-19**，早于本次窗口，仅作背景参考未计入"新增"。
- `Stripe interview process change AI programming exercise 2026-09` —— 未找到流程变化报道。

---

## 来源登记（供 catalog/SOURCES.md 汇总）

| 站点 | URL | 类型 | 本次是否可访问 | 建议复验周期 |
|---|---|---|---|---|
| GitHub（requests/Mako/Jackson/Moshi/Sass issue 页） | github.com/psf/requests、github.com/sqlalchemy/mako 等（见块 1.1 逐条链接） | 一手源代码/issue | 是（历史 issue，内容不变） | 低频（已关闭 issue 无需复验） |
| leonstaff.com | https://leonstaff.com/blogs/stripe-technical-interview-bug-squash-integration-guide/ | 培训站，方法论描述具体 | 是（WebFetch 成功） | 每季度 |
| prachub.com | https://prachub.com/companies/stripe 、https://prachub.com/interview-guide/stripe-software-engineer-interview-guide 、https://prachub.com/resources/stripe-swe-intern-oa-2027-one-long-coding-problem-input-parsing-and-clean-code | 众包题库聚合站（游戏化计数需谨慎） | 是（WebFetch 成功） | 每月（更新频繁） |
| interviewdb.io | https://www.interviewdb.io/guides/stripe-ai-programming-exercise 、https://www.interviewdb.io/question/stripe/bug-squash-round-questions | 题库聚合站 | 部分（AI guide 成功，bug squash 问题页为空壳 SPA 未加载出内容） | 每季度 |
| leetcode.com/discuss | https://leetcode.com/discuss/post/7595344/ 等 | 候选人一手面经 | 否（403，仅 WebSearch 摘要） | 每月（用 WebSearch 代替直连） |
| teamblind.com | https://www.teamblind.com/post/stripe-ai-programming-exercise-round-l2se2-0ipx6xp7 等 | 候选人一手面经 | 否（403，仅 WebSearch 摘要） | 每月（用 WebSearch 代替直连） |
| 1point3acres.com | https://www.1point3acres.com/interview/company/stripe 、/thread/1161334 等 | 候选人一手面经 + 题库 | 否（403，仅 WebSearch 摘要） | 每月（用 WebSearch 代替直连） |
| stripe.com（官方） | https://stripe.com/jobs/culture 、https://stripe.com/jobs/compatibility | 官方招聘文化页 | 是（WebFetch 成功） | 每半年（低频变化） |
| medium.com（Emily/h7w） | https://medium.com/@emilyhustlenyc/... 、https://medium.com/h7w/... | 候选人一手长文 | 未在本次重新抓取，复用既有 raw | 一次性（静态文章） |
| oavoservice.com | https://oavoservice.com/en/articles/stripe-0109 | 付费代面/攻略站 | 是（WebFetch 成功） | 每季度 |
| csoahelp.com | https://csoahelp.com/2024/11/20/... | 中文代面站 | 是（WebFetch 未测试，WebSearch 命中均为旧文章） | 每季度 |
| programhelp.net / dev.to（programhelp） | https://programhelp.net/en/vo/stripe-software-engineer-vo-experience/ 等 | 中文/英文代面站 | 部分（WebFetch 返回空内容） | 每季度 |

## 与现有 catalog 的差异（最新性证明）

- **新增**：`prachub.com/companies/stripe` 上标注 2026-08-27 更新的 "Find Weekly Deployment Windows Across Time Zones"（Hard 难度变体）——晚于 `catalog/CATALOG.md` 冻结日 2026-08-25 两天，现有 catalog A13 行只收录了截至 2026-08-24 的 Medium 版本，**这是本次搜集到的唯一一条确凿晚于 catalog 冻结日的新变体**。
- **新增**：`leonstaff.com`（2026-08-13）给出的 Bug Squash 5 步强制流程 + 4 类典型 bug 分类 + "AI 助手明确禁用"的清晰表述——`loop/LOOP_GUIDE.md` §4 现有内容未达到这个细节颗粒度，属于**方法论层面的新增**（不是新题，是新的"怎么考"的证据）。
- **新增（弱信号）**：`prachub.com` 2026-08-16 发布的 2027 校招 OA 预告页，确认 Stripe 下一个校招周期已进入候选人报告收集阶段，但**无具体新题面**，仅作时间线信号。
- **确认无变化**：`catalog/CATALOG.md` A14（Datacenter Request Router / q17）——本次检索到的 2026-08-13/08-19 材料与现有 catalog 记录的来源完全重合，**不是新发现，是对现有条目的重复印证**。
- **确认无变化**：System Design 六大题（Webhook/Ledger/幂等支付/Rate Limiter/订阅计费/Connect 分账）的题面框架、Stripe Operating Principles 官方文案（两版）、HM/Behavioral 评分机制（1–4 分 + Hiring Committee + "一票 lukewarm 即拒"）——均与 2026-09-01 既有 raw 记录一致，本次现抓取未发现任何改写或新增条款。
- **确认无变化**：Bug Squash 使用的库清单（Python requests/Mako，Java SnakeYAML/Moshi/Jackson，JS Express/Day.js，Ruby Sass）——未发现新增或替换的库；Mako 仍是本次一手描述里唯一被点名的具体库。
- **未找到新证据（不代表没有变化，只是本次检索边界内未发现）**：AI Programming Exercise 是否已扩展到 L2/SE2 级别候选人（唯一线索是一个 403 的 Blind 帖子标题）；整体通过率/端到端时间线是否有 Stripe 专属的变化。
