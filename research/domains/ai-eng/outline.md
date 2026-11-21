# AI 应用工程（AI Engineering）：把大模型做成可靠的产品

读者：资深后端工程师，机器学习基础薄弱，目标是在 AI 团队里说得出生产系统怎么搭、怎么测、怎么省钱、怎么防出事。
和 ai-literacy 的分工：那边讲「是什么、为什么」（概念层），这里讲「怎么做、哪里会坏、怎么量」（工程层）。
记号：`*` = 帕累托核心；`(需先: …)` = 真依赖。

## 1. 起点：什么时候该做、怎么选
- * AI 工程栈与它和传统后端的差别（AI engineering stack）— 应用层、模型层、基础设施层；输出是概率性的，「正确」要靠评测定义而不是单元测试断言 〔出处：ai-engineering Ch.1 The AI Engineering Stack（Three Layers、AI Engineering vs ML / Full-Stack Engineering）；Ch.2 The Probabilistic Nature of AI〕
- * 先用最简单的办法：单次调用 → 工作流 → 智能体（simplest thing first）— 每升一级换来什么、多付什么（延迟、成本、可调试性），用评测结果决定是否升级 〔出处：ai-engineering Ch.10 AI Engineering Architecture（Step 1–5 逐级加复杂度）；Ch.6 Agents；工作流到智能体的分级另见 https://www.anthropic.com/engineering/building-effective-agents〕
- * 用例评估与期望设定：哪些功能值得上 LLM — 人工替代成本、容错度、可验证性；「演示 80% 容易，最后 20% 要几个月」 〔出处：ai-engineering Ch.1 Planning AI Applications（Use Case Evaluation、Setting Expectations、Milestone Planning）〕
- * 模型选型流程：自建还是买接口（build vs buy）— 数据隐私、延迟、成本、可控性、供应商锁定五个维度；先用最强模型跑通再往下压 〔出处：ai-engineering Ch.4 Model Selection（Model Selection Workflow、Model Build Versus Buy）〕
- 读公开基准选模型：它回答不了的问题 — 基准与自家任务的相关性、污染；怎么用自己的评测集重新排名 〔出处：ai-engineering Ch.4 Navigate Public Benchmarks（Benchmark selection and aggregation、Data contamination）〕
- 框架该不该用：LangChain、LlamaIndex 与直接调接口 — 框架隐藏提示和响应带来的调试代价；先写裸调用，读懂框架在做什么再引入 (需先: 先用最简单的办法) 〔出处：无书，待找（书中多处顺带提到 LangChain / LlamaIndex，无专节）〕

## 2. 检索增强生成工程（RAG Engineering）
- * RAG 流水线全景：摄取、分块、索引、检索、重排、生成 — 每一段独立可测；先定位是检索错还是生成错 〔出处：ai-engineering Ch.6 RAG Architecture〕
- * 文档解析与分块（chunking）：固定长度、按结构、语义分块 — 块太大稀释信号、太小丢上下文；表格、代码、PDF 的特殊处理 〔出处：ai-engineering Ch.6 Retrieval Optimization → Chunking strategy；RAG Beyond Texts（Multimodal RAG、RAG with tabular data）〕
- * 嵌入模型选择与维度 — 领域适配、多语言、维度与存储成本的权衡；换模型要全量重建索引 〔出处：ai-engineering Ch.3 Introduction to Embedding；Ch.6 Embedding-based retrieval〕
- * 向量索引与近似最近邻（ANN）：HNSW、IVF、乘积量化 — 召回率、延迟、内存、更新代价四项权衡；什么时候用现有数据库的向量扩展就够 〔出处：ai-engineering Ch.6 Sparse Versus Dense Retrieval → Embedding-based retrieval（向量搜索算法 HNSW / IVF / PQ）〕
- * 混合检索：关键词（BM25）加向量，再做融合 — 为什么纯向量会漏掉专有名词和编号；倒数排名融合（RRF）怎么合并两路结果 〔出处：ai-engineering Ch.6 Combining retrieval algorithms（含 RRF）；Term-based retrieval〕
- * 重排序（reranking）：交叉编码器二次打分 — 召回要广、精排要准的两段式；加一级的延迟和成本 〔出处：ai-engineering Ch.6 Retrieval Optimization → Reranking〕
- 查询重写与扩展：HyDE、多查询、分解子问题 — 用户问题和文档措辞不匹配时怎么补；每种改写多一次模型调用 (需先: RAG 流水线全景) 〔出处：ai-engineering Ch.6 Retrieval Optimization → Query rewriting、Contextual retrieval（书中未讲 HyDE）〕
- 元数据过滤与多租户权限 — 检索阶段就按权限过滤，而不是生成后再遮蔽；先过滤还是后过滤对召回的影响 〔出处：无书，待找（书中仅在 Ch.6 顺带提 metadata）〕
- * 检索评测：召回率@k、精确率、MRR、nDCG — 没有标注就先用 LLM 合成问答对；检索指标和最终答案质量分开看 〔出处：ai-engineering Ch.6 Evaluating Retrieval Solutions〕
- * RAG 生成端评测：忠实度（faithfulness）与答案相关性 — 答案是否只来自给定上下文；引用核对 (需先: 检索评测) 〔出处：ai-engineering Ch.4 Generation Capability → Factual consistency；Ch.3 AI as a Judge〕
- RAG 的典型故障表：该检的没检到、检到了没用、过期数据、冲突文档 — 每类故障对应的排查入口与修法 〔出处：无书，待找（可查 Barnett 等《Seven Failure Points When Engineering a RAG System》，待核）〕
- 长上下文还是 RAG：什么时候直接塞整库 — 成本、延迟、「中间丢失」；缓存前缀让长上下文变便宜 〔出处：ai-engineering Ch.5 Context Length and Context Efficiency；Ch.6 RAG（部分）〕
- 智能体式检索与知识图谱检索（GraphRAG）— 多跳问题单次检索不够；图索引的构建成本和适用面 〔出处：无书，待找（GraphRAG 论文 arXiv 2404.16130，待核；Ch.6 Tools → Knowledge augmentation 仅涉及智能体检索）〕
- 索引的增量更新与数据新鲜度 — 变更捕获、软删除、嵌入版本；索引与源数据不一致怎么发现 〔出处：无书，待找〕

## 3. 智能体工程（Agent Engineering）
- * 工作流模式五件套：提示词链、路由、并行、编排者—执行者、评估者—优化者 — Anthropic 的分类；每种适用的任务形状 (需先: 先用最简单的办法) 〔出处：无书，https://www.anthropic.com/engineering/building-effective-agents（Ch.6 Planning 只讲控制流：顺序、并行、条件、循环）〕
- * 智能体循环的工程化：停止条件、最大步数、预算 — 没有终止条件的循环会烧钱；每步都要有环境反馈当地面真相 〔出处：ai-engineering Ch.6 Agent Overview、Planning（Reflection and error correction）、Agent Failure Modes and Evaluation → Efficiency〕
- * 工具设计（agent-computer interface）：命名、参数、描述、返回内容 — 工具描述就是给模型的 API 文档；让错误难以发生（poka-yoke）；返回精简而有信息量 〔出处：ai-engineering Ch.6 Tools（Knowledge augmentation、Capability extension、Write actions）；Tool selection〕
- * 工具的幂等、权限与副作用分级 — 读、写、不可逆三类；写操作带幂等键，高风险操作要确认 〔出处：ai-engineering Ch.6 Tools → Write actions（部分；幂等键书中无）〕
- * 错误处理与重试：把错误当观察返回给模型 — 可重试与不可重试、退避、重复调用检测、熔断 〔出处：ai-engineering Ch.6 Reflection and error correction；Agent Failure Modes → Tool failures；Ch.10 Gateway（Fallback，部分）〕
- * 智能体状态与记忆：会话内状态、外部存储、压缩 — 什么放上下文、什么放数据库；摘要压缩的信息损失 〔出处：ai-engineering Ch.6 Memory〕
- 上下文工程（context engineering）：窗口里放什么、怎么裁剪 — 工具结果清理、即时检索、笔记文件；上下文腐烂（context rot） 〔出处：ai-engineering Ch.5 Context Length and Context Efficiency、Terminology Ambiguity: Prompt Versus Context；Ch.6 Memory（部分）〕
- * 人在回路（human-in-the-loop）：审批点与升级 — 按风险分级打断；审批疲劳的后果；默认拒绝与可撤销设计 〔出处：无书，待找（书中 Ch.4 仅一处提及）〕
- * 长任务的持久化执行（durable execution）— 检查点、可恢复、幂等；用工作流引擎（如 Temporal 类）承载智能体循环 (需先: 智能体循环的工程化) 〔出处：无书，https://docs.temporal.io（待核）〕
- 多智能体：何时拆、怎么协作与汇总 — 并行研究类任务收益大、写代码类任务耦合高；token 成本放大数倍 〔出处：无书，https://www.anthropic.com/engineering/multi-agent-research-system（待核；Ch.6 仅少量提及）〕
- 子智能体与上下文隔离 — 用独立窗口做搜索，只回传摘要；避免主上下文被污染 〔出处：无书，同上（Anthropic 多智能体研究系统文章，待核）〕
- MCP 在生产里的用法与坑 — 工具数量膨胀、工具描述占上下文、远程服务器认证；代码执行方式降低 token (需先: 工具设计) 〔出处：无书，https://modelcontextprotocol.io（书未提及 MCP）〕
- 智能体沙箱与执行环境 — 容器、网络出口控制、资源限额；代码解释器与浏览器的隔离 〔出处：无书，待找（Ch.6 Tools → Capability extension 仅提代码解释器）〕
- 智能体的典型失败：错误累积、循环、目标漂移、过度行动 — 每步 95% 成功，二十步后剩多少；从轨迹里定位首个出错步 〔出处：ai-engineering Ch.6 Agent Failure Modes and Evaluation（Planning failures、Tool failures、Efficiency）〕

## 4. 评测工程（Evals as Engineering）
- * 为什么评测是第一优先级：三个循环（评估、调试、改动）— 没评测就只能凭感觉改提示，改一处坏一处 〔出处：ai-engineering Ch.4 Evaluation-Driven Development；Ch.3 Challenges of Evaluating Foundation Models〕
- * 先看数据：错误分析与失败模式归类（error analysis）— 读一百条真实轨迹，开放式标注再归类；评测从失败里长出来，不是从通用指标来 〔出处：ai-engineering Ch.4 Step 3 Define Evaluation Methods and Data → Annotate evaluation data、Iterate（部分）；另见 https://hamel.dev/blog/posts/evals/〕
- * 评测三层：断言单测、人工与模型评审、线上 A/B — 成本递增、频率递减；每层各自抓什么 〔出处：ai-engineering Ch.3 Exact Evaluation、AI as a Judge、Ranking Models with Comparative Evaluation；Ch.4 Step 3 Select evaluation methods〕
- * 黄金集（golden set）的构建与维护 — 来源（线上采样、专家编写、合成）、覆盖、版本化、防污染；定期补入新失败样本 〔出处：ai-engineering Ch.4 Step 3 → Annotate evaluation data；Ch.8 Data Curation（Quality、Coverage、Quantity）〕
- * 代码断言与可验证评测 — 能用正则、解析器、执行结果判定的就不要用模型判；评测成本差两个数量级 〔出处：ai-engineering Ch.3 Exact Evaluation → Functional Correctness〕
- * 以 AI 当裁判（LLM-as-judge）与它的坑 — 位置偏好、冗长偏好、自我偏好；二元判定加理由比打 1–10 分稳 (需先: 黄金集) 〔出处：ai-engineering Ch.3 AI as a Judge（Why / How / Limitations：Inconsistency、Criteria ambiguity、Biases）〕
- * 让裁判对齐人类：人工标注、一致率、精确率与召回率 — 不平衡数据上总体一致率会骗人；评委也要有自己的测试集 〔出处：ai-engineering Ch.3 How to Use AI as a Judge；Ch.4 Step 3 → Evaluate your evaluation pipeline〕
- * 回归测试与 CI 门限 — 每次改提示、改模型、改检索都跑；通过率阈值是产品决定；噪声下怎么判「真退步」 〔出处：ai-engineering Ch.4 Evaluation-Driven Development、Step 3 → Iterate（部分；CI 门限书中无）〕
- 评测的统计功效：样本量、置信区间与非确定性 — 多次采样、种子、温度；差 2 个点是不是噪声 〔出处：ai-engineering Ch.4 Step 3 → Evaluate your evaluation pipeline（部分）；Ch.2 The Probabilistic Nature of AI → Inconsistency〕
- 智能体评测：轨迹、工具调用、终态检查 — 评结果还是评过程；多轮与有状态环境的评测；pass@k 与 pass^k（可靠性） 〔出处：ai-engineering Ch.6 Agent Failure Modes and Evaluation；Ch.3 Functional Correctness（pass@k；pass^k 书中无）〕
- * 线上评测与生产监控：抽样打分、防护措施指标、用户信号 — 离线好不等于线上好；漂移时报警 (需先: 回归测试与 CI 门限) 〔出处：ai-engineering Ch.10 Monitoring and Observability（Metrics、Drift detection）；Ch.10 User Feedback〕
- 基准的完整性：污染、饱和、刷分 — 为什么公开榜单不能代替自家评测 〔出处：ai-engineering Ch.4 Navigate Public Benchmarks → Data contamination with public benchmarks〕

## 5. 护栏与安全（Guardrails & Prompt-Injection Defence）
- * 威胁模型：OWASP LLM Top 10（2025）— 提示注入、敏感信息泄露、供应链、输出处理不当、过度代理、无界消耗等十项 〔出处：无书，https://genai.owasp.org/llm-top-10/（Ch.5 Defensive Prompt Engineering 仅涉及其中提示注入与信息泄露）〕
- * 直接与间接提示词注入（prompt injection）— 间接注入来自网页、邮件、文档、工具返回；为什么模型分不清指令与数据 〔出处：ai-engineering Ch.5 Jailbreaking and Prompt Injection（Direct manual prompt hacking、Automated attacks、Indirect prompt injection）〕
- * 「致命三要素」：私有数据、不可信内容、对外通信 — 三者同时具备就可被窃取数据；设计上拆开比检测更可靠 〔出处：无书，https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/〕
- * 过度代理与最小权限（excessive agency）— 工具范围、凭据范围、按用户身份下发权限；读与写分离 〔出处：ai-engineering Ch.5 Defenses Against Prompt Attacks → System-level defense（部分）；另见 OWASP LLM Top 10〕
- * 输出处理：把模型输出当不可信输入 — 渲染链接与图片的外泄通道、拼接 SQL 与命令、XSS；模式校验后再执行 〔出处：ai-engineering Ch.10 Step 2 Put in Guardrails → Output guardrails（部分）；另见 OWASP LLM Top 10〕
- * 输入输出防护措施的分层 — 结构校验、内容安全分类、语义与事实性检查、PII 脱敏；各层的误杀与漏放 〔出处：ai-engineering Ch.10 Step 2 Put in Guardrails（Input guardrails、Output guardrails、Guardrail implementation）〕
- 防护措施产品与检测器的局限 — 「拦住 95%」在安全上不及格；检测只作为一层，不作为边界 〔出处：ai-engineering Ch.10 Guardrail implementation；Ch.5 Defenses Against Prompt Attacks〕
- 架构级防御模式：双模型隔离、计划后执行、能力令牌 — 受信模型规划、不可信数据只经隔离模型处理 (需先: 「致命三要素」) 〔出处：无书，https://arxiv.org/abs/2503.18813（CaMeL 论文，待核）〕
- 越狱、红队与对抗测试 — 自动化红队集合纳入回归；记录攻击成功率 〔出处：ai-engineering Ch.5 Jailbreaking and Prompt Injection → Automated attacks〕
- 系统提示泄露与数据外泄 — 不要把密钥放进提示；多租户下缓存与上下文串用 〔出处：ai-engineering Ch.5 Proprietary Prompts and Reverse Prompt Engineering；Information Extraction〕
- 无界消耗与滥用控制：限流、配额、成本上限 — 拒绝服务与「钱包攻击」；按用户与按租户限额 〔出处：ai-engineering Ch.10 Step 3 → Gateway（限流，部分）；另见 OWASP LLM Top 10〕
- 结构化输出与受约束解码作为防护措施 — 语法约束保证可解析，不保证内容正确 〔出处：ai-engineering Ch.2 Structured Outputs（Constrained sampling）〕

## 6. 成本与延迟工程（Cost & Latency）
- * 成本模型：输入、输出、缓存读写分别计价 — 每次请求成本公式；智能体里上下文每步重复付费 〔出处：ai-engineering Ch.4 Evaluation Criteria → Cost and Latency；Ch.9 Inference Service Optimization → Prompt caching（部分）〕
- * 延迟分解：首 token 时间、每 token 时间、端到端 — 流式输出、并行调用、减少输出长度往往最有效 〔出处：ai-engineering Ch.9 Inference Performance Metrics → Latency, TTFT, and TPOT〕
- * 提示词缓存（prompt caching）：稳定前缀放前面 — 命中条件、生存期、写入溢价；提示设计要把变量放后面 〔出处：ai-engineering Ch.9 Inference Service Optimization → Prompt caching；Ch.10 Step 4 Reduce Latency with Caches〕
- * 精确缓存与语义缓存 — 语义缓存有误命中风险；用约束输入或条目 ID 作键更安全 〔出处：ai-engineering Ch.10 Step 4 → Exact caching、Semantic caching〕
- * 模型路由与级联：小模型先答、不确定再升级 — 分类器路由、置信度级联、成本节省与质量下降要用评测验证 〔出处：ai-engineering Ch.10 Step 3 Add Model Router and Gateway → Router〕
- * 批量接口与异步处理 — 离线任务半价；批量用于评测、数据标注、回填 〔出处：ai-engineering Ch.9 Online and batch inference APIs〕
- 减 token：精简提示、压缩上下文、限制输出 — 先量出 token 花在哪一段，再砍 〔出处：ai-engineering Ch.5 Context Length and Context Efficiency（部分）〕
- 推理预算与思考模式的取舍 — 推理模型按需开启；思考 token 也计费 〔出处：ai-engineering Ch.2 Sampling → Test Time Compute〕
- 限流、重试与降级策略 — 429 退避与抖动、多供应商备份、流式中断的恢复 〔出处：ai-engineering Ch.10 Gateway（rate limits、fallback）（部分）〕
- 自托管还是接口：盈亏平衡点 — 利用率是关键变量；GPU 闲置成本 (需先: 成本模型) 〔出处：ai-engineering Ch.4 Model Build Versus Buy → Open source models versus model APIs；Ch.9 Selecting Accelerators（部分）〕

## 7. 可观测性与排障（Observability）
- * 追踪（trace）与跨度（span）：一次请求里的每次模型与工具调用 — 记录输入、输出、延迟、token、成本；OpenTelemetry 的生成式语义约定 〔出处：ai-engineering Ch.10 Monitoring Versus Observability → Logs and traces〕
- * 日志里的隐私与留存 — 提示与回复含个人信息；脱敏、采样、保留期 〔出处：ai-engineering Ch.10 Logs and traces（部分；隐私与留存书中无专节，待找）〕
- * 从线上轨迹到评测集：把失败变成测试 — 排障闭环的核心；标注界面要把所有上下文放一屏 〔出处：ai-engineering Ch.10 User Feedback；Ch.4 Step 3 → Annotate evaluation data（部分）〕
- 提示词与配置的版本管理 — 提示像代码一样入库、发布、回滚；变更与指标关联 〔出处：ai-engineering Ch.5 Organize and Version Prompts〕
- 质量指标与业务指标并看 — 拒答率、工具错误率、重试率、点赞率、任务完成率 〔出处：ai-engineering Ch.10 Metrics；Ch.4 Step 2 → Tie evaluation metrics to business metrics〕
- 供应商事故与模型静默变更的应对 — 固定模型快照、金丝雀、对照回放 〔出处：ai-engineering Ch.4 "Are OpenAI's Models Getting Worse?"；Ch.10 Drift detection（部分）〕

## 8. 数据飞轮与反馈（Data Flywheel）
- * 显式与隐式用户反馈 — 点赞、重新生成、采纳与忽略、编辑距离；隐式信号更便宜但更噪 〔出处：ai-engineering Ch.10 User Feedback → Extracting Conversational Feedback〕
- * 反馈设计与它的偏差 — 反馈稀疏、极端用户占多数；怎么让用户顺手给出信号 〔出处：ai-engineering Ch.10 Feedback Design、Feedback Limitations（Biases、Degenerate feedback loop）〕
- * 防御式用户体验（defensive UX）— 给出处、可撤销、易于忽略、设定预期；错误不可避免时的体面 〔出处：无书，https://eugeneyan.com/writing/llm-patterns/（待核）〕
- 把生产数据转成评测集与训练数据 — 去标识、去重、质量过滤；谁有权使用用户数据 〔出处：ai-engineering Ch.8 Data Curation、Data Processing（Inspect、Deduplicate、Clean and Filter、Format）；Ch.10 User Feedback〕
- 合成数据与蒸馏的工程流程 — 强模型生成、过滤、训练小模型；许可条款的限制 〔出处：ai-engineering Ch.8 Data Augmentation and Synthesis、Model Distillation〕

## 9. 微调决策（Fine-tuning Decisions）
- * 先提示、再检索、最后微调 — 决策树：缺知识用 RAG，缺行为/风格/格式才考虑微调 〔出处：ai-engineering Ch.7 When to Finetune；Finetuning and RAG〕
- * 微调的理由与反对理由 — 延迟与成本、专用格式、小模型替代大模型；数据需求、维护负担、模型升级后要重做 〔出处：ai-engineering Ch.7 Reasons to Finetune、Reasons Not to Finetune〕
- * LoRA 与参数高效微调的工程含义 — 只训小矩阵、可热插拔多适配器；显存账怎么算 〔出处：ai-engineering Ch.7 Parameter-Efficient Finetuning（PEFT techniques、LoRA）；Memory Math〕
- 偏好微调与强化微调的适用面 — DPO、基于可验证奖励的强化学习；什么任务值得 〔出处：ai-engineering Ch.2 Post-Training → Preference Finetuning（Reward model）（部分；DPO 与可验证奖励 RL 书中无专节）〕
- 数据集工程：质量、覆盖、数量 — 质量压倒数量；去重与格式化；标注一致性 〔出处：ai-engineering Ch.8 Data Curation（Data Quality、Coverage、Quantity）、Data Processing〕
- 微调后的评测与回退 — 对比基线、灾难性遗忘检查、保留旧模型的路径 〔出处：ai-engineering Ch.7 Finetuning Tactics（部分）；Ch.4 Design Your Evaluation Pipeline〕

## 10. 网关与平台（LLM Gateway & Platform）
- * 模型网关的职责：统一接口、路由、密钥、限流、审计 — 为什么应用不该直连供应商；多供应商回退 〔出处：ai-engineering Ch.10 Step 3 → Gateway〕
- * 多租户的配额、预算与成本归因 — 按团队与功能记账；超预算熔断 〔出处：ai-engineering Ch.10 Gateway（访问控制、成本，部分）〕
- * 编排与管道：队列、工作流引擎、异步任务 — 长耗时调用不放在请求线程里 〔出处：ai-engineering Ch.10 AI Pipeline Orchestration〕
- 发布与灰度：模型与提示的金丝雀与影子流量 — 双跑对比、自动回滚条件 (需先: 回归测试与 CI 门限) 〔出处：无书，待找〕

## 不收（out of scope）
- 神经网络、注意力、分词等原理 — 在 llm-inference:basics，先读那边
- 推理服务内部（批处理、KV 缓存、投机解码、量化）— 属于 llm-inference
- 训练基础设施与分布式训练 — 非应用工程范围；ml-system-design 有概览
- 经典推荐与搜索排序系统 — ml-system-design:classic
- 具体框架 API 的逐页用法（LangChain、LlamaIndex、LangGraph）— 变化太快，只在引用层出现
- 提示词技巧大全 — ai-literacy:use.prompting 已覆盖，这里只讲提示的版本管理与评测
- 模型对齐与可解释性研究 — ai-literacy:safety
- 行业格局与商业分析 — 放 ai-industry

## 与已有领域的重叠
| 已有叶子 | 处理 | 说明 |
|---|---|---|
| ai-literacy:use.rag / use.vector-search | 更深 | 那边讲概念与嵌入；这里讲切块、混合检索、重排、检索评测、增量更新 |
| ai-literacy:use.tool-calling / agents.loop / agents.mcp | 更深 | 那边讲「是什么」；这里讲工具设计、幂等、重试、持久化执行 |
| ai-literacy:agents.context-memory / use.context-engineering | 链接 | 这里只写工程化的取舍（裁剪、压缩、子智能体隔离），概念链回 |
| ai-literacy:agents.security / safety.jailbreak-guardrails | 更深 | 加威胁模型、致命三要素、架构级防御、输出处理 |
| ai-literacy:evals.app-evals / evals.benchmarks | 更深 | 这里是整个评测工程：错误分析、黄金集、评委对齐、CI、线上评测；基准完整性只留一叶并链接 |
| ai-literacy:use.prompt-caching / use.api-economics | 更深 | 加缓存设计、语义缓存风险、路由与级联、盈亏平衡 |
| ai-literacy:use.adaptation-choices / models.sft-vs-rl | 更深 | 决策树与数据集工程；训练原理跳过 |
| ai-literacy:use.structured-output | 链接 | 仅作护栏一叶引用 |
| ai-literacy:work.app-architecture | 更深 | 它是一页总览，这里把网关、护栏、缓存、可观测各拆成可追问的叶子 |
| ml-system-design:evaluation.llm-eval / regression-gates | 链接 | 回归门与 LLM 评委在设计题里出现；这里给工程实现 |
| ml-system-design:llm-platform.gateway-routing / observability / eval-platform | 链接 | 设计题答法在那边；这里讲网关与追踪的具体职责与坑，避免重复设计框架 |
| ml-system-design:genai.rag | 链接 | 设计题模板在那边；这里是它的零件 |
| ml-system-design:mlops.* | 跳过 | 经典 MLOps，不重复 |
| llm-inference:serving.* / metrics.* | 链接 | 延迟指标定义（TTFT、TPOT）引用，不重讲 |

## 卡片格式建议
- 每张卡先给一个具体故障或决策场景（「检索召回高但答案还是错」），再给机制与解法；不写「第几章说」。
- 带数字：延迟、成本、缓存命中后的价格比例、召回率改善量；没核实的数字不上卡（供应商价格会变，只写比例与公式）。
- 对比卡：混合检索 vs 纯向量、语义缓存 vs 精确缓存、工作流 vs 智能体、微调 vs RAG，各列适用条件与代价。
- 至少 30% 带图：RAG 流水线、智能体循环与重试、评测三层、网关架构、致命三要素三圈图（mermaid 或 svg）。
- 代码卡用短 Python 片段加行内注释：重试与幂等键、RRF 融合、LLM 评委的二元判定与一致率计算、缓存键设计。

## 书里有、大纲没有

**ai-engineering（Huyen）**

- 采样参数与非确定性（Ch.2 Sampling：温度、top-k、top-p、停止条件）— 大纲只在"评测统计功效"与"结构化输出"里间接涉及；工程上要懂怎么固定输出
- 评估标准的分类（Ch.4 Evaluation Criteria：领域能力、生成能力、指令遵循、成本延迟）— 大纲缺"评什么"的起点，建议作评测工程的第一叶
- 评估指南与评分细则（Ch.4 Step 2 Create an Evaluation Guideline：评分标准加示例、与业务指标挂钩）— 与"黄金集"互补
- 比较评估（Ch.3 Ranking Models with Comparative Evaluation）— 成对比较与排名的瓶颈，用来理解公开榜单
- 开源、开放权重与许可（Ch.4 Open source, open weight, and model licenses）— 自建还是买接口的法律面，大纲只有成本面
- AI 产品护城河与里程碑、维护（Ch.1 AI product defensibility、Milestone Planning、Maintenance）— 起点章节缺长期规划
- 超越文本的 RAG：多模态与表格数据（Ch.6 RAG Beyond Texts）— 包括文本转 SQL 一类检索
- 智能体规划：规划与执行分离、反思、工具选择（Ch.6 Planning）— 大纲只讲循环工程化，缺规划本身
- 把模型限定在上下文内回答（Ch.5 How to Restrict a Model's Knowledge to Only Its Context）— 与 RAG 忠实度相关
- 模型合并与多任务微调（Ch.7 Model Merging and Multi-Task Finetuning）— 微调章节缺这一块；内存与量化部分已在 llm-inference 范围

## 大纲有、书里没有

共 17 叶没有任何一本对应的书覆盖（总 89 叶；另有 20 叶只被书部分覆盖，已在叶尾标"部分"）。

- 框架该不该用：LangChain、LlamaIndex 与直接调接口
- 元数据过滤与多租户权限
- RAG 的典型故障表：该检的没检到、检到了没用、过期数据、冲突文档
- 智能体式检索与知识图谱检索（GraphRAG）
- 索引的增量更新与数据新鲜度
- 工作流模式五件套：提示词链、路由、并行、编排者—执行者、评估者—优化者
- 人在回路（human-in-the-loop）：审批点与升级
- 长任务的持久化执行（durable execution）
- 多智能体：何时拆、怎么协作与汇总
- 子智能体与上下文隔离
- MCP 在生产里的用法与坑
- 智能体沙箱与执行环境
- 威胁模型：OWASP LLM Top 10（2025）
- 「致命三要素」：私有数据、不可信内容、对外通信
- 架构级防御模式：双模型隔离、计划后执行、能力令牌
- 防御式用户体验（defensive UX）
- 发布与灰度：模型与提示的金丝雀与影子流量

## 术语改动（采用 ai-engineering-zh 译本用词）

只改了叶子标题，描述文字与章标题未动。

| 原用词 | 改为 | 译本依据 |
|---|---|---|
| 切块 | 分块 | 6.1.3「分块策略」 |
| 查询改写 | 查询重写 | 6.1.3「查询重写」 |
| 提示缓存 | 提示词缓存 | 全书「提示词缓存」 |
| 提示注入 | 提示词注入 | 5.3.2「越狱与提示词注入」 |
| 提示链 | 提示词链 | 6.2 工具/规划段「提示词链」 |
| 提示与配置（版本管理） | 提示词与配置 | 5.2.7「提示词的组织与版本管理」 |
| 以大模型当评委 / 让评委对齐人类 | 以 AI 当裁判 / 让裁判对齐人类 | 3.4「AI当裁判」 |
| 护栏（叶子标题 4 处） | 防护措施 | 10.1.2「设置防护措施」 |
| 偏好优化 | 偏好微调 | 2.3.2「偏好微调」 |
| LLM 网关 | 模型网关 | 10.1.3「添加路由器和模型网关」 |

未改、留给 Chi 定：全篇「评测」译本几乎都写「评估」（731 处对 1 处），「提示」译本多写「提示词」。第五章章标题「护栏与安全」也未改。「致命三要素」「持久化执行」「过度代理」「人在回路」译本无对应词。
