# Hello Interview 开放式题 · 核心打法

> 在 hellointerview.com/practice/ai-coding（Open-Ended）点 Start：clone → 本地 Claude Code（`CLAUDE_CONFIG_DIR=~/.claude-interview`）→ 计时 → 提交代码与 AI 对话 → 拿 hire 评级与逐项反馈。
> T/X 编号见 `claude_playbook.md`。"常丢分"来自已公开会话的 "The gap"（本机 `sources/local/hellointerview-ai-coding/sessions/`）。

## 两类题，两套开局

| 类 | 题 | 开局（前 15 分钟） | 收口 |
|---|---|---|---|
| A · 修 bug + 推到生产可用 | Schedulr · Transcribe · Fileshare · LinkLock | T1 → **自己写 bug 清单**（T3）→ 让 AI 补漏 → 合并成一份按影响排序的计划，写进 `TASKS.md` → T6 | 清单逐项标 done / out of scope（T12）；"production-ready" 自己定义，并说出排序理由 |
| B · 从零搭（只有 README） | Gridbot · LRU Cache · Collaborative Editor · Text Render Service | **先建实体模型和接口**（空函数体）→ T2 定模糊词 → T5 选数据结构 / 算法 → T7 测试先行 | 扩展点留出来但不实现（seam 说出口）；不做无关功能 |

A 类的公共清单（每题都先过一遍，按影响排序）：并发竞态 · 跨租户 / 越权 · 输入校验（400 而不是 500）· 时间与时区 · 吞掉的异常 · 非幂等的写操作 · 同步外部调用阻塞在请求路径上 · 资源泄露（连接、文件）· 机密（弱随机、明文存储、日志里有 PII 或 token）· 无限增长（内存 map、重试）。

## 逐题

### Schedulr · Calendly 式预约（60 min，A）
- 对应：`cb04_quarantine` t1–t2。
- 打法：T1 跑通 4 个端点 → T3 清单 → **T8 先复现**：双人抢同一时段的并发测试红 → 修（DB 唯一约束 + 条件更新，不是加锁）→ 时间统一转 UTC → 校验层 → 邮件移出请求路径（outbox）。
- 值得学：先写失败测试并明说 "don't fix anything"；把"先讲方案再动手"写进 CLAUDE.md；数据库约束作为兜底。
- 常丢分：发现了同步发邮件，却没把它移出请求路径；回执没有幂等键。

### Transcribe · Whisper 式转写队列（60 min，A）
- 对应：`cb04` t3 · `cb02` t2。
- 打法：竞态领取任务（lease + 条件更新）· 失败重试上限 + 死信 · POST /jobs 幂等键 · worker 和 API 拆开进程。
- 值得学：多个 subagent 各看一个角度做审计，结果自己分成四类：适用 / 暂缓 / 讨论 / 不做。
- 常丢分：用两线程测试去证明跨进程的保证；校验、鉴权、限流列进清单了，却没进 diff；同一 URL 重复提交会生成两个任务。

### Fileshare · WeTransfer 式分享（60 min，A）
- 对应：`cb04` t1。
- 打法：token 改用 `secrets` 生成 · 过期分享的 info 端点也要鉴权 · 文件大小上限 · 限流 · 已删除文件返回 404 而不是 500。
- 值得学：自己列了 14 条问题，再问 AI 漏了什么，AI 补上了两条最严重的。
- 常丢分：点名了弱随机却没改；限流排在第一优先，最后没做；想把失败测试 mock 掉。

### LinkLock · 魔法链接免密登录（60 min，A）
- 对应：`cb04` t1–t2 · `cb03` t3（审计与可追溯）。
- 打法：token 存哈希不存明文 · 一次性使用要原子（条件更新）· token 不放 URL query（或缩短有效期 + Referrer-Policy）· 请求端点限流 · 日志不打 token。
- 值得学：逐个端点审一遍，先只做标注不改代码，弄清哪里有覆盖、bug 藏在哪。
- 常丢分：token 明文存储；两次同时 verify 的竞态没问；CSRF 没想到。

### LRU Cache（30 min，B）
- 对应：数据结构设计模式；`cb05` 的"认出模式"练法。
- 打法：先说设计（哈希表 + 双向链表，或 `OrderedDict`）→ 让 AI 挑毛病（T5 的变体）→ 空函数 → 测试先行（容量 0 / 1、更新已有键会刷新新近度、淘汰顺序）→ 实现 → 如果做线程安全，必须有并发测试。
- 值得学：先把自己的设计讲出来，让 AI 先挑毛病再写代码。（例："按时间戳做键的 map，找最旧的一项要全表扫描。"）
- 常丢分：并发只在注释里论证、没有测试；分片包装层没有任何测试；benchmark 数字和最终代码对不上。

### Gridbot · 网格机器人模拟器（45 min，B）
- 对应：`cb05` t1（命令解析）。
- 打法：实体（Grid · Robot · Heading · Command）→ 命令抽象（turn / move 都是 Command，以后的回放、新命令都从这个接缝扩展）→ 解析器校验（负数、非整数、越界）→ 测试：转满一圈回到原朝向、碰到障碍停下。
- 值得学：自己先起草实体和规则，再让 AI 定义"非法状态"这类模糊词。
- 常丢分：AI 的自测说"没问题"就收下了；解析器接受负数坐标；所有逻辑长在 Robot 类里，没有命令接缝。

### Collaborative Editor · 协同编辑引擎（60 min，B）
- 对应：并发与收敛；比 Abnormal 的 AI 面试更偏算法，作为加练。
- 打法：先定操作模型（insert / delete + 位置）和收敛规则（OT 位置变换，或带 id 的序列 CRDT）→ 收敛测试用**随机交错的操作顺序**（属性测试），而不是手挑的几种交错。
- 值得学：先让 AI 把 brief 提炼成一份规则文件，再拿你的实体模型请它论证"该不该合并某些类"。
- 常丢分：只测了几种手挑的交错；有界队列的淘汰路径从没演示过。

### Text Render Service · 文字转图片服务（60 min，B；暂无公开会话）
- 打法：接口先行（请求参数：文字、字体、尺寸、格式）→ 输入上限（长度、尺寸）防资源耗尽 → 按内容哈希缓存 → 渲染放在 worker 或有并发上限 → 错误返回结构化的 4xx。
- 风险：资源耗尽（超大图、超长文字）、字体文件路径穿越、缓存键没包含全部参数。

## 用法

一周里做 3–4 道（计划见 `WEEK_PLAN.md`）：A 类优先（Schedulr → LinkLock → Transcribe），B 类做一道（LRU 30 min 当热身，或 Gridbot）。每道提交后把反馈里"The gap"类的条目抄进 `playbook.md` §7 复盘表。
