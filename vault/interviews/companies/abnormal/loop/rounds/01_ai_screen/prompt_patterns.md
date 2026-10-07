# 提示范式库

> 来源：Hello Interview《Learn AI Coding》带评级会话，本机存档 `sources/local/hellointerview-ai-coding/`（付费内容，不入库）。用到：38 份会话概览（Strong Hire 12 · Hire 14 · Lean Hire 12）；其中 7 份有完整聊天记录（s000 s001 s002 s003 s008 s009 s011，全部 Strong Hire）。引文 ≤ 20 词，其余为转述；模板提示词为本文自写。心法 X1–X10、技法 T1–T12 见 `claude_playbook.md`。

## 范式

每条：阶段 · 对应 T/X · 模板（`<…>` 为填空）· Strong Hire 怎么说 · 为什么有效 · 怎么失败。

### P1 只读地图 + 给测试加注释 + 生成 curl
- 阶段：0–10 分钟，探索。T1 / X2。
- 模板：
  ```
  Read-only: don't modify anything. Give me the repo layout, entry points, data flow and the test
  command. Then add a one-line comment above each existing test saying what it checks, and give me
  one curl per endpoint so I can call the service by hand.
  ```
- 原话（s011）：让 AI 给每个测试加注释，再给每个接口一条 curl。s010 同样先要"每个文件一段摘要"。
- 有效：测试注释把"已覆盖什么"变成可读清单；curl 让你在改代码前先亲手看到真实行为。s018 还追加"Trace one item through the entire system"，一条数据走完全程。
- 失败：只让 AI 汇总，自己一个文件都不打开（X7）；s019（Lean Hire）开场只要 Javadoc 注释，没有跑过任何行为。

### P2 生成项目指南，再删掉它的 bug 猜测
- 阶段：开场。T1 / T6。
- 模板：`/init`，随后 `Remove the gotchas / bugs section from CLAUDE.md for now — keep neutral facts only (commands, architecture, conventions).`
- 原话（s005 s009）："remove the gotchas / bugs"。
- 有效：指南保留命令与架构，不让 AI 过早"认定"缺陷，后面的 bug 清单仍由你先列（见 P5）。
- 失败：保留 AI 写的 bug 清单，后面的审计就变成对它的复述（违反 X3）。

### P3 先陈述假设，让 AI 证实或纠正
- 阶段：读码中。T3 / X3 / X4。
- 模板：
  ```
  I think <hypothesis about the code>. Confirm or correct me, citing file:line. If it can't happen
  in this process / entry point, say so instead of proposing a fix.
  ```
- 原话（s024）：先说"我已经能看出一些问题，告诉我对不对、漏了什么"；又问两个 audio_url 的 id 会不会撞。s013 反问"start_worker 只在 main 调用，两个 worker 从哪来"。
- 有效：AI 纠正了两条错误理论（id 冲突、lastrowid）。反问"这个场景在本进程里真能发生吗"能挡掉 AI 虚构的竞态。
- 失败：不核对就接受 AI 报告的 bug，白修一个不存在的问题（T9 ①）。

### P4 让 AI 采访你，再"实现计划"
- 阶段：10–16 分钟，读题。T2 / X4。
- 模板：
  ```
  Interview me one question at a time about <feature>: contracts, return values, edge cases,
  concurrency. Recommend an answer to each. When done, write PLAN.md. Then I'll say "implement the plan".
  ```
- 原话（s023）：先要求被采访实现细节与设计，再产出计划。计划里钉死了缺键返回值、线程安全、写入返回什么。
- 有效：所有会让 AI 猜的合同都成了文字；之后一句"implement the plan"没有歧义。
- 失败：让 AI 自己"挑最重要的"而不核对（s023 的缺口：测试范围由 AI 自述覆盖，没让它逐项对应到测试）。

### P5 我列你补，合并后排序
- 阶段：13–16 分钟，方案。T3 / X3。
- 模板：
  ```
  Here's my numbered list: <3–10 problems>. Verify each against the code, then add only what I
  missed. Merge both lists into one ranking by <customer impact | severity>. Don't rewrite my items.
  ```
- 原话（s010）：把你的点加进我的，按这个优先级排成一张表。s009 先写了 14 条再问"还有吗"，AI 补了过期检查和路径穿越两条最重的。
- 有效：38 场里 Strong Hire 最高频动作；AI 的补充受你的框架约束，排序决定权留在你手里。
- 失败：列表出来后不排序就"fix all"（s011 一次批量修完，把 CSRF 与 GET 重设计推迟了事）；或只列不做（见反范式 A3）。

### P6 多视角并行审计，人工分类
- 阶段：探索末或第 15 分钟左右。T10 / X4。
- 模板：
  ```
  Spawn <2–3> subagents, one lens each: (1) logic bugs, (2) security, (3) production readiness.
  Read-only. When done, give one merged list ordered by customer impact. Do not change code.
  ```
  拿到清单后自己标：applicable / park / discuss / out of scope，再动手。
- 原话（s001）：三个子代理分别查逻辑、安全、生产就绪，"Order them in terms of customer impact"。s000 开场 15 分钟发了两路审计。
- 有效：每个子代理只带一个视角，输出可比；分类这一步是你的判断，不是 AI 的。分类结果写进文件（P7）。
- 失败：子代理数量不加分（见 `claude_playbook.md` §四）；把合并清单整张接受，按 AI 的顺序做。

### P7 把决定写进文件
- 阶段：方案、里程碑之间。T6 / T12 / X9。
- 模板：
  ```
  Save the decisions we just made to <TASKS.md | CLAUDE.md>: priority list, what's parked, what's
  out of scope. Pause after writing it — don't start implementing.
  ```
  规则版：`From now on, go over approach and decisions before you implement. Add this to CLAUDE.md.`
- 原话（s001）：明确保存这些决定，写完后暂停。s000 第 14 分钟把"先讲方案再实现"写进了 CLAUDE.md。
- 有效：规则只说一次就会一直生效；任务文件是收口时核对"点了名的有没有做完"的底账。
- 失败：只写不执行：s000 的邮件 outbox 计划写进了 TASKS.md，却始终没把发信移出请求路径。

### P8 先要空壳，再口述设计
- 阶段：方案。T5 / T6 / X1。
- 模板：
  ```
  Create the skeleton: files, class and method signatures with empty bodies and one-line docstrings.
  Don't implement anything — I'll dictate the data structures and algorithm next.
  ```
  下一条：`Use <structure A> for <purpose> and <structure B> for <purpose>; on <operation> do <step>. Now fill in the bodies.`
- 原话（s002，Principal）：先搭骨架，架构由我口述，让一个子代理另提测试方案。s015、s036 也先锁接口再实现。
- 有效：设计在你手里，AI 变成打字员；接口先锁定后，测试可以并行写。
- 失败：不加"keep it empty"，AI 立刻开写实现（s003 被迫发"revert your changes, we are still only planning"）。

### P9 先摆自己的设计，请 AI 挑错
- 阶段：方案。T5 / X1。
- 模板：
  ```
  My design: <structure + why>. Poke holes: complexity of each operation, what breaks under
  <concurrency | large inputs>. Compare with <cheaper alternative> in 5 lines. Don't edit anything.
  ```
- 原话（s007）：先说"用 hash map 存值，再用一个按时间戳的 map"，问怎么看；AI 指出找最旧项要 O(n) 扫描。s014（Junior）故意提出 list 方案逼 AI 把复杂度讲清。
- 有效：设计选择落在可陈述的理由上，面试官听得到推理（X10）。
- 失败：让 AI 先推荐，你只负责同意（X1）。s036 把"验证 O(1)"留到编码之前，是好样子。

### P10 先要选项，不要代码
- 阶段：每个实现切片之前。T5 / T6 / X1。
- 模板：
  ```
  Before implementing <item>, give me 2–3 options with trade-offs and your recommendation. Don't
  edit files. I'll pick.
  ```
  变体：`Don't make any changes, propose how this would look.`（s000 提议把连接管理改成 with 语法）。
- 原话（s005）："Before implementing, give me choices"，随后按时间压力选更便宜的一项并说出口。
- 有效：每个决定你亲手落了一次；时间紧时能说清为什么选便宜方案。
- 失败：AI 被问意见却直接动手（s021 当场抓住并质问"我只是问意见，你已经实现了？"）。

### P11 先写红测试，明说不要修
- 阶段：每个 bug 之前。T7 / X6。
- 模板：
  ```
  Write a failing test that reproduces <bug> through <public entry point>, in <existing test file>.
  Test failures are fine — don't fix anything. Stop after the test; at most 3 attempts to make it red.
  ```
- 原话（s000）："Test failures are fine, don't fix anything"。s001 加了三次尝试的上限；s004 要求回归测试先于任何改动。
- 有效：每个修复都有明确的"转绿"目标。key-moment 文本里出现该动作的会话：Strong Hire 3/12，Lean Hire 1/12（正则统计，是下界）。
- 失败：红测试其实是环境问题却让 AI 去 mock 绕过（s026 两次要求 mock，是 AI 拒绝后才发现是真 500）。

### P12 点名机制，不只说症状
- 阶段：实现，M1 开始前。T5 / X1。
- 模板：
  ```
  Fix <symptom> using <mechanism>: <e.g. conditional UPDATE … WHERE state='free' as compare-and-swap;
  unique index as backstop>. Order: <backstop first>, then <app-level fix>. Then <edge test>.
  ```
- 原话（s000）：唯一索引和外键先加，"在原子预订修复之前"。s019（Lean Hire）也点名了 CAS，但批量打包了五件事。
- 有效：修复落在你要的位置，评审时能对着机制复述。
- 失败：同一时刻打包多个独立修复，之后无法逐条验证（见反范式 A1）。

### P13 追问生成的修复：解释、反问、对号
- 阶段：每个 diff 回来后。T9 / X7。
- 模板：
  ```
  Explain this change: how do we know <the claim> holds? Which test would fail on the old code?
  Show me the one test that covers it.
  ```
- 原话（s010）：对 AI 写的 CAS 注释说"Explain this"。s009："你确定不需要把 SELECT 和 UPDATE 放进同一个事务？" s000 追问 AI 如何确认行已被更新。
- 有效：逼出 AI 的论证，也逼自己能复述（X7）。s013 问"你加的是什么测试，为什么"。
- 失败：看到全绿就收下。s001 的两线程测试通过，但最终设计是多进程，跨进程保证从未被测。

### P14 点名测试用例，读回最难的一条
- 阶段：写测试。T7 / T9。
- 模板：
  ```
  Write tests for exactly these cases: <case list incl. boundary, invalid, rule-based>. Skip cases the
  existing suite already covers and list which test covers each. Then show me the hardest one.
  ```
- 原话（s028，Lean Hire）：把测试清单逐条交给 AI，再要求读回其中最难的一对；s038 要 AI 列出测试覆盖了哪些场景。
- 有效：套件对准你在意的行为，而不是模型的默认猜测。
- 失败：只说"跳过已覆盖的"而不要求对应关系（s023）；清单后没有真实运行（s014 返工后没让它重跑）。

### P15 把真实输出贴回去
- 阶段：验证、调试。T8 / X8。
- 模板：
  ```
  Here's the actual output of <command>:
  <paste>
  Line <n> is wrong because <expected vs got>. Reproduce it with one failing test first, then fix.
  ```
- 原话（s003）：贴上三次 place 的真实 CLI 输出，要求"一个房间只能有一个机器人"。s032 要 AI 先复现并确认失败，再由自己选修复策略。
- 有效：证据逼出精确修复；你选策略，AI 只执行。
- 失败：用子代理"玩一遍"，对方说没问题就信了（s003 的缺口：解析器仍接受负数与非整数）。

### P16 列出生产缺口，再选一个命名的切片
- 阶段：M1 之后、约 30–40 分钟。T2 / T12 / X9。
- 模板：
  ```
  What are the main gaps to production for <service>, ranked by customer impact? I'll choose. Implement
  only <#1 and #3>; park the rest in TODO.md with one line each.
  ```
- 原话（s025、s030）：先让 AI 说缺口，再自己决定动哪几项；s016 把其余项记入 todo.md。
- 有效：AI 给菜单、你点菜；未做的项有书面记录，收尾时可念出来。
- 失败：只要清单、不选，或选了时间做不完（s017 把限流列为首要，预算耗尽没写一行）。

### P17 一轮对抗式审查，然后分类
- 阶段：约第 40 分钟。T10 / X7。
- 模板：
  ```
  Act as a malicious attacker / an overconfident-author skeptic reviewing the current diff against the
  ticket. Max 5 findings, ranked, with a repro for each. Don't validate or summarize.
  ```
- 原话（s027）：让 AI 扮演攻击者去攻击账号；s033 另开第二个 AI 对着原题与实时工作树提反对意见；s000 修复落地后再审一次。
- 有效：修复后重审能抓到修复引入的新问题；第二个 AI 能提醒范围蔓延。
- 失败：审查放到最后两分钟，没有时间变成修复（s029）；或者对审查意见按一方说了算（s033 辩护自己的扩展而不是补题目要求的转向命令）。

### P18 收口：证据 + 已知缺口
- 阶段：42–45 分钟。T11 / T12 / X8 / X9。
- 模板：
  ```
  Run typecheck and the full test suite now and show me the output. Then call the real entry point
  (curl / CLI) for the main flow. Finally list every item we named today as done / out of scope.
  ```
- 原话（s005）：收尾做 typecheck 加一次目标测试，跳过慢的退避测试，并说明原因。s009 同时用 curl 打实机接口。s027 结尾要"只总结、不改代码"。
- 有效：说"done"之前有新鲜证据；跳过什么要说出来。
- 失败：s009 的 rate limiting 最后一条提示 AI 还在追问，没有落地却没记录；s000 把启动路径问题记为 known gap，是可接受的写法。

## 反范式

| # | 反范式 | 证据 | 修正 |
|---|---|---|---|
| A1 | 一条提示打包多个独立改动（原子更新 + 外键 + 时间格式 + 校验 + 重试 + 鉴权） | s019 同一时刻连发五项；s011 "fix all" | 一次一片，每片配测试（T7）；先排序再逐项（P5、P12） |
| A2 | 接受"没发现问题"：子代理说无问题就继续 | s003 玩测子代理空手而归，解析器仍有缺陷；s031 一条大提示驱动大 diff，之后没有任何追问 | 自己再试两个边界输入；要求 AI 对号指出哪个测试覆盖了该断言（T9、P13） |
| A3 | 审查放在最后一分钟，或点了名没交付 | s029 最后两分钟才做分级审查；s017 限流排首位却零行；s010 发信同步阻塞被自己列入清单却没改 | 第 40 分钟审一轮；第 45 分钟前每条要么做完要么写进 NOTES（T10、T12、X9） |
| A4 | 测试只证明你已相信的事 | s036 压力测试只查大小不变量，不查最近使用序；s016 分片封装完全无测试；s007 并发论点只写在注释里；s001 线程测试却部署多进程 | 在红测试里复现真实形态（进程/线程）；对每条论点问"哪个测试会在旧代码上失败"（T7、T8） |
| A5 | 让 AI 把失败的测试 mock 掉，或让测试迁就代码 | s026 两次要求 mock，其实是真 bug | 失败先走 Prove-It：一条命令复现症状，再列假设（T8）；测试只在确认它错了时才改（T6） |
| A6 | 已知风险写成 TODO 注释就当处理了 | s028 迭代器并发风险只写 TODO；s024 连接泄漏留作 TODO | 在 NOTES 里写成 known gap 并说出口；能在 5 分钟内修的就修（T12） |
| A7 | 重写后不重跑，或文档数字过期 | s014 返工后没让 AI 重跑；s012 基准是加锁前的数字 | 每次改动后重跑相关测试，关闭前跑全量（T11） |
| A8 | 扩展超出题目，反而漏了题目点名的要求 | s033 辩护箭头键扩展，题目里的转向命令缺失；s021 AI 被问意见却已动手 | 开工前复述题目要求并对照 diff（X9）；"只给建议"类提示明写 "Don't edit"（P10） |
| A9 | 终局提示过短且含糊 | s030 末尾只发"Implement 2"，AI 指出有歧义；s019 在 61 分钟才追问 200 的异常，没解决 | 最后 10 分钟每条提示都写清对象和验收（P18） |

## 对话节奏

脚本：`/Users/chizhang/.claude/jobs/03046b1d/tmp/rhythm.py`、`freq.py`（不在仓库内）。限制：7 份聊天导出把 AI 回复折叠成"Show N more replies"，用户消息与 AI 叙述行混排，无法在聊天文本里可靠切出每条用户消息，所以下面的消息数、首次跑测试等数字取自站点为每场会话给出的统计头（脚本从概览文件解析），阶段分布取自 7 场的 68 个 key moment（站点挑选的节点，不是全部消息）。

| 会话 | 消息 | 时长 min | 提示长度中位数（字符） | 首次测试 min | 排队追发 | 子代理任务 | AI 跑测 / 自己跑测 |
|---|---|---|---|---|---|---|---|
| s000 | 49 | 64 | 92 | 1 | 5 | 2 | 22 / 26 |
| s001 | 65 | 63 | 93 | 14 | 11 | 5 | 19 / 3 |
| s002 | 21 | 29 | 391 | 16 | 10 | 9 | 4 / 0 |
| s003 | 23 | 43 | 103 | 9 | 3 | 1 | 13 / 0 |
| s008 | 9 | 51 | 125 | 7 | 9 | 0 | 10 / 0 |
| s009 | 27 | 55 | 30 | 6 | 24 | 0 | 13 / 8 |
| s011 | 14 | 52 | 29 | 46 | 13 | 0 | 1 / 4 |
| 中位数 | 23（9–65） | 52 | 93（29–391） | 9（1–46） | 10 | 1（0–9） | — |

- 速率：每分钟 0.18–1.03 条，中位数 0.53（约每 2 分钟一条）。
- 提示长度：站点的会话中位数 29–391 字符，7 场中位数 93；68 个 key moment 的提示行，词数中位数 14.5（均值 17.9，最长 56，n=68）。多数是短而带指令的句子；长提示出现在 P5 的清单、P8 的数据结构口述（s002）。
- 阶段分布（68 个 key moment，按分钟）：0–10 为 13，10–20 为 11，20–30 为 13，30–45 为 17，45 以后 14。首个 key moment 的分钟：4、5、1、4、7、3、7（中位数 4）。
- 首次跑测试：7 场中位数第 9 分钟。s000 第 1 分钟（先审计覆盖率），s011 第 46 分钟（先逐端点读码，之后多在自己终端跑测）。
- "先提议、别动手"：对 key moment 文本做正则，7 场里匹配 5/68；38 场里 Strong Hire 5、Hire 5、Lean Hire 5（均为 12/14/12 场中的数目；正则偏粗，只作数量级）。s000 把它升级成了 CLAUDE.md 里的永久规则。
- 失败测试先行：Strong Hire 3/12、Hire 1/14、Lean Hire 1/12（同样的正则，下界）。
- 用子代理（站点统计）：Strong Hire 4/12、Hire 3/14、Lean Hire 3/12。
- 消息数中位数：Strong Hire 22（12 场）、Hire 16（10 场有统计）、Lean Hire 13.5（12 场）；首次测试中位数：Strong Hire 6.5、Lean Hire 8.5（8 场有数据）、Hire 10（5 场有数据）。

## 新增到 claude_playbook 的候选

1. 清理生成的项目指南：`/init` 后删掉其中的 bug 猜测，保持中性事实（P2，s005/s009）。
2. 先陈述假设，并问"这个场景在本进程里真会发生吗"，防止修虚构的竞态（P3，s024/s013）。
3. 让 AI 采访你，所有合同写进 PLAN.md，再一句 "implement the plan"（P4，s023；T2 的反向）。
4. 点名机制与顺序（唯一索引与外键先于原子更新），而不是只说症状（P12，s000/s019）。
5. 测试到论点的对应表：要求 AI 说明每条断言由哪个测试覆盖，并读回最难的一条（P13、P14，s028/s010）。
