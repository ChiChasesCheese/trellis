# out3.md — slice3 + slice4 榨取结果

产出者备注（先看这条）：
- **slice3 实际 20 帖，标题清单与任务描述不完全一致**。任务里点名的 "Stripe OA (Backend)"、
  "Just landed offers at Stripe and DoorDash (Staff)! AMA" **在 slice3 和 slice4 里都不存在**
  （我 `grep '^### '` 过两个文件的全部帖头）。这两帖若存在，应在 slice1/slice2。
  slice3 里确实存在的是："Stripe's New AI Programming Exercise Interview"、"Stripe intern interview experience"、
  "Stripe HackerRank Online Assesment"、"Stripe API integration Round"、"Stripe Interview"(London backend)、
  "Stripe interview feedback"(phone screen)、"Stripe Reference check" 等。
- slice4 共 45 帖全部过了一遍。**Stripe 相关的实质内容只有 5 处**，其余是市场吐槽 / referral 求助 /
  简历诊断 / 把 Stripe 当作"我用了 Stripe 支付 SDK"的技术栈罗列，按 BRIEF 直接跳过。

---

# 第一部分：slice3（2026-04 → 2026-08，20 帖）

## A. 题（problems）

### A3-1 · 实习 OA（45 或 60 min，1 题 4 part）— 字符串 + 交易流/LRU 设计
- **逐字引用**（帖子正文）：
  > "Online Assessment  Duration: 45 minutes Format: 1 question with 4 parts The question was very lengthy,
  > but definitely doable if you managed your time well. It was mostly string manipulation mixed with a
  > transaction-flow/LRU cache style design, where you had to implement 3–4 functions. Out of 19 test cases,
  > I passed 15."
- **同帖 OP 自己更正时长**（评论 27）：
  > "the time was 60 minutes for each round including oa,sorry I was actually confused, didn't remember at time of posting"
- 来源：https://www.reddit.com/r/leetcode/comments/1uz688l/ · 2026-07-17 · **帖子正文**（时长更正在**评论 27**）
- 轮次：**OA**（off-campus SDE Intern，Bengaluru；2025-08~09 投递，2025-10 收到 OA）
- 一手/二手：**一手**
- 对照 inventory：**疑似覆盖**。最接近 `q26_account_scheduler_lru` / `cd03_account_scheduler_lru`（LRU 自动选择）
  与 `q10_payment_intent_commands`（交易状态机）。差在：本题把"字符串处理"和"transaction-flow/LRU"**混在同一题的 4 个 part 里**，
  库里这两条线是分开的两道题；且"implement 3–4 functions"的类 API 形态更接近 cd03。**未覆盖的是这种"字符串 + LRU 混合"的组合形态。**
- 信息量：**SUMM**（有主题、part 数、函数数、测例数，但没有具体规则）

### A3-2 · VO 编码 Round 1（45 min，4 part）— CSV 字符串解析 + 多查询
- **逐字引用**：
  > "Round 1 (Coding – 45 mins) A Senior SDE took the interview. The problem involved parsing a CSV file
  > provided as a string. After parsing it correctly, you had to answer multiple queries based on the data.
  > Again, it had 4 parts.  I completed the first 2 parts successfully. I explained my approach for the 3rd part,
  > but time ran out before I could code it."
- 来源：https://www.reddit.com/r/leetcode/comments/1uz688l/ · 2026-07-17 · **帖子正文**
- 轮次：**VO coding**（实习 loop 的第一轮独立 45 min 编码）
- 一手/二手：**一手**
- 对照 inventory：**疑似覆盖**。最接近 `ps12_hierarchical_task_csv`（CSV 层级任务）、`q15_kyc_verification`（渐进式 CSV 校验）、
  `q14_join_dataset`、`q20_transaction_fees_reconciliation`。差在：本题强调 **"CSV 以字符串形式给你"**（自己切分，不给 DictReader 的现成文件）
  **+ 之后是"多个查询"**（query API 而非一次性报表）。库里"字符串形式的 CSV → 多查询"这条最接近 ps12，但 ps12 是层级结构而非任意查询。
- 信息量：**SUMM**
- ※ 这条正是 `LOOP_GUIDE.md` §0 里已记录的"2026-07 一手实习面经 R1"的**原始出处**，本次拿到全文，与已记录内容一致。

### A3-3 · VO 编码 Round 2（45 min）— 图 + 字符串，"类似 Splitwise"
- **逐字引用**：
  > "Round 2 (Coding – 45 mins) This question felt like a combination of graphs + strings, somewhat similar to
  > the logic behind a Splitwise application. It also had multiple parts.  I solved the first part but made a few
  > debugging mistakes. I ended up spending too much time fixing them, so I couldn't move to the later parts
  > before the interview ended."
- 来源：https://www.reddit.com/r/leetcode/comments/1uz688l/ · 2026-07-17 · **帖子正文**
- 轮次：**VO coding**（第二轮独立 45 min）
- 一手/二手：**一手**
- 对照 inventory：**已覆盖**。`q32_money_transfer_rebalancing` + `qA08_lc465_optimal_account_balancing`（债务最小化 / 最少转账笔数）。
  "图 + 字符串"的字符串部分不明（可能是人名/账户名解析），**不足以判断**是否还有额外的解析 part。
- 信息量：**SUMM**
- ※ 同为 `LOOP_GUIDE.md` §0 已记录条目的原始出处，一致。

### A3-4 · AI Programming Exercise — transactions + rules
- **逐字引用**（正文，节选原句）：
  > "The interview runs in HackerRank, but it's not the standard coding setup. There's a built-in AI chat window
  > (kind of like a lightweight Cursor) that you can talk to. ... You're given a list of transactions and a list of rules.
  > Each rule says whether to accept or block a transaction, followed by an if condition. You need to parse the rules
  > and decide whether a transaction matches the condition. The problem consists of multiple parts. It starts pretty
  > straightforward (mostly keyword/string matching), but later parts get trickier with boolean logic (AND/OR) and
  > build on previous sections. There's a detailed README, so reading and understanding the spec quickly is a big part
  > of it. The actual coding portion is apparently only around 30 minutes"
- 来源：https://www.reddit.com/r/leetcode/comments/1u51q4w/ · 2026-06-13 · **帖子正文**
- 轮次：**AI Programming Exercise**（onsite loop 新增轮）
- 一手/二手：**⚠️ 二手（重要更正）**。原文开篇是
  > "Sharing what I've gathered from a few candidates who went through it recently"
  发帖人 `/u/interviewdb` 是题库网站运营方（评论 1 直接质疑："Hey, let me guess, you sell something on your website
  like a question-bank of sorts, for this?"）。**`LOOP_GUIDE.md` §6 把这条标为"2026-06-13 一手长文已确认细节"，
  这是错的——它是二手汇总 + 商业来源。** 见 B 节 B3-14。
- 对照 inventory：**已覆盖**。`cd07_transactions_rules_ai` 高度吻合（关键词匹配 → AND/OR/NOT）。
- 信息量：**FULL**（够重建），但**证据等级需从"一手"降为"二手/商业来源"**。

### A3-5 · Technical Phone Screen — 题面里藏了滑动窗口约束
- **逐字引用**（评论 2，另一位做过同一题的候选人）：
  > "I also took it and the question was so hard to read. The sliding window constraints where no where mentioned
  > in the actual task (part 1) but rather was buried in the intro which i skimmed cause i knew i was gonna be tight
  > on time. This led me to make wrong assumptions and i wasted so much time. Now I'm blocked for 12 months wtf"
- 帖子正文（另一位，2/4 part）：
  > "I just completed my stripe phone screen round. The round was really exhausting. I took around 30-35 minutes to
  > solve Part A. Then I consumed the remaining 10 minutes to solve Part B.  Unfortunately, I only able to solve
  > 2/4 parts in the interview."
- 来源：https://www.reddit.com/r/leetcode/comments/1u0hnbq/ · 2026-06-08 · 正文 + **评论 2**
- 轮次：**Technical Phone Screen**
- 一手/二手：**两条都是一手**（两位不同候选人做了同一题，交叉印证）
- 对照 inventory：**疑似覆盖**，但**不足以判断**是哪道。只知道"part 1 就要用滑动窗口，且窗口约束写在题面 intro 里"。
  最接近 `ps01_transaction_stream_levels`（60s 滑窗）、`cd06_suspicious_users_window`、`qA05_lc1604_keycard_alerts`、`q23_rate_limiter`。
- 信息量：**TITLE**（只知道"滑动窗口 + 4 part + 题面 intro 藏约束"）

### A3-6 · Integration 轮 — 解析 JSON + 调 API，5 个 part
- **逐字引用**（London backend 候选人，评论 27 与 29）：
  > "We need to parse some Json's & hit some API's"
  > "Depends on question to question. But the one i got had 5 parts"
- 来源：https://www.reddit.com/r/leetcode/comments/1srvx7m/ · 2026-04-21 · **评论 27 / 评论 29**
- 轮次：**Integration**
- 一手/二手：**一手**
- 对照 inventory：**疑似覆盖**。`int03_multi_json_etl`（多份异构 JSON）+ `int02_payments_reconciliation`（分页/重试/幂等）。
  差在：这条只说"parse JSON + hit API"，**没说是不是对账、分页、幂等**，不足以对上具体某道。
- 信息量：**TITLE**

### A3-7 · Bug Squash 轮 — 私有 repo + 多个失败单测
- **逐字引用**（同上 London backend，评论 14 与 19）：
  > "For the BugSquash round, they give you a GitHub repository. You download and clone it locally, then build the
  > project. When you compile and run it, there will be some unit test failures. You then start debugging those failures
  > one by one, just like the interviewer guides you. You can use a debugger, print statements, or any approach you
  > prefer. Repository would be in the language which you have chosen for all interviews!"
  > "A repo will be given , with some failing UT's . You need to fix those UT's by debugging the flow."
  repo 是否公开（评论 15/16）：
  > "is that github repository is public ?" → "Nope!"
- 来源：https://www.reddit.com/r/leetcode/comments/1srvx7m/ · 2026-04-21 · **评论 14 / 15 / 16 / 19**
- 轮次：**Bug Squash**
- 一手/二手：**一手**
- 对照 inventory：**未覆盖（无具体 bug 内容）**——只有流程，没说是哪个库、什么 bug。
  流程本身与 `bs01`–`bs05` 的演练形态一致。
- 信息量：**TITLE**（流程 SUMM，题目 0）
- ⚠️ 与 `LOOP_GUIDE.md` §4 有摩擦：**"You can use a debugger, print statements, or any approach you prefer"**
  vs 指南写的"④ 用**断点**验证，不要靠 print"与挂点"① 只用 print、不会 debugger"。详见 B3-6。

### A3-8 · Mobile Industry Screen OA（60 min，3 个 requirement，14 个测例）—— **非本岗位**
- 逐字引用（正文 Update）：
  > "It was similar to any coding challenge but had some story and meaning behind what was expected to do.
  > There were 3 requirements, satisfying each requirement passed a set of predefined test cases. I was able to solve
  > 11/14 test cases (1 TC failed for 2nd requirement and 2 TC failed for 3rd requirement). Passed the round"
- 来源：https://www.reddit.com/r/leetcode/comments/1td6t5k/ · 2026-05-14 · 正文
- 岗位：**Stripe Mobile**（非 backend）。题目内容拒答（"Sry can't share, signed NDA."）。
- **存在但非本岗位**，只留一行。但**OA 有预置测例、按 requirement 分组**这一点对 backend OA 也适用，见 B3-9。

### A3-9 · PhD Machine Learning Engineer (New Grad) HackerRank OA — **非本岗位**
- 90 min，4 段：ML/概率/统计 5 道选择 + 1 道 LC 风格 DSA（easy/medium）+ pandas/ETL（"felt more like solving a
  complex SQL aggregation problem"）+ CV/DL 任务（ResNet18 + BCE + AdamW + 产出预测 CSV）。
- 来源：https://www.reddit.com/r/leetcode/comments/1t5gh52/ · 2026-05-06 · 正文 · 一手 · 结果 not selected。
- **存在但非本岗位（MLE），不展开。** 唯一可迁移的一点：Stripe 的 OA 在非 SWE 岗也是"工程重于理论"
  （"the assessment felt much more engineering-heavy than pure ML theory"）。

### A3-10 · Front-end phone screen 提问帖 — **非本岗位**，无信息（唯一评论是 bot 过滤）。
  https://www.reddit.com/r/leetcode/comments/1tcabgi/ · 2026-05-13

---

## B. 流程与事实（guidelines）

### B3-1 · London backend 的完整轮次表：**两轮 Programming，且没有 System Design**
- 逐字引用（评论 6）：
  > "Yes they, do. Rounds:  Phone Screen Programming Programming Round  Integration Bug Squash Round Hiring Manager"
- 来源：https://www.reddit.com/r/leetcode/comments/1srvx7m/ · 2026-04-21 · **评论 6** · 一手（London, Backend developer）
- ⚠️ **与 `LOOP_GUIDE.md` §0 的对照**：指南写 L2/L3 社招 = "Programming + Bug Squash + Integration + System Design + HM/Behavioral"。
  这位候选人的 loop **有两轮 Programming、没有 System Design**。评论 34 有人追问
  > "OP how much experience do you have? Did you not have any system design round?"
  **OP 没有回答**，所以 YOE/level 未知，**无法判断是不是因为 level 低才没有 SD**。
  **记为"与指南部分矛盾，但归因不明"。**

### B3-2 · 面试轮次的排期由候选人控制，不赶时间
- 逐字引用（评论 8）：
  > "Yes its a live interview! Once you clear the phone screen, only then rest of them are scheduled  Also, it's upto you,
  > how do you want to get them scheduled 🙂"
- （评论 23，回应"他们赶不赶"）：
  > "What do you mean by space the process? As in ask time for preparation?  No they weren't in rush."
- 来源：同上 · 2026-04-21 · **评论 8 / 23** · 一手

### B3-3 · AI 政策：禁 AI，但可以随便 Google
- 逐字引用（评论 12，回应"Do u have AI assistant in your Programming round?"）：
  > "No AI is allowed, you can google anything."
- 来源：同上 · 2026-04-21 · **评论 12** · 一手
- 与 `LOOP_GUIDE.md` §4/§5 **一致**（除 AI Programming Exercise 外禁 AI；integration 可联网查文档）。
  **新增点**：这条把"可 Google"扩展到 **Programming 轮**，指南原本只在 integration 轮写了"可联网查文档"。

### B3-4 · 所有轮次用**同一种语言**，repo 也是那种语言
- 逐字引用（评论 14 结尾）：
  > "Repository would be in the language which you have chosen for all interviews!"
- 来源：同上 · 2026-04-21 · **评论 14** · 一手
- 与 `LOOP_GUIDE.md` §4"库按语言分流"一致，并**明确了"语言是你在 loop 开始时一次性选定的"**。

### B3-5 · 语言建议：C++ 刷题 + JS 开发的人应该选 JS
- 逐字引用（评论 40 提问 / 评论 41 OP 回答）：
  > "Hi bro.I do dsa in c++ and development in Javascript.But stripe only allows one language.What do you suggest bro?"
  > "I'll suggest JS in that case, because there would be rounds, which require real API calling, and some json parsing.
  > And you wouldn't have done any of this in c++"
- 来源：同上 · 2026-04-21 · **评论 40/41** · 一手（OP 亲历后给的建议）
- 与 `LOOP_GUIDE.md` "语言结论：Python/JS" **一致**，且给出了理由（真实 API 调用 + JSON 解析）。
- **另注**："stripe only allows one language" —— 候选人的理解是**整个 loop 只能用一种语言**，不能这轮 C++ 那轮 JS。
  实习帖评论 30 也在问同一件事（"can we use c++ for first round and MERN stack for remaining"），**无人回答**。

### B3-6 · ⚠️ 与指南矛盾：Bug Squash 里 print 也行
- 逐字引用（评论 14）：
  > "You can use a debugger, print statements, or any approach you prefer."
- 来源：https://www.reddit.com/r/leetcode/comments/1srvx7m/ · 2026-04-21 · **评论 14** · 一手
- ⚠️ **矛盾**：`LOOP_GUIDE.md` §4 的 5 步硬流程写 "④ 用**断点**验证，不要靠 print"，挂点 top5 第一条是"只用 print、不会 debugger"。
  这位一手候选人转述的是**面试官的口头许可**。
  **判读建议（我的判断，非引文）**：这与 `LOOP_GUIDE.md` §1 已记录的"面试官口头允许的事被 recruiter 事后标 red flag"是同一类风险。
  按指南（用 debugger）准备仍是更安全的选择；但"用 print 会当场被打断"这一点**没有证据**。

### B3-7 · Bug Squash 是**多个**失败单测，逐个修
- 逐字引用：
  > "there will be some unit test failures. You then start debugging those failures one by one"
- 来源：同上 · 2026-04-21 · **评论 14** · 一手
- 与 `LOOP_GUIDE.md` §4"按 2–3 个准备"**方向一致**（复数），但**没给出确切数字**。

### B3-8 · ⚠️⚠️ 电面通过线：两位 recruiter 的说法**直接互相矛盾**
- 说法 A（正文，recruiter 面试前明确告知）：
  > "The recruiter explicitly mentioned before the interview that you need to solve 4/4 parts to proceed forward
  > to the interview loop."
- 说法 B（**评论 12**，另一位候选人，2/3 part **过了**，且拿到了面试官写的原始反馈）：
  > "It really depends on how you performed during the interview. The recruiter told me that it doesn't depend on how
  > many parts you solve. They are just assessing your technical and communication skills. I solved 2/3 parts in the
  > given time and passed the round, and later during the next call, the recruiter shared the exact feedback the
  > interviewer had written. PS: I got a callback from the recruiter more than 1 month later"
- 来源：https://www.reddit.com/r/leetcode/comments/1u0hnbq/ · 2026-06-08 · 正文 + **评论 12** · 两条都是一手
- ⚠️ **与 `LOOP_GUIDE.md` §3 的矛盾**：指南写"通过线：Python 3/4、Java/C++ 2/4"。
  - 说法 A（4/4）**比指南严**；
  - 说法 B（2/3 过 + "不看 part 数"）**比指南松**。
  三条互不相容。**结论：所谓"通过线"很可能不是硬线，且 recruiter 的口径不统一。**
  注意说法 B 的 part 总数是 **3**（不是 4），说明 part 数本身也不固定。
- **附带的第二个矛盾**：说法 B "I got a callback from the recruiter more than 1 month later"
  ⚠️ vs `LOOP_GUIDE.md` 数字表"电面 → 结果 1–5 天"。**1 个月以上**是明确的反例。

### B3-9 · ⚠️ Cooldown：电面挂 → 被封 **12 个月**
- 逐字引用（评论 2 结尾）：
  > "Now I'm blocked for 12 months wtf"
- 来源：https://www.reddit.com/r/leetcode/comments/1u0hnbq/ · 2026-06-08 · **评论 2** · 一手
- ⚠️ **与 `LOOP_GUIDE.md` 数字表矛盾**：指南写"Cooldown：6 个月（**早期轮被拒**，Stripe 员工）/ 12 个月（推荐）"。
  这位是**电面（早期轮）被拒，拿到 12 个月**。属早期轮 = 6 个月的反例。
  （不确定点：他没说 12 个月是 recruiter 邮件写的还是他自己从系统里看到的。）

### B3-10 · OA 有预置测例、按 requirement 分组通过；不强制视频监考，但会抓拍照片
- 逐字引用（Mobile OA，正文 Update）：
  > "There were 3 requirements, satisfying each requirement passed a set of predefined test cases."
- 逐字引用（实习帖，评论 25 提问 / 评论 26 OP 回答）：
  > "Does Stripe OA require video monitoring?"
  > "not for oa,they once take your photo and can take in between"
- 来源：https://www.reddit.com/r/leetcode/comments/1td6t5k/（2026-05-14，Mobile）；
  https://www.reddit.com/r/leetcode/comments/1uz688l/（2026-07-17，intern SWE，**评论 26**）· 均一手
- **与 `LOOP_GUIDE.md` 的关系**：指南 §3 说的"无自动测例"是**电面**的性质；OA（HackerRank）**是有测例的**，两者不冲突。
  但本仓库如果在别处把"没有自动测例"写成了全局结论，需要按轮次限定。
  **新增事实**：OA 会拍照（可能中途抓拍），但不是全程录像。

### B3-11 · **Reference check 是一个独立阶段**（指南完全没记）
- 逐字引用 1（2026-04-07，backend）：
  > "I have completed all the rounds with stripe for backend engineering. Today the HR reached out asking for
  > professional references before the next steps."
- 逐字引用 2（2026-04-26 正文）：
  > "I recently went through Stripe's onsite interviews process and got call from recruiter asking for 2 references -
  > one of them should be an ex- manager and another a peer."
- 逐字引用 3（评论 1，已通过该阶段者）：
  > "Yes, and I passed it as well. They do at least try and pry the negatives from your references. Make sure you actually
  > give someone you think will a) actually give you a good reference and b) can deflect or decline the ask for a negative.
  > Mine gave some generic "he can push himself too hard/work too hard" line and the recruiter was fine with it.
  > Unsure of the level you interviewed for but this also means you got at least Senior (L3) or higher."
- 来源：https://www.reddit.com/r/leetcode/comments/1seubp5/ · 2026-04-07 · 正文 · 一手
  https://www.reddit.com/r/cscareerquestions/comments/1sw4eb2/ · 2026-04-26 · 正文 + **评论 1** · 均一手
- **新增（`LOOP_GUIDE.md` 无此阶段）**：onsite 之后、offer 之前有 **reference check**，要 2 个人（1 前经理 + 1 peer），
  recruiter 会**主动挖负面**。评论 1 的"至少 L3 才做 reference check"是**该评论者的推测，未经证实**。
- ⚠️ **过了 reference check 仍被拒的实录**（同帖，**评论 4**，OP 自己的 Update）：
  > "Update: got rejected after the reference check - doesn't make any sense! Reason stated: other person is based in
  > Dublin, closer to the engineering team. Why even do a reference check when you're not going to make an offer.
  > Now at least 3 people know that Im laid off and looking for a job, and that Stripe also rejected me."
  → 与 `LOOP_GUIDE.md` §9 "team match 可能撤回"同类，但**发生在 reference check 之后**，且拒因是**地点**（Dublin 更近工程团队）。

### B3-12 · Team match 的欧洲长尾 + **招聘暂停**
- 逐字引用（London backend OP，2026-04-21 帖，评论 36；到 2026 年 8 月前后仍在 team match）：
  > "Hey! Nope still In team matching phase 🥲. I feel, my patience is getting tested that's it!"
- 逐字引用（同帖**评论 38**，另一位处境相同者）：
  > "Hey OP! I am in the same position. My recruiter informed me earlier this week that they have paused hiring for the
  > moment. No open roles for now. They asked me if I was interested in any other location and they could check with
  > some recruiters internally."
- 来源：https://www.reddit.com/r/leetcode/comments/1srvx7m/ · 2026-04-21 · **评论 36 / 38** · 均一手
- 与 `LOOP_GUIDE.md` §9 "L3 London onsite 通过后等 4 个多月无 match" **一致并加强**（原为单一 medium 来源，现有两条 Reddit 一手佐证），
  且新增"**recruiter 会问你要不要换地点**"这一具体动作。

### B3-13 · HR 会提前发一份 prep 文档
- 逐字引用：
  > "Before the interviews, HR had shared a preparation document that outlined the interview process and expectations.
  > If your recruiter shares something similar, it's definitely worth reading carefully."
- 来源：https://www.reddit.com/r/leetcode/comments/1uz688l/ · 2026-07-17 · **帖子正文** · 一手
- 与 `LOOP_GUIDE.md` §1 "一切以书面 prep 材料为准" **一致**。

### B3-14 · ⚠️ 证据等级更正：AI Programming Exercise 那篇是**二手 + 商业来源**
- 逐字引用（正文第 2 句）：
  > "Sharing what I've gathered from a few candidates who went through it recently:"
- 逐字引用（评论 1，质疑发帖动机）：
  > "Hey, let me guess, you sell something on your website like a question-bank of sorts, for this?"
- 逐字引用（评论 17，说明**当时无人出面确认**）：
  > "Has anyone actually gone through this and want to share what that looks like?"
- 来源：https://www.reddit.com/r/leetcode/comments/1u51q4w/ · 2026-06-13 · 正文 + **评论 1 / 17**
- ⚠️ **与 `LOOP_GUIDE.md` §6 矛盾**：指南写"**2026-06-13 一手长文已确认细节**（r/leetcode，正文 1989 字 + 23 评论）"。
  实际是**二手汇总**，且发帖账号 `/u/interviewdb` 自称做 crowdsourced interview question bank（评论 2 的自我调侃印证）。
  23 条评论里**没有任何一条是亲历者确认**（评论 4/5/16 是泛泛讨论；评论 12/14/15/21/23 是 "vibelevel ai" 广告刷屏）。
  **建议：把该条从"一手已确认"降级为"二手 · 商业来源 · 未经亲历者交叉验证"。** 结论内容本身可能仍然对，但证据等级要改。

### B3-15 · Integration 轮 part 数不固定：有人 5 part，有人 3 part
- 逐字引用（2026-04-21，London，一手）：
  > "Depends on question to question. But the one i got had 5 parts"
- 逐字引用（2026-08-26，正文，**二手**：为朋友代问，Dublin 4YOE）：
  > "For API integration Round - He completed 2/3 parts, explained the approach for the 3rd but ran out of time.
  > Is this a dealbreaker, or is partial completion normal for this round? Exp:4YOE"
  地点/YOE 在**评论 2**：
  > "Dublin, 4YOE"
- 来源：https://www.reddit.com/r/leetcode/comments/1srvx7m/ · 2026-04-21 · 评论 29 · 一手；
  https://www.reddit.com/r/leetcode/comments/1vyzxek/ · 2026-08-26 · 正文 + 评论 2 · **二手**
- 与 `LOOP_GUIDE.md` §5 "4–5 个递进 part" **部分矛盾**：Dublin 那位只有 **3 个 part**。
  该帖**无人回答结果**，所以"2/3 算不算过"仍未知。

### B3-16 · 电面时长有 45 min 和 60 min 两种说法
- 逐字引用（2026-05-23，同一位 Mobile OA 通过者）：
  > "I had a recent call with HR of STRIPE and she told me I have to clear one technical zoom call interview (45 mins),
  > and then we can move to the final set of rounds."
- 来源：https://www.reddit.com/r/leetcode/comments/1tljdkm/ · 2026-05-23 · 正文 · 一手（Mobile 岗）
- `LOOP_GUIDE.md` §3 写"60 min = 45 编码 + 15 Q&A"。这条说 recruiter 报的是 **45 min**。
  **不确定**：可能 recruiter 只报了编码部分，也可能 Mobile 岗与 SWE backend 不同。**不足以判定为矛盾。**

### B3-17 · 面试官提前 20 分钟结束（结果未知）
- 逐字引用（正文 + 评论 4）：
  > "After studying my ass for 2 months, i was only able to solve 2 parts in technical screen. Time ran out"
  > "Umm, he ended the interview early like 20 mins early, I wasn't that bad or stuck on something"
- 来源：https://www.reddit.com/r/leetcode/comments/1tdx8aw/ · 2026-05-15 · 正文 + **评论 4** · 一手
- 记录为信号：**电面被提前结束**在 2026 年仍有发生（`LOOP_GUIDE.md` §3 已记"面试官常在 part 2 后停下转 Q&A"，与此一致）。

### B3-18 · 语言分布：Go 和 Java 也是可选项
- 两个求助帖分别是 **Go/Golang**（2026-04-18，Bangalore fintech，https://www.reddit.com/r/leetcode/comments/1sowsae/）
  和 **Java + SpringBoot**（2026-05-07 https://www.reddit.com/r/leetcode/comments/1t6j9gy/ ；
  2026-05-26 https://www.reddit.com/r/leetcode/comments/1toj7bp/ ，3YOE，OA 已过）。
  逐字引用（2026-05-26）：
  > "Tech stack I'll be using for interview: Coding - Java Backend Framework - SpringBoot (if required)"
- **两个帖子都没人给出实质回答**（评论全是 bot 删帖 / "how did it go?"）。只作为"Go/Java 是被允许的选项"的证据。

---

## C. 打法与教训（tactics）

### C3-1 · ⚠️ 读题：约束会藏在 intro 里，跳过 intro 会写错方向（最高价值一条）
> "The sliding window constraints where no where mentioned in the actual task (part 1) but rather was buried in the
> intro which i skimmed cause i knew i was gonna be tight on time. This led me to make wrong assumptions and i
> wasted so much time."
- https://www.reddit.com/r/leetcode/comments/1u0hnbq/ · 2026-06-08 · **评论 2** · 一手
- 可操作化：**intro/背景段不是废话，是约束的藏身处**。`LOOP_GUIDE.md` §3 的"前 5 min 读完全部 part"要扩成
  "**前 5 min 读完 intro + 全部 part，并把 intro 里的每个数字/时间窗抄进注释**"。

### C3-2 · ⚠️ 别写类：多 part 快节奏下 OOP 会吃光时间（**但有反向证据**）
> "I would suggest don't go for classes as I went gor the use of classes but in these fast-paced interviews classes and
> oops concept will eat up your time completely. Go for some brute force way as judgement will be made on the number
> of parts solved surely. Use your time wisely."
- https://www.reddit.com/r/leetcode/comments/1u0hnbq/ · 2026-06-08 · **评论 11** · 一手（他自己 2/4 挂了）
- ⚠️ **反向证据**（Mobile OA，通过者，评论 17）：
  > "Maybe. OA was simple, it would be best if you use classes and functions, because they do judge the code quality and all."
  https://www.reddit.com/r/leetcode/comments/1td6t5k/ · 2026-05-14 · **评论 17** · 一手
- **两条直接对立**，且与 `LOOP_GUIDE.md` 的"代码质量 > 最优复杂度"、§6"类设计先写接口签名再填"更贴近后者。
  我的读法（非引文）：**分轮次**——OA/Programming Exercise 是类设计题（cd02/cd03 那种）就写类；
  电面 4-part 递进题不要一上来搭继承层级。**两条都记，重复次数=1:1，不做取舍。**

### C3-3 · 时间管理是唯一真正的瓶颈（一手复盘）
> "My biggest issue wasn't the logic—it was time management and coding under pressure. The questions themselves
> weren't impossible, but they were intentionally long and had multiple parts, so speed mattered a lot."
- https://www.reddit.com/r/leetcode/comments/1uz688l/ · 2026-07-17 · 正文 · 一手

### C3-4 · 调试失误会连锁吃掉后面的 part
> "I solved the first part but made a few debugging mistakes. I ended up spending too much time fixing them, so I
> couldn't move to the later parts before the interview ended."
- 同上 · 2026-07-17 · 正文 · 一手
- 可操作化：**第一个 part 写完立刻用 2–3 个 assert 验证再进下一 part**，别把 bug 带到 part 2 再回头查。
  （与 `LOOP_GUIDE.md` §3 备考动作"每 part 写 2–3 个自测 assert"一致，这是一条挂掉的实证。）

### C3-5 · 实习/校招的实际备考方向（一手，虽然本人挂了）
> "I mainly prepared by:  Solving hard string problems on LeetCode Practicing company-specific DSA questions
> Focusing on design-oriented DSA problems"
- 同上 · 2026-07-17 · 正文 · 一手
- 与本仓库的题型分布吻合（字符串解析 + design-oriented）。

### C3-6 · AI Programming Exercise 的执行顺序（**二手**，见 B3-14）
> "Have the AI read the full README Ask it to summarize the requirements Get a proposed implementation plan and
> actually review it Let it write the code Add your own tests / edge cases Run it, debug, and understand everything"
> "this round is testing whether you can use AI effectively without turning your brain off. The AI can handle a lot but it
> may over-engineer, miss edge cases, or make assumptions that aren't actually in the README."
- https://www.reddit.com/r/leetcode/comments/1u51q4w/ · 2026-06-13 · 正文 · **二手**
- `LOOP_GUIDE.md` §6 已完整收录此策略。**本次只需改证据等级，不需改策略内容。**

### C3-7 · Reference check 的选人标准
> "Make sure you actually give someone you think will a) actually give you a good reference and b) can deflect or
> decline the ask for a negative."
- https://www.reddit.com/r/cscareerquestions/comments/1sw4eb2/ · 2026-04-26 · **评论 1** · 一手
- 可操作化：挑 reference 时，**先确认这个人被追问"他的缺点是什么"时会怎么答**。

### C3-8 · 选语言按"有没有真写过 API 调用和 JSON 解析"来选，不按刷题语言选
> "I'll suggest JS in that case, because there would be rounds, which require real API calling, and some json parsing.
> And you wouldn't have done any of this in c++"
- https://www.reddit.com/r/leetcode/comments/1srvx7m/ · 2026-04-21 · **评论 41** · 一手

---

# 第二部分：slice4（45 帖，标题无 "Stripe"，2023-01 → 2026-05）

信噪比确实很低。45 帖里**只有 5 处**有 Stripe 面试实质内容，逐条如下。其余 40 帖是市场吐槽 /
referral 名单 / 简历诊断 / "我项目里用了 Stripe SDK"，按 BRIEF 跳过，不写入。

## A. 题（problems）

### A4-1 · ⚠️ **未覆盖的轮次形态**：给现成代码 → 加功能 → **写测试** → 再加更难的功能
- **逐字引用**（正文里的一句）：
  > "A few companies gave a codebase and had me find a bug in it and/or make a modification to it (stripe was one example)."
- **逐字引用**（**评论 2**，同一位 OP 展开细节）：
  > "The Stripe interview was a bit easier, they gave me some code and asked me to make a pretty simple addition to it.
  > When I did that, they asked me to write some tests to verify the correctness. After that, they asked me to make
  > another addition to the code, this time harder but still not too difficult. After I did that they let me ask them any
  > questions about their company, and we had a discussion about what it was like to work there. Then the interview
  > was over, and a few days later I got a rejection. Not sure what I did wrong, I thought the code I wrote was pretty
  > good and it solved the problems they asked me to solve. I guess somebody else did it even better."
- 来源：https://www.reddit.com/r/cscareerquestions/comments/1t86ldv/ · **2026-05-09** · 正文 + **评论 2**
- 轮次：**不明**——从"最后留时间问公司问题、之后就结束了"和"a bit easier"判断，最像 **technical phone screen**；
  但也可能是 onsite programming。**标不确定。**
- 一手/二手：**一手**（11 YOE senior backend，Toronto/加拿大，2025-10 起找工作）
- 对照 inventory：**未覆盖（作为形态）**。
  库里最接近的是 `bs01`–`bs05`（给 repo 找 bug）和 `cd01`–`cd11`（从零写类）。
  **但这条描述的是第三种形态：给一段已有代码 → 增量加功能 → 面试官主动要求补测试 → 再加更难的功能。**
  它既不是"找 bug"，也不是"从空文件写起"。库里没有这种"扩展既有代码 + 显式要求写测试"的练习。
- 信息量：**TITLE**（有形态和节奏，无题目内容）
- **对备考的直接含义**：`LOOP_GUIDE.md` 反复说"没有自动测例、要自己写测试"，这里是**面试官口头点名要你写测试**的实录。
  练 `cd0x` 时应加一个动作：**每写完一个功能，先不等提示，主动补测试并跑给面试官看。**
- **额外信号**：他"两个 addition 都做完了、代码自认不错"，仍然被拒（几天内）。
  与 `LOOP_GUIDE.md` §3 "多数面试官不按 rubric 判"、§6 "两 part 完成但有 bug 也可能拒"同向——**做完 ≠ 过**。

### A4-2 · ⚠️ 与"Stripe 不考 LeetCode"矛盾：**OA 里出现 LC Hard**
- **逐字引用**（唯一评论，回应"哪些公司不考 leetcode：Stripe, Doordash, Apple, Netflix..."）：
  > "Bruh, STRIPE literally had an LC hard in their OA which I recently gave"
- 来源：https://www.reddit.com/r/leetcode/comments/1tr1uqz/ · **2026-05-29** · **评论 1** · 一手（"which I recently gave"）
- 轮次：**OA**
- 对照 inventory：**无法比对**——没说是哪道、什么岗位、什么地点。
- 信息量：**TITLE**
- ⚠️ **与 `LOOP_GUIDE.md` §3 矛盾**：指南引 Stripe 员工原话"不是 LeetCode；数组/哈希为主"。
  **单一匿名评论，零细节，可信度低**，但**方向明确**，且是 2026-05 的近期数据。
  **注意**：本仓库 inventory 里的 `qA01`–`qA14` 全部是 LC 题号打底（787 / 1087 / 1169 / 465 / 2050 …），
  所以"Stripe OA 里出现 LC 风格题"与本仓库的实际题库并不冲突——**冲突的是 LOOP_GUIDE 的措辞**。
  建议把"不是 LeetCode"改成"**不是纯 LC，但会出 LC 变体包装成业务题；也有人报告过硬核 LC hard**"。

## B. 流程与事实（guidelines）

### B4-1 · Bug squash + integration 的结构性缺陷（候选人视角，2023）
> "Turns out bug squash and integration is extremely terrible for onsite because it takes a while to really understand
> the bug, and the integration. Just like in real life, reproducing the bug and understanding deeply what is it you're
> integration is 80% the battle. My interviewer wasn't able to ramp me up to that 80% so even after I started and thought
> I understood the problem, I really didn't. This is coupled by the fact that the debugging process under time pressure
> sucks. It was so time constrained that I had no time to be stuck. And being stuck is really me going through options
> really quickly and careful not to go down the wrong path. I ended up being too hurried, and made poor decisions to try
> things that I knew intuitively had little chance of being the problem, just for the sake of forward progress."
- https://www.reddit.com/r/cscareerquestions/comments/10o4xfq/ · **2023-01-29** · **评论 1** · 一手（时效性低，2023）
- 可操作含义：**"卡住"这件事本身没有时间预算**。他挂的机制是"为了显得在推进，去试自己都不信的假设"。
  与 `LOOP_GUIDE.md` §4 的 5 步流程（先说假设、再断点验证）正面对应——**说出假设本身就是防止乱试的手段**。

### B4-2 · Stripe 员工自述的通过水平线（2023）
> "I managed to complete all parts of the coding rounds and 95% of the integration and bug rounds and it was definitely
> incredibly difficult, but not impossible."
> "We tend to hire mainly senior engineers than juniors/intermediates, so our process makes sense.
> My team has 4 seniors, 1 staff, 1 junior and 1 intermediate engineer."
> "Stripe and Google have the same mentality on interviews. We know that we're going to filter out a lot of really good
> engineers with our interview process, but we're terrified of accidentally hiring a bad one."
- 同帖 · **2023-01-29** · **评论 3** · 一手（自称 Stripe 员工）
- ⚠️ 与 `LOOP_GUIDE.md` §5 "integration 通过线 2/5、2.5/5 with hints、3/5、3.9/5 都有人过" **张力**：
  这位员工报的是 "all parts + 95%"。**不构成硬矛盾**（他是通过者的上限样本，不是通过线），
  但提醒：**通过线的低值样本可能有幸存者/自述偏差**。时效性低（2023）。

### B4-3 · 面试官质量方差大（Stripe 内部激励导致）
> "I guess a big point would basically be that the quality/value of a big squash interview depends way more on the
> interviewer than your typical lc problem. In an environment where everyone is encouraged to be an interviewer to get
> promoted (Stripe) that's going to dramatically lower the bar."
- 同帖 · **2023-01-29** · **评论 2** · 二手/推测（该评论者未说自己面过 Stripe）
- 另一条一手正面样本（**评论 13**）：
  > "I agree, I enjoyed stripe's process and it was a nice breath of fresh air. My interviewer was also quite impressive
  > and made it a lot more relaxed, but I do see it depends a lot on who interviews you."
- 可操作含义：**面试官方差是真实变量**，"被 ramp up 到 80%"与否很大程度不由你控制 —— 这与 B4-1 是同一件事的两面。

### B4-4 · 高级别候选人的 VO 失败模式（含 Stripe，2023，二手价值低）
> "I have gone through the process with the big ones like Meta, Apple, Google, TikTok, Zynga, Stripe, Pinterest,
> Dropbox, Confluent, and Ripple. ... I was able to solve almost all DSA/Leetcode questions in those rounds
> (Meta has 2 questions/coding round), but it is almost always the System Design that killed me."
- https://www.reddit.com/r/cscareerquestions/comments/16nadcm/ · **2023-09-20** · 正文 · 一手，
  但**没有指明 Stripe 是因为 SD 挂的**（Stripe 只出现在公司清单里）。**不足以判断，仅登记。**

### B4-5 · 2026 年 Stripe 仍在招、且对 senior 仍是"能拿到面试"的档位
> "I had interviews with amazon, stripe, ebay, okta, carta, etc."（11 YOE，Toronto，2025-10→2026-04）
- https://www.reddit.com/r/cscareerquestions/comments/1t86ldv/ · **2026-05-09** · 正文 · 一手
- 另（评论 3，同帖，另一人）：
  > "I had a stripe OA that I failed in one of those 8 lol"（无细节）
- 只作为"OA 仍在发放、senior 岗仍开着"的时间戳，无题目信息。

## C. 打法与教训（tactics）

### C4-1 · 不要为了"显得在推进"去试自己都不信的方向
（引文见 B4-1）——这是 slice4 里唯一真正可操作的教训。
反过来说：**卡住时正确的动作是把候选假设按可能性排序说出来，而不是随便挑一个开始改代码。**
与 `LOOP_GUIDE.md` §4 第③步"把假设说出来"直接对应，且提供了"不这么做会怎样"的反面实证。

### C4-2 · 主动写测试（不要等面试官要）
（引文见 A4-1 评论 2：面试官在他写完第一个 addition 后**主动要求** "write some tests to verify the correctness"）
- 可操作化：把"写完一个功能 → 立刻补测试"做成肌肉记忆，别等这句提示出现。

---

# 汇总与建议改动清单

## 未覆盖 / 需新增的题或形态（3 条）
1. **A4-1**：给现成代码 → 增量加功能 → 写测试 → 再加更难功能。库里无此形态（既非 bug squash 也非从零写类）。
2. **A3-1**："字符串处理 + transaction-flow/LRU"**混在同一题 4 个 part 里**的组合（q26/cd03 + 字符串是分开的）。
3. **A3-2**：**CSV 以纯字符串给入**（自己切分）→ **多个任意查询**。ps12 是层级 CSV，不是任意查询。

## 与 LOOP_GUIDE.md 的矛盾（7 条，按重要性排序）
1. **B3-8**（★最重要）电面通过线三方互斥：recruiter 说 4/4 必须 / 另一 recruiter 说"不看 part 数"且 2/3 过 / 指南写 3/4。
   且 part 总数不固定（有 3 part 的电面）。
2. **B3-14**（★）AI Programming Exercise 那篇被指南标为"一手长文"，实为**二手汇总 + 题库网站商业来源**，
   23 条评论无一亲历者确认。策略内容可留，证据等级必须降。
3. **B3-9** Cooldown：电面（早期轮）挂 → **12 个月**封锁，指南写早期轮 6 个月。
4. **B3-8 附带** 电面结果等待"**more than 1 month**"，指南数字表写"1–5 天"。
5. **B3-6** Bug Squash：面试官口头允许 "debugger, print statements, or any approach you prefer"，
   指南写"不要靠 print"。（同 §1 已知的"口头许可不可信"风险类别。）
6. **B3-1** London backend 的 loop 是 **2 轮 Programming、无 System Design**，指南写社招含 SD。（归因不明，OP 未答 YOE。）
7. **A4-2** 2026-05 有人报"Stripe OA 里是 LC hard"，指南写"不是 LeetCode"。单一匿名评论，可信度低但方向明确。

## 与 LOOP_GUIDE.md 一致、被本轮加强的（5 条）
- 禁 AI / 可 Google（B3-3，并把"可 Google"扩到 Programming 轮）
- 全 loop 单一语言、repo 同语言、选 JS/Python（B3-4、B3-5、C3-8）
- Bug squash = 私有 repo + **多个**失败单测逐个修（B3-7）
- Team match 欧洲长尾 + 招聘暂停（B3-12，从单一 medium 来源升级为多条 Reddit 一手）
- HR 提前发 prep 文档、以书面材料为准（B3-13）

## 新增事实（指南完全没记，2 条）
- **B3-11 Reference check 是一个独立阶段**：onsite 后、offer 前，要 1 前经理 + 1 peer，recruiter 会主动挖负面；
  **过了 reference check 仍可能因"地点"被拒**。2026-04 有两条独立一手证据。
- **B3-10 OA 的监考方式**：不全程录像，但会拍照、且可能中途抓拍。
