---
id: nr-amz-s11-senior-3
node: amazon.followups
type: qa
step: 54
---
## Q
<p class="title">实习：Kafka 事件流<span class="meta">03 senior 追问</span></p>

*"How would you scale this ingestion path 10x, and what would you check first?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对并行度模型和瓶颈的判断顺序。

<span class="label">回答框架</span>

- 先看 partition 数，因为并行度被它封顶
- 然后看 replicas 乘以 tasks.max 是否用满了 partition
- 再看下游 Snowflake 摄取、转换开销（converter）和消息大小
- 最后看 lag 与重试，确认扩容后没有把问题搬到别处

<span class="label">为什么这是最佳实践</span>

并行度模型是 replicas 乘以 tasks.max，上限是 partition 数，所以加机器不会越过这个上限；先查上限，才不会白扩容。扩容之后要看 lag 和错误率是否真的下降。需要增加 partition 时还要考虑键的顺序语义，这是以后会权衡的点，我自己并没有运维过集群。

<div class="sources"><b>表达 · business English</b><br>• <b><i>bottleneck</i></b> — 瓶颈<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The first thing I&#x27;d check is whether partitions are the bottleneck.”</span><br>• <b><i>consumer lag</i></b> — 消费滞后<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d watch consumer lag to confirm the scale-up actually helped.”</span></div>
