---
id: bagu-link-github-cicd-workflow-1-map
node: links.github-cicd-workflow
type: qa
step: 1
---
## Q
**CI/CD 平台（类 GitHub Actions） · 会被追问哪些八股**｜必会

设计CI/CD 平台（类 GitHub Actions）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 构建是排队的不可信任务。基础是：任务队列与手动 ack、cgroup 隔离资源、超时与重试、滚动发布的探针与回滚、日志排查。

**下钻路线。**
- 构建任务怎么派发 → 任务队列加手动 ack，worker 崩溃重新入队，步骤要幂等，[[b.mq.rabbitmq|RabbitMQ 模型与可靠性]]
- 多个构建共用机器 → cgroup 内存上限，超限只杀这个任务，[[a.linux.mem-oom|内存占用高与 OOM 怎么查]]
- 构建占满 CPU → CPU 配额，超时强杀，[[b.linux.cpu-load|CPU 使用率高与 load 高但 CPU 低]]
- 单个任务卡死 → 每步设超时，整体 deadline，[[b.protect.timeout|超时时间怎么设置]]
- 滚动发布失败不影响线上 → 就绪探针，maxUnavailable，一键回滚，[[a.linux.k8s-pod|Kubernetes 里 Pod 起不来或反复重启]]
- 怎么让发布更安全 → 灰度，关键接口对比检查，一键回滚，[[a.linux.general-method|线上排查通用思路与「服务突然变慢」完整清单]]
- 构建日志里找失败原因 → grep、awk、sort、uniq 一行流，[[a.linux.shell-log|Shell 一行流分析日志与写脚本]]
- 流水线 DAG 某步失败 → 重试还是中止，人工审批怎么暂停，与工作流编排同构，[[b.agent.multi-agent-workflow|多 Agent 协作与 Workflow / Graph 编排]]

**业务场景。** 发布支付服务新版本：先灰度 1% 商户，发现回调异常立即回滚，回滚后的状态机要兼容新旧两种事件。
**系统设计。** [[links.job-scheduler-cron-history|分布式任务调度器（含 cron 与一年执行历史）]]：同样的派发、心跳与重新入队，构建多了依赖 DAG；[[links.coding-contest-platform|在线判题与编程竞赛平台（LeetCode）]]：同样限制沙箱资源，但执行的是用户提交的代码。
