---
id: nr-amz-s11-senior-2
node: amazon.followups
type: qa
step: 53
---
## Q
<p class="title">实习：Kafka 事件流<span class="meta">03 senior 追问</span></p>

*"At-least-once plus an idempotent consumer: where can that still break?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对幂等边界的理解，而不是背口号。

<span class="label">回答框架</span>

- 幂等要有稳定的业务键，键不稳定就去不了重
- 批内去重加数据库唯一约束，处理并发竞态
- 有副作用的下游（比如发出的费用事件）也要考虑重复
- 自动提交加短间隔偏 at-most-once，真正的防丢靠上游重试和对账

<span class="label">为什么这是最佳实践</span>

幂等不是一个开关，而是每个有副作用的步骤都要回答“重复执行会怎样”。唯一约束是最后一道防线，捕获冲突后跳过；对账则在管线之外发现漏掉的数据。口号“实际上恰好一次”的前提是这些环节都成立，所以我会按环节逐个核对，而不是只相信一个机制。

<div class="sources"><b>表达 · business English</b><br>• <b><i>idempotency key</i></b> — 幂等键<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Dedup only works if the idempotency key is stable.”</span><br>• <b><i>reconciliation</i></b> — 对账<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Reconciliation catches what the pipeline itself can&#x27;t.”</span></div>
