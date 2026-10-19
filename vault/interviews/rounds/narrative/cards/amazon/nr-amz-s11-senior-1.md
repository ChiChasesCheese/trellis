---
id: nr-amz-s11-senior-1
node: amazon.followups
type: qa
step: 52
---
## Q
<p class="title">实习：Kafka 事件流<span class="meta">03 senior 追问</span></p>

*"How do you make sure one bad message can't poison the pipeline without silently losing data?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对“容错”与“不丢数据”之间张力的理解。

<span class="label">回答框架</span>

- converter 对坏消息返回 null 记录，task 继续跑，管线不被卡住
- 但不能静默吞掉：要有可观测的信号，比如计数和告警
- 被跳过的消息要有地方可追溯，能事后查看和重放
- 原则是记录它，而不是丢掉它

<span class="label">为什么这是最佳实践</span>

只让 task 不死是不够的，因为静默跳过会把一个明显的故障变成隐蔽的数据缺失。正确的做法是把失败变成可见：计数、告警、可追溯。这样既保住吞吐，又不丢信息。这个直觉后来在 Amex 管线里变成 record, never drop。具体死信队列或告警在实习里的落地程度，以实际为准。

<div class="sources"><b>表达 · business English</b><br>• <b><i>fail loudly</i></b> — 出错时要响亮地报<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A skipped message should fail loudly in the metrics, not silently.”</span><br>• <b><i>dead-letter queue</i></b> — 死信队列<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d route skipped messages to a dead-letter queue so they can be replayed.”</span></div>
