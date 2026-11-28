---
id: hi-c-sd-temporal-n11-task-queues
node: sd.deep-dives.temporal.notes
type: qa
step: 7
---
## Q
**Temporal · Task Queue 与两种任务**｜摘要 · 必会

Temporal 怎么找到该执行下一段代码的 worker？Workflow Task 和 Activity Task 有什么不同？为什么要分开队列？

## A
- **Task Queue：** 应用给工作指定一个 Task Queue 名字（如 `payments`），能处理这类工作的 worker 配置成轮询同一个名字。它是工作的具名目的地；Matching Service 管理这些队列，把任务交给轮询的 worker。History 需要运行代码时，其后台处理器把任务发给 Matching 的对应队列，Matching 交给在该队列等待的某个 worker。
- **Workflow Task：** 告诉 worker 运行 Workflow 代码，决定下一步该做什么。**Activity Task：** 告诉 worker 执行一个操作，比如调 Stripe 或发邮件。两者不必在同一批机器上跑。
- **分开的价值：** 不同的 Activity 可以在完全不同的 worker 群上运行：CPU 密集型工作一批机器，GPU 工作另一批，敏感的支付 Activity 放在隔离的服务里。不需要分开时，一个 worker 进程也可以同时跑两种代码。
- **Matching 不关心 worker 的实现，** 只匹配任务与轮询该队列的 worker。已有 worker 在轮询时直接交付；否则任务存进持久化数据库，等有 worker 再取。队列还可以分区到多个 Matching 实例以提高吞吐。
