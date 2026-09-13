# Stripe 面试 Loop 指南（OA 之后每一轮：形式 · 评分 · 通过线 · 挂点 · 备考动作）

> 证据全部来自 `loop/raw/`（每条都能回溯）；题目主键见 `loop/CATALOG.md`；练习目录 `loop/rounds/`；准备材料 `loop/study/`；演练器 `loop/mock.py`。
> 面向读者：Python 刷题 ~1300 题、缺工作向 parse/LLD/调试经验的校招或 L1–L2 候选人。**结论先行，细节靠证据。**

## 0. 总图

```
简历 → HackerRank OA（60 min，仅 SWE/校招）→ Recruiter 电话 30 min（有时在 OA 前）
  → Technical Phone Screen 60 min（45 编码 + 15 Q&A；1 题 3–4 part）
  → Virtual Onsite（Zoom，全远程）
       校招/实习：Programming Exercise + Integration（+ Bug Squash）≈ 3–3.5 h 连排
       L2/L3 社招：Programming + Bug Squash + Integration + System Design + HM/Behavioral，常分 2 天
       2026 新增：AI Programming Exercise（HackerRank 内嵌 AI，30 min）——其余轮次严禁 AI
  → HM chat（校招常在 onsite 后 3–4 个工作日单独安排）
  → Hiring Committee（每周开会，1–4 分书面反馈，"一个 lukewarm 即拒"）→ Team match（2–6 周，可能撤回）→ Offer
```

| 数字 | 值 | 来源 |
|---|---|---|
| 校招 OA 通过率 | ≈13%（2025-11 样本）；new grad 岗整体 13%、SWE 岗 11% | InterviewCoder；Taro |
| 电面 → 结果 | 1–5 天 | Medium azn7u1；Blind 1hirauis |
| 电面 → onsite | 2–3 周（可要求延后） | Leon；linkjob |
| onsite → 决定 | 拒 2–5 天；5–10 工作日正常；>2 周 = 进池等 team match/HC | Blind VPdSosJJ；Leon；cn_forums §8 |
| 端到端 | 4–8 周；内推 2 周；校招 9 月 OA → 12 月 onsite | Exponent；Simplify |
| Cooldown | 6 个月（早期轮被拒，Stripe 员工）/ 12 个月（推荐） | Blind c7vzbrvh、yiPKLXYS |
| 校招 headcount | 受 returning intern 影响，可能面完到 1 月才被告知无 HC | Blind t6bahgt3 |

**贯穿所有技术轮的评分主线（据 Stripe 员工与一手反馈）**：① 代码质量 > 最优复杂度（"Time and space complexity carry little weight"）② 速度：多 part 必须推进 ③ 从一大段文字里抽出干净的问题 ④ 自己构造输入、自己写测试（**没有自动测例**）⑤ 边写边说 ⑥ 独立性：求助 ≥3 次被记负面 ⑦ 谦逊 ⑧ 别"太熟练"——2024 起题库加速轮换，面试官警惕背题。
**语言结论**：Python/JS。Java/C++ 样板在 coding/integration 反复被报道"做不完"；电面 Python 通过线约 3/4 part、Java 2/4。

---

## 1. Recruiter 电话（30 min）

- **形式**：非技术 fit check：背景、why Stripe、职业目标、地点/签证、时间线；senior 岗可能由 HM 直接打；onsite 前还有第二次 30 min "informational call"。[interviewing.io；Exponent]
- **评什么**："clear, structured communication"、相关经验、ownership/users-first 信号；"cultural alignment is a hard filter, not a tiebreaker"。[Exponent；ophyai]
- **必备答案**：30–60 s 经历概述；**具体的** why Stripe（API-first、"increase the GDP of the internet" 对你意味着什么，点名一个你用过/读过的 Stripe API 或博客）；"why payments"。
- **不要做**：此阶段不报薪资数字（"looking for a competitive offer"，先了解完整 package）；不提在面的其他公司。[interviewing.io；InterviewQuery]
- **红旗实录**：面试官口头允许的事（查语法、不必做完）被 recruiter 事后标 "red flag"（Taro 2025-07）——**一切以书面 prep 材料为准**；recruiter ghost 与 headcount 撤回多有报道。
- **练习**：`python3 loop/mock.py bq recruiter -n 5` · 题库 `loop/rounds/01_recruiter/questions.md` · 材料 `loop/study/10-rounds/01-recruiter.md`。

## 2. HM chat（30–45 min）

- **三种形态**：① 校招 onsite 后单独 30 min（"Managerial"：teamwork/ownership）② 社招 onsite 内一轮 45 min（behavioral + 项目深挖）③ senior 岗首轮由 HM 代替 recruiter。中文圈普遍困惑"考不考技术"——答案：**不写代码，但会深挖技术决策**。[hr_hm §HM；cn_forums §2]
- **问什么**：端到端项目（ideated → pitched → broke down → risk → stakeholders）；deadline/模糊需求/需求变化时怎么协作；ownership；沟通风格；出问题时的反应；why Stripe 再问一遍。
- **怎么打分**：对照 Operating Principles 写 1–4 分书面反馈；HC 周会；"all thumbs up or rejection"；有 L3 全 hire 仅一轮 lean-no 被 C-level 否决的案例；有 L4 "behavioral 里用了技术术语" 被拒的案例。[Blind VPdSosJJ、pGMZbjds、kt6bwgwv]
- **挂点**：故事太长被打断后接不上（HM "kept interrupting"）；只讲技术不讲用户结果；无 alternatives/trade-off；把分歧对方说成傻子；术语堆砌。
- **备考动作**：6 个故事 × 两个版本（90 s / 3 min）覆盖 ownership · 冲突 · 失败 · 模糊/紧迫 · 质量 · 学习；每个故事标注命中的原则（表在 `loop/rounds/02_hm/stories.md`）；用 `loop/raw/hr_hm_behavioral.md` §"原则 → 答题映射" 自查。
- **练习**：`mock.py bq hm -n 3` · `loop/study/10-rounds/02-hm.md`。

## 3. Technical Phone Screen（60 min = 45 编码 + 15 Q&A）

- **形式**：Zoom + CoderPad 或自己 IDE 共享屏幕（可选）；语言任意；一题 3–4 part，做完一 part 才给下一 part；**无自动测例**——自己造输入、自己验证；面试官常在 part 2 后停下转 Q&A。[Blind nqzaykah、mdtk4bmj、jcnxxpsh；LC 6696304]
- **题型**（Stripe 员工原话）："Read in this JSON, transform it / do something interesting with it"；不是 LeetCode；数组/哈希为主；难点是"把业务规则快速翻成好代码"与阅读理解（题面故意啰嗦）。
- **递进模板**（中文圈印证）：basics → 加约束/滑窗 → TopK/最优 → 边界/并发；**中间 level 往往最难**（区间边界、无显式类型）。[cn_forums §3、§10]
- **通过线**：Python 3/4、Java/C++ 2/4；rubric 存在但"多数面试官不按 rubric 判"，四个打动点：High code quality / Fast completion / Simple clear thought process / Humble attitude。[Blind 5d7673dy；interviewdb insider]
- **挂点 top5**：① 追求最优复杂度不先写能跑的（Taro 2024）② 期待自动测例（LC 6696304）③ 求助 ≥3 次 ④ 只做到第一个 follow-up（LC 5341224）⑤ 花太多时间打磨（prep 材料说 quality over speed，但候选人因此挂）。
- **备考动作**：每题 45 min 计时；前 5 min 读完**全部** part 再写；每 part 写 2–3 个自测 `assert`；边写边说"我现在处理的是 X，边界是 Y"；最后 5 min 跑全部样例。
- **练习**：`mock.py start ps01 -m 45` … ps01–ps08（`loop/rounds/03_phone_screen/`）+ OA 题库里的电面高频 q19 q21 q08 q25 q22 q18；材料 `loop/study/10-rounds/03-phone-screen.md`、`00-prereq/04`、`05`。

## 4. Onsite · Bug Squash（45–60 min）

- **形式**：真实开源项目的 fork（私有 repo，pin 版本）+ Stripe 加的一个失败单测或 issue 描述；在**自己 IDE** 里 clone → 跑测试 → 定位 → 修；通常 1 个主 bug + follow-up，senior 可能 2–4 个；"everything else is real"（Stripe 员工）。[Blind hkzsddkz、bekekkqf；Coditioning]
- **库按语言分流**：Python `requests` / `Mako`；Java `SnakeYAML` / `Moshi` / `Jackson`；JS `Express` / `Day.js` / React 组件竞态；Ruby `Sass`。Python 版通过率 "<10%"（Stripe 员工 2022）。
- **评什么**："solving the bug isn't the primary objective"——独立调试能力、方法论、沟通；强表现范文："read the entry point before touching code, set a breakpoint early, formed a hypothesis, verified it, applied a targeted fix"。[Blind bxonqpkp、gyamarmf；Leon]
- **挂点 top5**：① 只用 print、不会 debugger（多例）② 盯栈顶、想读懂整个库 ③ 不读 README/文档（Google 候选人主因）④ 环境（JDK/Python 2 vs 3/import）吃掉 10 min ⑤ 大范围重写而非最小修复。
- **备考动作**：用 recruiter 发的 sample repo 提前跑通 IDE + debugger + 测试；自己 clone 热门库注入 bug 计时 ≥4 次（其中 1 次不用 debugger）；流程固定：跑失败测试 → 读 README 30 s → 从失败断言向上追数据 → 假设 → 断点验证 → 最小修复 → 加回归测试 → 讲根因与副作用。
- **练习**：`mock.py start bs01`（拷到 `loop/work/bs01/`，用 IDE 打开）→ `mock.py test bs01` → `mock.py ref bs01` 看参考修复；bs01–bs05；真实库对应 issue 见 `loop/raw/github_repos.md` §2；材料 `loop/study/10-rounds/04-bug-squash.md`、卡片 `20-cards/python_debug.md`。

## 5. Onsite · Integration（60 min）

- **形式**："open-book"：私有 repo（README、boilerplate、示例数据、API 文档）→ 本地跑起来 → 4–5 个递进 part；**可联网查文档，禁 AI**；语言与 bug squash 通常相同；不要求单测；需求有时写在 GitHub issue 里且**不可复制**。[Medium diyaag；Blind vwunpzkn；learncswithus]
- **题库**：BikeMap 最高频但"不总是 bikemap"（Stripe 员工）；其余：调 API 存 DB、多 JSON ETL、文件抽字段 → 外部 API → 合并、request replayer、git diff + owners。校招 Simplify 转述"reconciliation script：分页、限流、幂等"。
- **评什么**：正确性优先、快速推进、按文档用 API、错误处理、代码组织；"very easy api calling but easy for everyone so you have to be perfect"。[Blind 1j2ckbta；Exponent；Leon]
- **通过线**：2/5、2.5/5 with hints、3/5、3.9/5 都有人过；共识"integration 没做完 **或** bug squash 差，二选一还能过；两个都弱必拒"；没做 Part 3 从 L3 降到 L2 的案例。[Blind ncjsazmm、vvjmavis]
- **挂点 top8（extrabrain）**：没搞清输出格式就写；环境配置太久；忽视错误处理；过度设计；忘跑面试官给的测试；硬编码样例特判；轻视支付安全细节；卡住沉默。
- **时间分配**：0–5 读题确认假设 · 5–15 跑通项目定位代码 · 15–35 happy path · 35–48 错误处理/边界 · 48–55 清理 · 55–60 总结。
- **备考动作**：熟到闭眼写 `urllib.request`/`requests` POST JSON、二进制落盘、`json.load` 嵌套取值、`csv.DictReader`；官方 docs 的分页/幂等/429/webhook 语义背下来（`20-cards/stripe_api.md`）；GeoJSON `[lng, lat]` 顺序。
- **练习**：终端 A `mock.py serve int01` → 终端 B `mock.py start int01`；int01–int04；材料 `loop/study/10-rounds/05-integration.md`、`00-prereq/06`。

## 6. Onsite · Programming Exercise（45–60 min）

- **形式**：与电面同类但更长、更多 part，常"从 JSON/测试数据出发按逐步加码的需求实现"，有时先 clone repo；CoderPad/本地 IDE/HackerRank 都有；"Stripe usually wants two parts"（L2）。[Blind x7beaq87、cnhknchr、8grkgwt1]
- **题型**：订阅通知调度、支付账本类 + 追问、账户调度/LRU、限流 4-part、规则引擎、滑窗可疑用户、清账。追问方向固定：部分退款/去重/时间范围/持久化/并发/海量。
- **AI Programming Exercise（2026）**：HackerRank 内嵌 AI；30 min；题为 transactions + rules（关键词 → AND/OR）；评"能否指挥/验证/调试 AI 输出而不关掉脑子"——让 AI 读 README 出计划、生成代码，**自己写测试**、抓过度工程与漏边界。[interviewdb AI guide]
- **反馈实录**：两 part 完成但第二 part 有 bug 未修 = 拒因之一；"output has some extra commas"；面试官要求改变量名可读性。
- **备考动作**：类设计先写接口签名再填；每个方法先写 3 个 assert；追问清单预演（见各题 REPORT "面试官会怎么追问"）。
- **练习**：cd01–cd07（`loop/rounds/06_coding_onsite/`）+ OA 的 q07 q13 q32 q23；材料 `loop/study/10-rounds/06-coding.md`、卡片 `20-cards/patterns.md`。

## 7. Onsite · System Design（45 min；校招通常无）

- **谁有**：L2+ 一轮 45 min（真正设计 30–35 min）；校招/实习通常无，设计能力在 integration 与 coding 追问里考；个别 L2/校招报告有。[system_design §1]
- **形式**：Whimsical；题面是"一大段业务描述"要自己抽需求（Toronto Money-as-a-Service 2025 帖抱怨题面不清）；不考"设计 Instagram"。
- **评什么（Exponent 五维）**：problem framing → **API & data model（权重最高）** → failure modes & scale → separation of concerns → delivery（rollout/测试/监控）。一手拒因："insufficient reasoning about failure modes and system abuse"（webhook 题，Staff 面试官）。
- **主线**：两句话复述 + 不变量（钱不丢/不双扣/账要平）→ API 契约（幂等键、错误码、版本、分页）→ 数据模型（可变业务对象 vs 不可变 ledger，整数最小单位）→ 一致性（DB 唯一约束是真相源，Redis 只加速）→ 失败（重试+退避+抖动、DLQ、outbox、saga、熔断、租户隔离）→ 对账 → 可观测 + rollout。
- **挂点**：单 region 单库；不先框需求就画；把 webhook 商户 500/hang/SSRF/exactly-once 四问答不上；30 min 讲完、无 concern、仍拒（面试官期望错位）。
- **练习**：sd01–sd06（`loop/rounds/07_system_design/`：prompt → 45 min 自画 → 对照 rubric 与 model_answer → 过 followups）；材料 `loop/study/10-rounds/07-system-design.md`、`loop/raw/system_design.md` §4 六大题中文模型答案。

## 8. Behavioral / 最终 HM（30–45 min）

- **形式**：社招 onsite 内一轮或与 HM 合并；校招 = HM chat；"behavioral woven into every round"。
- **题库**：Stripe 专属 28 题（ownership from start to finish · 不是你的责任但你顶上 · 信息不全决策 · 一切都紧急如何排序 · 复杂技术决策 · 改变主意 · 与工程师/经理分歧 · 失败 · 高质量标准 · 负反馈 · 技术债 · mission 对你的意义）+ 跨公司 20 题。[hr_hm §Behavioral]
- **模板 STAR-L**：S 1–2 句 · T 1 句用 "I" · A 3–5 个动作含 alternatives→决策（≥50%）· R 量化且回到用户 · L 今天会怎么做 + 教训在哪用上；每故事 90 s / 3 min 双版本；少术语。
- **原则映射**：Users first · Move with urgency and focus · Be meticulous/craft · Seek feedback/collaborate egolessly · Deliver outstanding results · Stay curious · Obsess over talent · Macro-optimistic/Resilient · Humble · Rigorous thinking——每条"面试官在找什么 / 故事必须含什么 / 反例"见 `loop/raw/hr_hm_behavioral.md`。
- **拒后**：recruiter 一般不给具体理由；"walk you through next steps" 邮件 = 好消息；反馈 48 h 内。
- **练习**：`mock.py bq behavioral -n 5 -m 3`；`loop/rounds/08_behavioral/`；材料 `loop/study/10-rounds/08-behavioral.md`。

## 9. Offer / 定级 / 薪酬（速查）

- 定级在面试后决定；integration 没做完 Part 3 → L3 降 L2；Staff 讲不清业务影响会降级。
- 美国 L1 TC ≈ $210K（base ~$147K + stock ~$40K/yr + bonus）；L2 ~$278K；班加罗尔 L1 ≈ 59L（base 29L + sign-on 4.4L + RSU 22L/yr）；实习无 RSU；股权 1 年 cliff、9 个月 refresh。[levels.fyi 2026；LC 7352963；Exponent]
- Team match：committee 过但原团队拒会转其他团队；池里 2–6 周；HM 被鼓励共享好候选人。

## 10. 备考顺序（4 周，Python，校招/L1–L2）

| 周 | 做什么 | 产物 |
|---|---|---|
| 1 | `study/00-prereq` 01–06 + ex01/ex02；电面 ps01–ps04 计时 | 每题 `starter.py` 全绿 |
| 2 | ps05–ps08 + OA 电面高频 q19 q21 q08 q25；bug squash bs01–bs03（先 debugger 走通） | 4 次 45 min 计时记录 |
| 3 | integration int01–int02（serve + 计时）；coding cd01–cd04；bs04–bs05 | 每题 REPORT 里的追问自己口述一遍 |
| 4 | int03–int04；cd05–cd07；6 个故事 STAR-L 双版本；`bq` 每天 5 题；（L2+）sd01–sd04 | 故事表 + 自评 rubric 打分 |
