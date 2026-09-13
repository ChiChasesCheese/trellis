# Stripe OA / HackerRank 题目 — 中文来源 sweep（截至 2026-08-25）

## 0. 方法 & 访问情况

- ~60 次 WebSearch（用完 200 配额中的大部分）+ ~120 次 WebFetch。
- **1point3acres.com/bbs/*（面经帖）全部 403**（含 forum.php?mod=viewthread、r.jina.ai、allorigins 代理；web.archive.org 被环境禁止）。帖子内容只能靠搜索引擎摘要碎片。
- **1point3acres.com/interview/problems/*（题库）可访问首屏**：题目标题、stage（OA/phone/onsite）、last-asked 日期、tags、部分题干；全文付费。
- **1o24bbs.com 连接被拒（ECONNREFUSED）**，1024bbs.net 域名不存在。只有搜索摘要。
- csoahelp.com、programhelp.net（含 zh_tw）、oavoservice.com、learncswithus.com、cscodehelp.com、interviewfox.ai、linkjob.ai、extrabrain.app、prachub.com、dev.to、medium 可正常抓取。
- leetcode discuss 帖大多 403。知乎/CSDN/掘金/小红书 无 Stripe OA 专帖（搜索无命中）。libaedu.com 题库标题可见，内容付费。
- 可信度标注：**high** = 原始详细帖/题库原文；**medium** = 二手转述但细节一致；**low** = SEO/AI 农场改写。

## 1. 考试形式（多来源一致）

| 时期 | 形式 | 来源 |
|---|---|---|
| 2020–2021 University HackerRank Challenge | 2 题：1 编程（"Stripe in a Box" / card network）+ 1 开放讨论/essay | 1point3acres 677836/677770 摘要 |
| 2021-09 NG | 60 min 1 题（Beta invite / bot） | 1point3acres 793401 摘要 |
| 2024 (某 OA) | **75 min：1 coding + 1 分析/essay 题**（"如何改进第一题代码"）；题：Radar Rule / Platform Balance | 1point3acres 1102706、446019、442716 摘要；1024bbs 10992/5821 摘要 |
| 2024-09 → 2026 University Recruiting (intern + NG) | **HackerRank，60 min，1 题，3–5 个 Part 依次解锁**（Part N 通过才给 Part N+1）；~17–25 个 test（有 hidden）；语言自选；只能 print 调试；有人 22/25、16/19 | 1point3acres 1085478/1091979/1101931/1147871/1163662 摘要；leetcode 7344444/7428741；programhelp；interviewfox |
| 2026-04 起 | 题库更新（Join Dataset 新题） | programhelp zh_tw 2026-04-28 |
| MLE NG OA 2026 | 2 题：PyTorch 分类 + pandas 查询 | programhelp 2026-04-10 |

反复出现的评价："题干很长，读题 ~10 min"、"不是 LeetCode，是 data processing / state simulation"、"逻辑好写但最后几个 test 卡住（边界/格式）"、"题库非常小"（programhelp 2026-03：约 3 道轮转）。

---

## 2. OA 题目清单（按频率/近期性排序）

### 2.1 Jupyter / WebSocket Load Balancer — `route_requests`  【confidence: high】

**来源**
- 1point3acres thread-1154050 「【求米】Stripe 2025 SWE Intern OA分享（含笔记）」(2025 intern；摘要："route_requests — Load-balancing WebSocket Connections"，含 markdown 笔记)
- 1point3acres interview/thread/1147122 「Server Load Balancer Design」(60 min OA，付费)
- 1point3acres 题库 `company/stripe/jupyter-load-balancer-oa`：stage **OA**，60 min，Medium，**last asked 2026-02-02**，摘要 "Five progressive parts: round-robin → duplicate-aware → disconnects → capacity limits → SHUTDOWN"
- learncswithus.com 2025-10-20 「Stripe SDE NG OA 原题」
- programhelp.net 2025-09-30 (NG OA 复盘)、2025-10-16 (5 阶段拆解)、2026-03-16/17 (「题库非常小」)；dev.to 转载
- cscodehelp.com/stripe/stripe-oa-review 「Jupyter 负载均衡模拟题，五层规则」
- prachub.com/coding-questions/simulate-sticky-load-balancer-with-shutdown（**完整题面**，含格式/约束）
- 1024bbs 5821 摘要提到 "load balancing / request routing"

**背景**：Stripe Notebook 平台基于 Jupyter；多用户导致性能下降，部署多台 Jupyter server，用 load balancer 分发 websocket 请求。

**签名**：`route_requests(int numTargets, int maxConnectionsPerTarget, string requests[n]) -> string[n]`

**请求格式（两种记录）**
- 变体 A (programhelp/learncswithus)：`CONNECT connectionId userId [objectId]`、`DISCONNECT connectionId`、`SHUTDOWN targetIndex`；输出日志 `connectionId,userId,targetIndex`（**target 1-based**）
- 变体 B (prachub 原题面)：`CONNECT connectionId objectId`、`DISCONNECT connectionId`、`SHUTDOWN serverIndex`；输出 `connectionId serverIndex`（空格分隔）

**Part 1 — Basic**：每个 CONNECT 路由到 active connections 最少的 server；平手取最小 index。
**Part 2 — DISCONNECT**：按 connectionId 找到 server，计数 -1；无效 id 忽略不报错。
**Part 3 — Object affinity / sticky**：同一 objectId 的连接必须去同一 server，即使它负载更高（需 object_map）。
**Part 4 — Capacity**：server 达到 `maxConnectionsPerTarget` 不可选；若 sticky 目标已满则拒绝（不记日志）。（programhelp 变体：全满则 reject）
**Part 5 — SHUTDOWN**：驱逐该 server 所有连接，**按原到达顺序**逐个按 CONNECT 规则重路由（含 sticky+capacity）；重路由期间该 server 不可用，之后以负载 0 重新可用（prachub）；programhelp 变体：shutdown server 从 pool 移除；放不下的连接 drop；需清理 object→server 映射。
**日志规则**：只有成功的 CONNECT（及成功的重路由）输出；被拒/被 drop 不输出；DISCONNECT/SHUTDOWN 不输出。
**约束（prachub）**：1 ≤ m ≤ 1e5，≤ 2e5 requests，capacity ≤ 1e9。
**test 数**：~17（含 hidden）。坑：1-based index、tie-break、shutdown 后清理、格式对齐。
**数据结构**：connection_map(connId→server)、object_map(objId→server)、target_load、shutdown_targets。

### 2.2 Merchant Fraud Score（商户欺诈评分：amount×factor / 同客户≥3 / 同小时惩罚）  【confidence: high】

**来源**
- csoahelp.com 2026-07-06 「Stripe OA真题：Merchant Fraud Score」（**题面最完整**）
- oavoservice.com 2026-01-03 「Merchant Fraud Scoring System — Why Do So Many Fail」
- programhelp.net 2025-10-26 「Stripe 2026 New Grad OA 经验分享｜一道题 60 分钟」(变体，见下)；2025-12-28 「Stripe Software Engineer OA 面经（2026）」；2026-01-20 「HackerRank OA 真题解析」
- medium @program.net 2025-12
- 1024bbs/1point3acres 摘要提及 "merchant / customer / 3 次"

**输入**
- `merchants_list`: `merchant_id, base_score`（1–50）
- `transactions_list`: `merchant_id, amount, customer_id, hour`（0–23）
- `rules_list`: 与 transactions **一一对应**：`min_transaction_amount, multiplicative_factor, additive_factor, penalty`
- n, m ≤ 1000；无整数溢出

**三条规则，分三个 pass 顺序应用**（每笔交易更新 merchant 的 current_score）：
1. **Amount**：若 `amount > min_transaction_amount`（**严格大于**）→ `current_score *= multiplicative_factor`
2. **Repeat customer**：若同一 `customer_id` 对该 `merchant_id` 累计（含当前）**≥3** 笔 → `current_score += additive_factor`（"add all the corresponding rules' additive_factors"）
3. **Hourly density**：同 customer→同 merchant **同一小时内第 3 笔及以后**：hour ∈ [12,17] → `+= penalty`；hour ∈ [9,11] ∪ [18,21] → `-= penalty`；其他小时不动

**输出**：按 merchant 名字典序，`"name, score"`（或 `merchant_id, score`）逗号分隔字符串列表。

**变体（programhelp 2025-10-26，NG OA）**：merch (名字+初始分)、trans (merchant, customer, amount)、rules；规则1：按 (m,c) 分组，**≥3 笔** → 把该组交易总额加到 merchant 分；规则2：按 (m,c,h) 分组 ≥3 → 再加一次总额；按名字典序输出；**严格比较**；**~17 test**，边界：0/负 amount、无交易 merchant、重复交易、输出格式、浮点精度。
**programhelp 2026-01-20 示例参数**：factor 2、customer bonus 1/笔、hour threshold 3、penalty 5；样例 M1/M2、6 笔、C1–C4。

### 2.3 Fraud Detection — MCC 阈值 + CHARGE/DISPUTE 流（"Catch Me If You Can"）  【confidence: high】

**来源**
- 1point3acres thread-1163662 「Stripe Summer 2026 OA 分享」(Toronto intern, HackerRank 60 min；摘要指向此题)；thread-1147871 「2026 SDE Summer Intern OA」；interview/post/7344444（"coding with a system design twist for fraud detection"）
- leetcode 7344444 (SWE Intern 2026)、7428741 (NG 2025-26 University Recruiting OA)
- interviewfox.ai 2026-07-28 「How I Took the Stripe OA in 2026」（**5 Part + 每 Part test 数**）
- linkjob.ai 2025-09-16、extrabrain.app 2026-02-10（3 Part 变体，含输入格式）
- programhelp 2025-08-07「Fraudulent Merchant Detection」(Ticketmaster/Amazon 背景)
- oavoservice.com/en/articles/stripe-0109 (2026-01-04) —— **注意：该文的 "4 part 交易风险引擎" 是另一题，见 2.20**

**Setup 数据**：merchant → MCC 映射；每个 MCC 一个 fraud threshold（**int = 计数阈值** 或 **float = 比例阈值**）；fraud result codes 列表（也可能同时给 non-fraud codes）；最小交易数（min transaction count）。
**事件流**：`CHARGE,charge_id,account_id,amount,code`；`DISPUTE,charge_id`（引用先前 charge）。

**5-Part 版（interviewfox，2026 NG，60 min）**
- P1 (3 tests)：解析 setup（merchant→MCC、MCC→threshold、fraud codes）
- P2 (5 tests)：顺序处理事件；每 merchant 维护 fraud_count / total_count
- P3 (5 tests)：判定：count 阈值 `fraud_count ≥ value`；ratio 阈值 `fraud_count/total_count ≥ value` → 标记 fraudulent
- P4 (5 tests)：DISPUTE 反转原 charge（"a dispute reverses the original charge completely"）：已计入的 fraud 减掉，重新评估
- P5 (7 tests)：边界：重复 dispute 同一笔、dispute 非 fraud charge、零交易量的 ratio merchant（除零）
**3-Part 版（linkjob/extrabrain）**
- P1：计数阈值，超过 MCC 的 max fraudulent transactions 即 fraudulent；输出 **字典序、逗号分隔的 fraudulent account_id**
- P2：比例阈值（达到 min transaction count 后 fraud fraction ≥ threshold）；**一旦标记永久保持**（即使比例回落）
- P3：`DISPUTE,charge_id`：被 dispute 的交易视为 non-fraud；若因此不再越线，merchant **可恢复** non-fraudulent（与 P2 "永久" 规则冲突——两种变体都被报道）
**programhelp 变体**：背景是生产模型误伤 Ticketmaster/Amazon 等大商户；用 0–1 比例 + 最小交易数；触发后永久。
**programhelp 2025-09-21 低可信变体**："同一用户 10 分钟内不同 IP" 或 "1 小时内总额 > $5000" → 输出 fraudulent transaction ids（可能是 AI 改写，low）。

### 2.4 Chat Billing — token 计费（payg vs fixed，$0.03/$0.04 per 100，$15 / 40,000）  【confidence: high】

**来源**
- 1point3acres 题库 `problems/59a39c1c-…`「Chat Billing Calculation (Monthly Billing by Token Usage and Plan Switching)」、`problems/f8e3ed43-…`「Chat Billing Calculation」、`company/stripe/chat-billing-oa`（**OA**，60 min，Medium，tags payment/simulation/string，**last asked 2026-04-17**，"recent high-frequency HackerRank OA"）
- 1024bbs 10992 摘要提及

**函数**：`calculate_monthly_billing(sessions) -> string[]`
**输入**：字符串数组，每条 `"user_id,input_tokens,output_tokens,plan"`，plan ∈ {`payg`,`fixed`}；tokens 非负整数。
**输出**：`"user_id: $x.xx"`，按 user_id 字母序，**所有用户都输出（含 $0.00）**，两位小数。
**Block 规则**：按 **每个 session** 以 100 token 为块计费，不足 100 免费：`blocks = floor(tokens/100)`；不同 session 余数不能合并。
**payg**：input $0.03/块，output $0.04/块。`floor(in/100)*0.03 + floor(out/100)*0.04`。
**fixed**：月费 **$15.00**；含额度：
- 变体 1（59a39c1c）：**40,000 tokens/月**（合并额度，按 100 块计）
- 变体 2（f8e3ed43）：**40,000 input + 20,000 output**
超额按 payg 费率；超额前先做每 session 块取整：`billable_input = Σ floor(in/100)*100`。
**Plan switching（同月混用）**：`r = fixed_sessions / total_sessions`；prorated fee = `15.00 * r`；prorated allowance = `40000 * r`（变体 2：input 40000r、output 20000r），额度仍按 100 块计；payg session 直接计费；fixed session 先消耗 prorated 额度，超出按 payg 费率。`total = payg_cost + prorated_fee + fixed_overage`。
**样例**：3 组（纯 payg / 纯 fixed / 混用），题库付费不可见。

### 2.5 Card Range Obfuscation（BIN 区间补洞）  【confidence: high】

**来源**
- csoahelp.com 2024-11-04 「Welcome to 2024-25 Stripe University Recruiting HackerRank Challenge — Stripe OA 真题」（**4 Part + 各 Part test 数**）
- programhelp 2025-08-07；linkjob 2025-09-16；extrabrain 2026-02-10；scribd "Card Range Obfuscation Methodology"；1024bbs 10992 摘要
- 1point3acres thread-1085478 「Stripe OA 2024-2025 University Recruitment」摘要（同期 OA）

**背景**：卡号 8–19 位，前 6 位 BIN；Stripe card metadata API 返回 BIN 内区间→brand 映射；区间间的 gap 会被 fraudster 用来探测有效卡号，需补齐 gap 使区间**完整覆盖整个 BIN range 且有序**。
**BIN range**：`424242` → `4242420000000000`…`4242429999999999`（16 位；start = BIN×1e10，end = +1e10−1）。
**输入**：第一行 6 位 BIN；第二行 N；接下来 N 行 `start,end,brand`（**start/end 为 BIN 后的 10 位 offset**）。
**输出**：按 start 排序的 `start,end,brand`，用**完整 16 位卡号**。
**Part 1 (4 tests)**：只补 range 两端（下界延伸到 …0000000000，上界延伸到 …9999999999）。
**Part 2 (4 tests)**：补中间 gap——**由较低的区间向上延伸**填满。
**Part 3 (2 tests)**：处理子集/嵌套区间——只延伸覆盖区间（covering interval）。
**Part 4 (3 tests)**：延伸后**合并相邻同 brand 区间**。
**样例 1**：BIN `424242`，`1500000000,6555555555,VISA` → `4242420000000000,4242429999999999,VISA`
**样例 2**：BIN `777777`，`1000000000,3999999999,VISA` / `4000000000,5999999999,MASTERCARD` → `7777770000000000,7777773999999999,VISA` / `7777774000000000,7777775999999999,MASTERCARD`
**programhelp 2025-09-21 低可信变体**："合并区间并把中间位替换成 X 只留前后 2 位"（疑似 AI 改写，low）。

### 2.6 Payment Processing / Payment Intent 命令系统（INIT/CREATE/ATTEMPT/SUCCEED…）  【confidence: high】

**来源**
- csoahelp.com 2024-12-15 「[Stripe] 2025 Start – 14 Dec OA」（**3 Part 完整**）
- csoahelp.com 2024-12-11 「[STRIPE] OA Transaction Intent Management System 2025 – 09 Dec」（改名变体）
- csoahelp.com 2025-04-22 「[Stripe] HackerRank OA 2025 start – 21 Apr」（REFUND + 时间窗变体，4 Part）
- 1point3acres thread-1091979「Stripe OA 2025 summer intern」摘要："Payment Processing System，4 parts"；thread-1101931「STRIPE OA，支付系统」；thread-1085478 摘要："OOD 模式、题很长代码量大、16/19"；thread-1099687「OA Stripe Interview.」摘要："4 parts，简单字符串处理，HackerRank 60 min"
- medium @azn7u1 「Stripe Intern OA + VO」(INIT/CREATE 样例)

**版本 A（2024-12-14 OA）**
- `INIT merchant_id balance`：初始化商户（已存在则忽略）
- `CREATE payment_id merchant_id amount`：创建 PaymentIntent，状态 `REQUIRES_ACTION`；重复 id / 商户不存在 / 负数 → 忽略
- `ATTEMPT payment_id`：`REQUIRES_ACTION → PROCESSING`
- `SUCCEED payment_id`：`PROCESSING → COMPLETED`，商户余额 += amount
- Part 2：`UPDATE payment_id amount`：仅 `REQUIRES_ACTION` 可改金额（负数忽略）
- Part 3：`FAIL payment_id`：`PROCESSING → REQUIRES_ACTION`；`REFUND payment_id`：仅 `COMPLETED` 且未退过，余额 −= amount
- 输出：每商户 `"merchant_id balance"`（按 id 升序）。样例：`INIT m1 0 | INIT m2 10 | CREATE p1 m1 50 | ATTEMPT p1 | SUCCEED p1 | CREATE p2 m2 100 | ATTEMPT p2` → `m1 50 / m2 10`
**版本 B（2024-12-09，改名）**：状态 PENDING/IN_PROGRESS/DONE；命令 START/NEW/PROCESS/COMPLETE/MODIFY/CANCEL/RETURN；**每条命令带时间戳**；START 可带 refund_limit（无限制=永远可退；0=不可退；否则仅窗口内可退）。输出 `["account1 50", …]` 按 id 升序。
**版本 C（2025-04-21）**：P1 `INIT m balance` / `CREATE p m amount`（→ `{"m1":1500}`）；P2 `REFUND p`（只退成功创建的）；P3 保持语义；P4 `timestamp INIT m balance refund_limit`、`t CREATE …`、`t REFUND p`：仅 `t_refund − t_create ≤ refund_limit` 成功。样例 `["1 INIT m1 1000 10","2 CREATE p1 m1 200","5 REFUND p1","15 REFUND p1"]` → `{"m1":1000}`。

### 2.7 Subscription Database（start / end / check + duration 累加）  【confidence: high】

**来源**：csoahelp.com 2024-11-27 「Stripe -Stack Position OA」
- 输入：`"timestamp,op,user[,duration]"` 字符串列表。
- P1：`start`（返回 ""）、`end`（返回 ""）、`check`（返回 `active`/`inactive`）。样例 `["1,start,Michael","5,check,Michael"]`。
- P2：`start` 可带 duration：`["1,start,Michael,9"]` → 到 t=10 active，t=11 起 expired；无 duration = 无限期；新的 start **覆盖**旧订阅。
- P3：改为**累加**：`["1,start,Michael,10","2,start,Michael,4"]` → active 到 15，16 起 expired；无限期订阅不受后续 start 影响。

### 2.8 Chargeback / Dispute 解析（解析 → 过滤损坏 → 排除 withdrawn）  【confidence: medium】

**来源**：leetcode discuss 5832245 「Stripe University New Grad OA 2024」(403，仅摘要)；programhelp 2025-08-08 「Parsing and Filtering Refund/Dispute Data」
- 背景：Stripe 日处理数十亿美元；chargeback = 盗卡/多收费。任务：解析 chargeback 信息，供 merchant 查看。
- P1：解析有效 refund/dispute 记录为可读格式（输入均合法）。
- P2：过滤无法解析成 dispute 对象的损坏行。
- P3：同一 network 上同一 transaction id 多行、后续行 reason 为 `withdrawn` → **两行都不输出**，只保留未撤回的。
- 可读多文件输入。

### 2.9 Join Dataset（legacy processor → Stripe 数据合并）  【confidence: medium】（2026-04 新题）

**来源**：programhelp.net zh_tw 2026-04-28 「Stripe OA 2026 | 4月 新題庫」
- `joinDataSet(fieldName, customerFile, processorFile, skipUnmatched)`（CSV 字符串）
- P1 Inner join：按 fieldName 匹配；列顺序 = customerFile 全部列 + processorFile 全部列；排序：先 customerFile 的 order 列再 processorFile 的 order 列；只保留匹配行。
- P2 Left join：保留 customerFile 所有行，未匹配处填空串。
- P3 One-to-many：一个 customer 对应多条 processor 记录 → 每条一行，customer 信息重复。

### 2.10 Platform Balance + Radar Rule（2024 版 OA，75 min）  【confidence: medium】

**来源**：1point3acres thread-1102706「Stripe OA 面经」、interview/software-engineer-446019「Stripe OA 挂经 + 求debug」(test 5、12 常挂)、442716、1099687；1024bbs 10992/5821 摘要
- **Platform Balance**：输入列表，两类记录：`API:` 更新账户余额（形如 `API: amount=1000&merchant=...` 的 query-string）、`BAL:` 查询/输出余额。摘要仅此。
- **Radar Rule**：解析规则字符串，只支持 `==` 与 `!=`；操作符两侧空格可选（`amount==100` / `amount ==100`），需小心 split。
- 第二题：essay "如何改进第一题的代码"。

### 2.11 Atlas 公司名可用性（normalize + 注册 + reclaim）  【confidence: medium】

**来源**：linkjob 2025-09-16；extrabrain 2026-02-10；programhelp 2025-09-21（低可信变体）
- 输入 `account_id|proposed_name` → 输出 `account_id|Name Available` / `account_id|Name Not Available`
- 归一化：忽略大小写；`&` 和 `,` 视为空格；连续空格合并；去后缀 `Inc.`/`Corp.`/`LLC`/`L.L.C.`/`LLC.`（不区分大小写）；去开头 `The`/`An`/`A`；忽略 `And`（除非在开头）；归一化后为空 → 不可用。
- P1：对已注册名列表做可用性检查。P2：持久注册集，一旦接受即对所有后续请求不可用。P3：`RECLAIM,account_id,original_proposed_name`——仅原注册者可回收，回收后名字释放。
- programhelp 低可信变体：字母数字空格、长度 2–50、黑名单 → valid/invalid。

### 2.12 Payment Card Validation（Luhn / 多网络 / `*` 遮罩 / `?` 损坏恢复）  【confidence: medium】

**来源**：linkjob 2025-09-16；extrabrain 2026-02-10；1point3acres interview/stripe-software-engineer-677770「2021 SDE Intern OA」/677836「Stripe OA」摘要（card networks Visa/Mastercard/Amex；C++/Python/Java/JS 可选；"Stripe in a Box"）；1024bbs 摘要
- 网络：VISA 16 位首位 4；MASTERCARD 16 位首两位 51–55；AMEX 15 位首两位 34/37。
- Luhn："从右起校验位前每第二位翻倍，>9 减 9，求和 %10==0"。
- P1：16 位 VISA → `VISA` / `INVALID_CHECKSUM`。
- P2：15–16 位多网络 → 网络名 / `INVALID_CHECKSUM` / `UNKNOWN_NETWORK`。
- P3：含 `*`（1–5 位遮罩）→ 每网络有效卡数，按网络名字母序。
- P4：以 `?` 结尾表示损坏，恰好一处错误（单位改错 或 相邻两位互换）→ 输出所有有效原卡 `card_number,NETWORK`，按数值升序。

### 2.13 Subscription Notification Scheduler（订阅邮件调度）  【confidence: medium-high；OA 与 VO 都出现】

**来源**：extrabrain 2026-02-10 / linkjob 2025-09-16（OA 3 Part）；oavoservice 2025-12-27；1point3acres 题库 `problems/4d6938ea-…`「Email Subscription」；linkjob 2025-12-07 intern VO；1point3acres 1100699「2025 intern team screen+VO」摘要（VO：Email Subscription）；collegesidekick 转载 1point3acres 793600 onsite「email notification for invoice events」；prachub「Generate Account Email Notifications」(完整规格)；showoffer/darkinterview
- P1：`send_schedule` 映射：`"start"` = 订阅开始，负整数 = 结束前 N 天，`"end"` = 结束日；用户 `name, plan, account_date, duration(days)`；按时间输出邮件（同时刻按 subscription id）。典型模板：welcome (start)、"Upcoming expiry" (T-15)、"Subscription expired" (end)。样例：Alice start=0 dur=30，Bob start=10 dur=30。
- P2：plan change 事件 `name, new_plan, change_date` → 立即输出 `[Changed]`，之后邮件用新 plan 名，不输出过期邮件。
- P3：renewal 事件 → `[Renewed]`，延长 duration，重算到期邮件。
- prachub 变体：`current_day`、accounts(`account_id, created_day, expires_day`)、rules(`name, trigger ∈ {on_create, days_before_expiration, after_expiration}, offset_days, template`) → `"<account_id> <rule_name> <template>"`，按账户输入顺序、规则配置顺序；≤2e5。

### 2.14 Store Closing Time Penalty（关店时间惩罚）  【confidence: medium】

**来源**：extrabrain 2026-02-10 / linkjob 2025-09-16（3 Part）；1point3acres thread-844359「stripe MLE NG OA和店面经验」摘要（技术面问 store open/close penalty）；jointaro 题库「Minimum Penalty for a Shop」；programhelp 2025-09-21 低可信变体
- log 字符串每小时 `Y`（有客）/`N`（无客）；closing_time ∈ [0, n]。惩罚：开门且无客 +1；关门且有客 +1。
- P1：`compute_penalty(log: str, closing_time: int) -> int`
- P2：`find_best_closing_time(log: str) -> int`（平手取最小）
- P3：`get_best_closing_times(aggregate_log: str) -> list[int]`：从 `BEGIN … END` 分隔的聚合日志提取合法日志（忽略无效/嵌套），逐个返回最佳关店时间。

### 2.15 Six Degrees of Collusion（OA，图/并查集，欺诈环）  【confidence: medium（题库摘要）】

**来源**：1point3acres 题库 `company/stripe/six-degrees-of-collusion-oa`：**OA**，60 min，Medium，HackerRank，**last asked 2026-06-24**；变体标题 "Risk Scoring / Fraud Ring Size / Direct Links"
- "Parse transaction strings to identify users connected by shared identifiers, compute the size of the target user's fraud ring, then decide whether to block."
- 关联题（VO）：csoahelp 2026-07-22「从商户属性匹配到间接关系查询」：P1 与目标商户共享任一属性(email/phone/website/bank) 的商户；P2 字段加权分 ≥ threshold；P3 直接 + 一跳间接。linkjob 2025-12-07 phone screen「User Record Linking」：weights `{name:0.2,email:0.5,company:0.3}`，threshold 0.5，follow-up 1-hop、transitive。1point3acres 1154050 摘要另提 "按共享属性分组商户，每日数据更新，跟踪 cluster 变化（union-find）"。

### 2.16 Datacenter Request Router（REGISTER / DISTANCE / ROUTE，Haversine）  【confidence: medium（题库摘要）】

**来源**：1point3acres 题库 `request-routing-haversine-oa`：**OA**，60 min，Medium，**last asked 2026-08-11**；OJ 题「Proximity-Aware Datacenter Request Router」「Data Center Registration and Health Management」「Datacenter Router Command Processor」；prachub「Register Data Centers and Route to the Nearest Healthy Region」
- 注册数据中心（坐标、容量）、切换健康状态、按大圆距离把请求路由到最近的健康数据中心。

### 2.17 Account Balance Manager（OA，Easy）  【confidence: medium】

**来源**：1point3acres 题库 `account-balance-manager`：**OA**，Easy，**last asked 2026-05-12**；linkjob 2025-12-07「Transaction Balance Problem」(intern VO)；prachub「Build an Account Transfer Ledger」；dev.to programhelp「transaction logs `user event amount` → final balance」
- 处理有序交易列表：P1 输出用户及非零余额；P2 记录被拒交易（`balance + amount < 0`）；P3(a) 平台借贷：非平台账户可向平台借款补缺口，计算 `max_reserve`。

### 2.18 KYC / Business Account Data Verification（OA / Tech Screen，5 步）  【confidence: medium】

**来源**：1point3acres 题库 `kyc-business-verification`（**OA / Tech screen**，Medium，last asked 2026-06-30，"five incremental steps"）、`problems/c2c4e3e9-…`「KYC Conundrum」（3 Part 可见）；1point3acres 1154573/1155516 team screen 摘要（"Data Verification"、"KYC CSV 30+ 行 6 列"）；darkinterview "Data Verification" 高频
- 输入 CSV 字符串，字段：`business_name, business_profile_name, full_statement_descriptor, short_statement_descriptor, url, product_description`
- P1：全部非空 → `VERIFIED: [business_name]` 否则 `NOT VERIFIED: …`
- P2：`full_statement_descriptor` 长度 5–31（含）
- P3：黑名单描述符：`ONLINE STORE`, `ECOMMERCE`, `RETAIL`, `SHOP`, `GENERAL MERCHANDISE`
- P4–5：未见（付费）。

### 2.19 Worker Task Assignment（OA / Onsite，4 Part）  【confidence: low-medium（题库摘要）】

1point3acres 题库 `worker-task-assignment`：**OA / Onsite**，Medium，last asked 2025-10-09："balance workload to the least-busy worker, restrict to workers with the required skills, prefer the …"。

### 2.20 Transaction Risk Engine（CSV 6 字段 → OK / SUSPICIOUS + 错误码）  【confidence: low-medium】

**来源**：oavoservice.com 2026-01-04「Fraud Detection System Walkthrough」（"45 min"，HackerRank 自写 test）
- P1：解析 CSV（amount, currency, card_type, location 等 6 字段），非空校验（空串/空白/null）。
- P2：金额区间校验；被禁支付方式（如 prepaid）→ SUSPICIOUS。
- P3：与 `behavioral_baseline` 比对，匹配比例 < 50% → `behavior_mismatch`。
- P4：输出错误码 `AMOUNT_TOO_HIGH` / `BLOCKED_METHOD` / `BEHAVIOR_MISMATCH`，最多 2 个，列对齐；干净则 `OK`。

### 2.21 Beta Invite / Bot 检测（2021-09 NG OA）  【confidence: low-medium（摘要）】

1point3acres thread-793401「Stripe NG HackerRank OA」：60 min 1 题；系统可发邀请、用户可请求邀请、激活邀请；**bot = 1 分钟内发 ≥5 条消息**。

### 2.22 Accept-Language Header 解析  【confidence: medium；programhelp 列为 OA，1point3acres 列为 phone screen】

1point3acres 题库 `http-language-preference`：phone screen，last asked 2025-10-22，4 Part："resolve Accept-Language against server-supported languages: exact match → prefix match → …"；programhelp 2025-09-21：解析 q 值，默认 1.0，按 q 降序、平手按出现顺序；1point3acres 1100699 摘要 "Card Len 题，类似 HTTP request"。

### 2.23 MLE NG OA 2026  【confidence: medium】

programhelp 2026-04-10：Q1 PyTorch 交通限速牌 3 分类（30/70/120 km/h），train.csv/test.csv → submissions.csv(`path,label`)，Accuracy 评分；Q2 pandas：员工同一月内到访所属分店 ≥3 次（同日多次算 1 次），空则返回带表头空 DataFrame。1point3acres 844359 摘要："MLE NG OA 题目比较简单"。

### 2.24 其它低可信 / 仅标题
- programhelp dev.to 2025-10-18：Email normalization（去点、`+` 后忽略、小写）判等；transaction log 余额；Rate limiter（3 req / 10 s）—— low。
- lodely.com 2026-05-03 列的 14 道 LeetCode 式题（90 min 2 medium 1 hard）与所有一手来源矛盾 —— **忽略（low）**。
- 1point3acres thread-662909「热乎 Stripe OA(Capital)」(2020-08)：Stripe Capital 相关，内容不可见。
- 1point3acres interview/software-engineer-292087「Stripe new grad OA」(旧)：不可见。
- 1point3acres OJ 参考题标题（可能来自 OA/onsite）：Find the First K Valid UTC Deployment Windows；Parse and Format a Hierarchical Task CSV；Weekly Deployment Window Scheduler；Incident Monitor；Calculate Service Fees；Matching Contacts by Email Domain and Preferences；Payment Reconciliation；Transaction Fee with Status- and Type-specific Rates；Review Assignment via Git Diff + CSV Owners。

---

## 3. 电面 / VO 题（OA 与电面互相回收，供参考）

| 题 | 内容要点 | 来源 / 日期 | 置信 |
|---|---|---|---|
| **Currency Conversion** | 字符串 `USD:AUD:1.4,CAD:USD:0.8,USD:JPY:110`（或 `AUD:USD:0.7,AUD:JPY:100,USD:CAD:1.2`）；P1 直接汇率；P2 反向汇率；P3 多跳最优路径（比较 `AUD->GBP->CAD` vs `AUD->USD->CAD`）BFS/DFS | 1point3acres 1048313「Stripe 電面新題」、1088332「Stripe滇缅」(LC medium)、题库 25b1c004；jointaro "Evaluate Division" | high |
| **Shipping cost（路线版）** | `"US:UK:FedEx:5,UK:US:UPS:4,UK:CA:FedEx:7,US:CA:DHL:10,UK:FR:DHL:2"`；`shippingCost(str, src, dst, method)`；找不到 −1；P2 允许一次中转（US→UK→FR，FedEx→DHL，cost 7），直达优先 | csoahelp 2024-11-20、2024-12-27、2025-01-18；libaedu；1024bbs 5821 | high |
| **Shipping cost（国家×产品矩阵版）** | 订单 {country, items[{product, qty}]} + 矩阵 country→product→单价(cents)；P2 数量阶梯（0–2 件 1000c，3+ 900c）；P3 固定价区间 + 阶梯混合、不重复计费 | 1point3acres 题库 shipping-cost-calculator (phone screen, 2025-12-19)；programhelp 2025-11-21；oavoservice 2025-12-29；linkjob 2025-12-07；medium azn7u1 | high |
| **Rate Limiter** | 同一用户 2 秒内最多 5 次；滑动窗口；follow-up：大小商户公平性、内存清理 | 1point3acres 817977「Stripe NG现场表演」、1081681；题库 rate-limiter (onsite, 2025-12-06) | medium |
| **Server allocate/deallocate** | `next_server_number([5,3,1])→2`；`Tracker.allocate("apibox")→"apibox1"`、`deallocate("apibox1")` | gist stealthbomber10；1point3acres 1093485 摘要 | high |
| **Receivables (Brazil) 聚合** | CSV `customer_id,merchant_id,payout_date,card_type,amount`（含表头）按 (merchant_id, card_type, payout_date) 求和，输出 `id,card_type,payout_date,amount` | csoahelp 2024-10-04 / 2024-11-12；1point3acres 1093626 摘要 "Brazil 题 group by" | high |
| **Authorization Request Processing** | `timestamp,unique_id,amount,card_number,merchant` → 按时间排序输出 `ts id amount APPROVE` | csoahelp 2024-11-15 | high |
| **Radar Rule Engine（VO 版）** | `should_accept_transaction(transaction: dict[str,str], rules: list[str]) -> bool`；`ACCEPT if (...)` / `BLOCK if (...)`；`:field: = "const"`（两侧可互换，常量含空格）；P2 布尔变量 + AND/OR（`BLOCK if (:known_stolen_card: AND :large_amount:)`）；顺序匹配首个命中；无命中默认 accept；缺字段返回 false | csoahelp 2026-08-05 | high |
| **Invoice / Payment Reconciliation** | `payment="paymentABC,500,Paying off: invoiceC"`，invoices `["invoiceA,2024-01-01,100",…]`；逐步放宽匹配规则；integration 变体加 API | 1point3acres interview/post/7379560；题库 (High freq, last asked 2026-08-13) | medium |
| **CSV 交易费用计算** | `payment_completed`: amount×2.1%+$0.30；`dispute_lost`: $15；`dispute_won`: provider=card 则 $15 否则 0；P2 (provider,country)→rate；prachub 版：`fee=floor(amount_cents*rate_bps/10000)` | programhelp 2025-12-04、2026-01-08；prachub | medium |
| **PaymentLedger 类** | `add_payment/add_refund/get_total_revenue/get_payments_by_date`；payment_id 幂等；partial refund；时间范围查询 | programhelp 2026-01-26/03-31/04-02/04-13 (intern VO) | medium |
| **Account balance settlement** | 账户当前/目标余额 → 构造转账序列；follow-up 最少笔数（DFS 剪枝）、审计 | programhelp 2026-02-27、2025-10-24 | medium |
| **AccountScheduler (LRU)** | `is_available(account_id, t)`；`acquire(account_id, duration)`；无参 acquire 选 LRU 可用账户 | linkjob 2025-12-07；题库 (onsite, 2026-03-27) | medium |
| **Suspicious transactions** | (user_id, amount, ts)，1 分钟内 >3 笔 → 可疑用户；滑动窗口 | programhelp 2025-08-20 | medium |
| **Matching Contacts** | 按 email domain 匹配联系人到人，按偏好过滤排序；"reading speed is the main constraint" | 题库 (phone screen, 2026-06-10) | low |
| **RBAC Role Resolver / Feature Flag SDK / Bitfont Renderer / Bikemap Integration / Mako Debug / SnakeYAML Debug** | onsite 专用（integration/debug/design），非 OA | 1point3acres 题库；programhelp | — |

---

## 4. 与任务清单的对照

| # | 任务清单项 | 结果 |
|---|---|---|
| 1 | Chat Billing | §2.4，high，2 变体 |
| 2 | Fraud detection MCC CHARGE/DISPUTE | §2.3，high，5-part 与 3-part |
| 3 | Merchant scoring ≥3 | §2.2，high |
| 4 | Card range obfuscation | §2.5，high，4 part + test 数 |
| 5 | Atlas 公司名 | §2.11，medium |
| 6 | Luhn / 遮罩 / 损坏 | §2.12，medium |
| 7 | Subscription notification | §2.13，medium-high |
| 8 | Store closing penalty | §2.14，medium |
| 9 | Platform balance API 串 | §2.10，medium（仅摘要） |
| 10 | Radar rule `amount==100` | §2.10 (OA) + §3 (VO 完整版) |
| 11 | Rate limiter | §3，电面 |
| 12 | allocate/deallocate | §3，电面 |
| 13 | Currency conversion | §3，电面，high |
| 14 | HTTP header / routing | §2.22 Accept-Language；§2.16 datacenter router；§2.1 load balancer |
| 15 | Invoice/payout/ledger | §3 Invoice reconciliation、PaymentLedger、balance settlement；§2.17 Account Balance Manager |
| 16 | 其它 | §2.6 Payment Intent 命令；§2.7 Subscription DB；§2.8 Chargeback；§2.9 Join Dataset；§2.15 Collusion；§2.18 KYC；§2.19 Worker；§2.20 Risk engine；§2.21 Beta invite；§2.23 MLE；shipping/tax 无 OA 记录（shipping 仅电面）；idempotency 仅 VO integration (POST /v1/charges Idempotency-Key)；webhook 仅 system design |

## 5. 未能获取（需登录/被墙）的关键帖，建议人工查看
- 1point3acres thread-1145788「stripe OA 彙整 2026」（2026 OA 汇总）
- thread-1163662「Stripe Summer 2026 OA 分享」、1147871「2026 SDE Summer Intern OA」、1154050「2025 SWE Intern OA分享（含笔记）」、1146781「Stripe Swe University OA」、1086440/1086447「2024-2025 ng OA (2024.09.15)」、1085478、1091979、1101931、1102706、1099687、1020963、793401、662909、677836/677770
- 1point3acres 题库付费全文：chat-billing-oa、jupyter-load-balancer-oa、six-degrees-of-collusion-oa、request-routing-haversine-oa、account-balance-manager、kyc-business-verification、worker-task-assignment
- 1024bbs 10992「Stripe 吐血面经总结」、5821「近期Stripe面经总结」、1989、1937
- leetcode discuss 5832245 (2024 NG OA chargeback)、840872 (2020 NG OA)
