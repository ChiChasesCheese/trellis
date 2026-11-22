# AI 辅助开发（AI-Assisted Development）：用 AI 写、审、测代码

术语规则：技术术语一律用英文原词，正文用中文（Chi 2026-11-20）

读者：资深后端工程师，已经在用 Claude Code、Cursor 之类，想把它用成稳定的工程流程，并能在团队里讲清楚证据与风险。
和 ai-literacy 的分工：work.ai-coding / agents.coding-agents 只给概念与一页总览；这里是可操作的流程、验证方法、安全与度量。
记号：`*` = 帕累托核心；`(需先: …)` = 真依赖。

## 1. 工具形态与 mental model
- * 编程助手的四种形态：completion、chat、agent、background async — 各自的上下文来源、自主程度、适用任务；从补全到智能体是权责的转移
- * Coding agent 的工作原理：loop、tools、context — 读文件、跑命令、改代码、看结果再继续；能力来自环境反馈，不来自一次写对
- * Context window 是核心稀缺资源 — 窗口越满表现越差；对话里每一次读文件、跑日志都在占用；清理与压缩的时机
- * Capability boundaries：模型擅长与不擅长 — 擅长：样板、迁移、测试、解释代码、范围明确的改动；不擅长：隐含约束、跨系统一致性、没有验证手段的任务
- Non-determinism 与同题多解 — 同一提示每次结果不同；需要把「对不对」交给测试，而不是交给「看起来对」
- Model tier 选择：何时用强模型、何时用快模型 — 规划用强、批量机械改动用快；成本与吞吐
- 工具对照：terminal agent、IDE assistant、cloud async agent — Claude Code、Codex、Cursor、Copilot 的定位差异（只讲类型，不讲界面）

## 2. Workflow：spec、plan、implement、verify
- * Explore → plan → implement → commit 的四段循环 — 先只读探索，再让它写计划，再动手；跳过计划的代价
- * Spec-first / spec-driven development — 先写需求、验收标准、边界条件，再让智能体实现；规格就是评测
- * 给 agent 一个可运行的 check：tests、type check、lint、expected output — 最高杠杆的一件事；没有检查，「做完了」不可信
- * 写具体的 prompt：scope、constraints、references — 指向文件与现有模式、说明不要做什么；模糊提示换来过度实现
- * Small commits 与可回退 — 每个任务一个检查点；用版本控制当撤销键；大改拆成可审查的块
- 先问后做：让 agent interview 你 — 在需求不清时让模型提问，产出规格
- * TDD with agent：red → green — 先让它写失败的测试并确认失败，再实现；防止它为通过测试而改测试
- * 纠偏的时机：interrupt、rollback、重开 session — 同一错误纠正两次仍不对就清空重来；长对话里的纠偏越积越差
- Headless 与 batch：脚本化运行、scheduled 与 event-triggered — 无头模式、CI 里调用；输出格式、权限与预算上限
- * 并行 session 与 Git worktree — 每个会话一个隔离目录；合并冲突与任务切分
- Subagents：把探索与审查放进独立 context — 只回传摘要，保护主上下文；成本的另一面
- 长任务：checkpoint、progress file、init script — 跨上下文窗口接力；用文件而非对话保存状态

## 3. Context files 与可复用配置
- * 项目 context file：CLAUDE.md / AGENTS.md — 放命令、约定、坑；每次会话都加载，所以要短；删掉智能体能从代码里读出的内容
- * 写好 context file 的规则 — 具体可检验、不放空话；过长则规则被忽略；定期修剪；分层（用户级、项目级、子目录级）
- * 确定性规则用 hooks 与 permissions，建议性规则用文字 — 「必须」的事交给 hooks、沙箱、权限规则强制；写在提示里只是请求
- Skills 与 slash commands：把团队流程封装起来 — 按需加载而非常驻；发布、迁移、审查流程
- 连接外部工具：MCP 与 CLI — 优先用已有 CLI；MCP 服务器的上下文开销与信任问题 (需先: Coding agent 的工作原理)
- Context file 的跨工具标准：AGENTS.md 与各家文件名 — 多工具共存时单一来源加导入
- 对 legacy codebase 的引导：architecture map、glossary、domain conventions — 让智能体先建立地图；记录「为什么」而非「是什么」

## 4. Verification 与 code review（AI 写的代码怎么信）
- * Verification 优先于 generation：review 成为 bottleneck — 生成变便宜后，限制产出的是阅读与验证；审查要变成流程而非凭感觉
- * AI 代码的典型缺陷：几乎对但不对、hallucinated API、吞掉错误、over-engineering、悄悄改测试 — 每类的识别特征与排查办法
- * Small-diff review：限制变更体量、逐段读 — 大块 AI 差异无人能审；强制拆分
- * 独立 reviewer：让另一个 session 或模型审查 — 新上下文看差异，避免自我认同；审查提示要对照规格
- * Tests as contract：不要让生成者同时定义「对」 — 人写或人审验收测试；变异测试、属性测试检验测试质量
- * 运行它：真实环境的 end-to-end verification — 启动服务、请求、看日志与界面；类型检查通过不等于功能正确
- * Dependency 与 API 核实：包是否存在、版本是否匹配 — 虚构包名（slopsquatting）与过时用法；锁文件与文档对照
- Performance 与 complexity regression — AI 常写出 O(n²) 或多余查询；基准与查询计划检查
- Maintainability：duplication、style drift、consistency — 复制粘贴式生成累积技术债；linter 与架构测试约束
- * Comprehension debt：合并了没人读懂的代码 — 规则：不能向同事解释的代码不合并
- Review etiquette：披露 AI 参与、责任仍归提交者 — 团队约定；开源项目对 AI 贡献的政策

## 5. 用 AI 做测试与质量工作
- * 生成 unit tests：覆盖路径与边界 — 好用的前提：被测代码清晰；盯住「只断言实现」的伪测试
- * 用 AI 复现并定位 bug — 给日志、复现步骤与失败测试；让它先写复现再改
- Legacy code 的 characterization tests — 先固定现有行为，再重构；AI 适合批量生成
- 大规模 migration 与 refactoring — 框架升级、API 替换：脚本化 + 分批验证 + 每批一个检查点
- End-to-end 与 UI 测试：browser automation — 让智能体操作页面并截图验证；脆弱点与成本
- Fuzzing 与 property-based testing 辅助 — 让模型提出不变量与输入生成器
- Docs、comments 与 change description — 生成再校对；文档与代码漂移的检查

## 6. Security 与 risk
- * Secrets 与敏感数据：不进 prompt、不进 repo、不进 log — 环境变量与密钥管理器；让智能体读不到 .env 的权限规则
- * Prompt injection via repos — README、依赖、issue、网页里藏指令；智能体读到即可能执行
- * Permission model 与 sandbox — 允许/询问/拒绝规则、受限目录、网络出口；自动模式与「跳过所有确认」的风险边界
- * Supply chain 风险：hallucinated packages、malicious packages、被投毒的 skills 与 MCP servers — 先核实再安装；锁版本；审查第三方技能与服务器
- * Lethal trifecta 在 coding agent 里的体现 — 私有代码或密钥 + 不可信内容 + 能联网；拆掉其中一个
- AI 生成代码的 security 缺陷 — 注入、鉴权缺失、弱加密、不安全默认值；静态分析与安全测试并入流程
- License 与 copyright：生成代码的合规 — 训练数据与代码相似度；企业条款与赔偿承诺的范围
- Data exfiltration 与企业 compliance — 哪些代码可发往哪个供应商；零保留、私有部署选项
- Destructive operations 的防护 — 删库、强推、生产环境；只给最小权限、备份、人工确认点

## 7. 团队 adoption 与 metrics
- * 证据 1：METR 2025 randomized controlled trial — 16 位有经验的开源开发者、246 个真实任务，允许使用 AI 时平均慢 19%，而他们自己以为快了约 20%；适用范围与局限（样本小、熟悉的大仓库、2025 年初工具）；METR 称结果已过时并发布了后续数据
- * 证据 2：DORA 2025 AI-assisted Software Development report — 核心结论：AI 是放大器，放大组织已有的强项与弱点；七项 AI 能力模型；吞吐与稳定性的关系（数字需核对原报告）
- * 证据 3：Stack Overflow 2025 Developer Survey — 84% 使用或计划使用，51% 的专业开发者每天用；信任准确性的只有 33%，最大困扰是「几乎对但不对」（66%）
- * Perception vs measurement 的落差：为什么自我感觉不可靠 — 等待时间、上下文切换、审查成本被忽略；需要实测
- * 该度量什么：cycle time、change failure rate、recovery time、rework — 别只数生成的代码行或接受率；先建立基线再比较 (需先: 证据 2)
- * Adoption 路径：从低风险任务起步 — 测试、迁移、文档；逐步扩大；培训与分享实践
- 团队规范：context file、review rules、disclosure 约定 — 把个人技巧变成共享资产
- * 成本管理：token budget、model tiering、subagent cost — 用量按人与按任务可见；上限与告警
- 对 junior engineer 的影响：学习路径与 skill atrophy 风险 — 调研显示信心下降的信号；刻意练习不借助 AI 的基本功
- 如何批判地读 productivity 研究 — 样本、任务类型、度量指标、厂商利益；同一结论不要外推到所有场景

## 8. 资深工程师的角色转变
- * Role shift：从写代码到定义问题与验证结果 — 规格、架构边界、验收标准、取舍成为主要产出
- * Architecture 与 judgment 的价值上升 — 智能体放大局部产出，系统级一致性仍靠人；评审与决策的杠杆
- 管理一组 agents 像带一个小团队 — 任务切分、上下文交接、验收；委派的粒度
- Readability 与 testability 成为「agent-friendly」的设计 — 清晰模块边界、快速测试、类型；也是对人好
- Staying sharp：持续学习、保持手感 — 定期手写、读生成代码、跟踪模型能力变化；每个新模型都重估「它能做什么」
- Hiring & interviews：面试与招聘中的变化 — 允许使用 AI 的考题、评估重点转向验证与设计（只讲趋势，不押具体公司）

## 不收（out of scope）
- 各 IDE 的快捷键与界面逐项教程 — 变化快，官方文档即可
- 提示词技巧大全与角色扮演 — ai-literacy:use.prompting 覆盖
- 构建面向用户的 LLM 产品（RAG、网关、评测）— 放 ai-eng
- 模型训练与推理内部 — llm-inference
- 具体厂商价格与套餐 — 易变；只讲成本机制
- 「氛围编程」（vibe coding）的娱乐化讨论 — 只在「Comprehension debt：合并了没人读懂的代码」一叶出现
- 非编程场景的 AI 使用（写作、数据分析）— 不在范围

## 与已有领域的重叠
| 已有叶子 | 处理 | 说明 |
|---|---|---|
| ai-literacy:work.ai-coding | 更深 | 它是一页总览；这里拆成工作流、上下文文件、验证、安全四个分支 |
| ai-literacy:agents.coding-agents | 更深 | 那边讲三类工具怎么工作；这里讲怎么用好、怎么管控 |
| ai-literacy:agents.context-memory | 链接 | 压缩、子智能体、记忆文件、技能的概念链回；这里写实操与取舍 |
| ai-literacy:agents.security | 更深 | 这里落到仓库注入、权限规则、沙箱与供应链 |
| ai-literacy:work.sde-impact | 更深 | 它列证据与争论；这里逐项读 METR、DORA、Stack Overflow 并给批判读法 |
| ai-literacy:agents.long-horizon / agents.multi-agent | 链接 | 只引用；工程上的并行会话与工作树在这里 |
| ai-literacy:work.reading-news | 链接 | 「如何批判地读 productivity 研究」可链回 |
| ai-eng 智能体与评测分支 | 链接 | 工具设计、人在回路、提示注入的构建方视角在 ai-eng；本域是使用方视角，互相链接避免重复 |
| llm-inference、ml-system-design | 跳过 | 无实质重叠 |

## 卡片格式建议
- **自包含（Chi 2026-11-21）：** 卡里出现的每个术语，要么在更靠前的叶子里教过（按卡组顺序），要么在这张卡里用一句话定义；靠前的叶子按教科书写，不默认读者有背景。
- 场景开头：一次具体的失败（「智能体说测试通过，其实它改了测试」），再给机制与做法；动作要带触发条件。
- 证据卡写清规模与局限：样本数、任务类型、效应大小、是否被后续研究更新；数字必须当次核对原文。
- 做法卡带「做/别做」对照，附一小段命令或配置片段（上下文文件示例、钩子、权限规则）并加行内注释。
- 至少 25% 带图：四段循环、上下文窗口占用曲线、致命三要素、审查瓶颈示意、并行工作树布局。
- 风险卡写清攻击路径的每一步和阻断点，而不是只列名词。
