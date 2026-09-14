---
id: analytics-lambda-vs-kappa
node: analytics.derived
type: qa
---
## Q
Lambda architecture vs Kappa architecture for keeping derived views both fresh and correct — what does each run, and what pain made the industry drift from the first toward the second?

## A
- **Lambda**: run the same derivation **twice** — a streaming layer produces fast approximate/incremental results, a nightly batch layer recomputes authoritative ones from the raw archive, and a serving layer merges the two (batch overwrites stream).
- **Kappa**: run **one streaming pipeline** off a long-retention log; when logic changes or correctness is in doubt, don't run a batch — **replay**: start a second instance of the stream job from an earlier offset into a new output table, and cut over when it catches up.

The pain that killed Lambda in most shops: **every metric implemented twice**, in two frameworks with different semantics — double the bugs plus a new class of subtle stream/batch disagreements, and the merge logic at serving time is its own source of errors.

What Kappa requires to be honest: log retention (or an archived, replayable copy) deep enough for full rebuilds; a stream engine with exactly-once state and event-time windowing so replays reproduce batch-grade answers; and the side-by-side view-versioning discipline for cutovers. Lambda survives where those don't hold, or where huge historical recomputations are genuinely cheaper as batch scans.

## Q zh
为了让派生视图既新鲜又正确，Lambda 架构 vs Kappa 架构——各自运行什么？是什么痛点让业界从前者漂移到后者？

## A zh
- **Lambda**：同一套派生逻辑**跑两遍**——流式层产出快速的近似/增量结果，夜间批处理层从原始归档重算权威结果，服务层把两者合并（批的结果覆盖流的）。
- **Kappa**：只跑**一条流式管线**，数据源是长保留期的 log；逻辑变更或正确性存疑时，不跑批——而是**回放（replay）**：从更早的 offset 启动流作业的第二个实例，写入新的输出表，追平后切换。

杀死 Lambda 的痛点（对多数团队而言）：**每个指标都要实现两遍**，在语义不同的两套框架里——bug 翻倍，还多出一类微妙的流/批不一致，而服务层的合并逻辑本身又是一个错误来源。

Kappa 要成立的前提：log 保留（或可回放的归档副本）深到足以整体重建；流引擎具备 exactly-once 状态和 event-time 窗口，使回放能复现批处理级的答案；以及切换时的并排视图版本化纪律。在这些前提不成立、或超大规模历史重算确实按批扫描更便宜的地方，Lambda 仍然活着。
