# Cron / Job Scheduler（"SQL engine as cron job" + Reliable Job Scheduler）

我们有一个 SQL 执行引擎，用户会往里面提交查询；现在很多用户其实不是临时跑一次查询，而是想要"这条 SQL 每天凌晨两点自动跑一次""每隔 15 分钟跑一次增量处理"这种周期性任务——本质上就是把大量的 SQL 查询当成 cron job 来管理和触发。请给我设计支撑这件事的调度系统：用户注册一个任务，带上一个类似 cron 表达式的调度规则（或者固定间隔），系统要在到点的时候准确地把这个任务丢给执行引擎去跑，并且记录每次运行的结果。这里有几个现实问题：第一，任务的规模非常大——预计整个系统里会有上百万量级的已注册任务，调度精度要求是分钟级（不是秒级，但也不能有大的漂移）；第二，执行引擎本身跑一个任务可能要几秒到几十分钟不等，任务失败了（比如底层查询报错、依赖的资源不可用）要能重试，但绝对不能因为某次调度器自己的实例挂了就导致这个任务这一轮彻底不跑；第三，调度器这个组件本身一定是多实例部署的（不可能单点），所以必须搞清楚多个调度器实例之间怎么分工，既不能出现同一个任务在同一个触发时刻被两个实例同时拿去执行、抢占同一份资源，也不能因为某个实例宕机了就导致它名下的任务全部漏跑；第四，调度器进程本身也会崩溃重启，重启之后要能正确地恢复出"接下来该跑哪些任务"，而不是把过去攒的任务一股脑全部补跑一遍，也不能全部丢掉。请设计这个系统。

---

**面试环境说明**：这是 Snowflake 技术电面或 onsite 的 System Design 轮，时长 45–60 分钟。白板工具未证实；面试官风格两极分化，一份一手报告明确记录"面试官全程沉默"，需要候选人主动推进、主动提出假设，不要等待引导式追问。这道题在该题库里样本量最大、复现度最高，值得优先吃透。

**题目原始报告与来源**（置信度见 `catalog/raw/system_design.md` §1.4、§1.5）：
- **一手（高置信度）**：Blind 帖"Snowflake IC1/IC2 System Design Interview"（2025-07-03）：题面为设计一个 **SQL 引擎，把大量查询当 cron job 跑**；面试官全程沉默 —— teamblind.com（**高**，复用 `../../raw/process_research.md` §3.2 #9）。这题与 Snowflake 真实产品 **Tasks**（CRON/间隔调度、可组成 DAG）高度对应，面试官很可能是想看候选人能否推导出 Snowflake 内部真实在用的"调度 + 幂等重试 + 失败隔离"模型。
- **聚合站补充**（同族但独立收录）："Design a Cron Job Scheduler"，"a service that triggers user-defined jobs"，PracHub 标注 **768 人做过、2026-04-12**，是该聚合站里被做次数最高的 Snowflake SD 题（**低**，但样本量最大，值得优先练）。
- "Design a Reliable Job Scheduler"（Hard），题面 "a fault-tolerant scheduler for one-time and recurring jobs"，89 人做过（**低**）。
- "Design Multi-Core Service Startup Scheduler"，用 DAG 表达依赖，215 人做过；对应 `../../raw/process_research.md` §3.2 #11 "Service Startup 依赖排序 (Kahn)"（**低**）。
- 复用材料：`../../raw/process_research.md` §3.2 #12 "Job Scheduler 等（雪花系统设计大汇总）"，1p3a thread-1091322（正文 403，仅标题级，本文件重试抓取仍 403）（**中**）。
