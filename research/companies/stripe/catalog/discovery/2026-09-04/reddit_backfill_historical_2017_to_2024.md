# out5 — back_old.md 切片分析（14 帖，2017-08-30 → 2024-11-27）

**读取范围**：整个 `back_old.md`，371 行 / 60,274 字符 / 14 帖全部逐条读完（含全部评论）。
**切片性质**：这批是**老帖**。14 帖里有 **6 帖完全没有面试内容**（2024-11-27 实习简历含金量、2024-10-13 Stripe vs Amazon、
2023-05-12 "现在 Stripe 怎么样"、2022-06-10 花钱买 mock、2022-01-12 performance engineer 简历被拒、
以及 2024-01-23 那帖的绝大部分评论）——按 BRIEF 的"无关内容直接跳过"处理，只从里面捞出极少数与流程有关的句子。

**⚠️ 全篇总声明**：本文件里**所有**条目都来自 2017–2024。
凡未在正文里单独标"仍成立/已被 2025–2026 证据复现"的，一律**默认已过时，不要拿去当 2026-09 的行动依据**。

**岗位过滤**：本仓库只关心 SWE backend。本切片里的非 backend 岗位内容一行带过，不展开：
- **ML new grad OA**（2022-02-09, 1 帖）：只确认了"OA 内容按岗位定制"，无题面、无回答。
- **Performance Engineer**（2022-01-12, 1 帖）：简历阶段被拒的吐槽帖，0 条流程事实。
- **Intern / New grad**（2017-08-30、2017-11-12、2018-10-25、2022-10-20、2024-09-06、2024-11-27）：
  这几帖里的**轮次结构和 OA 形态**与 backend 全职有交集，所以下面照收；纯实习待遇/含金量的内容全部丢弃。

---

## A. 题（problems）

> **结论先行：这个切片里没有一道可重建的题。**
> 14 帖里**一次都没有人贴出题面**——连 2017-08-30 那条 37 评论的 "Stripe coding challenge" 帖也没有
> （帖里被追问了 4 次"是什么题 / 有什么建议"，最具体的回答只到"和公司业务有关，不难"）。
> 这与协调者在 `LOOP_GUIDE.md §11` 里下的那条方法论结论完全一致：**r/leetcode / r/cscareerquestions 是求助场，不是交付场。**
> 下面 5 条全部是 **TITLE 级**，其中 A-1 是唯一一条真正有"题型指纹"的。

### A-1 · 2017 校招 OA 题型（TITLE）— **常青，值得记**
- **原文（#20，回答"是 easy/med hackerrank 类型吗"）**：
  > "Not your typical leetcode question. Something relating to what the company does. Fairly easy though."
- **紧接着的确认（#21 / #22）**：
  > "Just one question?"
  > "yes"
- **来源**：https://www.reddit.com/r/cscareerquestions/comments/6x35k8/ · **2017-08-30** · 评论 #20、#21、#22
- **一手/二手**：**一手**（是回答"你做过吗、什么样"的人；但账号未自述岗位，帖子上下文是 Summer 2018 实习校招）
- **轮次**：**OA**（帖子正文："60min hackerrank coding challenge"，campus challenge invitation）
- **对照 inventory**：**未覆盖**（没有任何可对应的题 id——它根本不是一道题，是一句题型描述）
- **信息量**：**TITLE**
- **为什么这条值得留着**：这是本切片里唯一一条能拿去做**跨年份验证**的东西。
  "不是典型 LeetCode / 和公司业务有关 / 一道题 / 60 分钟" 这四点，在 **2017** 就已经成立，
  而 `LOOP_GUIDE §3` 里 2025–2026 的一手证据（"Read in this JSON, transform it"、"Leetcode is useless for Stripe"、
  "no leetcode and strictly no ai"）说的是同一件事。
  **→ 这是"Stripe 的 OA 题型 9 年没变"的最早锚点**，也顺带给 §3 里那条 2026-05 的"OA 里有 LC hard"孤证再添一条反向旁证。

### A-2 · 2017 校招 OA 的判分粒度：15 个测例（TITLE）
- **原文（同一帖 #37）**：
  > "Anyone know if you got 13/15 test cases you will hear anything back?"
- **同期另一帖的一组一手报分**（https://www.reddit.com/r/cscareerquestions/comments/6zqmaz/ · **2017-09-12**）：
  > #2: "Got the rejection today. Had 12/15 cases."
  > #3: "had 15/15 cases, did it about 2 weeks ago, but no response so far."
  > #4: "i just got 13/15, hope it's enough."
  > #7: "Got 15/15- took it the day it was sent, it's been three weeks now and I still haven't heard back. :/ I'll note that though I got 15/15 my code was pretty sloppy so... idk."
- **五年后仍是 15 个**（https://www.reddit.com/r/cscareerquestions/comments/y9d629/ · **2022-10-20** · 帖子正文，一手）：
  > "Just did the Stripe Software Intern OA Hackerrank Assessment. Was hard but I managed to get 13/15 test cases -- Didn't have time to debug the issue for the last 2 test cases."
- **轮次**：**OA**
- **对照 inventory**：**不适用**（不是题，是判分形态）
- **信息量**：**TITLE**
- **判断**：**"OA 有自动测例、按测例数打分"这点从 2017 到 2022 稳定，且大概率仍成立。**
  ⚠️ 但注意**不要**把它推广到电面——`LOOP_GUIDE §3` 明确记录"电面**无自动测例**，自己造输入自己验证"。
  这两条不矛盾，是**两个不同轮次的不同规则**，本切片给 OA 那一侧补了 2017 / 2022 两个时间点。
  另：2017 的 12/15 → 明确被拒（#2），15/15 → 三周无音讯（#7），**样本太小，不足以推出通过线**，只能说"测例数不是唯一变量"。

### A-3 · 2018 校招 onsite 的两道题（TITLE，唯一一条一手 onsite 描述）
- **原文**（https://www.reddit.com/r/cscareerquestions/comments/9rdjpi/ · **2018-10-25** · 评论 #6，**一手**，刚面完 onsite）：
  > "Had a super fun time with the manager interview and thought the more design/data structures-ey question was pretty straightforward. 'watch you code'/trawl through API docs portion was harder for me because I have the attention span of a goldfish and couldn't focus on reading and understanding documentation while also giving running commentary. Ended up not quite finishing the second part of that one and walked out a little bummed, but that was more on me and not on the interview being particularly hard. I think it was the sort of task that would have been fairly straightforward as a take-home assignment."
- **轮次**：一段话里同时描述了 **VO coding（"design/data structures-ey question"）** 和 **integration（"trawl through API docs"）**
- **对照 inventory**：**未覆盖**（无题面，无法对应任何 id）
- **信息量**：**TITLE**
- **价值**：它不给题，但**给了 integration 轮的难点定位，而且这个定位到今天没变**：
  难的不是 API 本身，而是**一边读文档一边出声讲**（"giving running commentary"）。
  这与 `LOOP_GUIDE §5` 的"open-book、可联网查文档"和 §3 的"边写边说"是同一件事的 2018 版。
  也印证了 §5 那条"part 没做完仍可能推进"的形态（他"not quite finishing the second part"）。

### A-4 · 2024 OA / 电面里"要真的调 API"（TITLE，问题不是回答）
- **原文**（https://www.reddit.com/r/cscareerquestions/comments/1cu77pw/ · **2024-05-17** · 帖子正文，**一手，但是"担心"不是"经历"**）：
  > "So for Stripe assessments, it seems that there is the initial OA on hackerrank and then another tech screen with 3 to 4 parts. My concern is that either the OA or tech screen involve calling an API."
  > "I'm having to learn how to use plain Java libraries(httprequest, httpresponse) to call the API. And also even after I get the response I'm used to having the response parsed automatically into a class. I've seen people post trying to use Gson that doesn't work in hackerrank IDE."
- **轮次**：**OA / phone screen**
- **对照 inventory**：**未覆盖**（无题面）
- **信息量**：**TITLE**
- **⚠️ 证据等级**：**帖主自己没面过**，他是在推测（"it seems that"、"My concern is"）。两条回复也都不是亲历者。
  **不要当成"2024 的 OA 一定要调 API"的证据。**
- **仍值得记的原因**：它把 `LOOP_GUIDE §0` 那条 2026 的选语言理由（"there would be rounds which require
  **real API calling, and some json parsing**"）往前推到了 **2024-05**，说明"要真调 HTTP + 解 JSON"不是 2026 新增的。
  以及一条硬约束：**HackerRank IDE 里第三方库（Gson）用不了**（见 B-6）。

### A-5 · 2024-01 Staff 候选人的题型概括（TITLE，**且不能归给 Stripe**）
- **原文**（https://www.reddit.com/r/leetcode/comments/19e2vle/ · **2024-01-23** · 评论 #15，**一手**）：
  > "I can anticipate 80% of the questions I got were Medium. And most of them were in the top 100 chart of LeetCode (not exactly the same, but some variation of it). I did NOT get ask any dynamic programming. I did get asked a lot of array, tree traversal, hash map sort of questions. But again - all on the Medium side."
- **同串 #20（被问"剩下 20% 是 hard 吗"）**：
  > "Yes, but odd enough they were from mid-sized companies. I probably got 2-3 hards. But no hards from the ones listed here!"
- **轮次**：VO coding（跨公司）
- **⚠️ 归属问题（必须标出来）**：这位拿了 **Amazon / Meta / Stripe / Braze 四家 Staff/L6 offer**，
  他这段话是**四家合起来说的**，**没有任何一句把某道题归给 Stripe**。所以：
  - 不能用它论证"Stripe 考 LC medium"；
  - **但 #20 那句"no hards from the ones listed here"里的 "here" 包含 Stripe**，
    所以可以弱推出一条：**这位 Staff 候选人在 Stripe 没遇到 LC hard。**
- **对照 inventory**：**不适用**
- **信息量**：**TITLE**
- **用法**：只作为 `LOOP_GUIDE §3` 里那条 "2026-05 匿名评论说 OA 里有 LC hard" 的**第二条弱反证**，别的什么都别用它证明。

---

## B. 流程与事实（guidelines）

> 按 BRIEF 要求，2017 年的薪资 / 招聘节奏 / 公司规模已全部丢弃。
> 下面只留两类：**(a) 有独立证据表明今天仍成立的**、**(b) 与今天明显不同、因而能说明"什么变了"的**。
> 每条都标了年份和"今天还算不算数"。

### === B-I. 明显仍然成立的 ===

#### B-1 · Bug Squash 轮 **2017 年就存在**（跨 9 年的常青轮次）
- **原文**（https://www.reddit.com/r/cscareerquestions/comments/7ce1bz/ · **2017-11-12** · 帖子正文，**二手**：帖主"saw online"，本人还没面）：
  > "I saw online that for full time the onsite has 4 components: Design, Bug Squash, Refactoring, and Pair Programming (as well as a 'lunch interview')."
- **同帖 #2（有人纠正，语气像已排上 onsite 的人，**一手偏强**）**：
  > "You should've gotten an email about it if you have had your onsite scheduled. There is no Design interview, and lunch interview is just lunch; instead, there is an interview with an engineering manager."
- **今天还算不算数**：**算。** Bug Squash 是 Stripe 最稳定的一轮，2017 → 2026 一直在，
  `LOOP_GUIDE §4` 里 2025-10 Dublin 校招、2026-04 London 都还有。
  **对备考的意义**：`bs01–bs05` 的投入是本仓库里**时效风险最低**的一块，可以放心多花时间。
- **顺带确认（2017 就成立、今天也成立）**：**校招/实习 onsite 没有 System Design 轮**（#2："There is no Design interview"），
  与 `LOOP_GUIDE §7`"校招/实习通常无 SD"一致。

#### B-2 · "recruiter 会发一封 what to expect 邮件" — 2024 年就有
- **原文**（https://www.reddit.com/r/cscareerquestions/comments/1fa2idq/ · **2024-09-06** · 评论 #2）：
  > "The recruiter will send a 'what to expect' email with details."
- **⚠️ 但同帖帖主（一手，new grad）当场否认了在 OA 阶段能拿到**（#3）：
  > "I didn't get that. just an oa invitation"
  > 回复方随即改口（#4）："Oh you're at the oa stage? Sorry, I misread the post."
- **今天还算不算数**：**算，但要注意阶段。** 这正好和 `LOOP_GUIDE §3` 里那份 2025-12 的
  "information packet"（写着 "expect screen sharing and hackerrank... no leetcode and strictly no ai"）对上。
  **可操作结论：那份 packet 是过了 OA 之后才发的，OA 阶段拿不到；别指望在 OA 前收到任何书面说明。**

#### B-3 · "OA 不是 LeetCode 风格"在 2024 已是圈内共识（但当时没人能说清要准备什么）
- **原文**（同 1fa2idq · **2024-09-06** · 帖子正文，**一手**，new grad 收到 OA）：
  > "I've done a lot of research regarding the interview process and the main thing I found was that Stripe doesn't really do leetcode style interviews. So what should I prepare?"
- **同帖 #5（帖主追问，仍无人回答）**：
  > "everything i've seen so far has just said that the OA isn't leetcode like. i'm just confused as to what topics I should prepare if the OA is different"
- **今天还算不算数**：**算。** 与 `LOOP_GUIDE §3` 一致。
- **附带的元信息**：这条帖 8 条评论，**没有一条回答了"该准备什么"**——
  再次印证 §11 那条"Reddit 是求助场"。

#### B-4 · 电面/OA 的 **"3 到 4 个 part"** 结构在 2024-05 已被外部描述
- **原文**（https://www.reddit.com/r/cscareerquestions/comments/1cu77pw/ · **2024-05-17** · 帖子正文）：
  > "it seems that there is the initial OA on hackerrank and then another tech screen with 3 to 4 parts"
- **⚠️ 二手**（帖主自述是从别人的帖子读来的，他本人还没面）。
- **今天还算不算数**：**算，但注意 `LOOP_GUIDE §3` 已把 part 数改成"不固定"**（有 3-part 也有 2-part 的电面）。
  这条只是把"多 part 递进"这个形态的时间下限推到 2024-05，**不改变 §3 现有结论**。

#### B-5 · OA 内容**按岗位定制**（非 backend，一行）
- **原文**（https://www.reddit.com/r/cscareerquestions/comments/so4rna/ · **2022-02-09** · 帖子正文，**一手**，ML new grad）：
  > "the email does say that the challenge is geared towards the position one is applying for"
- **今天还算不算数**：大概率算，但**与 backend 无关**，只说明"别拿 ML/其他岗的 OA 面经当 backend 的参考"。该帖 5 条评论全是 karma bot 和无效追问，**0 信息**。

#### B-6 · HackerRank 环境的硬约束：只能用标准库，第三方库不可用
- **原文**（https://www.reddit.com/r/cscareerquestions/comments/1cu77pw/ · **2024-05-17**）：
  帖子正文：
  > "I've seen people post trying to use Gson that doesn't work in hackerrank IDE."
  评论 #2（**二手但具体，是 HackerRank 通用知识**）：
  > "Hackerrank has always dictated how API calls should be done per language. Usually it is using the standard library, as you have found. If you know the test will be on hackerrank, learn and memorize that library and method. That's all there is to it. A similar oddity existed for JavaScript. Previously, node.js did not have a native fetch method (which is what most js devs use in browser). You had to learn the standard library way to do it instead. That's just how hackerrank wants it done."
- **今天还算不算数**：**算，而且这条现在比 2024 更重要。**
  `LOOP_GUIDE §3` 已经记录了 2025-10 那个 **Java + Lombok + Jackson 被当场禁用、两天后被拒**的案例，
  以及"按裸写、无补全、无外部库准备"的对策。
  **本条是同一结论的 2024 年独立佐证，而且给出了原因：不是面试官挑剔，是 HackerRank 平台本来就只给标准库。**
  → **备考动作（与 §5 现有条目合并即可）**：Python 侧把 `urllib.request` / `json` / `csv` 的裸写练到闭眼，
    **不要依赖 `requests`**（HackerRank 上未必有）。

### === B-II. 与今天不同 → "什么变了"的证据 ===

#### B-7 · 【变迁·大】2017–2018 是**真·onsite**（飞过去、有午餐）；今天是全远程 Zoom
- **2017-11-12 帖子正文**：
  > "...as well as a 'lunch interview'"
- **同帖 #2**：
  > "lunch interview is just lunch"
- **2018-10-25 #6（一手，刚面完）**：
  > "Side note, lunch was so good, holy shit."
- **对比今天**：`LOOP_GUIDE §0` = "Virtual Onsite（Zoom，全远程）"。
- **意义**：**这是本切片里最干净的一条"变了"。** 直接后果是：
  **任何 2019 年以前的 Stripe 面经在"环境/工具"层面全部作废**（白板、现场机器、午餐社交轮），
  只有**题型和轮次名**还能跨年份使用。挑老面经时按这条切。

#### B-8 · 【变迁·大】2017 的 onsite 有 **Refactoring** 和 **Pair Programming** 两个已消失的轮次名
- **原文（2017-11-12 帖子正文，二手）**：
  > "the onsite has 4 components: Design, Bug Squash, Refactoring, and Pair Programming"
- **对比今天**：`LOOP_GUIDE §0` 的 VO 轮次是
  Programming Exercise / Integration / Bug Squash / System Design / HM，**没有 "Refactoring"，也没有 "Pair Programming"**。
- **判断（标明这是推测）**：最可能的解释是**改名而非取消**——
  "Pair Programming" ≈ 今天的 **Programming Exercise**（面试官全程在旁看你写），
  "Refactoring" ≈ 被吸收进 **Bug Squash / Integration**（在既有 repo 上改代码）。
  **但本切片没有任何证据支持这个映射，标为不确定。**
- **可操作的一点**：`LOOP_GUIDE §11` 记过一条"库里没有的形态"——
  *"给现成代码 → 增量加功能 → 面试官主动要求写测试 → 再加更难功能"*。
  **那个形态和 2017 的 "Refactoring" 轮长得很像。**
  如果这是同一条线索的两端，说明"在别人的代码上加东西"是一个**持续存在、但我们题库覆盖薄弱**的形态。
  → **建议**：练 `cd0x` 时刻意加一次"在已有代码上增量改 + 主动补测试"的变体。

#### B-9 · 【变迁·中】2017 的 OA 反作弊靠"劝阻搜索"；今天是 AI 政策 + 抄袭检测
- **原文（2017-08-30 · #4 提问 / #5 回答，二手，是社区通识不是 Stripe 官方）**：
  > #4: "How do these challenges work? Are you allowed to tab out and just google similar to a real world problem? Probably not right?"
  > #5: "generally no (when it comes to Big N / 'elite companies'). they're fine with searching regarding like language syntax / documentation (when they say so), but searching anything directly related to the problem (code, concepts) is very discouraged (they usually say, 'don't do this!!!' in bold text)"
  > #6: "No way to enforce it though.."
- **同帖 #9（这句才是重点）**：
  > "the problem is that you can't look anything up during the whiteboard on-site (it's probably less harder to 'cheat')"
- **对比今天**：`LOOP_GUIDE` 里今天的规则是
  ① OA **必须在 HackerRank 网页里直接写，外部 IDE 复制粘贴可能触发抄袭检测**；
  ② **strictly no ai**，且 bug squash / integration 等轮明确禁 AI；
  ③ integration 轮反而是 **open-book、可联网查文档**。
- **意义**：**规则的方向反过来了。**
  2017 = "白板轮什么都不能查"；2026 = "integration 轮鼓励你查文档，但严禁 AI，且 OA 有抄袭检测"。
  → **别把老面经里"什么都不能查"的心态带进 integration 轮**；那一轮查文档是**预期行为**。

#### B-10 · 【变迁·中，且已在指南里】2017–2018 的 OA→回复是"批量 + 分波次"，以周为单位
- **2017-09-12 #3（一手）**：
  > "had 15/15 cases, did it about 2 weeks ago, but no response so far. i think they are probably batching their responses, as it took a long time to get the challenge after applying anyways."
- **2017-08-30 #26 / #31**：
  > #26: "I applied on the 21st and heard back today, but judging from the replies I'm guessing they're doing it in waves."
  > #31: "According to the comments here, they are sending out the challenges in waves depending on when you applied."
- **2018-10-25（多条一手）**：
  > #1: "Yeah it took 10 days"
  > #2: "Heard back in a week (did HR at the end of September), my onsite is in a couple weeks."
  > #4: "I heard back within ~7-10 days after submitting to schedule a phone interview."
- **今天还算不算数**：**"具体天数"已过时，不要用。**
  `LOOP_GUIDE §0` 现在的口径是"电面 → 结果 **5 小时 ~ 1 个月以上**"。
  **唯一还成立的是那个定性判断：Stripe 的回复是批量的，长时间没消息不代表被拒。**
  这条 2017 的 "batching" 观察，恰好给 §0 那个宽得离谱的时间区间提供了**机制解释**——
  你的回复时间取决于你落在哪一波，不取决于你考得多好。

#### B-11 · 【已过时，仅存档】2018 校招的 headcount / 排期挤压
- **2018-10-25 #9 / #11（一手）**：
  > #9: "I heard back soon after, but they're probably done hiring interns this year. Tried to schedule an onsite and their next available slot was in January, LOL"
  > #11: "Well, my thought was that since they're already so overbooked, they might be slowing down hiring for interns."
- **#3（一手）**：
  > "Just wanna ask where did you apply, because I only saw openings at Dublin, Ireland."
- **今天算不算数**：**不算，这是 2018 的招聘节奏。** 存这条只为一个**结构性**观察：
  **"OA 通过了但排不上 onsite / 只有 Dublin 有坑"这个模式，2018 和 2026 是同一种病**
  （`LOOP_GUIDE §9`：2026 London team match 等 4 个月、recruiter 说 "they have paused hiring for the moment"、
  以及 §0 表里"校招 headcount 受 returning intern 影响，可能面完到 1 月才被告知无 HC"）。
  → **它不是新事实，是"这家公司一直这样"的旁证**，对期望管理有用，对备考没用。

#### B-12 · 【2024，非流程但影响校招判断】Stripe 员工自述：new grad 大部分来自转正实习生
- **原文**（https://www.reddit.com/r/cscareerquestions/comments/1g2miay/ · **2024-10-13** · 评论 #24，**自述 Stripe 员工**）：
  > "I'm biased because I work at Stripe... A good chunk of our interns get return offers once they graduate, which means the bulk of our new grad hires were previous interns."
- **⚠️ 等级**：自称员工、无法验证；且是 2024-10。
- **今天算不算数**：**不确定，倾向仍成立。** 与 §0 表里"校招 headcount 受 returning intern 影响"同向。
  **对 backend 社招无影响**，只影响对校招名额的期望。

#### B-13 · 【2024】定级：Stripe 会拒绝按 Staff 收简历、压到 Senior
- **原文**（https://www.reddit.com/r/leetcode/comments/19e2vle/ · **2024-01-23** · 评论 #106）：
  > "I applied at Stripe and they refused to even accept my application at staff level. Had to be senior."
- **一手**（讲自己的申请）。
- **今天算不算数**：**不确定。** `LOOP_GUIDE §9` 只记了"定级在面试后决定"和"Staff 讲不清业务影响会降级"，
  **没记"申请阶段就被压级"这一步**。这条把压级的时点提前到了**投简历阶段**。
  ⚠️ 单一 2024 来源，未复现，**不建议改 §9 正文**，记一笔即可。
- **同帖对照（#5 → #6，一手，同一人拿到了 Stripe Staff offer）**：
  > "did you ask each company for L6 interviews or did they set your level there?"
  > "For Stripe/Braze I did apply to a specific 'Staff' level position. Amazon/Meta I just applied to SWE and they levelled me according to my EOY and resume."
  → **Stripe 是"按坑位申请、级别在 JD 上"**，不是像 Amazon/Meta 那样先面完再定级。两条互相不矛盾。

### === B-III. 与 LOOP_GUIDE 的矛盾 ===

**矛盾数：0（硬矛盾）。** 逐条核过了，本切片**没有任何一条直接推翻 `LOOP_GUIDE.md` 现有记载的说法**。
最接近"矛盾"的三处，核完都不是矛盾，分别记在这里以免下次重复核：

| # | 看起来像矛盾的地方 | 核完的结论 |
|---|---|---|
| 1 | 2017/2022 说 OA 有 15 个自动测例；§3 说"**无自动测例**" | **不矛盾**。§3 那句讲的是 **Technical Phone Screen**，不是 OA。OA 在 HackerRank 上，有测例；电面在 CoderPad/共享屏幕上，没有。本切片给 OA 侧补了 2017/2022 两个锚点（见 A-2）。 |
| 2 | 2017 onsite 有 "Refactoring"/"Pair Programming"，§0 没有 | **不是矛盾，是变迁**（B-8）。相隔 9 年，轮次改名/合并属正常演化。 |
| 3 | 2018-10-25 #6 说 integration 那轮"没做完第二部分"仍继续走流程 | **不矛盾，是同向佐证**。§5 已记"integration 没做完或 bug squash 差，二选一还能过"。 |

**另有一条"我们记的比切片细"的情况（不算矛盾，但值得注意方向）**：
§3 现在把电面平台记成"CoderPad **或** HackerRank"，本切片 2024-05 那帖（B-4/B-6）默认 **tech screen 也在 HackerRank 上**。
**这与 §3 里 2025-12 information packet 的 "expect screen sharing and hackerrank" 同向**，
说明"电面在 HackerRank 上"不是 2025 才出现的新情况，**2024 年候选人就已经这样预期了**。
→ 建议：**按 HackerRank 裸环境准备电面**（无外部库、无补全），把 CoderPad 当成运气好的情况。

---

## C. 打法与教训（tactics）

> 只收可操作的。这个切片能榨出的可操作条目**只有 5 条**，其中 C-1 / C-2 是真正有价值的（且都跨年份仍成立）。

### C-1 · 【2017，且今天更成立】"不难，但要**逐字读题**"
- **原文**（https://www.reddit.com/r/cscareerquestions/comments/6x35k8/ · **2017-08-30** · 评论 #35，
  回答 "#34: I'm taking it tomorrow. Any advice that hasn't been shared here yet?"）：
  > "don't think it's algorithmically challenging, just make sure to read the problem statement carefully."
- **一手/二手**：**一手**（给出建议者在同串里表现为已做过的人；但未明确自述，标为**偏一手**）
- **今天还算不算数**：**算，而且这是本切片里最该被吸收的一条。**
  它和 `LOOP_GUIDE §3` 里 2026 那条**代价 12 个月 cooldown** 的一手挂经说的是**完全同一件事**：
  > "the sliding window constraints where nowhere mentioned in the actual task (part 1) but rather was **buried in the intro** which i skimmed cause i knew i was gonna be tight on time."
  **→ 2017 有人提醒过、2026 有人因此挂掉。这条"读题"建议穿越了 9 年。**
  §3 现有的对策（"前 5 min 连 intro 一起读，把 intro 里每个数字/时间窗/阈值抄进代码注释再动手"）**不需要改，但可以加权重**。

### C-2 · 【2018】**不要在最后 30 秒重构**（一手挂经，代价具体）
- **原文**（https://www.reddit.com/r/cscareerquestions/comments/9rdjpi/ · **2018-10-25** · 评论 #6，**一手**）：
  > "I've been convinced I've bombed every section of the Stripe interview process thus far (tried to refactor my code in the last thirty seconds of the HackerRank and it stopped compiling. 0/10 would not recommend)."
- **今天还算不算数**：**算。** 平台没变（还是 HackerRank），机制没变（提交的是最后状态）。
- **可操作**：**OA 的最后 2 分钟只做一件事：确认当前代码能编译/能跑，然后停手。**
  想改的东西写成注释，不要动结构。
  ⚠️ 这与 `LOOP_GUIDE §3` 的"最后 5 min 跑全部样例"**是同一个动作的两半**：
  §3 说的是"留时间验证"，这条补的是"**留出来的时间不许用来重构**"。

### C-3 · 【2024】跨 HackerRank 语言选择：为"能不能裸写 HTTP + 解 JSON"而选，别为刷题舒适度而选
- **原文**（https://www.reddit.com/r/cscareerquestions/comments/1cu77pw/ · **2024-05-17** · 评论 #1）：
  > "This is not what you want to hear - but if you need to learn a new library anyway, you'll save much more time just figuring out how to do it with Python. The requests library makes it way simpler than anything Java (even Springboot)."
- **同帖 #2**：
  > "If you know the test will be on hackerrank, learn and memorize that library and method. That's all there is to it."
- **⚠️ 等级**：两条都是**二手/通用建议**，不是 Stripe 亲历者。
- **今天还算不算数**：**算，且与 `LOOP_GUIDE §0` 的 2026 结论完全一致**
  （"按'哪门语言你真写过 HTTP 调用和 JSON 解析'来选，不按刷题语言选"）。
  本条把这个论证从 2026 往前推到 2024-05，说明它不是一时现象。
  ⚠️ **一个技术上的分歧**：#1 推荐 `requests`，但 #2 和帖主正文都指出 **HackerRank 只给标准库**。
  **以 #2 为准：练 `urllib.request` 而不是 `requests`**（见 B-6）。

### C-4 · 【2018】"边读文档边出声讲"要专门练
- **原文**（2018-10-25 #6，**一手**，同 A-3）：
  > "'watch you code'/trawl through API docs portion was harder for me because I have the attention span of a goldfish and couldn't focus on reading and understanding documentation while also giving running commentary."
- **可操作**：练 `int01–int04` 时，**至少有一次全程开口录音**——
  专门练"读一段没见过的 API 文档 + 同时讲我在找什么"。
  这是一个**双任务负载**问题，不是知识问题，只能靠练。
- **今天还算不算数**：**算**（§5 的 integration 轮形态未变，仍是 open-book 读文档）。

### C-5 · 【2024，一行，非 Stripe 特异】付费 mock 的价格与替代
- **原文**（https://www.reddit.com/r/leetcode/comments/19e2vle/ · **2024-01-23** · 评论 #94，**一手**）：
  > "~$200 per session. I got some deals and got some for 50% off... If you don't have the money, interviewing.io offers free peer to peer practises with other people that are also interviewing. You don't get as much of a nice feedback, but the most important part here IMO is training solving a coding question w/ someone staring at you. Cannot emphasize how much you need to practise this."
- **为什么只给一行**：与 Stripe 无关，是通用建议。**唯一可操作的内核**是最后半句——
  "练的是有人盯着你写代码"这件事本身。本仓库的 `loop/mock.py` 已经覆盖计时，**但覆盖不了"被人看着"**。

### C-6 · 明确**不收**的内容（记在这里，避免下次重复挖）
- 2024-01-23 那帖 110 条评论里的 L6/Staff 系统设计与行为面建议（#6、#54、#65）：
  **不是 Stripe 特异的**，是跨四家公司的通用 staff 级建议，且与本仓库目标级别（backend，L1–L2 向）不匹配。
  ——唯一擦边的一条是 #64/#65 关于 "product design interview" 的问答，
  **但无法确定他说的是哪家公司的哪一轮**，标为不可用。
- 2022-06-10 整帖（29 评论）：一位 20 YOE 候选人连挂 8 家 final round 的求助帖，
  **通篇没有一条 Stripe 的具体信息**；唯一沾边的 #4 "I spent no time preparing for my stripe interviews and got an offer.
  Their interview process is pretty fun." 被追问后**没有回答**（#5 问了，无下文）。**0 可用信息。**
- 2023-05-12 整帖（3 评论）、2024-11-27 整帖（7 评论）、2024-10-13 整帖（68 评论）：
  分别是"现在 Stripe 怎么样""实习含金量""Stripe vs Amazon"，
  **除 B-12 那一句员工自述外，全部是 prestige/comp 讨论**，按 BRIEF 跳过。
- 2022-01-12 整帖（8 评论）：Performance Engineer 简历被拒，非 backend SWE，且无流程事实。

---

## 附：本切片的元结论（给协调者）

1. **老帖的题面价值 ≈ 0，但"轮次名"的价值很高。**
   14 帖 0 道可重建的题；却拿到了 **2017 年的完整 onsite 轮次表**（B-1、B-8），
   这是判断"哪些轮次是常青的、哪些是新加的"的最早基线。
   **Bug Squash 跨 9 年不变 → `bs01–bs05` 是仓库里时效风险最低的投入。**

2. **本切片对现有 `LOOP_GUIDE` 的唯一"改动级"建议**：
   在 §3 或 §5 的"备考动作"里把 **"HackerRank 只有标准库，别依赖第三方库"** 写死
   （现在只以"2025-10 Lombok/Jackson 被禁"这个个案形式存在，读起来像面试官个人偏好；
   B-6 表明它是**平台约束**，因而适用于所有语言、所有场次）。

3. **一条负面情报（省预算用）**：`r/cscareerquestions` 的 **2017–2022 存量帖已经挖完了，别再回去挖。**
   这 14 帖合计 ~300 条评论，产出 5 条 TITLE 级"题" + 13 条流程事实 + 5 条打法，
   **单位信息密度远低于 2025–2026 的帖**。§11 那条"预算往 1point3acres 镜像与 Blind 倾斜"的结论，本切片再次支持。
