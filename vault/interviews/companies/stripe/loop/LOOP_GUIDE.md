# Stripe 面试 Loop 指南（OA 之后每一轮：形式 · 评分 · 通过线 · 挂点 · 备考动作）

> 证据全部来自 `loop/raw/`（每条都能回溯）；题目主键见 `loop/CATALOG.md`；练习目录 `loop/rounds/`；准备材料 `loop/study/`；演练器 `loop/mock.py`。
> 面向读者：Python 刷题 ~1300 题、缺工作向 parse/LLD/调试经验的校招或 L1–L2 候选人。**结论先行，细节靠证据。**

## 0. 总图

```
简历 → HackerRank OA（60 min，仅 SWE/校招）→ Recruiter 电话 30 min（有时在 OA 前）
  → Technical Phone Screen 60 min（45 编码 + 15 Q&A；1 题 3–4 part）
  → Virtual Onsite（Zoom，全远程）
       校招/实习：Programming Exercise + Integration（+ Bug Squash）≈ 3–3.5 h 连排
         ※ **轮次组合并不固定**（2026-09-04 Reddit 一手，三例）：Dublin 校招只有 2 轮
           = Programming + Bug Squash，**没有 integration**；London backend 是 **2 轮
           Programming** + Integration + Bug Squash + HM，**没有 System Design**；
           India SWE2 是 Programming + Bug Squash + Integration 三轮，也没有 SD。
           **不要按固定表排期，以 recruiter 给的日程为准。**
       ※ 2026-07 一手实习面经：**coding 是两轮独立 45 min**（R1 CSV 字符串解析+多查询 4 part；
         R2 图+字符串、"类似 Splitwise" = 债务最小化 = q32/qA08），之后才是 debugging + HR
       L2/L3 社招：Programming + Bug Squash + Integration + System Design + HM/Behavioral，常分 2 天
         ※ **SD 不是 L2/L3 的必有项**：见上面 London / India SWE2 两例（归因不明，
           两位 OP 都没回答自己的 YOE/level）
       2026 新增：AI Programming Exercise（HackerRank 内嵌 AI，30 min）——其余轮次严禁 AI
  → HM chat（校招常在 onsite 后 3–4 个工作日单独安排；**排期邮件常在 VO 当天就到**）
  → Hiring Committee（每周开会，1–4 分书面反馈，"一个 lukewarm 即拒"）
  → **Reference check**（onsite 后 / offer 前，2 人 = 1 前经理 + 1 peer，recruiter 会主动挖负面）
  → Team match（2–6 周，可能撤回）→ Offer
```

| 数字 | 值 | 来源 |
|---|---|---|
| 校招 OA 通过率 | ≈13%（2025-11 样本）；new grad 岗整体 13%、SWE 岗 11% | InterviewCoder；Taro |
| **社招也可能有 OA** | 8 YOE senior（Canada remote）2026-04 仍收到 HackerRank OA；**别假设社招跳过 OA** | Reddit 1scjqoq（一手） |
| 电面 → 结果 | **5 小时 ~ 1 个月以上**（原记的 1–5 天是中位区间，不是范围）：最快 5 h 收到下一轮通知；也有一手报告一个多月后才回 | Medium azn7u1；Blind 1hirauis；Reddit 1ounzsh#159、1u0hnbq#12（均一手） |
| 电面 → onsite | 2–3 周（可要求延后） | Leon；linkjob |
| onsite → 决定 | 拒 2–5 天；5–10 工作日正常；>2 周 = 进池等 team match/HC | Blind VPdSosJJ；Leon；cn_forums §8 |
| 端到端 | 4–8 周；内推 2 周；校招 9 月 OA → 12 月 onsite | Exponent；Simplify |
| Cooldown | **按 12 个月规划。** 候选人侧证据一边倒：OA 挂 → 12 个月、电面挂 → 12 个月、4 人被 recruiter 告知 we recommend a year，**0 人复现 6 个月**。早期轮 6 个月仅存于单一 Blind 员工来源 | Blind c7vzbrvh、yiPKLXYS（6 个月，未复现）；Reddit 1scjqoq#31、1u0hnbq#2、1nn1ppj#1/#3/#13、1o4c5kp#5（12 个月，均一手） |
| 校招 headcount | 受 returning intern 影响，可能面完到 1 月才被告知无 HC | Blind t6bahgt3 |

**贯穿所有技术轮的评分主线（据 Stripe 员工与一手反馈）**：① 代码质量 > 最优复杂度（"Time and space complexity carry little weight"）② 速度：多 part 必须推进 ③ 从一大段文字里抽出干净的问题 ④ 自己构造输入、自己写测试（**没有自动测例**）⑤ 边写边说 ⑥ 独立性：求助 ≥3 次被记负面 ⑦ 谦逊 ⑧ 别"太熟练"——2024 起题库加速轮换，面试官警惕背题。
**语言结论**：Python/JS。Java/C++ 样板在 coding/integration 反复被报道"做不完"；电面 Python 通过线约 3/4 part、Java 2/4。
**三条 2026 增补**：① **onsite 各轮必须同一门语言**，在 recruiter 处一次性选定，**bug squash 的 repo 就是这门语言**；
**但电面可以与 onsite 用不同语言**（单一来源，中等置信）；**Go 也在可选清单里**（单一来源，低置信）；
② 官方语言清单里**只有 JavaScript，没有 TypeScript**（一位选 TS 的候选人被排成 JS 场次）；
③ 一位亲历者给"C++ 刷题 / JS 开发"的人的建议是**选 JS**，理由是"there would be rounds which require
**real API calling, and some json parsing**. And you wouldn't have done any of this in c++"——
**按"哪门语言你真写过 HTTP 调用和 JSON 解析"来选，不按刷题语言选。**
但注意 Java 仍是官方选项且有人主动选（India SWE2、Dublin 社招各一例）。[Reddit 1kr3kyn、1srvx7m#40/#41、1qfm8lh、1qsxpcl]

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
- **⚠️ 会回头问你 VO 里没修好的那个 bug**：候选人追问"会不会 reference 前面轮次的技术内容"，答复是
  "they'll **reference a theme from earlier rounds, like a bug you missed**, and ask how you'd diagnose it and
  what prevention steps you'd put in place"。
  **可操作（成本极低）：VO 每一轮结束后 5 分钟内写下"我卡在哪 / 事后想明白根因是什么 / 我会怎么预防"**，
  manager chat 前直接拿来用。⚠️ 该建议出自一条疑似软广的评论（点名了两个商业产品），
  **但动作本身零风险且与 §8 的 STAR-L 里的 L 完全一致，仍建议做**。[Reddit 1oe0ct2#3/#5]
- **备考动作**：6 个故事 × 两个版本（90 s / 3 min）覆盖 ownership · 冲突 · 失败 · 模糊/紧迫 · 质量 · 学习；每个故事标注命中的原则（表在 `loop/rounds/02_hm/stories.md`）；用 `loop/raw/hr_hm_behavioral.md` §"原则 → 答题映射" 自查。
- **练习**：`mock.py bq hm -n 3` · `loop/study/10-rounds/02-hm.md`。

## 3. Technical Phone Screen（60 min = 45 编码 + 15 Q&A）

> **校招流程里这一轮官方叫 "team screen"**（2025-09/10 三位 new grad 独立复述）。
> 和 offer 之后的 team match 是两回事，recruiter 说 team screen 时指的是这一轮。[Reddit 1nudha0、1oe0ct2]

- **形式**：Zoom + CoderPad 或自己 IDE 共享屏幕（可选）；语言任意；一题 3–4 part，做完一 part 才给下一 part；**你这边没有自动测例**——自己造输入、自己验证
（⚠️ 但**面试官那边可能有**：一条一手说 "my interviewer had prior TCs to check the code success"。
所以"没有测例"指的是"你看不到"，不是"没人在判"）；面试官常在 part 2 后停下转 Q&A。[Blind nqzaykah、mdtk4bmj、jcnxxpsh；LC 6696304]
- **⚠️ 平台可能就是 HackerRank，不是 CoderPad**：2025-12 一位候选人读 recruiter 发的 information packet 原文是
  "expect **screen sharing and hackerrank**, a programming exercise, no leetcode and **strictly no ai**"。
  同一份材料还说明 **loop 在此前 9 个月内改过**（"it is not the same interview loop from 9 months ago which had leetcode"）。[Reddit 1pddxxc，一手]
- **OA 与电面的 IDE 规则不同（容易踩）**：**OA 必须在 HackerRank 网页里直接写**，用外部 IDE 写完复制粘贴**可能触发抄袭检测**；到了 Technical Screen 阶段才可以用自己的 IDE。[teamblind stripe-oa-tips-iw8632ms]
- **⚠️ 但"可以用自己 IDE"是书面条款，现场可能被推翻（有实拒案例）**：2025-10 一位 Backend 候选人按 recruiter 发的
  prep guide 准备了 Java + Lombok + Jackson，面试官当场要求改用 HackerRank、并禁用 Lombok；
  **两次争论各 2–3 分钟，两天后被拒**。同帖两条独立回复："don't use your own IDE because they aren't prepared
  for it **even though they say so**"、"you should expect to code in the **whiteboard kind of a scenario**,
  i.e. without any assistance at all"。
  **对策：按裸写、无补全、无外部库准备；面试官要求换什么就换什么，一句 sure 结束，不要引 prep guide 反驳。**
  - **这大概率是平台约束，不是面试官脾气**（所以别指望争论能赢）：那位面试官给的理由就是
    "do not use Lombok as **it will not [work] on hackerrank**"；2024-05 另有两条同向说法——
    "I've seen people post trying to use **Gson that doesn't work in hackerrank IDE**"、
    "**Hackerrank has always dictated how API calls should be done per language. Usually it is using the
    standard library**... A similar oddity existed for JavaScript"。
    ⚠️ 后两条**都不是一手**（一条是"我看到有人发帖"，一条是社区判断），所以写成"大概率"而非事实。
    **实际含义对 Python 是明确的：练 `urllib.request`，不要练 `requests`。**[Reddit 1cu77pw 正文 + #2]
  （与 §1 的"口头许可被事后追责"是同一类风险的两个方向：**书面宽松条款同样不可依赖**。）[Reddit 1o4c5kp，一手 + 已知结果]
- **AI 政策的执行方式**：用 Cursor/Windsurf 类 AI 编辑器不自动出局，但要**主动当场演示 AI 已关闭**
  （新建空文件、打字、展示无补全）——一位这么做的候选人通过了该轮。[Reddit 1o4c5kp#10，一手]
- **题型**（Stripe 员工原话）："Read in this JSON, transform it / do something interesting with it"；**不是纯 LeetCode**（多条一手印证："Leetcode is useless for Stripe"、"Don't stress about DPs and graphs. It won't be cliche LC question. **It's gonna be super similar to your OA**"）；数组/哈希为主；难点是"把业务规则快速翻成好代码"与阅读理解（题面故意啰嗦）。
  ⚠️ **一条低可信度反例**：2026-05 有人评论 "STRIPE literally had an **LC hard** in their OA which I recently gave"
  ——**单一匿名评论、零细节、未说岗位地点**，不足以推翻上面的结论，但记一笔。
  （本仓库的 `qA01`–`qA14` 就是 LC 题号打底的一批，留着是对的。）[Reddit 1ounzsh#142/#143；1tr1uqz#1]
- **递进模板**（中文圈印证）：basics → 加约束/滑窗 → TopK/最优 → 边界/并发；**中间 level 往往最难**（区间边界、无显式类型）。[cn_forums §3、§10]
- **⚠️ 通过线：没有硬线，recruiter 口径互相矛盾。** 三条一手证据互不相容：
  ① 一位 recruiter **面试前明说** "you need to solve **4/4 parts** to proceed forward to the interview loop"；
  ② 另一位候选人的 recruiter 说 "**it doesn't depend on how many parts you solve**, they are just assessing your
     technical and communication skills"，该候选人 **2/3 part 过了**（且事后拿到了面试官写的原始反馈）；
  ③ 本指南原记的 Python 3/4、Java/C++ 2/4。
  **并且 part 总数本身不固定**——有 3-part 的电面、也有只有 2 part 的。
  **实用读法：把 part 数当努力方向而不是及格线，把"代码质量 + 出声沟通"当真正的评分项。**
  [Blind 5d7673dy；interviewdb insider；Reddit 1u0hnbq 正文 + #12（两条均一手）；1ounzsh#145/#146]
- 四个打动点仍然成立：High code quality / Fast completion / Simple clear thought process / Humble attitude。
- **挂点 top5**：① 追求最优复杂度不先写能跑的（Taro 2024）② 期待自动测例（LC 6696304）③ 求助 ≥3 次 ④ 只做到第一个 follow-up（LC 5341224）⑤ 花太多时间打磨（prep 材料说 quality over speed，但候选人因此挂）。
- **⚠️ 约束会藏在 intro 里，不在 part 正文里**（一手挂经，代价是 12 个月 cooldown）：
  "the **sliding window constraints where nowhere mentioned in the actual task (part 1)** but rather was
  **buried in the intro** which i skimmed cause i knew i was gonna be tight on time. This led me to make wrong
  assumptions and i wasted so much time."
  **对策：前 5 min 连 intro 一起读，把 intro 里每个数字 / 时间窗 / 阈值抄进代码注释再动手。**[Reddit 1u0hnbq#2，一手]
- **做完一个 part 立刻主动要下一个**，别等到最后 15 分钟：一位候选人剩 15 min 才开口要 part 3，面试官直接转 Q&A 了；
  另一位剩 10+ min 却"没得到机会"尝试。**口头 checkpoint："this part works, here are my asserts — can we move on?"**[Reddit 1nudha0 正文 + #8，均一手]
- **备考动作**：每题 45 min 计时；前 5 min 读完 **intro + 全部 part** 再写；每 part 写 2–3 个自测 `assert`
  （有一手挂经就是把 part 1 的 bug 带进 part 2 才回头查，连锁吃掉后面的 part）；边写边说"我现在处理的是 X，边界是 Y"；最后 5 min 跑全部样例。
- **练习**：`mock.py start ps01 -m 45` … ps01–ps08（`loop/rounds/03_phone_screen/`）+ OA 题库里的电面高频 q19 q21 q08 q25 q22 q18；材料 `loop/study/10-rounds/03-phone-screen.md`、`00-prereq/04`、`05`。

## 4. Onsite · Bug Squash（45–60 min）

- **形式**：真实开源项目的 fork（私有 repo，pin 版本）+ Stripe 加的一个失败单测或 issue 描述；在**自己 IDE** 里 clone → 跑测试 → 定位 → 修；"everything else is real"（Stripe 员工）。[Blind hkzsddkz、bekekkqf；Coditioning]
- **几个 bug：不定，1–5 都有一手报告。按"逐个跑、逐个修，修不完是常态"准备，不要背一个数字。**
  证据谱系（本日补抓后重排）：老证据"1 个主 bug + follow-up，senior 2–4 个"；2026 三份材料说"2–3 个"
  （其中两份只是搜索摘要）；**2025-10 Dublin new grad 一手"only resolved 1/3 bugs"**；
  **2025-08 Dublin senior 一手"There'd be 4-5 unit tests failing"**；India 校招一手报 1 个。
  ⚠️ 注意"**失败的单测数 ≠ 不同的 bug 数**"——一个 bug 可以让多个测试红。原文说的是 unit tests。
  **2026-09-04 更正**：本文件当天早些时候曾据单条证据写成"按 3 个准备"，补抓到的两条一手把它推翻了。
  [`catalog/discovery/2026-09/rounds_material.md` §1.2；Reddit 1oagvvw、1oe0ct2、1srvx7m#14、**1mgcc99**]
- **形态（2026-04 London 一手全文）**：给一个**私有** GitHub repo → 本地 clone → build → 跑出若干失败单测 →
  在面试官引导下逐个调。**repo 的语言就是你在 loop 开始时一次性选定的那门语言。**[Reddit 1srvx7m#14/#15/#16/#19]
- **明确禁用 AI**：这一轮（以及除 AI Programming Exercise 外的所有轮）禁止使用 AI 编码助手，
  **一手证据明确到"含 IDE 自动补全"**（不只是聊天框）。用 Cursor/Windsurf 类编辑器要**当场演示已关闭**。
  [leonstaff 2026-08-13；Reddit 1mgcc99#11、1o4c5kp#10（均一手）]
- **⭐ 用不用 IDE / debugger 本身是显式评分项**（不是"允许"而已）：一手原文
  "**Use of an IDE is permitted and is actually one of the evaluation parameters**"。
  两条独立一手同向。[Reddit 1mgcc99 正文、1u0mgyy 正文]
- **issue 里若同时给了一个通过的测例和一个失败的测例**：**先 diff 这两个测试的输入**，
  差异处就是 bug 的触发条件——比从头读库快得多。[Reddit 1u0mgyy 正文，一手（Android 岗，但方法通用）]
- **库按语言分流**：Python `requests` / `Mako`；Java `SnakeYAML` / `Moshi` / `Jackson`；JS `Express` / `Day.js` / React 组件竞态；Ruby `Sass`。Python 版通过率 "<10%"（Stripe 员工 2022）。
  - ⭐ **2025-08 Dublin senior 一手，逐字**："you're given the **entire repository of a built-in library**,
    for instance, **for python, it could be either \"requests\" or \"mako\"**. There'd be **4-5 unit tests failing**
    and you'll be expected to **run the tests one by one and make them pass by fixing the actual code**.
    The challenge here is again **time** since, **if it is an unfamiliar library like mako, it is quite challenging
    to figure out what it does in the first place**."
    → **本仓库 `bs01_mini_template_engine`(minimako) 与 `bs02_mini_http_client`(minihttp) 正好是这两个库的缩微版**，
    这是我们对 bug squash 轮最直接的一次外部确证。**那句"不熟的库先搞懂它在干什么最难"就是 `CODE_GUIDE.md` 存在的理由**
    （所以第二遍起别读它——真实面试里没有导读）。[Reddit 1mgcc99 正文，一手]
  - **bug 的来源**：问"是招聘团队注入的还是该库 GitHub 上真实报过的"→ 一手答"**Could be either.**"[Reddit 1mgcc99#6]
  - **JS / Java 场次的库仍然零证据**：帖里被问了 5 次，全部转私信。**不要以为上面这份清单是完整的。**
- **一场 SnakeYAML 的真实 bug 对**（候选人原文）：① `flag: on` 解析不出来（YAML 1.1 把 `on` 当布尔）② CSV 解析结果漏掉引号。两个都属"逻辑错误"类。[prachub assign-reviewers-from-changed-files]
- **评什么**："solving the bug isn't the primary objective"——独立调试能力、方法论、沟通；强表现范文："read the entry point before touching code, set a breakpoint early, formed a hypothesis, verified it, applied a targeted fix"。[Blind bxonqpkp、gyamarmf；Leon]
- **挂点 top6**：① 只用 print、不会 debugger（多例）② 盯栈顶、想读懂整个库 ③ 不读 README/文档（Google 候选人主因）④ 环境（JDK/Python 2 vs 3/import）吃掉 10 min ⑤ 大范围重写而非最小修复
  ⑥ **修复层级选错**——2025-10 一手："[面试官] told me to implement the fix in some **other function,
  higher up in the stack trace** rather than the function I was fixing"。
  **定位到根因之后，先问自己"这个 fix 该落在栈的哪一层"，再动手。**[Reddit 1ohkp31 正文，一手]
- **四类典型 bug（背下来，进场先按这四类猜）**：逻辑错误 · off-by-one · 符号反转 · **跨调用残留的状态**（该重置没重置）· 排序里用错 comparator。[leonstaff 2026-08-13]
- **备考动作**：用 recruiter 发的 sample repo 提前跑通 IDE + debugger + 测试；自己 clone 热门库注入 bug 计时 ≥4 次（其中 1 次不用 debugger）；流程固定：跑失败测试 → 读 README 30 s → 从失败断言向上追数据 → 假设 → 断点验证 → 最小修复 → 加回归测试 → 讲根因与副作用。
- **5 步硬流程（面试官在看你做没做这几步，不只看你修没修好）**：① **先跑失败测试**把错误亲眼确认一遍——"跳过这步直接读代码，是有经验的工程师不会犯的错" ② 读入口点、追数据流，再动代码 ③ **把假设说出来**（"我怀疑在 X，因为 Y"）④ 用**断点**验证，不要靠 print ⑤ 写生产级修复，不是能过测试就行的补丁。[leonstaff 2026-08-13]
  - **关于第 ④ 步的一条反证**：2026-04 London 一手转述面试官原话 "You can use a **debugger, print statements,
    or any approach you prefer**"。**所以 print 不会当场被打断**——但这属于"面试官口头许可"（见 §1 的红旗实录），
    而"只用 print、不会 debugger"仍然是被独立记录过的挂点。**结论不变：按会用 debugger 准备，print 当补充手段。**[Reddit 1srvx7m#14]
- **卡住时不要为了"显得在推进"乱试**（一手挂经的自我剖析）："I ended up being too hurried, and made poor decisions
  to try things that **I knew intuitively had little chance of being the problem, just for the sake of forward progress**."
  ——第 ③ 步"把假设说出来"正是防止这件事的机制：**说不出理由的方向就别动手改。**[Reddit 10o4xfq#1，一手]
- **从零学调试**：`loop/rounds/04_bug_squash/DEBUG_101.md` —— 假设你没用过 pdb，从读 traceback 讲到 `pytest --pdb`，含在 bs01 上真跑出来的实录（两条命令找到根因）；卡片 `loop/study/20-cards/python_debug.md`。
- **练习**：`mock.py start bs01`（拷到 `loop/work/bs01/`，用 IDE 打开）→ `mock.py test bs01` → `mock.py ref bs01` 看参考修复；bs01–bs05，每题旁边有中文 `CODE_GUIDE.md` 逐模块讲代码（**第二遍起别读**）；真实库对应 issue 见 `loop/raw/github_repos.md` §2；材料 `loop/study/10-rounds/04-bug-squash.md`。

## 5. Onsite · Integration（60 min）

- **形式**："open-book"：私有 repo（README、boilerplate、示例数据、API 文档）→ 本地跑起来 → 4–5 个递进 part；**可联网查文档，禁 AI**；语言与 bug squash 通常相同；不要求单测；需求有时写在 GitHub issue 里且**不可复制**。[Medium diyaag；Blind vwunpzkn；learncswithus]
- **⭐ 四段式结构（2025-08 Dublin senior 一手，逐字）**："there's **4 sub-rounds**. To begin with, you're given a
  **hello world boiler plate code** and you're expected to **call an API and print the response**. The request
  parameters are expected to be **read from a file — so file parsing is essential**. In the second one, you're asked
  to **parse the response and use it to call yet another API**. The subsequent rounds follows suit by increasing
  complexity in terms of forming the request and parsing the response. **Use of an ide is permitted.** The challenge
  here is **time** since **requirements change across sub-rounds** and thus **if the code is modular enough from
  the beginning, it helps**."
  → **可操作：part 1 就把 `build_request()` / `call()` / `parse()` 三件事拆成三个函数**，别写成一个 main。
  需求每个 sub-round 都变，不拆分就是每轮重写。**"请求参数从文件里读"这条也要练**——不是硬编码 URL。
  [Reddit 1mgcc99 正文，一手]
- **题库**：BikeMap 最高频但"不总是 bikemap"（Stripe 员工）；其余：调 API 存 DB、多 JSON ETL、文件抽字段 → 外部 API → 合并、request replayer、git diff + owners。校招 Simplify 转述"reconciliation script：分页、限流、幂等"。
- **评什么**：正确性优先、快速推进、按文档用 API、错误处理、代码组织；"very easy api calling but easy for everyone so you have to be perfect"。[Blind 1j2ckbta；Exponent；Leon]
- **通过线**：2/5、2.5/5 with hints、3/5、3.9/5 都有人过；共识"integration 没做完 **或** bug squash 差，二选一还能过；两个都弱必拒"；没做 Part 3 从 L3 降到 L2 的案例。[Blind ncjsazmm、vvjmavis]
  - **part 总数不固定**：2026-04 London 一手是 **5 part**；2026-08 Dublin（4 YOE，二手代问）只有 **3 part**。
    "4–5 个递进 part"是常见值，不是定值。[Reddit 1srvx7m#29；1vyzxek]
  - **一个"做完了仍被拒"的实录**（校招 VO，programming exercise 4/4 part 全做完、bug squash 1/3）：
    仍拿到 manager chat 邀请，说明单轮差不等于出局；但另一位说"bad/average performance in bug round is a
    deal breaker（我认识的人就因此被拒）"。**两边都记着：不要用它安慰自己，也不要因为一轮崩了就放弃后面。**[Reddit 1oagvvw、1oe0ct2]
- **挂点 top8（extrabrain）**：没搞清输出格式就写；环境配置太久；忽视错误处理；过度设计；忘跑面试官给的测试；硬编码样例特判；轻视支付安全细节；卡住沉默。
- **⚠️ 60 分钟里可能只剩 35 分钟写代码**（2026-04 一手，4 YOE）：面试官"gave me **35 minutes only**, told he would
  use **10 minutes in the end for discussion, 10 minutes in starting for setting up my IDE and github account**
  ... (Also the interviewer kind of **arrived late 4-5 minutes**)"，他因此只做完 2/4 part。
  **对策：IDE、GitHub 登录、SSH key、clone 目录、语言 runtime 必须在面试开始前全部就绪并跑过一次**——
  这 10 分钟是唯一你能自己拿回来的。[Reddit 1semjq1#46]
- **时间分配（按满 60 min 排；若开场装环境，把每段整体左移）**：0–5 读题确认假设 · 5–15 跑通项目定位代码 · 15–35 happy path · 35–48 错误处理/边界 · 48–55 清理 · 55–60 总结。
  **保守版（实测更接近）**：装环境 0–10（提前做掉就是白赚）· 读题 + happy path 10–30 · 错误处理 30–42 · 清理 42–48 · 讨论 48–60。
- **备考动作**：熟到闭眼写 `urllib.request`/`requests` POST JSON、二进制落盘、`json.load` 嵌套取值、`csv.DictReader`；官方 docs 的分页/幂等/429/webhook 语义背下来（`20-cards/stripe_api.md`）；GeoJSON `[lng, lat]` 顺序。
- **练习**：终端 A `mock.py serve int01` → 终端 B `mock.py start int01`；int01–int04；材料 `loop/study/10-rounds/05-integration.md`、`00-prereq/06`。

## 6. Onsite · Programming Exercise（45–60 min）

- **形式**：与电面同类但更长、更多 part，常"从 JSON/测试数据出发按逐步加码的需求实现"，有时先 clone repo；CoderPad/本地 IDE/HackerRank 都有；"Stripe usually wants two parts"（L2）。[Blind x7beaq87、cnhknchr、8grkgwt1]
- **题型**：订阅通知调度、支付账本类 + 追问、账户调度/LRU、限流 4-part、规则引擎、滑窗可疑用户、清账。追问方向固定：部分退款/去重/时间范围/持久化/并发/海量。
- **AI Programming Exercise（2026）**：HackerRank 内嵌 AI；30 min；题为 transactions + rules（关键词 → AND/OR）；评"能否指挥/验证/调试 AI 输出而不关掉脑子"——让 AI 读 README 出计划、生成代码，**自己写测试**、抓过度工程与漏边界。[interviewdb AI guide]
  - **✅ 2026-09-04 补抓后能确认的（一手）**：① **平台确实是 HackerRank 内嵌的 AI**——亲历者原文
    "its the interview round where you are **allowed to use AI models provided within hackerrank** to solve a
    **more challenging problem**"；② **这一轮已经进了校招 VO**——2026-08-07 一位 new grad 把
    "**AI Coding, Integration or Bug Squash**" 并列为自己 VO 的三轮。
    ❌ **仍然拿不到的**：题目内容。那位亲历者关于 Stripe 这轮只写了两句，帖子里 36 条评论中所有详细的 AI 轮
    描述**全都是别的公司**（Meta / Amazon / DigitalOcean），有人专门追问 Stripe 细节——**无人回答**。
    [Reddit 1vbpool 正文（一手）、1vhpsgz 正文（一手）]
  - **⚠️ 证据等级更正（2026-09-04）：题面那一条不是一手。** 本指南此前把它记成"一手长文已确认细节"，
    **错了**。原帖正文第二句自述 "**Sharing what I've gathered from a few candidates** who went through it
    recently"，发帖账号 `/u/interviewdb` 是做众包题库的网站（评论 1 当场质疑其商业动机），
    **23 条评论里没有任何一条是亲历者出面确认**（还有人在问 "Has anyone actually gone through this?"）。
    **正确等级：二手汇总 · 商业来源 · 未经亲历者交叉验证。**（补抓 33 帖后**依然没有**亲历者一手题面
    可以替换它——`cd07` 的题面来源仍旧只有这一个二手帖。）下面的细节内容**保留不删**——
    它与本仓库 `cd07` 吻合、也与 2026 年其他材料同向，但**不能当作已证实的事实**去背。
  - **细节（按上面的等级读）**（r/leetcode 1u51q4w，正文 1989 字 + 23 评论）：HackerRank 内嵌**类 Cursor 的 AI 对话框**；题目是 transactions + rules（每条规则 accept/block + 一个 if 条件），**前面 part 是关键词/字符串匹配，后面 part 加 AND/OR 布尔逻辑并叠加前面的成果**；README 很长，**读规格的速度本身是考点**；真正编码只有约 30 分钟，"trying to hand-code everything yourself may not be realistic"。
    有效打法：让 AI 读完整 README → 让它总结需求 → 要实现计划**并真的 review** → 让它写 →**自己加测试和边界** → 跑、调。**本仓库 `cd07_transactions_rules_ai` 与此高度吻合。**
  - **范围可能比这更广（仍存疑）**：一位 Senior+ 候选人（2026-08-25）说自己"Two phone screens, coding with AI"——两轮电面都是 AI 辅助编码，而非只有一轮独立 AI Exercise。另有候选人形容该轮"自己手写 80% 概率写不完，主要依赖 AI"。**单一来源 medium，未改写上面的正文，下一轮需交叉验证。**[prachub ie1；assign-reviewers-from-changed-files]
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
- 美国 TC 中位数（levels.fyi 2026-09-03 直抓复核）：**L1 $209,973 · L2 $289,675 · L3 $435,992**。L1 与旧记录一致；**L2 比旧记录的 ~$278K 高约 4.2%**；L3 是本次新增。班加罗尔 L1 ≈ 59L（base 29L + sign-on 4.4L + RSU 22L/yr）**本轮未能复核**（levels.fyi 该地区细分页返回空模板）。实习无 RSU；股权 1 年 cliff、9 个月 refresh。[levels.fyi 2026-09-03；LC 7352963；Exponent]
- **Reference check（本指南此前完全没记的一个阶段）**：onsite 之后、offer 之前，recruiter 要 **2 个人：
  1 位前经理 + 1 位 peer**，并且会**主动向他们打听你的负面**。一位通过者原话："They do at least try and pry
  the negatives from your references. Make sure you actually give someone who a) will actually give you a good
  reference and b) **can deflect or decline the ask for a negative**." 他的 reference 用了一句
  "he can push himself too hard/work too hard"，recruiter 就接受了。
  ⚠️ **过了 reference check 仍可能被拒**：同期另一位一手的 Update —— "got rejected after the reference check
  ... Reason stated: **other person is based in Dublin, closer to the engineering team**"。
  **可操作：提前跟你打算写的 reference 对一遍"被问缺点时你会怎么答"。**[Reddit 1seubp5、1sw4eb2（两条独立一手，2026-04）]
- Team match：committee 过但原团队拒会转其他团队；池里 2–6 周；HM 被鼓励共享好候选人。**但存在数月级长尾**：有 L3 London 候选人 onsite 通过后等了 4 个多月仍无 match（"there have been only 2 open roles in the last 3-4 months"），欧洲团队 headcount 紧张时尤甚。
  **2026-09-04 更新：这条已从"单一来源 medium"升级为多源。** 2026-04 London backend 那位到 8 月前后仍在 team match
  （"still In team matching phase 🥲"）；同帖另一位被 recruiter 告知 "**they have paused hiring for the moment.
  No open roles for now**"，并被问是否愿意换地点。**recruiter 主动问你换不换地点 = headcount 出问题的信号。**
  [teamblind stripe-l3-team-match-swe-passed-onsite-2ov4b8tc；Reddit 1srvx7m#36/#38（两条一手）]

## 10. 备考顺序（4 周，Python，校招/L1–L2）

| 周 | 做什么 | 产物 |
|---|---|---|
| 1 | `study/00-prereq` 01–06 + ex01/ex02；电面 ps01–ps04 计时 | 每题 `starter.py` 全绿 |
| 2 | ps05–ps08 + OA 电面高频 q19 q21 q08 q25；bug squash bs01–bs03（先 debugger 走通） | 4 次 45 min 计时记录 |
| 3 | integration int01–int02（serve + 计时）；coding cd01–cd04；bs04–bs05 | 每题 REPORT 里的追问自己口述一遍 |
| 4 | int03–int04；cd05–cd07；6 个故事 STAR-L 双版本；`bq` 每天 5 题；（L2+）sd01–sd04 | 故事表 + 自评 rubric 打分 |

---

## 11. 2026-09-04 Reddit 全量分析：改了什么、没改什么

**做了什么**：把 `catalog/discovery/harvest/` 里 115 帖 / 3188 条评论**全部逐条读完**（分三片、三个代理独立处理），
逐字引用 + URL + 日期落盘在 `catalog/discovery/2026-09-04/reddit_slice*.md`。协调者对最关键的 12 条引文
做了逐字回查，全部对得上原文。

### 改了的（本次动过正文的地方）
| 位置 | 原来写的 | 改成 | 为什么 |
|---|---|---|---|
| §0 总图 | 校招必有 integration、L2/L3 必有 SD | 轮次组合不固定，三条一手反例 | Dublin 校招无 integration；London / India SWE2 无 SD |
| §0 表 | OA 仅 SWE/校招 | 社招也可能有 OA | 8 YOE senior 2026-04 仍收到 |
| §0 表 | 电面 → 结果 1–5 天 | 5 小时 ~ 1 个月以上 | 两端都有一手反例 |
| §0 表 | cooldown 6 / 12 个月并列 | **按 12 个月规划** | 候选人侧 6 条说 12 个月，0 条复现 6 个月 |
| §0 总图 | 无 reference check | 新增该阶段 | 2026-04 两条独立一手 |
| §2 | — | 新增"HM 会回头问你 VO 里没修好的 bug" | 有具体追问链 |
| §3 | 通过线 Python 3/4 | **没有硬线，recruiter 口径互相矛盾** | 4/4 必须 vs 不看 part 数且 2/3 过 |
| §3 | CoderPad | 平台可能就是 HackerRank | 2025-12 官方 information packet 原文 |
| §3 | 电面可以用自己 IDE | 书面允许≠现场允许，有实拒案例 | 2025-10 一手，两天后被拒 |
| §3 | 前 5 min 读完全部 part | 读 **intro + 全部 part**，抄下 intro 里的数字 | 有人因跳过 intro 漏掉滑窗约束而挂 |
| §4 | bug 数 2–3 个 | **按 3 个准备**，校招也是 3 个 | 2025-10 完整可读的一手 |
| §5 | 60 min 时间表 | 实际可能只剩 35 min 写代码 | 装环境 10 + 尾部讨论 10 + 面试官迟到 |
| §5 | 4–5 个 part | part 数不固定（3 / 5 各有一手） | 两条一手 |
| §6 | AI Exercise"一手长文已确认" | **降级为二手 · 商业来源** | 见下 |
| §9 | team match 长尾"单一来源 medium" | 升级为多源 | 两条 Reddit 一手 |
| §4 | bug 数"按 3 个准备"（当天早些时候刚写的） | **1–5 不定** | 补抓拿到 1 个 / 4–5 个两条新一手，**推翻了我们当天的结论** |
| §4 | 库清单无一手来源 | Python `requests`/`mako` 有一手背书 | 直接对上 `bs02` / `bs01` |
| §4 | 挂点 top5 | top6，加"**修复层级选错**" | 面试官明确要求在栈上层修 |
| §4 | "允许用 IDE" | **用不用 debugger 是显式评分项** | 两条一手同向 |
| §4 | 禁 AI | 明确到**含 IDE 自动补全** | 一手 |
| §5 | 只有题库列表 | 加**四段式 sub-round 结构** + "part 1 就拆三个函数" | Dublin senior 一手全文 |
| §3 | 无自动测例 | "**你看不到**测例"≠"没人在判" | 一手：面试官侧有 TC |
| §3 | Lombok 案例像面试官脾气 | **大概率是 HackerRank 平台约束**（标了非一手） | 2024-05 两条同向 + 面试官自陈理由 |
| §6 | AI 轮全部靠二手 | **平台与难度升为一手**；**已进校招 VO**；题面仍无一手 | 两条一手 |
| §0 | loop 单一语言 | onsite 同一门，**电面可不同**；Go 也可选 | 单一来源，已标置信度 |

### ⚠️ 一条我们自己的记账错误（保留在此，不删）
§6 曾把 2026-06-13 那篇 AI Programming Exercise 的帖子标为"**一手长文已确认细节**"。
**它不是一手**：原文第二句就写着 "Sharing what I've gathered from a few candidates"，
发帖号 `/u/interviewdb` 是众包题库网站，23 条评论无一亲历者确认。
细节内容仍保留（与 `cd07` 吻合），但等级已改。
**教训与站点台账那条同源：证据等级要按原文自述判定，不能因为"写得长、写得具体"就当一手。**

### 没改的（明确记录为什么不改）
- **§4 第 ④ 步"用断点不要靠 print"**：有一条一手转述面试官说 print 也行。**但那是口头许可**（§1 已有被事后追责的先例），
  而"只用 print、不会 debugger"是被独立记录过的挂点。**保持原样。**
- **§3 求助 ≥3 次扣分**：一位 Staff offer 拿到者说"卡在 regex 就直接问面试官，省了 3–5 分钟"。
  折中读法（写在这里，不改正文）：**问语法 / API 细节没事，问"这题怎么做"才扣分。**
- **§5 integration 通过线 2/5–3.9/5**：一位 2023 年的 Stripe 员工自述"all parts + 95%"。
  那是通过者的上限样本，不是通过线，**不构成矛盾**。
- **"不是 LeetCode"**：一条 2026-05 匿名评论说 OA 里有 LC hard。单一来源、零细节，**只在 §3 记了一笔，没改结论**。

### 补抓的 33 帖（2026-09-04 当天发现并补齐）
`HANDOFF.md` 原记"盲区期还有 4 篇因 429 没取到"。拿 418 帖 index 与已抓正文做差集后发现
**标题含 stripe 的 83 帖里有 33 帖只有标题、从未取过正文**——原来的 4 是低估（只比对了盲区期）。
33 帖全部补齐（506 条评论），落盘 `catalog/discovery/harvest/reddit_backfill_2026-09-04.json`，
分析见 `catalog/discovery/2026-09-04/reddit_backfill_*.md`。**又是 0 道新题**，但拿到了两条最硬的确证
（bug squash 的库、integration 的四段式结构），以及一条推翻我们当天早些时候结论的证据（bug 数量）。

### 这一轮的题库增量
**新题 0 道。** 三片合计只找到 3 条"库里没有的形态"，且全部是 TITLE/SUMM 级、没有可重建的题面：
① 给现成代码 → 增量加功能 → **面试官主动要求写测试** → 再加更难功能（既不是 bug squash 也不是从零写类）；
② "字符串处理 + transaction-flow/LRU" 混在同一题 4 个 part 里；
③ CSV **以纯字符串给入** → 多个任意查询。
**最值得吸收的是①里那个动作**：写完一个功能**不等提示就主动补测试**——练 `cd0x` 时把它做成肌肉记忆。

反过来，**q17 被一条 2026-04 的一手 OA 复现完整证实**（registry / Haversine 伪码 / "path traversed to find one
with capacity" 三点全中），并附带三条增量：约 20 个测例、**dict + 线性扫描就能 20/20 全过**
（同帖一条高赞的"不写 kd-tree 必挂"被通过者当场证伪）、题主是 Canada senior remote 岗。
`q17` 的 Part 4 `RELEASE` 该候选人未提及，**"reconstructed"标注保持不变**。

### ⭐ 两条最硬的外部确证（补抓批）
1. **bug squash 的库**：一手原文说 Python 场次"could be either **requests** or **mako**"——
   本仓库的 `bs02_mini_http_client` 和 `bs01_mini_template_engine` 正是这两个库的缩微版。
   **这是我们对 bug squash 轮设计的第一次外部确证。**
2. **integration 的四段式**：hello-world 骨架 → 调 API 打印（**参数从文件读**）→ 解析响应再调下一个 API →
   逐段加复杂度，且"requirements change across sub-rounds"。→ §5 已据此加了"part 1 就拆三个函数"的动作。

### 一条方法论结论
r/leetcode 的 Stripe 帖是**求助场**，不是交付场：**五片累计追问具体题面 ≥28 次，零次得到回答**。
一个直接原因被抓到了：给答案的人在引流，AutoMod 因 "DM farming" 删评
（"We do not allow DM farming. All of the conversation must happen within the post itself."），
**剩在公开区的就只有泛泛之谈**。
三片里最有价值的产出全部是**流程事实和挂经**，不是题。
**题面证据的主产地是 1point3acres 镜像与 Blind，后续抓取预算应该往那边倾斜，而不是继续扫 Reddit。**
（r/cscareerquestions 的 2017–2022 存量帖也已挖完，单位信息密度远低于 2025–2026 帖，不必再回去。）
