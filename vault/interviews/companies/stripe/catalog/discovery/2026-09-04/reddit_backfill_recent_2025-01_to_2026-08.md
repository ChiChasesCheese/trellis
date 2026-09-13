# Reddit slice `back_recent.md` 分析（19 帖 / 2025-01 → 2026-08 / 48,952 字符，已整读）

分析人：agent 4。输出遵循 BRIEF 的 A/B/C 三节，末尾附两个"特别要求"的专项回答。
**逐字引用**用 `>` 标注；所有非引用文字是我的判断，会写明确定/不确定。
岗位过滤：仅 SWE backend；Android / Security / MLE 内容只在与流程通用部分交叉时记录，并标注岗位。

---

## ⭐ 先说三条最重要的结论（其余细节在下面）

1. **`Stripe and Meta new AI interview experience`(2026-07-31) 里没有 Stripe AI 轮的一手题面。**
   OP 是 Stripe AI 轮的**亲历者**（"Just had stripe's new AI interview"），但他**全帖只写了两句关于该轮的事实**，
   没有任何题目内容；36 条评论里**详细描述 AI 轮流程的那几条全部是别的公司**（Meta / "a FAANG company" /
   Amazon / DigitalOcean），**没有第二个 Stripe 亲历者**。所以 §6 的 AI Programming Exercise 仍然只有
   `/u/interviewdb` 那个二手商业来源。详见 §D1。
2. **bug squash 的库被一手证实了：Python 场次是 `requests` 或 `mako`**（2025-08-03，Dublin senior，一手）。
   这直接对上本仓库的 `bs01_mini_template_engine`(minimako) 和 `bs02_mini_http_client`(minihttp)。
   **这是前三片 12 次追问都没拿到的东西，本片拿到了。** 详见 §D2。
3. **bug 数量与 LOOP_GUIDE §4"按 3 个准备"冲突。** 本片出现两个互不相容的一手数字：
   Dublin senior = **4–5 个失败单测**；India 校招 = **只有 1 个失败单测**。详见 §B-矛盾-①。

---

# A. 题（problems）

> 本片共 **11 条**可算"题"的记录。**FULL 0 条**（没有任何一条够重建题面），
> **SUMM 5 条，TITLE 6 条**。**未覆盖的新题：0 道**（与前三片结论一致）。
> 但有 **2 条对现有题库的强确证**（A-02 bug bash 库、A-05 integration 递进结构）。

---

### A-01 · Bug Bash：Python 场次的库就是 `requests` 或 `mako`，4–5 个失败单测 ⭐

- **原文逐字**：
  > "In the bug bash round, you're given the entire repository of a built-in library, for instance, for python,
  > it could be either "requests" or "mako". There'd be 4-5 unit tests failing and you'll be expected to run the
  > tests one by one and make them pass by fixing the actual code. The challenge here is again time since, if it
  > is an unfamiliar library like mako, it is quite challenging to figure out what it does in the first place.
  > Use of an IDE is permitted and is actually one of the evaluation parameters."
- **来源**：https://www.reddit.com/r/leetcode/comments/1mgcc99/ · 2025-08-03 · r/leetcode ·
  `Stripe Integration and Bug Bash rounds interview experience` · **帖子正文**
- **轮次**：Bug Squash（帖子里叫 bug bash）
- **一手/二手**：**一手**。原文 "I had interviewed for Stripe a couple months back in **Dublin, Ireland** for a
  **senior SDE position**. ... I had both integration and bug bash rounds on the same day."
  → 即 **2025 年年中 · Dublin · senior SDE · 一手亲历**。
- **对照 inventory**：**已覆盖（双中）**
  - `mako` → `bs01_mini_template_engine :: minimako — a tiny Mako-style template engine` ✅
  - `requests` → `bs02_mini_http_client :: minihttp — a tiny stdlib HTTP client` ✅
  - 这是本仓库 bug squash 题库选型的**第一条一手外部确证**（LOOP_GUIDE §4 原来记的"Python `requests`/`Mako`"
    来源是 Blind/Coditioning 二手，现在有 Reddit 一手对上了）。
- **信息量**：**SUMM**（有库名、有 bug 数量、有形态"逐个跑失败测试并修真实代码"，但**没有任何具体 bug 内容**）
- **补充（同帖评论，bug 的来源）**：
  > 评论 5：「For bug bash the bugs are introduced by the recruiting team or publicly reported bugs in github for that lib?」
  > 评论 6（OP 回）：「Could be either.」
  → **一手**。意思是 Stripe 既会自己注入 bug，也会用该库 GitHub 上真实报过的 bug。
  **可操作推论**：练 bs01/bs02 之外，去 mako / requests 的 GitHub issue 里翻真实 bug 复现，是有据可依的准备方式
  （LOOP_GUIDE 已有 `loop/raw/github_repos.md` §2，这条给它加了一条一手背书）。

---

### A-02 · Integration：4 个递进子轮，"读文件取请求参数 → 调 API 打印 → 解析响应 → 用它调下一个 API" ⭐

- **原文逐字**：
  > "In Integration round, there's 4 sub-rounds. To begin with, you're given a hello world boiler plate code and
  > you're expected to call an API and print the response. The request parameters are expected to be read from a
  > file - so file parsing is essential. In the second one, you're asked to parse the response and use it to call
  > yet another API. The subsequent rounds follows suit by increasing complexity in terms of forming the request
  > and parsing the response. Use of an ide is permitted. The challenge here is time since requirements change
  > across sub-rounds and thus if the code is modular enough from the beginning, it helps."
- **来源**：https://www.reddit.com/r/leetcode/comments/1mgcc99/ · 2025-08-03 · **帖子正文**（同上，Dublin senior，一手）
- **轮次**：Integration
- **对照 inventory**：**疑似覆盖**
  - 最接近：`int02_payments_reconciliation`（分页拉取 → 退避重试 → 幂等退款 + 对账 → webhook 验签）
    和 `int03_multi_json_etl`（三份异构 JSON → 统一字典 → join → 异常报告）。
  - **差在哪**：本条描述的核心链路是 **"从文件读请求参数 → 调 API → 解析响应 → 拿响应字段去调第二个 API"**
    这个**链式调用**结构。`int02` 是同一个 API 的分页 + 重试，`int03` 是纯本地 JSON 变换，
    **两者都没有"A 的响应喂给 B 的请求"这一步**。`int01_bikemap` 有"解析 → 渲染 → 最近地标"的递进但不是链式 HTTP。
  - **判断**：形态覆盖了 80%，缺的那一环（response → next request 的链式调用 + 请求参数来自文件）
    值得在 int02/int03 上加一个 part 自练，**但不构成一道新题**。
- **信息量**：**SUMM**（有轮次结构、递进方式、时间压力来源，但没有具体 API / 数据 / 业务）

---

### A-03 · Integration：POST + 非 JSON 响应 + 把 PNG 图片写盘

- **原文逐字**：
  > "Depends on language, I used js which has "fetch" api call already. You should set up your dev env already,
  > no? You don't need anything fancy, just basic stuff, you need be able to make a POST call, need to deal with
  > **non-json response**, and also, familiar with file system, **how to write to file(png image)**"
- **来源**：https://www.reddit.com/r/leetcode/comments/1u8c305/ · 2026-06-17 · r/leetcode ·
  `Stripe Interviews` · **评论 3**
- **轮次**：Integration
- **一手/二手**：**一手**（同一人评论 1 说 "My experience for integration is to make an api call to fetch some
  data, then work with the data. Multiple steps." — 用 "My experience"，且能说出响应体细节，判定一手；
  **但没有给日期，也没说岗位/地点**，时效不确定）
- **对照 inventory**：**疑似覆盖**
  - 最接近 `int01_bikemap`（GeoJSON → 地图渲染）——"渲染"多半就是产出图片。
  - **差在哪**：本条明确说 **响应不是 JSON**、并且要**把二进制 PNG 写到文件**。
    inventory 里 int01–int04 的描述都没有明写"非 JSON 响应 / 二进制落盘"。
    LOOP_GUIDE §5 的备考动作里已经有"二进制落盘"这一句，**这条一手把它坐实了**。
- **信息量**：**TITLE→SUMM 之间**（只有能力清单，没有题面）
- **可操作**：Python 侧对应 `requests.get(...).content` / `urllib` 后 `open(path,'wb').write(...)`；
  练 int01 时**务必真的落一次盘并用图片查看器打开**，不要只做到内存里。

---

### A-04 · Integration：给的是 repo，Java 依赖里已经带好 http client

- **原文逐字**：
  > 评论 4：「I used java. They had some http client already added to the dependency. You just need to check
  > example code/docs and see how you can use that http client to make API calls.」
  > 评论 5：「I've done it before few years ago. I believe it is a repo, yes.」
- **来源**：https://www.reddit.com/r/leetcode/comments/1u8c305/ · 2026-06-17 · **评论 4、评论 5**
- **轮次**：Integration
- **一手/二手**：评论 4 **一手**（"I used java"，无日期）；评论 5 **一手但自述"few years ago"**，时效差。
- **对照 inventory**：不是题，是形式事实（也见 §B-06）。
- **信息量**：**TITLE**
- **意义**：回答了发帖人的核心疑问——**不是从零搭 HTTP 客户端，repo/依赖已经准备好**。
  这条降低了"Java/C++ 样板做不完"的部分风险，但不推翻 LOOP_GUIDE 的语言结论。

---

### A-05 · 电面（technical screen）：字符串题，2 part

- **原文逐字**：
  > "then I got link to choose a date for technical screening, and I chose it today and after completing it I
  > thought I rocked the interview, I enjoyed it despite being my first interview, **it had two parts to solve a
  > string based problem** and I written the code in a good way too, I felt I explained it well, the approach,
  > code modularity and all"
- **来源**：https://www.reddit.com/r/leetcode/comments/1ownvu4/ · 2025-11-14 · r/leetcode ·
  `Stripe technical screening rejection [new grad software]` · **帖子正文**
- **轮次**：Technical Phone Screen（new grad software，US，国际学生）
- **一手/二手**：**一手**（含已知结果：**6 小时后被拒**）
- **对照 inventory**：**信息不足以判断覆盖**。只知道"string based problem, 2 parts"。
  `ps05_numeronym_validation` / `ps07_redact_card_numbers` / `q34_compress_url` 都是字符串题，
  但**没有任何依据把它对到具体哪一道**。
- **信息量**：**TITLE**

---

### A-06 · OA（backend IC2）："a data processing question"

- **原文逐字**：
  > 正文：「I have competed the hackerrank assessment which included **a data processing question**.」
  > 评论 5：「Can you share the type of question asked in hackerrank assessment ? Were you able to complete the assessment ?」
  > 评论 6（OP）：「Yes. **It was a data processing question**」
- **来源**：https://www.reddit.com/r/leetcode/comments/1sdw8ux/ · 2026-04-06 · r/leetcode ·
  `Anyone giving interviews for backend IC 2 at stripe?` · **正文 + 评论 6**
- **轮次**：HackerRank OA（**backend IC2，4.6 YOE，非 FAANG 背景** — 见评论 1-4）
- **一手/二手**：**一手**
- **对照 inventory**：**不足以判断**。"data processing" 与 `q14_join_dataset` / `q20_transaction_fees_reconciliation`
  / `q15_kyc_verification` / `q42_loose_record_aggregation` 都相容，**无法收敛**。
- **信息量**：**TITLE**
- **顺带的流程事实**（记在 §B-12）：backend IC2（4.6 YOE）**照样有 HackerRank OA** →
  再次印证 LOOP_GUIDE §0 表里"社招也可能有 OA"。

---

### A-07 · 校招 VO Round 1「Advanced Programming」：multi-part，做了 2 part + 边界追问

- **原文逐字**：
  > "Online Assessment:- **One coding question** to kick things off.
  > Phone Screening:- A multi-part problem-solving round. **I was able to solve 4 parts within 45 minutes**,
  > followed by a 15-minute discussion related to stripe and some questions.
  > ...
  > Round 1: **Advanced Programming**:- Multi-part problems; **I solved two parts along with follow-up questions
  > on edge cases (45 minutes)**. This round went fairly well."
- **来源**：https://www.reddit.com/r/leetcode/comments/1tkb1iw/ · 2026-05-22 · r/leetcode ·
  `Stripe New Grad Interview Experience` · **帖子正文**（India 校招，语言 Java —— 见评论 5）
- **轮次**：OA / Phone Screen / VO Programming Exercise
- **一手/二手**：**一手**（含已知结果：**VO 后被拒**）
- **对照 inventory**：**无法判断**（完全没给题目内容）
- **信息量**：**TITLE**
- **额外价值**：这是本片唯一一条同时给出 **"电面 4/4 part 完成"** 与 **"VO programming 只做 2 part 也评价 fairly well"**
  的一手数据点，见 §B-通过线。

---

### A-08 · 校招 VO Round 2「Bug Squash」：大而复杂的 Java 代码库

- **原文逐字**：
  > "Round 2: **Bug Squash (Most Challenging)**:- This round stood out. **I was given a large, complex codebase
  > and asked to identify and fix bugs.** While I managed to find and fix the issue with the interviewer's
  > guidance, I realized **I wasn't as strong as I wanted to be in advanced Java and deep debugging**. I truly
  > felt I could've done better here."
- **来源**：同上 1tkb1iw · 2026-05-22 · **帖子正文**
- **轮次**：Bug Squash（Java，India 校招）
- **一手/二手**：**一手**
- **对照 inventory**：**不足以判断**（没说库、没说 bug）
- **信息量**：**TITLE**
- **⚠️ 必须记的一件事**：这一帖下面 **有 5 条独立的追问专门问 bug 是什么**
  （评论 6「Can you share what kind of a bug was there in bug bash round and what concept of Java you struggled with」、
  评论 15「I am also interested to know what Java concept you steuggled with in the debugging round」、
  评论 17「can you share your difficulties with the bug round?」…），
  **OP 每一条都回"我们私聊"**（评论 7「We can chat to discuss」、评论 9「Dmed you」、评论 16「Sure, let's discuss in chat.」）。
  → **本片再次复现了前三片那个方法论结论：Reddit 上 Stripe 的具体题面从不公开落地，全部转私信。**
  本片 19 帖里这类"问了 → 转私信/未答"的实例我数到 **至少 14 次**（详见文末统计）。

---

### A-09 · Bug Squash（校招）：整个 repo 只有 1 个失败单测 ⚠️

- **原文逐字**：
  > "My VO rounds went pretty smoothly, finished each round with 5-10 minutes to spare. However, in the bug squash
  > round, my interviewer gave me a small hint - **told me to implement the fix in some other function, higher up
  > in the stack trace rather than the function I was fixing**. In her defense, this fix was infinitely simpler,
  > but in my defense, my fix would have worked as well if she gave me 5 more minutes on it. But after her hint,
  > I only took 5 more minutes to complete the bug fix after incorporating her hint with 20 minutes to spare.
  > **There was only 1 failing test in the repo which we had fixed**, and she told me that we are done with the
  > round at that point after going over the changes."
- **来源**：https://www.reddit.com/r/leetcode/comments/1ohkp31/ · 2025-10-27 · r/leetcode ·
  `Stripe New Grad` · **帖子正文**（2025 grad，**India** —— 见评论 2）
- **轮次**：Bug Squash
- **一手/二手**：**一手**
- **对照 inventory**：**不足以判断题目**，但**是本片最重要的流程矛盾源**（见 §B-矛盾-①）。
- **信息量**：**TITLE**（题目层面）/ **SUMM**（流程层面）
- **两条可操作的东西**（我认为这是本片对 bug squash 最有用的一条）：
  1. **修复位置本身是考点**：面试官明确要求"把修复放到调用栈更上层的另一个函数里，而不是你正在改的那个函数"。
     → **练 bs01–bs05 时，定位到根因后先停 30 秒问自己："这个 bug 的最小、最正确的修复点在栈的哪一层？"**
     LOOP_GUIDE §4 挂点里有"大范围重写而非最小修复"，这条给出了**反方向的挂点：修得太局部/太靠下**。
  2. **修完 1 个测试面试官就宣布结束**——所以"3 个 bug"不是硬结构，**面试官会按你的表现决定何时收**。

---

### A-10 · Bug Bash（JS 场次）：bug 类型清单（可信度存疑）

- **原文逐字**：
  > 评论 1：「Stripe Bug Bash is about reading code and fixing real bugs. **In JS, expect logic errors, edge cases,
  > async/await or promise issues, wrong conditions, and small broken implementations.** It's more than just null
  > checks, but not very complex.. Practice debugging small JS functions, fixing failing tests, and understanding
  > async code. There are no official mocks, so try small open-source JS repos and focus on clean, correct fixes..」
  > 评论 2：「Have you already been a part of the process?」
  > 评论 3（同一人）：「Yes, I went through a similar Bug Bash round recently. The experience I shared is based on that.. .」
- **来源**：https://www.reddit.com/r/leetcode/comments/1ps3akr/ · 2025-12-21 · r/leetcode ·
  `Need help for the upcoming Stripe Bug Bash round in JS` · **评论 1 / 3**
- **轮次**：Bug Squash（JS）
- **一手/二手**：**自称一手，但我判定可信度低**。理由：① 措辞是通用总结口吻、没有任何"我当时那个 repo/那个 bug"的
  具体细节 ② 说的是 "a **similar** Bug Bash round"，不是 Stripe 的 ③ 同帖同一人评论 5 给出的另一条说法
  与多条一手证据冲突（见 §B-矛盾-③）。**标为"疑似 AI 生成或泛化的回答"**。
- **对照 inventory**：**疑似覆盖**——"async/await or promise issues" 对得上
  `bs05_asyncio_fetch_race :: fetchrace — a small bounded-concurrency async fetcher`（虽然我们的是 Python asyncio）；
  "logic errors / wrong conditions / off-by-one 类" 对得上 LOOP_GUIDE §4 的四类典型 bug。**没有新增。**
- **信息量**：**TITLE**
- **⚠️ 注意**：OP 问的三个最关键问题（"difficulty of bugs"、"simple null checks or a function implementation"、
  **"what are the repos which are probable for this round in JS"**）——**repo 那个问题全帖无人回答**。
  LOOP_GUIDE §4 记的 JS 库（Express / Day.js / React 组件竞态）**在本片没有得到任何独立印证**。

---

### A-11 · Android 岗的三轮题（**非本岗位，只记一行**）

- 岗位：**Android / mid level / US**，来源 https://www.reddit.com/r/leetcode/comments/1u0mgyy/ · 2026-06-08 · 一手。
- **存在但非本岗位**：screening = 字符串解析多 part；integration = 给一个 app、把功能接到另一个 class/library、
  用 Android Studio + 模拟器；bug squash = 给 unseen repo + git issue，issue 里同时给一个失败 TC 和一个通过 TC 作参考。
- **但它有 3 条通用流程事实值得抽出来**，已记在 §B-04 / §B-05 / §B-16（含一条与 LOOP_GUIDE 的矛盾）。

*（另：`Stripe New Grad - Integration + Threat Modeling Interviews`(2026-04-01) 是 **Security Engineer 校招**，
有 Threat Modeling 轮、问 STRIDE/OWASP —— **存在但非本岗位，不展开**。全帖 2 条评论都在聊简历，无题面。）*

---

# B. 流程与事实（guidelines）

## ⚠️ 与 `loop/LOOP_GUIDE.md` 矛盾的（共 4 条 —— 按 BRIEF「矛盾比新增更重要」优先列）

### 矛盾 ① · bug squash 的失败单测数量：本片给出 **1** 和 **4–5**，都与 LOOP_GUIDE §4「**按 3 个准备**」不符 ⭐⭐

- LOOP_GUIDE §4 原文：「**几个 bug：按 3 个准备。** …**2025-10 一条完整可读的一手校招证据把这件事定住了**：
  Dublin new grad VO "only resolved 1/3 bugs" …**校招也是 3 个**。」
- **本片反证 A（少于 3）**：
  > "**There was only 1 failing test in the repo which we had fixed**, and she told me that we are done with the
  > round at that point after going over the changes."
  > — 1ohkp31 正文，2025-10-27，India 校招，**一手**
- **本片反证 B（多于 3）**：
  > "There'd be **4-5 unit tests failing** and you'll be expected to run the tests one by one and make them pass
  > by fixing the actual code."
  > — 1mgcc99 正文，2025-08-03，Dublin senior SDE，**一手**
- **注意时间点**：反证 A（2025-10-27）与 LOOP_GUIDE 引以为据的那条 "1/3 bugs"（记为 2025-10，Dublin 校招）
  **几乎同期、但地点不同（India vs Dublin）、数字不同（1 vs 3）**。这两条**不是同一个人**
  （本片这位在评论 2 明说 "India"）。
- **我的建议改法（供协调者判断）**：
  §4 的「按 3 个准备」应降级为「**1–5 个不等；按"多个、逐个修"准备，不要按固定数量安排时间**」。
  更稳的表述是这条一手给的形态：「run the tests **one by one** and make them pass」+
  「**修完面试官就可能宣布结束**」。**"3 个"这个数字目前只有单一来源支撑，而反例有两条、覆盖 1 和 4–5 两端。**

### 矛盾 ② · 「无自动测例」 vs 面试官手里**有**预先准备的测试用例

- LOOP_GUIDE §3 原文：「**无自动测例**——自己造输入、自己验证」。
- **本片反证**：
  > "Screening round(45 min coding +15 min buffer) : Basic string parsing and doing operations on it and returning
  > result in a specific format. **For this round my interviewer had prior TCs to check the code success.** Round
  > has multiple parts to solve, starting from scratch writing for 1st part and then building over that for
  > subsequent parts(**later parts were hidden, and only made visible after success with prev part**)."
  > — 1u0mgyy 正文，2026-06-08，**一手**
- **岗位限定：Android，US，mid level。** 所以严格说不能直接推翻 backend 的结论。
- **但它改变的是一个战术判断**：LOOP_GUIDE 的读法是"没人验你，所以你必须自己写 assert"。
  这条说的是"**你看不到测例，但面试官那边有一套，他用它判定你这个 part 过没过、决定放不放下一个 part**"。
  → **两者不冲突于"你要自己写 assert"，但冲突于"没有客观判定"。**
  **可操作**：写完一个 part 后**主动问一句 "do you want to run any cases against this before I move on?"**——
  如果面试官手里有 TC，这句话直接把判定提前，避免带着 bug 进下一个 part（LOOP_GUIDE §3 已记的连锁挂点）。
- **确定性**：中。单一来源 + 非本岗位。**建议记为"Android 岗一手；backend 未证实"。**

### 矛盾 ③ · bug squash 的语言是**候选人选的**还是**轮次固定的**

- LOOP_GUIDE §0 原文：「**整个 loop 只能选一门语言**，在 recruiter 处一次性选定，**bug squash 的 repo 就是这门语言**」。
- **本片反证（低可信度）**：
  > 评论 4：「Can you choose your language? Isn't it optima to choose Python?」
  > 评论 5：「what I've seen, **the language is fixed for the round**. If it's a JS Bug Bash, you'll be working in
  > JavaScript, not choosing another language like Python.」
  > — 1ps3akr，2025-12-21
- **同帖正文直接反驳它**：OP 说 "**I have chosen JavaScript as the language** for the interview"。
- **本片正向证据（支持 LOOP_GUIDE）**：
  > 评论 12：「Hello, I am using Java for any DSA problem and Go for my job and personal projects. Do you have any
  > idea if I can use Java for the programming round and Go for Bug Squash and Integration rounds?」
  > 评论 13：「**unfortunately, for onsites no, for phone screen yes** - I am in the same situation as you, using
  > Python for coding challenges and using Go for job, it sucks」
  > — 1mgcc99，2025-08-03
- **结论：LOOP_GUIDE 是对的，评论 5 是错的（说话人自己也只说 "what I've seen"）。**
  但评论 13 补了一条 LOOP_GUIDE 没写清的**细化**：**电面可以和 onsite 用不同语言**（"for phone screen yes"）。
  这条值得加——它意味着"电面用 Python 刷题语言、onsite 全套换成工作语言"**不可行反过来可行**，
  即 **onsite 五轮必须同一门，但电面那一轮可以单独选**。⚠️ 单一来源，标不确定。

### 矛盾 ④ · Dublin/Ireland 校招「没有 integration」这条要放宽

- LOOP_GUIDE §0 原文：「Dublin 校招只有 2 轮 = Programming + Bug Squash，**没有 integration**」。
- **本片证据**：
  > "Interview process: Stage 1: 1 programming round (3 parts) Stage 2: **Programming + Integration + Bug squash
  > + Hiring manager**"
  > — 1t0v98p 正文，2026-05-01，**Stripe (Ireland)**，一手（他自己收到的 recruiter 流程说明）
- **注意**：这位**不是校招**（正文说 "My work hours are 11 AM – 8 PM"，是在职者），所以**严格说不构成矛盾**，
  但它证明 **Ireland 的 loop 是有 integration 的**，"Dublin 无 integration"只能限定在那一个校招个例上。
- **同时它再次印证 LOOP_GUIDE §0 的"SD 不是必有项"**：Stage 2 四轮里**没有 System Design**。

---

## 新增 / 印证的事实

### B-01 · AI Coding 轮已经进入**校招 VO** 的轮次组合里 ⭐（2026-08，最新）

> "Anyone know what I can expect for the **AI Coding, Integration or Bug Squash round**? I've never done these
> types of interviews before, so just wondering what they're looking for and what kind of questions I can expect,
> thanks so much!"
> — https://www.reddit.com/r/leetcode/comments/1vhpsgz/ · **2026-08-07** · `Stripe newgrad virtual onsite` · 正文 · 一手（他自己的 VO 安排）

- **这是本片时间最新的一条**，也是**校招 VO 含 AI Coding 轮的第一条外部证据**。
- LOOP_GUIDE §0 把 "AI Programming Exercise" 记在"2026 新增"，但没说它进了校招组合。**这条补上了。**
- 全帖只有 2 条评论，**都没有回答**：
  > 评论 1：「I have been using this site to practice, its been pretty helpful to me: aicodingprep.com」
  > 评论 2：「You will need to solve task by using AI.」
  评论 1 是**软广**（贴自家网站），评论 2 是一句废话。**零信息量，但"轮次名称"本身是硬事实。**

### B-02 · AI 轮的一手事实（Stripe 亲历者，仅两句）⭐

> "Just had **stripe's new AI interview**, and had Meta's AI interview earlier this year. … For context, its the
> interview round where **you are allowed to use AI models provided within hackerrank** to solve **a more
> challenging problem**"
> — https://www.reddit.com/r/leetcode/comments/1vbpool/ · 2026-07-31 · 正文 · **一手（Stripe 亲历者本人）**

- **印证 LOOP_GUIDE §6 的两点**：① 平台是 **HackerRank 内嵌 AI**（不是 Cursor、不是自带工具）
  ② 题目比常规轮**更难**（"a more challenging problem"）——这与 §6 记的"自己手写 80% 概率写不完"同向。
- **他还写了一句关于评估导向的**：
  > "It felt completely different from doing leetcode, and actually felt more like **testing your competencies
  > when doing your work** (considering our work heavily uses AI now)."
- **⚠️ 但他没有写题目内容、没有写时长、没有写 part 数、没有写 AI 用量限制。** 详见 §D1。

### B-03 · 「Stripe 从来不考 LeetCode」——两条独立复述

> 评论 16：「**Stripe hasn't had LC style questions for years**」
> 评论 17：「**Stripe never asked LC questions. Even when I interviewed in 2018.**」
> 评论 19：「what is their interview pattern? what do they mostly focus on then if it's not LC style」
> 评论 20：「**Coding, but more like day to day tasks rather than algorithms you never use in your daily work.
> Also sys design and behaviour.**」
> — 1vbpool，2026-07-31，评论 16/17/19/20

- 评论 17 是**一手**（"Even when I interviewed in 2018"）。评论 16/20 来源不明。
- **印证 LOOP_GUIDE §3 的"不是纯 LeetCode"结论**，并给 2018 年加了一个时间锚点。
- **⚠️ 反向噪音**：本片有**两条**建议按 LC 准备的评论，**但两条都带商业推广**，见 §B-19。

### B-04 · 校招/mid VO 的时长切分：45 min 编码 + 15 min buffer；integration/bug squash 前有 5 min 环境检查

> "Screening round(**45 min coding +15 min buffer**) …
> Programming exercise(**45+15**) : Same as Screening Round, this time I had to think of TCs, Unit TCs, and edge
> cases for every part. Discuss with the interviewer and move forward if satisfied.
> Integration Round (**45+15**): **5 mins for intro, 5 mins for setting up environment, git cloning etc. 45 mins
> coding and 5 mins to ask questions.**
> Bug Squash (**45+15**): **5 min for intro, 5 min for env check and cloning, 45 mins coding and 5 mins to ask questions.**
> Hiring Manager (45 mins): 40 mins of grinding on the resume …"
> — 1u0mgyy 正文，2026-06-08，**Android/US/mid，一手**

- **岗位是 Android**，但这是本片**唯一一份逐轮时长切分**，且与 LOOP_GUIDE §5 记的
  "60 分钟里可能只剩 35 分钟写代码"**同向但更乐观**（这里是 45 min 净编码，因为总时长是 45+15 而非 60）。
- **可操作**：**5 分钟 env setup 是排进日程的**，但仍然不够 clone + build + 跑测试。
  LOOP_GUIDE §5 的"面试开始前全部就绪"这条建议不变。

### B-05 · 面试前 recruiter 会发一份**说明文档**（多次出现）

> "Before rounds they provide a **descriptive doc**, which helps you to how and what to prep."
> "Got the call from HR, moving forward in the interview process, **shared the docs** along with other details.
> Scheduled **4 rounds in two days**."
> — 1u0mgyy 正文，2026-06-08，一手（Android）

> "**From the doc I understood** that we will be expected to integrate with an external API"
> — 1u8c305 正文，2026-06-17，一手

- 两条独立来源印证 LOOP_GUIDE §3 记的 "recruiter 发的 information packet"。
- **⚠️ 文档可能不准**：同帖 1u0mgyy 说 "Understanding of **Retrofit** was suggested me in the doc, but **didn't
  found any usage in the interview**." → **prep doc 里点名的库不一定真用得上**，别把准备时间压在文档点名的单一库上。

### B-06 · Integration 是给 repo，不是从零搭

- 见 A-03 / A-04。三条评论（1u8c305 的 #1/#3/#4/#5）合起来的一致结论：
  **给 boilerplate/repo，HTTP client 已在依赖里，你的活是"调用 + 解析 + 用数据"**。
- 印证 LOOP_GUIDE §5「私有 repo（README、boilerplate、示例数据、API 文档）」。

### B-07 · AI 政策：整轮**严禁**，连 VS Code 自动补全都不行 ⭐

> 评论 1：「When you say you were allowed to use IDEs - were you allowed to use cursor? Are you encouraged to use AI?」
> 评论 2（OP）：「**Use of any sort of AI was strictly prohibited, whether ChatGPT or Cursor.**」
> 评论 10：「Are we allowed to have auto-suggestions on VS code?」
> 评论 11（OP）：「**No AI usage is allowed including suggestions**」
> — 1mgcc99，2025-08-03，**一手**

- 比 LOOP_GUIDE §4/§5 的"禁 AI"更严：**IDE 自动补全（Copilot 类 suggestion）也算违规**。
- **强化 LOOP_GUIDE §3 已有的对策**：进场前**主动演示补全已关**（新建空文件打字给对方看）。
  这条一手把"suggestions 也不行"坐实了，**该动作从"加分"变成"必做"**。

### B-08 · 但**联网查语法/文档是允许的**

> 评论 3：「Was Internet Usage Allowed to Lookup Syntax? Or Was it Expected to Remmber The Systaxes For Integration
> Round and Bug Bash Round」
> 评论 4（OP）：「**It was allowed.**」
> — 1mgcc99，2025-08-03，**一手**

- 印证 LOOP_GUIDE §5「可联网查文档，禁 AI」，并把它扩展到 **bug bash 轮也允许**。

### B-09 · **IDE 的使用本身是评分项** ⭐

> "Use of an IDE is permitted and **is actually one of the evaluation parameters**."
> — 1mgcc99 正文，2025-08-03，一手

> "**Use all the debugging tolls available in IDE, these all things are reviewed and noted.**"
> — 1u0mgyy 正文，2026-06-08，一手（Android）

- **两条独立一手**，直接支撑 LOOP_GUIDE §4「只用 print、不会 debugger」是挂点，
  并且**比 LOOP_GUIDE 现有措辞更强**：不是"不会 debugger 会扣分"，而是"**你怎么用 IDE 是被单列打分的一项**"。
- **建议 LOOP_GUIDE §4 加一句**：*IDE/debugger 的熟练度是显式评分项（两条一手），
  所以要**出声演示**你在用什么（"我在这里下个断点"/"我用 IDE 的 find usages 追一下调用方"），
  不要沉默地用。*

### B-10 · Bug squash 的 bug 来源：**注入的 or 该库真实报过的 GitHub issue，两者皆有**

- 见 A-01 补充（1mgcc99 评论 5/6，一手）。
- 这条**新增**了 LOOP_GUIDE §4 没写的一件事：**可能直接用该库 GitHub 上的真实 bug**。

### B-11 · 电面 → 结果：**6 小时**被拒（再次落在 LOOP_GUIDE 的"5 小时 ~ 1 个月"区间内）

> "at the end I thought I'll at least make it to next round, but **just after 6 hours I got a rejection email**"
> — 1ownvu4 正文，2025-11-14，一手

> 评论 23：「After how long did you hear back from phone screening?」
> 评论 24（OP）：「**2 days**」
> — 1tkb1iw，2026-05-22，一手

- 两条都在 LOOP_GUIDE §0 表的区间内，**不构成矛盾，构成印证**。

### B-12 · 社招（backend IC2，4.6 YOE）**照样有 HackerRank OA**

> "I got a call from a recruiter for scheduling a **machine coding round** in Stripe, **I have competed the
> hackerrank assessment** which included a data processing question. I want to know about the machine coding round
> in stripe a bit more, I am being told **an inerviwever will already be present in the call**"
> — 1sdw8ux 正文，2026-04-06，一手（YOE 4.6，非 FAANG）

- 印证 LOOP_GUIDE §0 表「社招也可能有 OA」（原证据是 8 YOE Canada remote，这条是 4.6 YOE，**第二例**）。
- "machine coding round" = 他对 Programming Exercise 的叫法（印度语境常用词）。

### B-13 · 电面 part 数：**Stripe 侧刻意不告知通过线** ⭐

> 评论 2：「**There are questions that have 4 parts as well. We aren't supposed to tell you how many parts are
> needed to clear the round.** Did the interviewer ask nudge to complete the 2 section faster?」
> 评论 3（OP 回）：「No it was just a 2 part question, she mentioned it. And also I still have time left after
> completing both parts.」
> — 1ownvu4，2025-11-14

- **评论 2 的措辞 "We aren't supposed to tell you" 说明说话人自称站在 Stripe 一侧**（面试官/员工）。
  **无法验证身份，标为"自称内部人士，未验证"。**
- **但它与 LOOP_GUIDE §3 的结论完全一致**：「**⚠️ 通过线：没有硬线，recruiter 口径互相矛盾**」。
  这条给出了一个**机制性解释**：通过线是刻意不公开的，所以候选人听到的口径互相矛盾是必然的，不是谁记错了。
- **另一条硬事实**：这位 OP **2 part 全做完、还有剩余时间、代码质量自评良好 → 仍被拒**。
  → **再次证明"做完 part 数"不是通过条件**（LOOP_GUIDE §3 已记，本条是第 N 次印证）。

### B-14 · 校招 VO 轮次组合：又两个"没有 Integration"的例子

> "Virtual Onsite:- … Round 1: Advanced Programming … Round 2: Bug Squash … Final Round: Managerial Discussion"
> — 1tkb1iw 正文，2026-05-22，**India 校招，一手** → **VO = Programming + Bug Squash + Managerial，无 Integration、无 SD**

> "It will be having **two rounds coding exercise and bug squash**. I chose the language as python"
> — 1o11q3k 正文，2025-10-08，**校招（new graduate），一手** → **VO = 2 轮，无 Integration**

> "From what I've read **there will be 2 1-hours interviews**. The first part will be very similar to the first two
> steps in the process(OA + very first interview). **The second part (the one where you download a repo and
> integrate a feature)**"
> — 1p5p8z7 正文，2025-11-24，一手（他自己的安排；注意他描述的第二轮是 **integration** 不是 bug squash）

- **合起来的结论**：LOOP_GUIDE §0 的「轮次组合并不固定」**在本片又拿到 3 个独立数据点**，
  而且**校招 VO 只有 2 轮技术面是常态**（2 例明确，第 3 例 "2 1-hours interviews"）。
  第三轮（Managerial / HM chat）是否算 VO 因人而异。

### B-15 · 语言选择：一条**同一人跨两次面试**的对照实验 ⭐

> 评论 3：「I used to give all my coding interviews in **C++** since uni. **I failed stripe phone screen for L2 2
> years back as it was very time consuming to code the problems they give in C++.** I have been working with
> **Java** for a few years now. So, I decided to give my coding interviews in Java this time for **L3** and I
> would say **it did help a bit**. **Python would have been the best for stripe interviews though.**」
> — 1tkb1iw，2026-05-22，**一手（同一人两次 Stripe 面试）**

- 这是本片**质量最高的语言证据**：同一个人 C++ 挂过、换 Java 有改善、并且自己得出"Python 最好"。
- **完全印证 LOOP_GUIDE §0 的语言结论**（Python/JS；Java/C++ 反复"做不完"）。
- **也给出了 level 信息**：同一人 2 年前面 **L2** 挂在电面，这次面 **L3**。

### B-16 · Go 可以用于 Stripe onsite 全套（**LOOP_GUIDE 没记过 Go**）

> 评论 14：「**Yep, I used Go for all of them…**」
> — 1mgcc99，2025-08-03（回复评论 12 关于 Java/Go 的提问）

- **一手，但极简短。** LOOP_GUIDE §0 只写了「官方语言清单里只有 JavaScript，没有 TypeScript」，**没有提 Go**。
- **新增事实（低置信）**：Go 是可选语言，且可用于全部 onsite 轮次（含 bug squash——意味着存在 Go 的 repo 场次）。
- **对我们无操作意义**（我们走 Python），但**如果 LOOP_GUIDE 的语言清单要更新，这是一条**。

### B-17 · AI 轮正在向其他岗位推广（HR 口径）

> 评论 9：「Also is this programming exercise an AI assisted round?」
> 评论 10（OP）：「**No, not for me, as android role But my HR said, they are slowly adding these type of
> interviews for other roles.**」
> — 1u0mgyy，2026-06-08，一手转述 HR

- 与 B-01（2026-08 校招 VO 已含 AI Coding 轮）**时间上吻合**：2026-06 是"正在推广"，2026-08 校招已经排上。
- **对 2026-09 面试的直接含义：backend 校招/社招都应该按"会有 AI 轮"准备。**

### B-18 · HM 轮开始问 **AI 相关的行为题**

> "Hiring Manager (45 mins): 40 mins of grinding on the resume, majorly on one complex project, going deep on it
> details(**not technical but more of a logistical and behavioural**). Along with some **AI focused behavioural
> questions**. Last 5 mins was my time to ask some questions."
> 评论 11：「what were the AI focused behavioral questions about?」
> 评论 12（OP）：「**Basic, about day to day use of AI in your life.**」
> — 1u0mgyy，2026-06-08，一手（Android）

- **LOOP_GUIDE §2/§8 完全没有这一条。建议新增。**
- **可操作**：准备一个 90 秒的"我日常怎么用 AI 写代码"故事——**要有边界感**
  （我用它做什么 / 我不让它做什么 / 我怎么验证它的输出）。这与 §6 AI Exercise 的评分维度是同一套价值观。
- ⚠️ 单一来源、Android 岗。标不确定。

### B-19 · 本片的**软广/低可信度**内容清单（避免污染证据库）

我在本片识别出 **5 条**带商业推广或疑似 AI 生成的评论。**它们的内容不应进入 LOOP_GUIDE**，
但因为其中两条给的是"按 LC 准备"这种与主结论相反的建议，必须点名：

| 位置 | 内容要点 | 推广对象 | 判断 |
|---|---|---|---|
| 1vhpsgz#1 (2026-08) | "I have been using this site to practice" | **aicodingprep.com** | 纯软广，零信息 |
| 1p5p8z7#1 (2025-11) | 「**I'd prep LC style DSA for the first hour, mostly mediums on arrays, strings, hash maps, and a simple graph or two**」 | **Beyz** + **IQB interview question bank** | ⚠️ **与"不是 LeetCode"主结论相反**，且同段落推两个产品 → 不采信 |
| 1o11q3k#3 (2025-10) | Python 调试 kata + 库清单 | **Beyz** + **IQB**（同一套话术） | 同上，**内容本身尚可但来源不可信**，见 §C-06 |
| 1ownvu4#4 (2025-11) | 「I've been **collecting some recent Stripe screen patterns + common mistakes**… Happy to share」→ 之后 6 条全是"DMed you / Replied" | 私信引流 | 典型题库引流，无实质内容 |
| 1vbpool#14 (2026-07) | Meta AI 轮 60 min 描述 | **Runable** | 讲的是 **Meta 不是 Stripe**，且带产品名 |

- **注意 1p5p8z7#1 和 1o11q3k#3 是同一套模板**（都点名 "Beyz coding assistant" + "IQB interview question bank"），
  时间相隔 6 周、出现在两个不同的 Stripe 帖下。**这是同一个账号群在刷。**

### B-20 · 其他零散事实

- **VO 后到 manager chat**：1oagvvw 类似形态在本片是 1ohkp31（2025-10-27，India 校招）——
  "Got done with my **manager chat** today. My VO rounds went pretty smoothly" → **manager chat 在 VO 之后单独排**，印证 LOOP_GUIDE §0。
- **实习 team match 时间**：> "Type of work: **Not sure until team matching in February**"（Dublin 实习，1oogutn 正文，2025-11-04，一手）。
  Stripe Dublin 实习的 team match 在**次年 2 月**。工作时间 "Hours: 9 am to 6 pm"。
  （该帖其余是 offer 比较/薪资，按 BRIEF 跳过。）
- **内部转岗（Stripe 员工一手）**：> "It's definitely possible, but easiest when done **when joining the company**
  … To do it as an internal transfer you'd have to find a "**business need**" … You'd have to be there **at least a
  year** and in good performance standing for that, but honestly **it'd be a bit hard as an L1, would realistically
  take a couple years**. **Stripe did relocate me from Canada to the U.S. but I did it while joining.**"
  （1oogutn#12，2025-11-04，**自述 Stripe 员工**）→ 与面试无关，但如果仓库有地点/relocation 记录，这是一条一手。
- **Integration Engineer 岗（≠ SWE）流程**：> "Next steps are a **Hiring Manager interview followed by a
  technical/coding assessment**"（1ox2n7y 正文，2025-11-14）。**0 条评论，无更多信息。存在但非本岗位。**
- **Bangalore 校招**：1oi4ht2（2025-10-28）整帖是"manager chat 之后有没有消息"的互问，**4 条评论无一给出实质信息**。无可用事实。

---

# C. 打法与教训（tactics）

> 只收可操作的。共 **9 条**。每条标注来源可信度。

### C-01 · Integration：**从第一个 sub-round 就写模块化的代码**，因为需求每一轮都会变 ⭐

> "The challenge here is time since **requirements change across sub-rounds** and thus **if the code is modular
> enough from the beginning, it helps**."
> — 1mgcc99 正文，2025-08-03，Dublin senior，**一手**

- **这是本片对 integration 最实用的一条。** LOOP_GUIDE §5 的"代码组织"是评分项之一，但没说清**为什么**。
- **可操作**：练 int01–int04 时，**part 1 就把 `build_request(params) / call_api(req) / parse_response(resp)`
  三个函数拆开**，哪怕 part 1 只用得上其中一个。不要为了快而全写在 `main()` 里——
  part 2 要求"用响应去调下一个 API"时，你能直接复用 `call_api`。

### C-02 · Bug Squash：定位到根因后，**先想清楚该在调用栈的哪一层修** ⭐

> "my interviewer gave me a small hint - **told me to implement the fix in some other function, higher up in the
> stack trace rather than the function I was fixing**. In her defense, **this fix was infinitely simpler**"
> — 1ohkp31 正文，2025-10-27，India 校招，**一手**

- **LOOP_GUIDE §4 目前只记了反方向的挂点（"大范围重写而非最小修复"）。这条是另一半：修得太靠下/太局部。**
- **可操作（成本 30 秒）**：找到 failing assert 的根因后，**先沿栈往上问一遍**
  "这个错误值是从哪一层开始变错的？在更上层修是不是更简单、影响面更小？"，**说出来再动手**。

### C-03 · Bug Squash：**别在没跑起来之前先读代码**；从失败测试倒推

> "In the bug bash round, you're given the entire repository … you'll be expected to **run the tests one by one
> and make them pass** by fixing the actual code."
> — 1mgcc99 正文，2025-08-03，一手

> "Task was to see the issue, understand it and **get the failing TC write**. For my reference a **passing TC was
> also given** in same issue. **You have to quickly go through the TC, see what's failing and move to that function
> and find the exact problem.**"
> — 1u0mgyy 正文，2026-06-08，一手（Android）

- **第二条给了一个 LOOP_GUIDE 没记的技巧**：issue 里常常**同时给一个通过的 TC 和一个失败的 TC**。
  → **可操作：先 diff 这两个测试用例的输入差异，那个差异就是 bug 的触发条件。**
  这比读源码快得多。**练 bs01–bs05 时刻意训练这一步。**

### C-04 · Bug Squash：**在 repo 里"移动"的速度本身是被评的**

> "**Practise more for bug squash and integration rounds**, as these are rounds are unconventional and check your
> real world working and handling of issues. … **Be fast in finding bugs and moving around in the repo.**"
> — 1u0mgyy 正文，2026-06-08，一手（Android，且该轮反馈为唯一的差评）

- **可操作**：练熟 IDE 的 **go to definition / find usages / call hierarchy / 全局搜索**，
  以及 Python 侧的 `pytest -k`、`pytest --pdb`、`pdb` 的 `u`/`d`（上下移动栈帧 —— **正好配合 C-02**）。

### C-05 · Integration：**别在语法上耗时间**（该帖作者的自我归因）

> "I personally **spent too much time on getting right syntax**, so was not able to move to next part. But was
> able to completely solve 1st part."
> — 1u0mgyy 正文，2026-06-08，一手（Android；该 OP **最终没拿到 offer**，评论 2 "nope"）

- 同帖评论 4 补了一条**统计性说法**：
  > "My recruiter told me for android roles had a **very bad passing rate for integration round**"（二手转述 recruiter）
- **可操作**：这与 B-15 的语言结论是同一件事的两面——**用你打字最快、不用查语法的语言**。
  对我们（Python）：把 `requests` / `urllib.request` 的 POST JSON、`json.load` 嵌套取值、
  `csv.DictReader`、二进制写盘这四段**背到肌肉记忆**（LOOP_GUIDE §5 备考动作已有，这条是一手的挂经背书）。

### C-06 · Bug Squash（Python）：调试 kata + 常见 bug 类型 + 标准库清单

> "I went through Stripe's virtual onsite in Python last cycle. What helped me was treating the bug squash like a
> quick debugging kata: **run the tests, read the traceback first, then add tiny prints or a quick pytest style
> check to pinpoint the failing branch. Watch for off by one, mutated default args, shallow vs deep copies, and
> None handling.** I leaned on **collections deque and Counter, heapq, itertools, bisect, and functools lru_cache**."
> — 1o11q3k#3，2025-10-08

- ⚠️ **来源可信度低**：同一段落推销 "Beyz coding assistant" 和 "IQB interview question bank"（见 §B-19）。
- **但技术内容与 LOOP_GUIDE §4 的"四类典型 bug"高度一致**，且 "**mutated default args**"（可变默认参数）
  和 "**shallow vs deep copies**" 是 LOOP_GUIDE **没有明确列出**的两个 Python 特有陷阱。
- **我的建议**：**不采信这条作为证据**，但**把"可变默认参数"和"深浅拷贝"加进 `loop/study/20-cards/python_debug.md`
  的自查清单**——这两个是 Python 真实高频 bug，代价极低，不依赖来源可信度。

### C-07 · 调试轮的练法：**让 LLM 给你造带 bug 的项目，刷 20 个**

> "**Ask ChatGPT to make you a python project folder with a bug in it and then debug it. Do like 20 of these and
> you should be golden.**"
> — 1snjn0e#13，2026-04-16（`How to prep for the debugging round?`）

- 来源不明（无自述经历），**但这是全帖 16 条评论里唯一一条给了具体可执行动作的**。
- 与 LOOP_GUIDE §4 备考动作「自己 clone 热门库注入 bug 计时 ≥4 次」**是同一个方法，只是量级从 4 提到 20**。
- **注意：本仓库已有 bs01–bs05（5 道）**，这条的价值是提示**数量不够**，可以用 LLM 批量造。

### C-08 · Integration/repo 轮的开场流程（低可信度，但动作本身零风险）

> "For the repo exercise, what helped me was a **quick 5 minute scan of README and tests**, then a **small plan in
> plain English before touching code**. **Run tests early, add logs to trace data flow, and write one tiny happy
> path first, then edge cases like idempotency or pagination.** … **Ask clarifying questions fast, leave clear
> TODOs if time is short.**"
> — 1p5p8z7#1，2025-11-24

- ⚠️ **软广**（Beyz + IQB，见 §B-19），且**同一条评论建议按 LC medium 准备，与主结论相反**。
- **但"先扫 README/tests 5 分钟 → 用大白话说计划 → 跑测试 → happy path → 边界"这条流程**
  与 LOOP_GUIDE §4 的 5 步硬流程、§5 的时间分配**完全一致**，**不构成新增，也不构成风险**。
- **唯一值得单独拎出来的一句：「leave clear TODOs if time is short」**——
  时间不够时**显式写 `# TODO: handle 429 with backoff — would add retry here`**，
  比默默留空好，因为面试官在评"你知不知道还差什么"。LOOP_GUIDE 没有这一条，**建议加**。

### C-09 · AI 辅助轮的 prompting 打法（**Amazon，不是 Stripe** —— 但形态相同，值得借鉴）⭐

**必须先说清楚：这一段说的是 Amazon 的 OA，不是 Stripe。** 我把它记进来是因为
本仓库 `cd07_transactions_rules_ai` 的练习方式目前**只有二手商业来源支撑**，而这条是**一手的、可操作的 prompt 策略**。

> "So I chose the MERN option and I had to implement 2 features and I could use AI's help in that sandboxed
> environment but the explicitly told that **you can't ask ai to solve the problem for you** so I figured this out;
> **Obviously they will monitor the prompts I input. Along with that, the quality of those prompts will also be
> crucial.** So I asked important questions like: **1. Summarise the issue for me. 2. Tell me what the developer
> has already implemented so I can know what already exists there** And a few more"
> — 1vbpool#25，2026-07-31，**Amazon OA 一手**

> "See majorly my approach was to **gain as much context as possible about what code is already there in the files
> they provided**. … Then after that **I clearly specified what I need to implement** … I asked the ai to **combine
> the context of code already given and the requirements** to have a better picture because I remember the
> requirements weren't that much clear in question. Then I did the implementation and **if there were errors so I
> pasted those in the chat to ask the assistant to guide me that: 1. What broke. 2. Is it a logical issue, a
> syntax issue or something else.** Basically **used the AI to guide me in the right direction** to know exactly
> what went wrong **because you can't just ask the AI to correct it** … Just chat with the AI keeping in mind that
> **someone will look at this shit and my conversation is a signature to how much I understand conversing with an
> AI model**"
> — 1vbpool#27，2026-07-31，**Amazon OA 一手**（评论 29 确认他**通过了**这一轮）

- **可迁移到 Stripe AI Exercise 的三个动作**（与 LOOP_GUIDE §6 记的打法一致，但更具体）：
  1. **开场三个 prompt 固定**：① "Summarise the requirements/README for me" ② "Tell me what's already implemented
     in these files" ③ "Combine the existing code context with these requirements and restate what I need to build"
  2. **报错时不要说 "fix it"，要说 "what broke, and is this a logical issue or a syntax issue?"**
  3. **心态锚点：prompt 记录会被人读，它就是你的评分材料之一。**
- **同帖另有两条同向的（均非 Stripe）**：
  > 「Instructions candidates are given for the **Meta** AI interview literally tell them to **not just ask the AI
  > for a complete solution**. In fact, their LLM's are specifically trained not to spit one out.」（#3）
  > 「I had about **1 hour to fix 4 bugs**. But I had to do it the classic way. i.e. **put breakpoints and see where
  > the code fails.** The AI only gives information about the repo and "meta"-advice (e.g. How to run the unit
  > tests). However, **you can't tell it "i have this bug. Scan the repo and fix it"**.」（#11，"a FAANG company"，**不是 Stripe**）
- **⚠️ 不要把这些写成 Stripe 的事实。** 它们是"2026 年这类轮次的行业形态"，仅此而已。

---

# D. 两个专项要求的直接回答

## D1 · `Stripe and Meta new AI interview experience` (2026-07-31) 逐条核查 ⭐

**结论先行：这一帖里有 Stripe AI 轮的亲历者，但他没有描述题目。帖子里所有详细的 AI 轮描述都不是 Stripe。**

### D1.1 · 亲历者身份认定

- **OP `/u/xxxconcatenate` 是 Stripe AI 轮的亲历者（一手）**。依据是正文第一句：
  > "**Just had stripe's new AI interview**, and had Meta's AI interview earlier this year."
- **他关于 Stripe 那一轮说的全部内容，逐字如下（这是全帖关于 Stripe AI 轮的一手信息的总和）**：
  > "Just had stripe's new AI interview, and had Meta's AI interview earlier this year. Also heard similar tech
  > companies start doing these kind of AI interviews. **It felt completely different from doing leetcode, and
  > actually felt more like testing your competencies when doing your work (considering our work heavily uses AI
  > now).** For context, **its the interview round where you are allowed to use AI models provided within
  > hackerrank to solve a more challenging problem** I'd like to know other people's perspective: 1. Do you think
  > this AI interview will replace leetcode? 2. Does anyone know of websites that allows you to practice? 3. Any
  > technical recruiters can provide insights on if their company is currently looking into doing something
  > similar? For someone who hates doing leetcode, I really hope the industry starts to move away from it"
- **他没有说**：题目内容、时长、part 数、可用的 AI 模型是哪个、AI 是否有使用限制、
  是否禁止直接要完整解、评分反馈、结果。**一个字都没有。**

### D1.2 · 36 条评论逐条来源归属（这是关键）

我把 36 条按"讲的是哪家公司"分类：

| 评论号 | 讲的是谁 | 是否一手 | 有无 Stripe AI 轮信息 |
|---|---|---|---|
| 1, 2 | 未具名公司（PR review 类、voice AI 类 3h onsite） | 一手 | ❌ |
| 3 | **Meta** | 二手（转述 Meta 给候选人的说明） | ❌ |
| 4 | 无（吐槽） | — | ❌ |
| **5** | **不明** | 疑似 OP 本人回复 | **⚠️ 可能是唯一一条额外的 Stripe 信息，见下** |
| 6 | **Amazon** | 一手 | ❌ |
| 7, 9, 11, 13 | "**a FAANG company**"（明说不是具名） | 一手 | ❌ |
| 8, 10, 12 | 追问 | — | ❌ |
| **14** | **Meta**（60 min：fix a bug / build a feature / optimize） | 二手 + **软广 Runable** | ❌ |
| 15–20 | Stripe **但是关于 LC 政策**，不是 AI 轮 | 混合 | ❌（已记在 §B-03） |
| 21, 22 | **DigitalOcean** | 一手 | ❌ |
| 23, 24 | 追问 / deleted | — | ❌ |
| 25–33 | **Amazon**（MERN/Python OA，含最详细的 prompt 打法） | 一手 | ❌（已记在 §C-09） |
| 34, 35 | 无关（转岗提问 / 求 repo） | — | ❌ |
| **36** | **直接向 OP 索要 Stripe 细节 —— 未被回答** | — | ❌ |

- **评论 5 逐字**：
  > "**I find the AI they provided largely useless, it's still down to your actual problem solving skills**"
  **我的判断：不确定这是不是 OP。** 帖子导出格式里没有作者名，无法确认。
  **如果**是 OP，那它是一条重要的一手评价（"HackerRank 提供的 AI 基本没用，最终还是靠你自己的解题能力"）；
  **如果不是**，它可能在说 Meta 或别的公司。**按 BRIEF 的要求，标为"不确定，不足以作为 Stripe 事实使用"。**
- **评论 36 逐字（这条本身就是证据）**：
  > "**Hey I have a similar interview at Stripe, could you please tell what kind of question was it? It would be
  > great if you could tell your stripe process in detail**"
  **→ 无人回答。这是本片第 14 次"问题面 → 没答案"。**

### D1.3 · 对仓库的直接结论

1. **`loop/LOOP_GUIDE.md` §6 里那条"AI Programming Exercise = 二手 · 商业来源 · 未经亲历者交叉验证"的
   证据等级标注，本次核查后 —— 保持不变，不能升级。**
   这一帖没有提供任何可以交叉验证 `/u/interviewdb` 那篇内容（transactions + rules、30 分钟、
   前 part 关键词匹配 / 后 part AND/OR）的一手材料。
2. **但有两条一手细节可以从二手降格里"救"出来，因为 OP 本人说了**：
   - ✅ **平台确认：HackerRank 内嵌 AI 模型**（"AI models provided within hackerrank"）——
     这与 `/u/interviewdb` 的描述一致，**现在有一手背书**。
   - ✅ **难度确认：题目比常规轮更难**（"a more challenging problem"）——
     与 §6 记的"自己手写 80% 概率写不完"同向，**现在有一手背书**。
   - ❌ **题目内容（transactions + rules）：仍然零一手证据。`cd07` 的题面来源依旧只有那一个商业二手帖。**
3. **另有一条独立的一手证据把这轮的存在性钉死了**：2026-08-07 的 `Stripe newgrad virtual onsite`
   正文把 "**AI Coding**" 与 Integration、Bug Squash 并列为自己 VO 的三轮之一（§B-01）。
   → **"AI 轮存在且已进入校招 VO"是确定的；"AI 轮考什么"仍然不确定。**

---

## D2 · bug squash 到底是什么 bug / 什么库 / 几个 bug —— 逐字汇总 ⭐

**结论先行：库拿到了（一手，且与我们题库对得上）；数量拿到了但互相矛盾；具体 bug 内容——本片仍然一个都没有。**

### D2.1 · 库（**本片最大的收获**）

> "In the bug bash round, you're given the entire repository of a built-in library, **for instance, for python, it
> could be either "requests" or "mako"**."
> — 1mgcc99 正文，2025-08-03，**Dublin senior SDE，一手**

- ✅ 对上 `bs01_mini_template_engine`（**minimako**）
- ✅ 对上 `bs02_mini_http_client`（**minihttp**）
- **这是前三片 12 次追问一次都没拿到的东西。** LOOP_GUIDE §4 原来记的库清单来源是 Blind/Coditioning，
  **现在 Python 侧有了 Reddit 一手交叉验证。**
- **同帖还给了"为什么难"的原因（可操作）**：
  > "The challenge here is again time since, **if it is an unfamiliar library like mako, it is quite challenging to
  > figure out what it does in the first place.**"
  → **准备动作：不要只练"修 bug"，先花 15 分钟练"5 分钟内摸清一个陌生库在干什么"**
  （读 README → 读顶层 `__init__.py` 的导出 → 读一个 example → 读失败测试）。
  **这正是 `bs01` 的 CODE_GUIDE 存在的意义，但真实场景没有中文导读。第二遍起别读 CODE_GUIDE 是对的。**
- **JS 侧：本片零证据。** 1ps3akr 的 OP 明确问 "**what are the repos which are probable for this round in JS?**"
  —— **6 条评论无一回答**。LOOP_GUIDE §4 记的 Express / Day.js / React 竞态**未获印证**。
- **Java 侧：本片零证据。** 1ohkp31 下面有 3 条一模一样的 Java 求助
  （"I have bug squash round of stripe, And i chose Java lang, can you please tell me like what kind of bugs are
  there?"，评论 5/7/17）—— **OP 全部回"DM me"，无一公开回答。**

### D2.2 · 几个 bug（**矛盾**，已在 §B-矛盾-① 详述）

| 数量 | 逐字 | 来源 | 岗位/地点 | 等级 |
|---|---|---|---|---|
| **4–5** | 「There'd be **4-5 unit tests failing**」 | 1mgcc99 正文，2025-08-03 | Dublin, senior SDE | 一手 |
| **1** | 「**There was only 1 failing test in the repo which we had fixed**」 | 1ohkp31 正文，2025-10-27 | India, 校招 | 一手 |
| （3） | LOOP_GUIDE 现记「按 3 个准备」 | 前几片 1oagvvw | Dublin, 校招 | 一手 |

**→ 1 / 3 / 4–5 三个数字并存，且都是一手。"按 3 个准备"这个说法不成立，应改为"数量不定，按逐个修准备"。**
注意 senior（4–5）明显多于校招（1、3），**可能与 level 相关**，但 3 个样本不足以下这个结论，**标为假设**。

### D2.3 · 具体是什么 bug —— **本片零收获，但我把所有"接近"的表述都列出来**

| 描述 | 逐字 | 来源 | 可信度 |
|---|---|---|---|
| 修复位置在栈的上层 | 「told me to implement the fix in some **other function, higher up in the stack trace** rather than the function I was fixing」 | 1ohkp31 正文，2025-10-27 | **一手**（唯一一条关于 bug **形态**的一手线索） |
| Java 场次涉及"advanced Java" | 「I realized I wasn't as strong as I wanted to be in **advanced Java and deep debugging**」 | 1tkb1iw 正文，2026-05-22 | 一手，但"advanced Java"是什么**追问 5 次全部转私信** |
| JS 场次的 bug 类型 | 「In JS, expect **logic errors, edge cases, async/await or promise issues, wrong conditions, and small broken implementations**. It's more than just null checks, but not very complex」 | 1ps3akr#1，2025-12-21 | ⚠️ **自称一手但我判低可信度**（泛化口吻、说的是"a similar round"） |
| bug 的来源 | 「Could be either.」（回答"是招聘团队注入的还是该库 GitHub 上真实报过的 bug"） | 1mgcc99#6，2025-08-03 | **一手** |
| issue 里同时给通过和失败的 TC | 「For my reference a **passing TC was also given** in same issue」 | 1u0mgyy 正文，2026-06-08 | 一手，**Android 岗** |

**→ 关于"具体哪个 bug"，本片依然是 0。** 但 §C-02（修复层级）和 §C-03（diff 通过/失败 TC）
这两条**打法**是本片从 bug squash 里榨出来的真正新东西，它们不依赖具体 bug 内容。

### D2.4 · `How to prep for the debugging round?` (2026-04-16) 单独说明

**这一帖对 bug 内容零贡献，但确认了一件事：提问者是 Stripe backend、在 final loop。**
> 评论 7：「Is this a phone-screen round?」→ 评论 8（OP）：「**No , got past that. Now I'm in the final loop**」
> 评论 9：「Is this for mobile development?」→ 评论 10（OP）：「**No, backend**」
> 评论 11：「Is this for DoorDash ?」→ 评论 12（OP）：「**Stripe**」

- 16 条评论里，**5 条被删除或被 mod 因"DM farming"删掉**：
  > 评论 6（AutoMod）：「Your comment has been removed. **We do not allow DM farming. All of the conversation must
  > happen within the post itself.**」
  → **这解释了为什么 Reddit 上 Stripe 题面永远拿不到**：给答案的人在引流，引流被 mod 删，
  剩下的公开内容就只有泛泛之谈。**这条对 BRIEF 的方法论结论（往 1point3acres / Blind 倾斜）是又一个支撑。**
- **唯一有用的评论就是 C-07 那条**（让 ChatGPT 造 20 个带 bug 的项目）。
- 评论 2 顺带确认了 OP 打算怎么练：「**Thank you ! I'll probably try using Claude or ChatGPT as well to generate
  some** thanks again」。

---

# E. 附：本片"问题面 → 未被回答"的次数统计

BRIEF 说"一个 slice 里同一条信息被多人重复说，每一条都记，重复次数本身是信号"。
**本片最强的信号是负向的**：

| 帖子 | 追问题面的次数 | 结果 |
|---|---|---|
| 1vbpool (AI 轮) | 1（评论 36） | 无人答 |
| 1u0mgyy (Android) | 1（评论 13：「like in the repo questions, what type of questions were they」） | 无人答 |
| 1tkb1iw (校招) | 5（评论 6/15/17 + 2 条 DM 请求） | 全部转私信 |
| 1ohkp31 (校招 bug squash) | 3（评论 5/7/17，全是 Java bug 求助，**逐字重复同一句话**） | 全部「DM me」 |
| 1ps3akr (JS bug bash) | 2（正文问 JS repo；评论 6 问经验） | 无人答 |
| 1mgcc99 (Dublin senior) | 3（评论 15/16/19：「exact questions」「exact types and difficulty levels」「what kind of repository」） | OP 明确拒答：「**PLEASE DO NOT DM ME. IT'S BEEN A WHILE AND I DON'T REMEMBER ANYTHING MORE THAN WHAT'S IN THIS POST.**」 |
| 1snjn0e (debugging prep) | 1 | 被 mod 以 DM farming 删 |
| **合计** | **≥16 次** | **0 次拿到具体题面** |

**前三片记的是 12 次，本片再加 16 次 —— 累计 ≥28 次追问，零次得到 Stripe 的具体题面。**
**这条方法论结论现在是压倒性的：不要再往 Reddit 投抓取预算找题面；Reddit 的产出是流程事实、挂经和打法。**
（本片恰恰印证了这一点：**A 节 0 道新题，B 节 20 条事实 + 4 条矛盾，C 节 9 条打法。**）

---

# F. 给协调者的改动建议清单（按优先级）

| # | 位置 | 建议 | 依据 | 置信度 |
|---|---|---|---|---|
| 1 | §4 bug 数量 | 「按 3 个准备」→「**1–5 个不等，按"逐个跑逐个修"准备**」 | 两条新一手：1 个 / 4–5 个 | **高** |
| 2 | §4 库清单 | Python 的 `requests`/`Mako` **加一条 Reddit 一手来源** | 1mgcc99 正文 | **高** |
| 3 | §4 新增挂点 | 加「**修复层级选错**（该在栈上层修却在下层修）」 | 1ohkp31 一手 | **高** |
| 4 | §4 新增技巧 | 加「issue 里若同时给 passing/failing TC，**先 diff 两个测试的输入**」 | 1u0mgyy 一手（Android） | 中 |
| 5 | §4/§5 | 「IDE/debugger 使用是**显式评分项**」（两条一手，措辞要加强） | 1mgcc99 + 1u0mgyy | **高** |
| 6 | §0 / §6 | AI 轮**已进入校招 VO**；HR 说正在向其他岗位推广 | 1vhpsgz(2026-08) + 1u0mgyy#10 | **高** |
| 7 | §6 | AI 轮的**平台（HackerRank 内嵌 AI）与难度（more challenging）现在有一手背书**；**题目内容仍无一手** | 1vbpool 正文 | **高** |
| 8 | §0 语言 | 补「**电面可与 onsite 用不同语言**（onsite 五轮必须同一门）」 | 1mgcc99#13 | 中（单一来源） |
| 9 | §0 语言 | **Go 也是可选语言**，且可用于全部 onsite | 1mgcc99#14 | 低（单一、极简短） |
| 10 | §2/§8 | 新增「**HM 轮会问 AI 相关行为题**（日常怎么用 AI）」 | 1u0mgyy 一手（Android） | 中 |
| 11 | §3 | 「无自动测例」补一句「**但面试官侧可能有 TC 来判定 part 通过**」 | 1u0mgyy 一手（Android） | 中 |
| 12 | §5 | 加 C-01「**part 1 就拆 build/call/parse 三函数**」和 C-08「**时间不够写显式 TODO**」 | 1mgcc99 正文；1p5p8z7#1（软广但动作无害） | 中 |
| 13 | §0 | 「Dublin 校招无 integration」限定为个例；**Ireland 在职岗 loop 是有 integration 的** | 1t0v98p 正文 | 中 |
| 14 | §4 AI 政策 | 「禁 AI」明确到「**含 IDE 自动补全**」 | 1mgcc99#11 一手 | **高** |
| 15 | study 卡片 | `python_debug.md` 加「**可变默认参数**」「**深浅拷贝**」两个自查项 | 1o11q3k#3（来源不可信，但内容零风险） | 低（作为练习项而非证据） |

