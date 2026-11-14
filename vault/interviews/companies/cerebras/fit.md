# fit · 你的简历 vs Senior SDET, Release Integration Testing（逐条）

这页把 Cerebras 这个岗位的职位描述（JD）拆成一条一条，逐条对照你的简历：哪些是你能直接讲 3 分钟的强项，哪些只有相邻经验，哪些是空白。每条都写了该怎么说，以及空白要补什么。读完你应该知道：经理面里主动把话题引向哪里，哪里要诚实地划出边界。

> 评级：**强** = 简历上有直接证据且能讲 3 分钟 · **部分** = 有相邻经验，但缺关键一层 · **缺口** = 没有证据，不要硬说，补课 + 诚实表述。
> 诚实线：数字只说故事里的；不点同事和商户名；自己没做的不说自己做的；个人项目先说是个人项目。

## 0. 总览

| 类别 | 条数 | 强 | 部分 | 缺口 |
|---|---|---|---|---|
| Minimum qualifications | 9 | 4 | 5 | 0 |
| Preferred skills | 8 | 0 | 6 | 2 |
| What you will do | 10 | 3 | 7 | 0 |

**一句话画像**：你的强项是"**证明一个改动在多个阶段之间是安全的**"：行为一致性测试、跨阶段端到端测试、质量门、值班排查、用证据给出上不上线的建议。弱项是 JD 后半的那一层：**AI 推理、编译器、运行时、硬件**，以及 Linux 级别的调试工具。面试策略：把强项讲成"集成验证"的证据，把 AI 讲成"我知道它在哪、懂到哪一层、怎么学"。

---

## 1. Minimum qualifications

| # | JD 原文 | 评级 | 证据 | 该怎么说 | 缺口：补什么 |
|---|---|---|---|---|---|
| M1 | Strong software engineering fundamentals with professional experience developing software, automated testing frameworks, or test infrastructure | **强** | PayPal 近两年全职 + 实习；从桩代码建 Amex 结算管线；配置驱动的质量门框架；schema pool（个人仓库）；个人平台 470+ 测试文件 | "I've built production software end to end, and the parts I'm proudest of are the verification parts: a quality-gate framework and a deterministic test-environment tool." | — |
| M2 | Proficiency in Python, Go, or a similar programming language, with demonstrated experience writing maintainable, production-quality code | **部分** | Python：个人平台 66K+ 行；工作里主要是 Java、SQL、Kotlin。Go：简历没有 | "My largest Python codebase is my own research platform, 66 thousand lines with 470-plus test files; at work it's Java and SQL. I haven't written Go in production." | 编码轮全程用 Python；`asyncio`、`concurrent.futures`、`subprocess`、pytest fixture 与 marker |
| M3 | Experience designing, developing, and maintaining automated tests and frameworks for complex software systems | **部分** | 迁移的行为一致性测试；跨"promote → fee"的端到端测试；质量门框架（数据校验） | "My frameworks have been for data correctness: config-driven checks with a readiness status that downstream jobs join on. The shape — checks as entry criteria, a status as the exit — is the same as a release gate." | 通用测试框架的结构：fixture、插件、结果存储、分片、重跑 |
| M4 | Strong debugging and problem-solving skills, including the ability to investigate failures across multiple components, analyze logs and system behavior, and identify root causes | **强** | S3 静默 NULL：切片 → 单行 → 回溯到函数重载；S8 7 分钟根因 + 扫全仓库；值班 | 讲 S3，强调"每个阶段的单元测试都过了，bug 在阶段之间" | — |
| M5 | Solid understanding of software testing methodologies, including integration testing, system testing, regression testing, and end-to-end validation | **部分** | 做过端到端、回归（行为一致性）、切换验证；但没有系统地用过 SDET 的术语 | "I've done all four in practice; I'd describe them as…" 然后用测试金字塔、回归分层、风险驱动这几个词讲你做过的事 | 测试分层、回归套件分层、风险驱动测试、flaky 管理、测试替身 |
| M6 | Experience working with CI/CD pipelines, test automation infrastructure, and software development workflows | **部分** | 个人平台自托管 CI；迁移里的版本化 `DROP`；部署与上线分开、默认关闭的开关 | "I separate deploy from release, ship dark behind a toggle, and run my own CI for the research platform." | 【待补：PayPal 的 CI/CD 里你实际做过什么】；CI 流水线设计、构建缓存、测试选择 |
| M7 | Working knowledge of operating systems, networking, distributed systems, or systems-level software concepts | **部分** | 分布式：Kafka 消费侧（并行度 = replicas × tasks.max，上限是分区数）、至少一次 + 幂等、Snowflake 存储模型。OS 和网络：没有亲手经验 | "Distributed systems from the data side — at-least-once delivery, idempotent writes, partition-capped parallelism. OS and networking I know as a user." | 进程与线程、调度、共享内存、`strace` / `gdb` / `py-spy`、TCP 基础 |
| M8 | Ability to independently own complex technical problems, prioritize testing efforts, and drive issues through resolution | **强** | S1 从桩代码到 18 个月生产；S7 没人分配；S6 用规模估算叫停上线 | 讲 S1 或 S7；"No ticket, no owner — I chose to remove the friction." | — |
| M9 | Strong communication and collaboration skills, with experience working across multiple engineering teams to deliver reliable software | **强** | S9 事故里给出 SLA 定论、主张 region conditional；跨三个团队 50 条回复的争论用一条查询结束（1,079,627 vs 0 行） | "I end arguments with a query anyone can re-run." | — |

## 2. Preferred skills

| # | JD 原文 | 评级 | 证据 | 该怎么说 | 缺口：补什么 |
|---|---|---|---|---|---|
| P1 | Experience testing or developing distributed systems, infrastructure software, runtime systems, compilers, kernels, or other low-level software | **部分** | 分布式数据管线有；运行时、编译器、内核没有 | "Distributed pipelines yes; runtimes and compilers no — I'd learn the stack top-down from a request's path." | 编译器流水线、内核、运行时的白话版；[02-role-and-team.md](02-role-and-team.md) 第 2 节 |
| P2 | Experience with AI/ML infrastructure, LLM inference, model deployment, multimodal workloads, or large-scale compute environments | **缺口** | 只有相邻：个人 8-GPU 服务器上跑过 PyTorch 训练；用 OpenAI API 做过应用；每天用 AI 编程代理 | 先说 "I'm new to ML"，再说你懂到哪一层（解码受内存带宽限制、为什么晶圆快、跨晶圆流水线） | **最大的单项缺口**：`LLM 推理与 AI 加速器` 牌组按顺序学 |
| P3 | Exposure to hardware accelerators, GPU systems, software/hardware integration, or high-performance computing | **缺口** | 8-GPU 服务器的使用者 | "I've used a GPU server as a user; I haven't worked at the hardware boundary." | GPU 与 HBM、SRAM、模拟器 vs 真机、固件与驱动版本不匹配 |
| P4 | Experience building scalable test frameworks, distributed test systems, release pipelines, or internal developer tools | **部分** | 质量门框架（铺开 8 个数据域）；schema pool（几个代理会话并发跑迁移和测试）；值班副驾（相邻团队在用） | 讲 D3 + D5 | 测试执行平台的设计：排队、分片、资源锁、结果存储 |
| P5 | Familiarity with performance testing, profiling, observability, fault injection, reliability engineering, or production failure analysis | **部分** | 可观测性与生产故障分析：强（Sentry、Datadog、RCA）。性能测试、剖析、故障注入：没有 | "Observability and production failure analysis, yes. Profiling — the honest version is capacity reasoning before shipping, not profiling a running system." | 推理的性能指标（TTFT、每 token 间隔、tok/s）；基准噪声与回归阈值；故障注入 |
| P6 | Experience with containers, Kubernetes, cloud infrastructure, cluster orchestration, or large-scale distributed computing environments | **部分** | 实习：Kafka proxy 跑在 Kubernetes 里；Docker；AWS Developer Associate 认证；GCP | "I've deployed and debugged on Kubernetes as an application engineer, not as a cluster operator." | Pod、Deployment、Job、资源限制、`kubectl logs/describe` |
| P7 | Experience using debugging and observability tools to diagnose complex system-level issues | **部分** | Datadog、Sentry、交易追踪、查询剖面；没有 `gdb`、`strace` | 讲 D7；说清"system-level"那一层你还在学 | `gdb -p`、`strace -f`、`py-spy dump`、core dump |
| P8 | Experience working in fast-paced engineering environments, including startups or teams developing complex systems software | **部分** | 没有创业公司经历；个人项目节奏快；NULL 事故当天出根因、Terraform 当天三环境上线 | "I haven't worked at a startup. I've done same-day fixes in production and I'm comfortable with release-window intensity." | 【待补：你真实能接受的加班程度】 |

## 3. What you will do

| # | JD 原文 | 评级 | 证据 | 该怎么说 | 缺口：补什么 |
|---|---|---|---|---|---|
| W1 | Design, develop, and maintain automated test frameworks, tools, and infrastructure to validate AI inference software across multiple components and system layers | **部分** | 框架与工具有（质量门、schema pool、个人 CI）；对象不是 AI 推理 | "The frameworks I've built validate data across pipeline stages; the target changes, the shape doesn't." | 推理软件栈每一层是什么 |
| W2 | Independently own integration testing and qualification activities for complex inference-core features, identifying dependencies, interaction risks, and potential coverage gaps | **部分** | S5：一个人负责数据源切换的验证，列出风险（双写重复扣费、一个月去重盲区） | 讲 D4，强调"我把已知风险写在代码旁边" | 功能交互风险怎么列：运行时 × 内存 × 调度 × 模型执行 |
| W3 | Develop and execute comprehensive end-to-end, integration, regression, and system-level tests across AI frameworks, runtime, compiler, kernels, infrastructure, and hardware | **部分** | 端到端和回归有；AI 框架、编译器、内核、硬件没有 | 讲 D2 的"bug 在阶段之间"，再说 4.1 节的推理端点测试思路 | 参考实现对比、容差、评测集 |
| W4 | Analyze unit, simulation, benchmark, feature-test, and integration results to assess readiness, identify gaps, and provide evidence-based recommendations for release qualification | **强** | S5：逐字段比对 >99.9% + 生产查询 +0.224% 后才切换；S6：用规模估算给出分阶段上线建议 | "I don't recommend a cutover on a feeling: field-level parity, then the production query itself, then ship dark." | 五类证据各自能证明什么、不能证明什么 |
| W5 | Investigate and debug complex cross-stack failures, perform root cause analysis, collaborate with engineering teams on fixes, and implement automated tests to prevent regressions | **强** | S3 全流程：根因 → 复盘四个测试漏洞 → 加固 → 端到端测试；S8 修一个再扫一类 | 讲 D2 | — |
| W6 | Improve master and release-branch stability by identifying regressions, triaging failures, validating fixes, and contributing to release-quality metrics and reporting | **部分** | 值班分诊、健康检查；没有管过分支健康 | "I've triaged production failures daily as on-call; branch health is the same discipline one step earlier." | 失败分类、`git bisect`、flaky 隔离、分支健康指标 |
| W7 | Build and enhance internal tooling for test automation, diagnostics, monitoring, dashboards, CI/CD workflows, and release qualification pipelines | **部分** | 监控与告警（Datadog、健康检查）；值班副驾（拉 Slack、PagerDuty、Datadog 上下文，起草回复给我审） | 讲值班副驾和健康检查 | 发布验证流水线的结构 |
| W8 | Collaborate with feature engineering, Integration, Core Infrastructure, and release teams to improve test coverage, accelerate debugging, and support coordinated feature rollouts | **强** | S9 三人修复小组里给出 SLA 定论；跨团队争论；S8 先问再推 PR | "Own the piece you're the authority on, let others defer, stay out of the steps you don't own." | — |
| W9 | Contribute to test architecture, risk-based testing strategies, and continuous improvements in automation efficiency, system observability, and release reliability | **部分** | S6 的容量推理、S5 的有界扫描；ADR 写作 | "I write the trade-off down: three ADRs for the schema pool, one recording what I deliberately didn't fix." | 风险驱动测试、测试选择、回归分层 |
| W10 | Provide technical guidance and mentorship to junior engineers through code reviews, debugging sessions, and sharing testing best practices | **部分** | 团队上手文档（2024 年写，一直维护）；新同事的三块接入我的平台时，先定边界和契约再评审设计 | 只说真的；"I read every diff in money code, including the AI's." | 【待补：一次真实的代码评审或带人排查】 |

---

## 4. 缺口优先级（按"被问的概率 × 补得上的程度"）

| 优先 | 缺口 | 为什么 | 做什么 |
|---|---|---|---|
| 1 | **LLM 推理的白话理解**（P2、W3） | 测试岗也被问机器学习基础；经理一定会试探 | `LLM 推理与 AI 加速器` 牌组按顺序；[01-company-brief.md](01-company-brief.md) 第 1、3 节能口述 |
| 2 | **测试与发布的术语**（M5、W6、W9） | JD 的主体；你做过但说不出标准名字 | `软件测试与发布工程` 牌组：分层、flaky、分诊、发布门 |
| 3 | **Python 现场编码**（M2） | 技术面偏 Python | 编码练习全部用 Python；日志解析题 |
| 4 | **Linux 调试工具**（M7、P7） | "debug across components" 的下一层 | `strace`、`gdb`、`py-spy`、`top` 各会一个用法 |
| 5 | **编译器、运行时、硬件的白话版**（P1、P3） | JD 反复点名 | [02-role-and-team.md](02-role-and-team.md) 第 2 节的表能讲出来 |
| 6 | **Kubernetes 与 CI**（M6、P6） | 基础设施团队在这上面 | 基本对象和排查命令 |
| 7 | **性能测试**（P5） | 推理的速度就是产品 | TTFT、每 token 间隔、吞吐；基准噪声 |

## 5. 一句话版（放在回答的结尾，可复用）

> "My experience is strongest in proving changes are safe across components — parity tests, quality gates, end-to-end tests, and on-call root-causing. I'm new to ML inference and the hardware layers, which is what I've been learning in order; I'd expect my first months here to be about learning the stack from a request's path down to the wafer."
