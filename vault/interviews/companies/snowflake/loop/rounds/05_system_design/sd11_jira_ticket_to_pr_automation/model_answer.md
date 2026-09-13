# 模型答案：设计 Automated Jira-Ticket-to-PR System

> 取材：PracHub "Automated Jira-Ticket-to-PR System"；1p3a thread-1180916 一手 onsite 报告（候选人形容"very unique"，正文 403 仅摘要）；`catalog/raw/system_design.md` §1.14。按 `LOOP_GUIDE.md` §6 主线组织。

## 0. 两句话复述 + 不变量

**复述**：工单被标记后要触发一个多步骤、长耗时的自动化流程——理解需求、生成代码、跑测试、开 PR，任何一步都可能失败需要重试；多个工单要能并发独立处理；无论自动化流程多顺利，最终代码变更必须经过人工 review 才能合入，自动化系统本身没有直接合并的权限。

**核心不变量**：

1. **人工 review 是不可绕过的强制关卡**：不存在任何路径能让代码在没有真人批准的情况下被合并，这是本题最核心的一条边界，不因为自动化"看起来很有信心"而例外。
2. **流程状态持久化、可恢复**：长耗时多步骤流程的进度必须落盘，组件重启不能导致进度丢失或流程从头重来。
3. **LLM 步骤的失败是"软失败"**：生成代码这一步不是单纯的成功/失败二元判断，"生成了内容"不等于"生成的内容是对的"，需要独立的验证步骤。
4. **工单之间并发隔离**：一个工单卡在某一步不能阻塞其他工单的处理。

明确"不做什么"：不追求自动化流程能处理所有类型的工单（复杂度超出阈值的工单应该被识别出来直接转人工，而不是让自动化流程勉强硬跑）；不承诺生成代码一次就能通过 review（多轮重试和人工反馈迭代是正常预期路径，不是异常情况）。

## 1. API 契约

```
POST /internal/v1/automation/trigger    {jira_ticket_id}
                                         -> {automation_id}
                                         # 幂等：同一 jira_ticket_id 已有进行中流程则直接返回该流程 id

GET  /v1/automation/:id/status          -> {status, current_step, retry_count, history: [...]}

POST /v1/automation/:id/review/approve  {reviewer_id}
                                         # 唯一能推进 pending_review -> merged 的接口
POST /v1/automation/:id/review/reject   {reviewer_id, feedback}
                                         # 打回，feedback 作为下一轮生成的额外上下文
```

- 没有任何接口允许系统内部自动调用 `approve` 路径——这条边界要在设计里体现为"根本不存在这样的内部接口"，而不是"有接口但默认不调用"。

## 2. 数据模型

```
automation_runs(
  automation_id, jira_ticket_id, status[triaged|analyzing|generating|testing|
    pending_review|approved|merged|failed|needs_human],
  current_step, retry_count, created_at, updated_at
)
-- (jira_ticket_id) 上的唯一约束/查询防止重复触发同一工单的第二条流水线

step_results(
  automation_id, step[analyze|generate|test|open_pr], attempt_number,
  input_context, output, verification_status, error, started_at, finished_at
)
-- 每一步、每一次尝试都独立记录，包括生成代码这一步的完整产出和验证结果

review_records(
  automation_id, reviewer_id, decision[approved|rejected], feedback, decided_at
)
-- 人工 review 的决定，是唯一能让 status 从 pending_review 前进的写入来源
```

**为什么每一步、每次尝试都要独立记录**：这条流水线里"生成代码"这一步本身是概率性的（同样的输入，模型可能生成不同的输出），需要能追溯"第几次尝试生成了什么、为什么验证没通过、下一次尝试的 prompt 里加了什么反馈"，这既是调试自动化系统本身的必要数据，也是给人工 reviewer 呈现"这个 PR 是怎么一步步产生的"的审计轨迹。

## 3. 核心流程

**触发**：Jira webhook（工单被打标签/分配给自动化账号）→ 触发层做幂等检查（该工单是否已有进行中/已完成的流程）→ 创建 `automation_runs` 记录，状态 `triaged`，推入编排层的调度队列。

**编排（状态机推进）**：编排层是一个类似 sd02 cron scheduler 的调度器——每个 `automation_run` 是一个独立的任务，编排层负责把它推进到下一步：
1. `analyzing`：调用理解需求的步骤（可能是同一个编码 agent 的一次调用，输出结构化的"要改哪些文件、大致思路"），产出写入 `step_results`。
2. `generating`：基于分析结果生成实际代码改动（diff），产出同样落盘。
3. `testing`：**独立的验证步骤**——把生成的代码应用到隔离的沙箱环境跑编译/lint/单元测试，`verification_status` 记录是否真正通过；这一步是把"LLM 生成了看似合理的代码"转化为"这段代码是不是真的能用"的关键校验，不能省略。
4. 验证通过 → `pending_review`，生成 PR 草稿，通知人工 reviewer；验证失败 → 把失败的测试输出/错误信息作为额外上下文反馈给下一轮 `generating`（回到步骤 2），`retry_count += 1`。

**失败与放弃**：`retry_count` 超过上限（如 3 次连续生成都无法通过验证）→ 状态转 `needs_human`，流水线不再自动重试，转入人工介入队列，附带完整的尝试历史供工程师参考（可能是工单本身描述不清楚，或者需求超出自动化系统当前能力范围）。

**人工 review**：`pending_review` 状态下，reviewer 看到生成的 PR diff、测试结果、以及这条流水线的完整尝试历史；`approve` 是唯一能把状态推进到 `merged` 的动作；`reject` 附带的 `feedback` 会被喂回 `generating` 步骤作为新一轮尝试的上下文（本质上是把人类的反馈当作比自动化测试失败更高质量的信号），`retry_count` 重置或独立计数（人工反馈驱动的重试可以给更宽松的次数上限，因为人类反馈的信息量通常远高于测试失败信息）。

## 4. 失败模式与规模

**LLM 步骤的失败模式细分（本题的核心差异化设计点）**：
- **硬失败**：调用超时、返回内容为空、接口报错——直接判定这次尝试失败，走标准重试逻辑。
- **软失败（更常见也更危险）**：模型生成了语法正确、看起来合理，但实际逻辑错误或者不满足需求的代码——这种情况**不会**在"生成"这一步本身报错，必须靠独立的 `testing` 步骤（编译、跑测试）才能发现；这正是为什么"生成代码"和"验证代码"必须是流水线里两个独立的步骤，不能把"模型调用成功"直接等同于"这一步任务完成"。
- 进一步，即使测试全部通过，也不能等同于"这次生成绝对正确"——测试本身的覆盖率是有限的，这正是"人工 review 作为不可绕过的最终关卡"存在的根本原因：自动化验证能过滤掉大部分明显错误，但不能替代人类对需求理解、代码质量、潜在副作用的判断。

**"能不能因为自动化流程反复生成同一个高置信度答案就跳过人审"——这是面试官大概率会追问的边界，答案必须坚决是不能**：置信度再高的自动化输出，本质上仍然是概率性系统的产出，"高置信度"不等于"正确性可证明"；保留强制人工关卡的设计目的正是为了给这类系统性风险兜底，一旦允许"足够自信就自动合并"这个例外，整个"人工把关"的不变量就形同虚设。

**并发隔离**：每个工单的自动化流程是独立的任务实例，编排层按 `automation_id` 分片调度（可以直接复用 sd02 cron scheduler 或 sd05 队列服务的并发隔离设计），一个工单卡在 `testing` 步骤（比如测试环境资源紧张排队很久）不会阻塞其他工单进入 `generating` 或 `pending_review`。

**幂等与重复触发**：Jira webhook 可能重复投递（网络重试导致），触发层必须能识别"这个工单已经有一条进行中/已完成的流程"，直接返回已存在的 `automation_id` 而不是创建第二条重复的流水线（这与 stripe webhook 题"消费者按幂等键去重"是同一类问题在不同产品里的体现）。

**规模估算**：假设组织内每天有数十到数百个工单被标记为自动化候选，每条流水线的处理时长可能从几分钟到几小时不等（取决于代码复杂度和测试耗时），编排层的并发度需要能水平扩展；测试沙箱环境本身可能是稀缺资源，需要类似 sd03 SQL notebook 题里"排队 + 公平调度"的思路管理多个流水线对测试资源的竞争。

## 5. 分层与组件

- **触发/接入层**：监听 Jira webhook，做幂等检查，创建流水线记录。
- **编排层**：管理多步骤状态机的推进、重试、超限转人工介入，不关心每一步具体怎么实现（这一层的设计可以直接复用 sd02 调度器的思路）。
- **执行层**：每个步骤（分析/生成/测试/开 PR）是独立可替换的执行单元，未来更换底层编码 agent 实现不影响编排层。
- **人工 review 层**：唯一拥有"允许产生可合并代码"权限的组件，与前面全自动化的执行层在权限模型上有本质区别，不是流水线的"最后一步"而是一个完全独立的、必须由人类主动触发的权限边界。

## 6. rollout/测试/监控

- **监控**：各阶段成功率（尤其是"生成代码通过验证"这一步）、平均端到端处理时长、人工 review 的通过率与平均等待时长、转入 `needs_human` 的工单占比（异常升高可能意味着上游模型能力或代码库发生了不兼容变化）。
- **测试**：针对已知类型的工单构造回归测试集，验证流水线在典型场景下的行为；专门测试失败重试路径——模拟测试失败，验证失败信息确实被正确带入下一轮生成的上下文，而不是简单重复一模一样的 prompt。
- **rollout**：先在低风险的工单类型（如小的文档修复、简单的依赖版本升级）上灰度，观察生成质量和人工 review 通过率，确认稳定后再逐步扩大到更复杂的工单类型；对生成代码通过率的骤降设置告警，作为发现系统性问题（而不是等大量工单堆积在 `needs_human` 才发现）的早期信号。

## 7. 用 Snowflake 自己的原语作参照

这道题直接对应 Snowflake 当前真实的工程文化转向——公司与 Anthropic 合作条款明确内部使用 **Claude Code**，SVP Eng 提出"treat your developers like customers"，CEO 提出"a tech lead of agents rather than an IC that writes code one line at a time"（`01-company-brief.md` §2），AI 编码 agent **CoCo**（原 Cortex Code）本身就是 Snowflake 的核心产品之一。本题设计里"多步骤流水线 + 独立验证步骤 + 强制人工 review 关卡"的架构，正是 Snowflake 内部推行 AI-native 开发时必然要解决的问题——工程师从"逐行写代码"转向"审阅 agent 产出的代码"，人机协作边界的设计（"agent 可以生成，但不能自己合并"）是这套工程文化能落地的关键前提。另外，本题"编排层管理多步骤重试与失败转人工"的设计模式，也与 Snowflake **Tasks** 的 `SUSPEND_TASK_AFTER_NUM_FAILURES`（连续失败后自动挂起，转人工介入）在思路上完全一致。面试时可以说："这本质上是在设计 Snowflake 自己正在推广的 AI-native 开发流程的一个具体实现——CoCo 生成代码、人类 review 合并，我的简历里也提到过用 AI-native workflow 的经验，这道题正好能展开讲。"

## 8. 45 分钟口述时间表

- **0–5 min**：复述题目 + 不变量（人工 review 不可绕过、状态持久化可恢复、LLM 步骤是软失败、工单间并发隔离），确认重试上限和风险分级需求。
- **5–12 min**：API 契约（触发/状态查询/人工 approve-reject）+ 数据模型（多阶段状态机 + 每步独立记录 + review_records）。
- **12–22 min**：核心流程——状态机推进（分析→生成→测试→待审）、失败重试与人工反馈回灌、幂等触发。
- **22–35 min**：失败模式——LLM 软失败的细分、坚决回答"不能因为高置信度跳过人审"、并发隔离、规模估算。
- **35–42 min**：分层图（人工 review 层的权限边界）+ rollout（灰度低风险工单类型）+ 监控指标。
- **42–45 min**：总结 + 直接对照 Snowflake CoCo 与 AI-native 工程文化，反问面试官。
