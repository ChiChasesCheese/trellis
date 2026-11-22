# ai-dev claims (card id | claim | source)

aid-glossary-basics | 定义 context window 内容：对话历史、文件内容、命令输出、CLAUDE.md、系统指令 | code.claude.com/docs/en/how-claude-code-works §The context window（2026-11-21 读取）
aid-glossary-basics | prompt injection 定义：攻击者插入恶意文本，覆盖或操纵 AI 助手的指令 | code.claude.com/docs/en/security §Protect against prompt injection
aid-four-forms | Claude Code 三种环境 Local / Cloud / Remote Control | code.claude.com/docs/en/how-claude-code-works §Execution environments（2026-11-21）
aid-four-forms | Cursor cloud agents 在云端隔离 VM、单独分支推回 | cursor.com/docs/background-agent（2026-11-21）
aid-four-forms | Codex cloud 每个任务独立工作区，可提交或开 PR | learn.chatgpt.com/docs/cloud（2026-11-21，原 developers.openai.com/codex/cloud 重定向）
aid-four-forms-pick | 无人值守前五问：知道什么叫完成、能自检、能碰什么、什么让它停、结果交给谁签字 | code.claude.com/docs/en/best-practices §Let Claude run without you（2026-11-21）
aid-agent-loop | 三阶段 gather context / take action / verify results；五类内置工具 | code.claude.com/docs/en/how-claude-code-works §The agentic loop, §Tools（2026-11-21）
aid-agent-says-done | 官方建议要证据：命令及输出或截图；"All tests pass" 本身信息量很少 | code.claude.com/docs/en/best-practices §Give Claude a check to run（2026-11-21）
aid-context-what-fills | compaction 保留请求和关键代码，早期详细指令可能丢失；/context 看占用 | code.claude.com/docs/en/how-claude-code-works §When context fills up（2026-11-21）
aid-context-clear-habits | 多数现行模型 1M token 窗口；任务间 /clear；/compact 可带重点 | code.claude.com/docs/en/best-practices §Keep cost and context down, §What you can stop doing（2026-11-21）
aid-limits-table | 只写 Claude 读代码找不到的信息；Claude 停下的依据是"看起来完成"，除非有可运行的检查 | code.claude.com/docs/en/best-practices（2026-11-21）
aid-limits-probe | 需求不清时让 Claude 访谈你直到能写出 spec | code.claude.com/docs/en/best-practices §Brainstorm with Claude first（2026-11-21）
aid-non-determinism | 官方把 prompt/CLAUDE.md/skills 归为 non-deterministic，hooks/deny rules/tests/CI 归为 deterministic | code.claude.com/docs/en/best-practices §Deterministic and non-deterministic instructions（2026-11-21）
aid-model-tier | effort 默认 medium（Fable 5.2/Opus 5.5/Sonnet 5.5/Haiku 5.5）；max 留给无人看守的难题；Haiku 适合简单子任务 | code.claude.com/docs/en/best-practices §Change the model and effort（2026-11-21）
aid-tool-types | Claude Code 接口：终端、桌面、IDE、网页、Remote Control、Slack、CI/CD | code.claude.com/docs/en/how-claude-code-works §Interfaces（2026-11-21）
aid-epic-loop | Plan 模式：Claude 探索并提出计划，不编辑源文件；Shift+Tab 循环切换权限模式 | code.claude.com/docs/en/how-claude-code-works §Control what Claude can do（2026-11-21）
aid-epic-loop-probe | 先用 spec 文件，然后开新 session 实现，起点是干净 context 和书面的"完成定义" | code.claude.com/docs/en/best-practices §Brainstorm with Claude first（2026-11-21）
aid-spec-first-basics | 官方示例：访谈后写 SPEC.md，在新 session 构建，并用它做审查标准 | code.claude.com/docs/en/best-practices（2026-11-21）
aid-spec-review-prompt | 审查 prompt 示例含 "skip style"；被要求找问题的 reviewer 总会找到点什么 | code.claude.com/docs/en/best-practices §Review against your spec（2026-11-21）
aid-check-highest-leverage | 检查形式与严格程度由低到高：prompt、/goal、Stop hook、独立审查 | code.claude.com/docs/en/best-practices §Give Claude a check to run（2026-11-21）
aid-check-stop-hook | Stop hook 退出码 2 阻止结束，stderr 回给 Claude；连续 8 次阻止后放行（env CLAUDE_CODE_STOP_HOOK_BLOCK_CAP 可调） | code.claude.com/docs/en/best-practices §Enforce the check with a Stop hook（2026-11-21）
aid-prompt-specific | 官方对照表：fix the login bug vs. 带症状、范围、失败测试的 prompt；"be ambitious" 说明范围 | code.claude.com/docs/en/best-practices §Write a specific prompt（2026-11-21）
aid-prompt-rewrite | 改写示例取自官方对照表（Instead of / Try） | code.claude.com/docs/en/best-practices §Write a specific prompt（2026-11-21）
aid-small-commits-undo | checkpoint 不覆盖仅由 Bash 命令改动的文件；不能撤销数据库/API/部署；与 git 并用 | code.claude.com/docs/en/best-practices §Steer the session；how-claude-code-works §Undo changes with checkpoints（2026-11-21）
aid-small-commits-split | /batch 把大型机械改动拆成 5 到 30 个单元，各自在独立 worktree 里开 PR | code.claude.com/docs/en/best-practices §Run sessions in parallel（2026-11-21）
aid-tdd-red-green | 官方 prompt 示例要求先写复现的失败测试再修 | code.claude.com/docs/en/best-practices §Write a specific prompt（2026-11-21）
aid-tdd-cheat | PreToolUse hook 对 migrations/ 路径退出码 2 阻止编辑（官方示例，此处类比到 tests/） | code.claude.com/docs/en/best-practices §Enforce steps with hooks（2026-11-21）
aid-steer-two-strikes | 两次纠正失败后 /clear 重写 prompt；Esc 停止；/rewind 或 Esc 两次回滚代码/对话 | code.claude.com/docs/en/best-practices §Steer the session（2026-11-21）
aid-steer-rewind-limits | checkpoint 只覆盖主对话中文件编辑工具改的文件；Bash 改动不还原；远程系统动作不能检查点；跳过符号链接和硬链接 | code.claude.com/docs/en/how-claude-code-works §Undo changes with checkpoints；best-practices §Steer the session（2026-11-21）
aid-worktree-basics | 链接 worktree 有自己的 HEAD 和 index，共享历史与 refs；一个分支不能同时在两个 worktree 检出；remove 只删干净的 | git-scm.com/docs/git-worktree（2026-11-21）
aid-worktree-basics | claude -w <name> 在新 worktree 开 session | code.claude.com/docs/en/best-practices §Run sessions in parallel（2026-11-21）
aid-worktree-split | .worktreeinclude 复制被 gitignore 的小文件，大目录用 worktree.symlinkDirectories；claude -p --worktree 需自行清理 | code.claude.com/docs/en/best-practices §Run sessions in parallel（2026-11-21）
aid-interview-first | 访谈 prompt 示例与 SPEC.md 流程 | code.claude.com/docs/en/best-practices §Brainstorm with Claude first（2026-11-21）
aid-headless-batch | claude -p 脚本示例及 --bare/--allowedTools/--permission-mode dontAsk/--max-turns/--max-budget-usd/--output-format json | code.claude.com/docs/en/best-practices §Run Claude from a script（2026-11-21）
aid-subagents-cost | subagent 成本主要是 token；新 subagent 需重新收集上下文；委派给 subagent 不会让答案更好，新鲜 reviewer 才有帮助 | code.claude.com/docs/en/best-practices §Know what subagents cost, §What you can stop doing（2026-11-21）
aid-long-task-files | initializer agent 建 init.sh、claude-progress.txt、初始 git 提交、feature list JSON（示例中 200+ 功能）；后续 session 一次一个功能 | anthropic.com/engineering/effective-harnesses-for-long-running-agents（2026-11-21）
aid-ctxfile-what | 只写 Claude 读代码找不到的信息；两问测试；/init 生成起稿 | code.claude.com/docs/en/best-practices §Keep CLAUDE.md short（2026-11-21）
aid-ctxfile-prune | 官方列入"可停止做"：加 IMPORTANT/全大写强调；在 CLAUDE.md 描述架构和文件布局 | code.claude.com/docs/en/best-practices §What you can stop doing（2026-11-21）
aid-ctxfile-rules | 每个 CLAUDE.md 目标低于 200 行；矛盾指令可能任选其一；各层文件拼接而非覆盖，根到工作目录排序；子目录 CLAUDE.md 在读到该目录文件时按需加载；/doctor prompt-audit | code.claude.com/docs/en/memory §Write effective instructions, §How CLAUDE.md files load（2026-11-21）
aid-ctxfile-ignored | CLAUDE.md 是上下文，不是强制配置；要无视 agent 决定地阻止某动作用 PreToolUse hook | code.claude.com/docs/en/memory §CLAUDE.md vs auto memory（2026-11-21）
aid-hooks-vs-text | deny 规则在所有权限模式（含 auto、bypassPermissions）下生效；hook 在固定点运行；零例外才用 hook | code.claude.com/docs/en/best-practices §Enforce the rules that can't have exceptions（2026-11-21）
aid-hooks-perm-edges | Read 规则会拦 cat .env，但拦不住打开该文件的脚本；deny 规则示例 | code.claude.com/docs/en/best-practices §Limit access with permission rules and the sandbox（2026-11-21）
aid-skills | skill 位于 .claude/skills/<name>/SKILL.md；名字和描述常驻，全文按需；disable-model-invocation: true 使其只能手动触发 | code.claude.com/docs/en/best-practices §Put team procedures in skills（2026-11-21）
aid-mcp-cli | 已连接 MCP server 把工具名和说明加入 context；有 CLI 时优先；Anthropic 不审计 MCP server | code.claude.com/docs/en/best-practices §Connect the tools Claude needs；security §MCP security（2026-11-21）
aid-ctxfile-cross-tool | Claude Code 同时有 AGENTS.md 和 CLAUDE.md 时只读 CLAUDE.md；可用 @ 导入，最大递归 4 层 | code.claude.com/docs/en/memory §AGENTS.md, §Import additional files（2026-11-21）
aid-ctxfile-cross-tool | Codex：根到当前目录每层一个文件，拼接，近者靠后；project_doc_max_bytes 默认 32 KiB | learn.chatgpt.com/docs/agent-configuration/agents-md（2026-11-21）
aid-ctxfile-cross-tool | Cursor：.cursor/rules 的 .mdc；Always/Intelligently/Specific files/Manually 四种；支持 AGENTS.md，嵌套时近者优先 | cursor.com/docs/context/rules（2026-11-21）
aid-legacy-map | 值得写入 CLAUDE.md：代码中会误导的地方、不在仓库里的决定 | code.claude.com/docs/en/best-practices §Keep CLAUDE.md short（2026-11-21）
aid-verify-bottleneck | DORA 2025：AI 采用与吞吐正相关、与稳定性仍负相关；无强自动化测试、成熟版本控制、快速反馈时更多变更导致不稳定 | cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report（2025-09-23）
aid-verify-bottleneck | SO 2025：66% 受访者困扰"几乎对但不对"；45.2% 说调试 AI 生成代码更耗时 | survey.stackoverflow.co/2025/ai（2026-11-21 读取）
aid-verify-pipeline | 官方表：最后一句话由分支保护和批准合并的人决定，而非 Claude 的总结 | code.claude.com/docs/en/best-practices §Deterministic and non-deterministic instructions（2026-11-21）
aid-defects-catalog | SO 2025：66% 认为最大困扰是"almost right, but not quite" | survey.stackoverflow.co/2025/ai（2026-11-21）
aid-defects-swallow | 无新增数字 | 本卡为示例
aid-small-diff | /batch 把大改拆成独立单元，每个单元一个 PR | code.claude.com/docs/en/best-practices §Run sessions in parallel（2026-11-21）
aid-small-diff-order | 无新增数字 | 实务顺序，无外部来源
aid-reviewer-fresh | /code-review 在从未见过对话的新 subagent 里审 diff；reviewer 可只给 Read/Grep/Glob 工具，限制由 Claude Code 强制 | code.claude.com/docs/en/best-practices §Give Claude a check to run, §Know what subagents cost（2026-11-21）
aid-reviewer-noise | 同 aid-spec-review-prompt：被要求找问题的 reviewer 总会找到点什么 | code.claude.com/docs/en/best-practices §Review against your spec（2026-11-21）
aid-tests-contract | 无新增数字 | 概念
aid-tests-contract-mutation | 无数字来自来源；95% 与 40% 为题目设定的示例数字 | 本卡为示例
aid-e2e-run-it | Claude 常在只做单元测试或 curl 后标功能完成；用浏览器自动化明显改善 | anthropic.com/engineering/effective-harnesses-for-long-running-agents（2026-11-21）
aid-e2e-run-it | /verify 让 Claude 构建并运行应用并查看结果 | code.claude.com/docs/en/best-practices §Give Claude a check to run（2026-11-21）
aid-e2e-checklist | 要求命令及输出或截图作为证据 | code.claude.com/docs/en/best-practices §Give Claude a check to run（2026-11-21）
aid-dep-slopsquatting | 576,000 样本、16 个模型、商业至少 5.2%、开源 21.7%、205,474 个不同名字 | arxiv.org/abs/2406.10279 摘要（2026-11-21 读取）
aid-dep-slopsquatting | 2026 年复测显示前沿模型比例较低（约 4.6%–6.1%），仅见于二手摘要，卡中只作"更低"表述 | arxiv.org/pdf/2605.17062 经搜索摘要，未直接读取
aid-dep-api-check | @路径引入文件内容 | code.claude.com/docs/en/best-practices §Write a specific prompt（2026-11-21）
aid-comprehension-debt | DORA："acceleration can expose weaknesses downstream" | cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report（2025-09-23）
aid-comprehension-debt | "comprehension debt" 术语来源未核实，卡内已说明来源有争议 | 搜索结果显示归属有争议（Gorman 2025-09、Osmani 2026-03 传播），未读原文
aid-comprehension-explain | 你负责在批准前审查建议的代码与命令 | code.claude.com/docs/en/security §User responsibility（2026-11-21）
aid-perf-regression | 无数字来自来源；200ms 与 1 万条为示例设定 | 本卡为示例
aid-maintain-drift | PostToolUse hook 在 Edit/Write 后跑 prettier 的官方示例 | code.claude.com/docs/en/best-practices §Enforce steps with hooks（2026-11-21）
aid-review-etiquette | 用户负责审查提议的代码与命令 | code.claude.com/docs/en/security §User responsibility（2026-11-21）
aid-review-etiquette | 开源项目 AI 政策差异（有的禁止，有的要求披露）仅作一般性陈述，未读各项目原文，未引用具体项目 | 搜索摘要
aid-unit-tests | 无新增数字 | 概念
aid-unit-tests-fake | 无新增数字 | 本卡为示例
aid-ai-bug | 官方对照：users report login fails after the session times out… write a failing test that reproduces it, then fix it；cat error.log | claude -p 管道 | code.claude.com/docs/en/best-practices §Write a specific prompt（2026-11-21）
aid-ai-bug-hypothesis | 无新增数字 | 概念
aid-characterization | 无新增数字 | 概念，无外部来源页
aid-migration | 官方 for-loop 脚本与"先在三个文件上试"；/batch 拆 5–30 单元 | code.claude.com/docs/en/best-practices（2026-11-21）
aid-e2e-ui | Claude 看不到浏览器原生 alert 弹窗，依赖它们的功能更容易出错 | anthropic.com/engineering/effective-harnesses-for-long-running-agents（2026-11-21）
aid-e2e-ui | 官方 check 形式包括浏览器截图与设计稿对照 | code.claude.com/docs/en/best-practices §Give Claude a check to run（2026-11-21）
aid-property-fuzz | 无新增数字 | 概念
aid-docs-drift | 官方原则：只写 agent 读代码读不出来的内容 | code.claude.com/docs/en/best-practices（2026-11-21）
aid-secrets-where | deny Read(./.env) 等示例配置；Read 规则也拦 cat .env | code.claude.com/docs/en/best-practices §Limit access with permission rules and the sandbox（2026-11-21）
aid-secrets-leak-probe | 官方提到 hook 可扫描提交中的密钥，工具崩溃时应阻止提交 (onFailure: "block") | code.claude.com/docs/en/best-practices §Enforce steps with hooks（2026-11-21）
aid-injection-repos | Manual 模式下 curl/wget 默认提示批准；最佳实践：审查命令、避免把不可信内容直接管道给 Claude、用 VM | code.claude.com/docs/en/security §Protect against prompt injection（2026-11-21）
aid-injection-probe | Willison：guardrail 检出 95% "very much a failing grade"；"we still don't know how to 100% reliably prevent this from happening" | simonwillison.net/2025/Jun/16/the-lethal-trifecta/（2026-11-21 读取）
aid-sandbox-permissions | 四种权限模式：Auto/Manual/Accept edits/Plan；deny 规则在所有模式有效；auto mode 连续 3 次或累计 20 次拦截后暂停询问 | code.claude.com/docs/en/how-claude-code-works §Control what Claude can do；best-practices（2026-11-21）
aid-sandbox-permissions | 工作目录边界是权限提示，批准的 Bash 命令仍可写账户能写的位置；sandbox 提供 OS 级限制 | code.claude.com/docs/en/security §Built-in protections（2026-11-21）
aid-sandbox-probe | 官方建议为额外隔离，在 sandbox runtime 或 dev container 里运行整个 Claude Code | code.claude.com/docs/en/security §Security best practices（2026-11-21）
aid-supply-chain | Anthropic 按上架标准审核 connectors，但不做安全审计也不管理任何 MCP server | code.claude.com/docs/en/security §MCP security（2026-11-21）
aid-supply-chain-probe | 无新增数字 | 概念
aid-trifecta | 三条腿定义、日期 2025-06-16、"avoid that lethal trifecta combination entirely"；MCP "encourages users to mix and match tools" | simonwillison.net/2025/Jun/16/the-lethal-trifecta/（2026-11-21 读取）
aid-trifecta-break | 官方：网络命令如 curl/wget 默认提示；可用 deny 规则或 sandbox network isolation 做强制 | code.claude.com/docs/en/security §Protect against prompt injection（2026-11-21）
aid-ai-code-vuln | /security-review 对当前分支改动做安全检查 | code.claude.com/docs/en/security §Related resources（2026-11-21）
aid-license | 数据保留与训练偏好按 Commercial Terms（Team/Enterprise/API）与 Consumer Terms（Free/Pro/Max）区分 | code.claude.com/docs/en/security §Privacy safeguards（2026-11-21）
aid-license | 版权与赔偿承诺的法律结论未核实，卡中只给检查框架，不给法律结论 | 未读法律来源
aid-data-compliance | Claude Code 云端：默认限制网络，可禁用或只放行指定域名；managed settings、OpenTelemetry 监控 | code.claude.com/docs/en/security §Cloud execution security, §Team security（2026-11-21）
aid-data-compliance | Cursor 云端 agent：secrets 工作区/团队范围、启动时注入；管理员可限制出站域名 | cursor.com/docs/background-agent（2026-11-21）
aid-destructive | auto mode 默认拦生产部署、强推覆盖他人工作；定时任务前保护 main 的分支规则 | code.claude.com/docs/en/best-practices §Enforce the rules, §Start runs on a schedule（2026-11-21）
aid-destructive | 云端 GitHub 代理拒绝删除分支及推送非分支 | code.claude.com/docs/en/security §Cloud execution security（2026-11-21）
aid-metr-rct | 16 位开发者、246 个 issue、平均约两小时、22k+ star、1M+ 行、慢 19%、预期快 24%、事后认为快 20%、Cursor Pro + Claude 3.5/3.7 Sonnet | metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/（2026-11-21 读取）
aid-metr-rct | 置信区间 +2% 到 +39% | metr.org/blog/2026-02-24-uplift-update/（2026-11-21 读取）
aid-metr-rct | 局限：样本小、选择偏差、50 小时学习效应、不适用于新手 | metr.org/blog/2025-07-10-...（2026-11-21）
aid-metr-update | 57 开发者（10 回访 + 47 新）、143 仓库、800+ 任务、$50/小时；回访 -18%（-38%~+9%），新人 -4%（-15%~+9%）；30%~50% 扣下任务；"very weak evidence"，估计为下限，正在重新设计 | metr.org/blog/2026-02-24-uplift-update/（2026-11-21 读取）
aid-metr-update | 2025 年研究报酬 $150/小时 | metr.org/blog/2025-07-10-...（2026-11-21）
aid-dora-amplifier | 近 5,000 受访者、100+ 小时定性数据；90% 使用；>80% 认为提高生产力；吞吐正相关；稳定性仍负相关；30% 几乎不信任；amplifier 语句 | cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report（2025-09-23，2026-11-21 读取）
aid-dora-amplifier | 七项能力（未列名）；页面更新 2025-11-25 | dora.dev/ai/capabilities-model/（2026-11-21 读取）
aid-dora-probe | 同 aid-dora-amplifier：无强测试、成熟版本控制、快反馈则变更量增加导致不稳定 | cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report（2025-09-23）
aid-dora-probe | DORA 为调查研究，相关性而非随机实验 | 对方法的一般判断，未逐页核实报告方法章节
aid-so-survey | 84%（上年 76%）；专业开发者 50.6% 每天用；信任 33%（3.1%+29.6%）、不信任 46%（26.1%+19.6%）；66% 几乎对但不对；45.2% 调试更费时；30.9% 用 agent（14.1% 每天） | survey.stackoverflow.co/2025/ai（2026-11-21 读取）
aid-so-survey | "自选参与的在线问卷"为对调查类型的一般判断 | 未读方法章节
aid-so-probe | 同 aid-so-survey | survey.stackoverflow.co/2025/ai（2026-11-21）
aid-perception-gap | 20 个潜在因素，5 个可能造成变慢；时间追踪对并行多 agent 的开发者不可靠 | metr.org/blog/2025-07-10-...；metr.org/blog/2026-02-24-uplift-update/（2026-11-21）
aid-perception-gap | 表中"容易被忽略的"为假设，未逐一核对 METR 的五个因素 | 本卡为假设
aid-metrics | 四个指标的定义为通用工程度量定义，非引自 DORA 报告原文 | 概念；DORA 2025 的吞吐正相关、稳定性负相关见 aid-dora-amplifier
aid-metrics-probe | 数字为题目设定 | 本卡为示例
aid-adoption-path | 无人值守前五问 | code.claude.com/docs/en/best-practices §Let Claude run without you（2026-11-21）
aid-adoption-path | 四阶段为建议路径，无外部数据 | 本卡为建议
aid-team-norms | 团队安全建议：managed settings、版本控制共享权限配置、培训、OpenTelemetry 监控 | code.claude.com/docs/en/security §Team security（2026-11-21）
aid-cost-budget | 每次请求发送整个对话；缓存热有折扣；缓存订阅约 1 小时、API key 约 5 分钟；/usage 按 skill/subagent/plugin/MCP 分解 | code.claude.com/docs/en/best-practices §Keep cost and context down（2026-11-21）
aid-cost-probe | 后台工作（/loop、goal 检查、subagent）在你不打字时也持续发请求；Each /loop run is another turn in the same session | code.claude.com/docs/en/best-practices §Keep cost and context down, §Start runs on a schedule（2026-11-21）
aid-junior-atrophy | METR 明确说不能说明 AI 对经验较少者或陌生代码库无帮助 | metr.org/blog/2025-07-10-...（2026-11-21）
aid-junior-atrophy | 技能萎缩的实证数据未核实，卡内已声明证据很少 | 未找到来源
aid-read-productivity | 无新增数字 | 综合 METR、SO、DORA 的方法局限
aid-role-define-verify | 官方：长任务中留给人的是启动、决定"完成"的含义、批准最后的合并 | code.claude.com/docs/en/best-practices §Let Claude run without you（2026-11-21）
aid-role-define-probe | 数字为题目设定 | 本卡为示例
aid-role-architecture | DORA amplifier 语句 | cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report（2025-09-23）
aid-role-architecture-probe | 无新增数字 | 示例
aid-manage-agents | 无新增数字 | 综合官方并行与无人值守做法
aid-agent-friendly | 同 aid-dora-amplifier：无强测试、成熟版本控制和快速反馈则变更量引发不稳定 | cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report（2025-09-23）
aid-keep-skills | 官方"可以不再做"清单：强调语、"think hard"、为保护 context 用 subagent 等 | code.claude.com/docs/en/best-practices §What you can stop doing（2026-11-21）
aid-keep-skills | METR 页面写 "These results are out of date." | metr.org/blog/2025-07-10-...（2026-11-21）
aid-hiring | 趋势性陈述，无外部来源，不含数字或公司 | 本卡为趋势性判断
