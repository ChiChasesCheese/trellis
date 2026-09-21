# 项目深挖 · 题库（14 题）—— R1 前 15 min + 后续轮的一整轮

> 来源：LeetCode Discuss 6020524（Bangalore SWE 2024-06，整轮 = "pick a project → objectives, approach, tech stack, design, challenges, database strategy"）· PracHub 2026-04 "Explain a project and its hardest engineering challenge" · Blind ghkhxn3o "30 of 45 min on resume" · 1p3a 1124751（chatbot 项目：栈、模块关系、异步追问）· devclub-iitd（R1 简历/项目）。练：`python3 loop/mock.py bq exp -n 4 -m 3`。
> 首选项目 **Quant-Stroller**（口播在 `../01_first_round/playbook.md` §2.2）；备选 [[S1]]（生产系统）、[[S5]]（迁移与数据源切换）。每答：headline → mechanism → **I decided** → 量级 → 学到什么，≤ 90 s。

| # | 题 | 首选答法 | 来源 |
|---|---|---|---|
| 1 | Pick a project you're proud of and walk me through it. | Quant-Stroller headline + mechanism（90 s） | LC 6020524 |
| 2 | What was the objective — what problem were you solving and for whom? | "make it hard to fool yourself with a backtest"；用户是我自己 + 未来的策略研究者 | LC 6020524 |
| 3 | What was your approach and why that approach? | 三层：point-in-time 数据面 / 窄接缝的策略层 / 双门验证；为什么先建数据面 | LC 6020524 |
| 4 | Walk me through the tech stack and why each piece. | Python · DuckDB/Parquet（列存、本地、零运维）· NautilusTrader（撮合与成本模型现成）· PyTorch（因子模型训练）· FastAPI + React（研究台）· Prefect（调度）· 自托管 CI | LC 6020524 · 1p3a 1124751 |
| 5 | How are the modules related? Draw the architecture. | DataSource → Factor → Strategy → Broker 四个接缝；数据面 raw → bars → panel；ledger 是 append-only | 1p3a 1124751 |
| 6 | What was the hardest engineering challenge? | point-in-time panel（as-of join + 未来泄漏回放校验） | PracHub 2026-04 |
| 7 | What was your database / storage strategy? | Parquet 分区（market/date）+ DuckDB 谓词下推；为什么不用 Postgres；ledger 追加不改 | LC 6020524 |
| 8 | How did you test it? | 470+ 测试文件；数据面的泄漏回放；策略层的 golden backtest；执行层对拍 NautilusTrader | 通用 |
| 9 | What would you do differently? | 更早做成本模型校准；把 factor catalog 的元数据放进 DuckDB 而不是 YAML | 通用 |
| 10 | Tell me about the async / concurrency in your project. | 数据拉取用 asyncio + 信号量限并发（对应 pc02）；训练用多进程；为什么不混用 | 1p3a 1124751 |
| 11 | （PayPal）Walk me through the Amex settlement pipeline end to end. | [[S1]] §5 英文首答 | Blind（简历深挖） |
| 12 | （PayPal）What's the hardest production issue you've handled? | [[S3]]（NULL 传播）或 [[S9]]（出款延迟）；先说止血再说根因 | Glassdoor "RCA" 场景 |
| 13 | （PayPal）How did you decide between the two designs in the data-source switch? | [[S5]]（静态拆分 vs fallback；影子核对 0.224%） | 通用 |
| 14 | How do you use AI tools in your work, and how do you trust the code? | Claude Code 做 review/测试生成/重构；信任来自测试与行为对拍（[[S7]] schema pool 让多 agent 并行）；Chakra 复盘里这题答过 | JD "AI-native"；Snowflake Chakra 亲历 |
