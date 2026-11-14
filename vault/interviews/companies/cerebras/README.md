# Cerebras · Senior SDET, Release Integration Testing —— 从这里开始

这是 Cerebras Systems "AI Inference Core – Senior SDET, Release Integration Testing" 的备考入口。Cerebras 做整块晶圆大小的 AI 芯片，用它卖"让大语言模型回答得特别快"的推理服务；你申请的是推理软件核心团队里新建的发布集成测试小组（RIT），负责在功能合到一起之后、发布之前，证明整条推理链路跨层一起跑是对的。第一轮大概率是和招聘经理的 45 分钟视频面。你不懂 AI 没关系：公司简报从零讲起，经理面那页给了诚实说明缺口的说法。

**岗位**：AI Inference Core → Release & Feature Qualification → Release Integration Testing。
**地点**：Sunnyvale 或 Toronto，混合办公，每周至少 3 天到办公室，不接受全远程。
**下一轮**：经理面，45 分钟，视频（Microsoft Teams）。【待补：日期和时间、面试官姓名】
**之后**：三轮左右、每轮约 45 分钟的技术面，偏 Python，在 HackerRank 上写代码。

## 经理面之前必须做的事

1. **问招聘官三件事**：经理面要不要写代码、面试官是谁（是不是 RIT 的技术负责人）、后面几轮各考什么。
2. **把自我介绍说出声 3 遍**：30 秒版和 2 分钟版，见 [04-hm-screen.md](04-hm-screen.md) 第 1 节。录音听一遍，超时就删。
3. **能用 4 句话讲清"为什么晶圆级推理快"**：生成每个 token 都要读一遍全部参数 → 解码卡在内存带宽 → 参数放在片上 SRAM → 代价是容量小、大模型跨很多块晶圆。见 [01-company-brief.md](01-company-brief.md) 第 1、3 节。
4. **背 5 条公司事实**：[01-company-brief.md](01-company-brief.md) 第 9 节挑 5 条。
5. **准备 3 个项目深挖**：D2（静默 NULL）、D3（质量门）、D4（切换验证），各 60 秒，见 [04-hm-screen.md](04-hm-screen.md) 第 3 节。
6. **练一遍"你会怎么测 X"**：推理端点和一次发布，见 [04-hm-screen.md](04-hm-screen.md) 第 4 节。
7. **填完下面的【待补】**。
8. **挑 3 个反问**：见 [05-questions-to-ask.md](05-questions-to-ask.md)。

## 只有你能填的空

- 【待补：为什么离开 PayPal 的真实原因，一句话】
- 【待补：Ruby/Kotlin → Java 迁移的规模、最难的一个行为差异、数值怎么比】
- 【待补：个人项目 CI 每次跑什么、多久；一个测试救过你的真实例子】
- 【待补：一次和上级或资深同事意见不同、最后你让步并全力执行的经历；没有就用 S9 并如实说】
- 【待补：工作许可的状态、能否每周 3 天去 Sunnyvale、其他面试的时间线】
- 【待补：PayPal 的 CI/CD 里你实际做过什么；有没有写过 Go】

## 地图

| 想做什么 | 去哪 |
|---|---|
| **先看图**：面试流程、团队位置、发布流程、一次推理请求、晶圆为什么快、测试分层、分诊、带回家题、自我介绍、两周计划，14 张图 | [09-图解.md](09-图解.md) |
| Cerebras 卖什么、为什么快、怎么赚钱、对手是谁 | [01-company-brief.md](01-company-brief.md) |
| 团队在哪、RIT 管什么、一周做什么、用什么工具 | [02-role-and-team.md](02-role-and-team.md) |
| 每一轮的形式、考什么、怎么准备 | [03-loop.md](03-loop.md) |
| **经理面打法**：自我介绍、三个为什么、项目深挖、测试策略、AI 缺口 | [04-hm-screen.md](04-hm-screen.md) |
| **三轮技术面**：每轮考什么、45 分钟怎么分、出过的题和追问、允许用 AI 的轮次、带回家题详解 | [06-technical-rounds.md](06-technical-rounds.md) |
| **技术面练习**：五组可运行的 Python 题（失败签名、并行执行器、多频道队列、性能表判读、评测集剪枝），做的顺序和限时 | [07-practice.md](07-practice.md) |
| **力扣题**：和 Cerebras 有关的 49 道力扣题，按面试出现、公司题单频率、同类常考排好，对应牌组 `7 Cerebras 力扣` | [08-leetcode.md](08-leetcode.md) |
| 简历逐条对 JD：强项、相邻、缺口 | [fit.md](fit.md) |
| 反问：经理、工程师、CEO | [05-questions-to-ask.md](05-questions-to-ask.md) |
| 故事全文（S1、S3、S5、S6、S7、S8、S10、R1） | [Headlands 故事](../headlands/behavioral/stories/S3_silent-null-root-cause.md) 同目录 |
| 背景问题怎么答的方法 | [00_how_it_works.md](../headlands/behavioral/00_how_it_works.md) |

## Anki 牌组

每天刷 **`6 Cerebras`**（知识）和 **`7 Cerebras 力扣`**（每天 10 道题）。它按下面的顺序把各个牌组里和这个岗位有关的卡借过来，每天最多 60 张新卡，编号小的先出。每个知识点是一个子牌组：先出这次新写的卡，再出你以前学过的相关卡（名字带「· 延伸」）。

| 部分 | 内容 | 卡数 |
|---|---|---|
| 01 公司与岗位 | 公司、产品、晶圆级推理一张图、客户与 OpenAI、竞争对手、团队与 RIT、流程 | 33 |
| 02 招聘经理面 | 自我介绍、为什么、项目深挖、「怎么测 X」、AI 缺口怎么说、故事对题、反问 | 32 |
| 03 AI 从零开始 | 模型是什么 → 矩阵 → 神经网络 → 训练与推理 → 硬件 → token → 语言模型 → 生成循环 → 嵌入 → 注意力 → Transformer → 大模型 → 推理服务 | 54 |
| 04 机器学习基础 | 损失与梯度下降、优化器、反向传播、过拟合、L1 与 L2、分类指标、常见网络部件 | 28 |
| 05 测试策略与判定 | 测试计划、风险驱动、分层、集成、「怎么测 X」、回归分档、flaky、差分测试、浮点容差、黄金文件 | 110 |
| 06 发布工程与分诊 | 分支、主干常绿、cherry-pick、RC、发布门、阻断项、分诊、二分、失败签名、指标、测试框架、CI | 176 |
| 07 LLM 推理 | 前向计算、KV 缓存、批处理、投机解码、量化、并行、MoE、推理引擎、OpenAI 接口、指标与基准、数值与精度验证 | 137 |
| 08 加速器与编译器 | GPU、屋顶线、晶圆级引擎、为什么快、权重流式、主机与设备、编译器、kernel、运行时、软硬件集成 | 58 |
| 09 Python 与测试工具 | pytest 夹具、标记、插件与钩子、xdist、subprocess、asyncio、Go 基础 | 69 |
| 10 调试、Linux 与 K8s | 调试方法、日志、gdb、perf、死锁、Linux、网络、K8s 排障、指标与告警 | 98 |
| 11 编程题 | 解析日志、LeetCode 高频题、LLD 练习、并发编码、数值与并行编程 | 186 |
| 12 可靠性与性能测试 | 故障注入、长稳、故障切换、负载设计、性能回归检测 | 42 |
| 13 行为面方法 | 跨栈 bug、端到端负责、推迟发布、影响他人、排优先级、带人 | 28 |

经理面之前，01 和 02 一定要全部过完，03 至少过到「推理服务在做什么」。
