---
id: nr-amz-s1-senior-1
node: amazon.followups
type: qa
step: 2
---
## Q
<p class="title">Amex 结算管线<span class="meta">03 senior 追问</span></p>

*"How would you know the pipeline is correct in production, beyond the tests?"*

## A
<span class="label">面试官在探</span> 面试官在探：你有没有把正确性做成持续运行的信号，而不只是上线前的测试。

<span class="label">回答框架</span>

- 先说分层：行级（坏字段不炸整批）、批级（每笔结算交易都有费用）、对账级（费用总额对 Amex 自己发的汇总记录）
- 再说失败时的动作：对账不一致就停 task 并 page on-call，而不是继续往下游放
- 最后说监控：Streamlit 任务监控加 Datadog 告警，让不一致能被人看见

<span class="label">为什么这是最佳实践</span>

单靠上线前测试证明不了生产里的数据是对的，因为输入是对方每天发来的文件，随时会变。把校验放在数据流里、并且对账不一致时主动停下来，错误就不会扩散到出款。分层则让你一眼知道是哪一层出了问题，缺哪层补哪层。

<div class="sources"><b>表达 · business English</b><br>• <b><i>defense in depth</i></b> — 纵深防御（多层校验互相兜底）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Row, batch and reconciliation checks gave us defense in depth on fee correctness.”</span><br>• <b><i>reconcile against the source of truth</i></b> — 对照权威数据源做对账<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“We reconcile fee totals against the summary record Amex itself sends.”</span></div>
