# 01 · 三套时间框架 + 出声模板 + follow-up 应对

> 通用课（[[Code Core MOC|code-core]]）：[[round.reading]] · [[round.time]] · [[round.communication]] <!-- code-core-links -->

> 适用于：Snowflake 技术电面（60 min slot = 10 介绍 + **40 min 编码** + 10 反问）、onsite 的 **45 min OOD/类设计**、以及 HackerRank OA（历史 90–135 min，2026 新毕业一手 **120 min**）。
> 依据：`../../loop/LOOP_GUIDE.md` §3/4/5、`../../catalog/CATALOG.md` 漏斗描述。三套框架**形状相同**（读题定型 → 分段实现锁死 → 边界扫描 → 交卷复核），只是分钟数和"锁死"的对象不同：OA 锁 part，电面锁 base case，OOD 锁 API 契约。

---

## 0. 三套时间框架一览

| | 40 min 电面编码 | 45 min OOD | 120 min OA |
|---|---|---|---|
| 题目形状 | 1 道 LC medium + 1 个更难 follow-up | 1 个类，2–4 个递进方法 | 2–3 道大题，每题 3–5 个 part |
| 最先做的事 | 复述 + 约束 | **列出全部 public 方法签名**（契约先行，见 `04-class-design-and-concurrency.md`）| 通读全部 part，倒着设计状态 |
| 锁死的对象 | 能跑的 base case | 契约 + 单线程正确性 | 每个 part 各自的样例 |
| 最后 5–10 min | follow-up 口述（写不完就口述方向）| 并发/持久化追问 | 边界扫描 + 格式复核 |
| 对应 kit 题 | q01–q10、pc02–pc06、pc10 | od01–od09 | q02–q05、q09（image-only 多 part） |

**这类题不是纯 LeetCode 竞速**：Snowflake 的电面/OOD 会给 hint（多数面试官），但也有沉默型（`sd_checklist.md` 已经处理 SD 轮的沉默问题，这里处理 coding/OOD 轮）；OA 是隐藏测试部分给分。三套框架的共同纪律是：**先说思路，被打断也不慌；能跑的先锁死，别追求优雅。**

---

## 1. 40 min 电面编码：分钟表

| 分钟 | 阶段 | 产出 | 绝不做的事 |
|---|---|---|---|
| 0–3 | 复述 + 约束 | 用自己的话把题面说一遍，暴露误解 | 直接开始写代码 |
| 3–8 | approach + 复杂度声明 | 说出算法名字和 Big-O，等面试官点头 | 埋头想，不出声 |
| 8–12 | 接口 + 自测用例 | 函数签名 + 2–3 个手算的期望输出 | 跳过自测直接写实现 |
| 12–32 | 实现 base case | 跑通至少 1 个自测 | 一边写一边改需求理解 |
| 32–38 | 边界 + 自测复核 | 空输入 / 单元素 / 重复 / 极值 | 引入新功能 |
| 38–40 | follow-up 讨论 | 说出复杂度能压到哪、并发版怎么改 | 匆忙重写整个方案 |

**对照 kit**：`pc02`（多源 BFS 网格）、`pc03`（滑窗事件流）、`pc06`（Happy Number → Floyd O(1)）都是这个节奏——8–12 分钟想清楚状态形状，20 分钟写完 O(n) 或 O(n²) 版本，最后 follow-up 才谈优化。`pc01`（RBAC DAG，4-part）例外：它本身就是缩小版 OA，套用下面的 120 min 表按比例压缩到 40 min（每 part ~8 min）。

---

## 2. 45 min OOD：分钟表

| 分钟 | 阶段 | 产出 | 绝不做的事 |
|---|---|---|---|
| 0–5 | **契约先行** | 全部 public 方法签名 + 2–3 条不变量，说出口 | 先画数据结构再想接口 |
| 5–10 | 数据结构选择 | 说出"为什么用这个结构，不用那个" | 直接默认用 dict 不解释 |
| 10–30 | 实现核心方法 | 单线程正确，跑通 2 个自测 | 一上来就写线程安全版本 |
| 30–38 | 并发/持久化 follow-up | 口述或改代码：锁在哪、崩溃后怎么恢复 | 忘记这几乎是必考项（S10/S11） |
| 38–45 | 边界 + 反问 | 重复 id、空状态、越界查询怎么办 | 留一个"其实没测过"的方法 |

**为什么 OOD 单独给 45 min 而不是套用电面的 40 min**：`../../catalog/skills_matrix.md` S09/S10/S11 显示 5/10 道 OOD 题有明确并发追问、2 道有持久化追问——这 8 分钟的 follow-up 槽位是刚需，不是超时后随便压缩的部分。契约先行的 5 分钟同理：`od01`（Task Scheduler）挂经案例的根因就是契约没定清（重复 id 的语义、`execute()` 空队列返回什么）。

---

## 3. 120 min OA：分钟表（3-part 题为例，2-part 按比例合并）

| 分钟 | 阶段 | 产出 |
|---|---|---|
| 0–10 | 通读全部 part | 一句话说清最后一个 part 需要什么状态（同 Stripe 框架 §2 的"倒着设计"）|
| 10–20 | 定状态 + 写 parse | 能把输入变成记录的函数 |
| 20–55 | Part 1 | 跑通样例，**锁死** |
| 55–85 | Part 2 | 跑通样例，锁死 |
| 85–110 | Part 3 | 跑通样例 |
| 110–120 | 边界扫描 + 格式复核 | 空输入、n 的量级重新核对、trailing newline |

**Snowflake OA 与 Stripe OA 的差异**：Snowflake 的 part 递进经常是**同一道题换更大的 n**（`q02` part1 无模数 → part2 mod 1e9+7 且 n ≤ 2500 → part3 变成子串问题），而不是 Stripe 那种"业务规则层层加码"。所以"倒着设计"在这里更多是"**这个 O(n²) 会不会在 part2 卡死**"，而不是"这个数据结构撑不撑得住反向修改"。`q01`、`q04`、`q05` 都有 part1 慢版本 + part2 快版本的结构，先写 part1 拿到正确性分，再优化。

---

## 4. 出声模板：复述 → 约束 → approach → 接口 → 自测 → 实现 → follow-up

每一步给一句可以直接说出口的英文句子，照抄不丢人——面试评的是**思路可见**，不是文采。

1. **复述（Restate）**
   > "Let me restate the problem: I'm given ... and I need to return ..."
2. **约束（Constraints）**
   > "Before I start — what's the expected scale of n? Are ties broken by index, and can inputs repeat?"
   （对应 `01-python-for-interviews.md` 之外，这一步是抠 Stripe 框架六件事的 Snowflake 版：严格/非严格比较、tie-break、重复 id、空结果。）
3. **approach**
   > "My plan is a topological DP over the DAG: process nodes in topo order, union each node's own set with its parents'. That's O(V + E)."
   （对应 `pc01` 的 `_toposort` + `_dp_union`）
4. **接口（Interface）**
   > "I'll expose `add`, `execute`, and later `snapshot`/`replay` for persistence, so let me define those signatures first."
   （对应 OOD 的契约先行）
5. **自测（Self-test）**
   > "Let me trace through the example by hand before coding: with priorities [3,1,3] and timestamps [..], execute() should return task A first because ..."
6. **实现（Implement）**
   > "I'll write the straightforward version first, then optimize if time allows." （先 O(n²) 保底，见 §1 的取舍顺序）
7. **follow-up**
   > "If I had more time, I'd compress this to O(1) with a lazy-deleted heap / add a lock around the critical section / persist via an operation log."

---

## 5. Follow-up 的四种形状与应对

Snowflake 的题几乎每道都带 follow-up（catalog 明确写"**每题至少准备一个更难 follow-up**"）。四种形状，按频率排序：

### ① 压复杂度（O(n) → O(1) / O(n²) → O(n log n)）

**信号**："can you do this in constant space" / "bonus point if..." / n 从题面小样例突然放大到 1e5+。

**应对模板**："I have a correct O(X) version. The bottleneck is [具体操作]; I can trade [空间/预处理] for [时间] by [具体技巧]。"

| Kit 题 | 慢版本 → 快版本 |
|---|---|
| `q07` | 递归 O(h) 栈 → 迭代栈 → **Morris O(1) 空间**（临时线索树） |
| `pc06` | HashSet 判环 O(n) 空间 → **Floyd 双指针 O(1) 空间** |
| `q09` | O(m²n) 枚举所有前驱 → **O(mn) 只存 best/second-best** |
| `q01` | O(states) 朴素 DP → **Pareto frontier 剪枝**保状态数有界 |

### ② 加并发（单线程正确 → 线程安全）

**信号**："what if multiple threads call this concurrently" / "how would you make execute() thread-safe"——OOD 题默认自带这问。

**应对模板**："The critical section is [具体操作]; I'd guard it with [`Lock`/`threading.local`/CAS]，minimal 到 [这几行]，理由是 [不变量]。" 详细五步答法见 `04-class-design-and-concurrency.md` §5。

| Kit 题 | 并发形状 |
|---|---|
| `od01` | 单锁包住"扫描候选 → 标记已执行"整个临界区，避免两个 `execute()` 拿到同一个 id |
| `od02` | 结构锁（树形状）与文件锁（chunk 列表）**分段**，不同文件互不阻塞 |
| `od03` | 每线程一份 `threading.local()` 事务栈，读写全局态才用锁 |
| `od04` | 多规则版 `simulate_rate_limiter` 本身是纯函数式推进，但"谁先占到这个时刻"是线程安全的天然考点 |

### ③ 加持久化（内存态 → 崩溃可恢复）

**信号**："what if the process crashes" / "how do you make this durable" ——`od01`、`od02`、`od05` 都有。

**应对模板**："I wouldn't serialize internal state directly; I'd persist [操作日志/WAL]，重启时 replay 到内存态，因为 [幂等/顺序] 保证重放等价。"

| Kit 题 | 持久化形状 |
|---|---|
| `od01` | `snapshot()`/`replay()` 存操作日志，不存堆本身；重放日志等价重建调度器 |
| `od02` | 文件系统的追问是加 WAL + 快照 |
| `od05` | 崩溃不丢触发：`LeaseStore` 把 claim 结果持久化，多副本用同一个 lease store 判断谁执行过 |

### ④ 加反向查询（正向索引 → 反向索引）

**信号**："given a permission, find all users who have it" / "given a role, find who's assigned" —— `pc01` part 4 是这类题的原型。

**应对模板**："That's a different access pattern; I'd add a reverse index [user→role 或 privilege→role] built incrementally，而不是每次查询时扫描一遍所有节点。"

`pc01` part 4 的 `users_with_privilege`（遍历 assignments，检查 `effective_privileges[role_id]` 是否含目标权限）和 `filter_users_by_role`（纯过滤，不走继承）是两种不同的反向查询——**先分清"按权限反查"要不要走继承链，"按角色反查"要不要**，这是这道题唯一真正的陷阱。

---

## 6. 三套框架为什么可迁移

第 4 节的出声模板和第 5 节的四种 follow-up 形状，在 OA、电面、OOD 里原样成立——变的只是第 1–3 节的分钟数分配。换一道没见过的 Snowflake 题，先问自己："这是压复杂度、加并发、加持久化，还是加反向查询？" 四选一之后，对应小节的应对模板直接套用。
