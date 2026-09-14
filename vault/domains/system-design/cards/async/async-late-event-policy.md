---
id: async-late-event-policy
node: async.streaming.processing
type: qa
---
## Q
Your streaming job's watermark says the 12:00–12:05 window is complete and its aggregate is emitted — then a mobile client that was in a tunnel uploads three events stamped 12:03. What are your options for these stragglers, and what does each one cost downstream?

## A
Three policies, in increasing order of downstream burden:

- **Drop them** (and count them in a metric): the emitted result is final and downstream stays simple — appends only. Cost: silent undercounting; acceptable only if you *monitor* the late rate and it stays negligible.
- **Allowed lateness — keep the window open and re-emit**: retain window state for an extra grace period and publish corrected aggregates when stragglers arrive. Cost: downstream must handle **updates, not appends** (upsert by window key, or process retraction + new value), and state size grows with the lateness horizon.
- **Side-output the late events** to a separate stream and reconcile out-of-band (e.g. a periodic batch correction). Cost: two code paths and delayed correctness.

The knob behind it all: watermark delay itself trades **latency vs completeness** — a conservative watermark makes windows late but final; an eager one is fast but leaks stragglers to the policy above. State it as a product decision: "how stale may a first answer be, and may an answer change afterwards?"

## Q zh
你的流处理任务的 watermark 判定 12:00–12:05 窗口已完整，聚合结果已经发出——随后一个刚出隧道的移动端客户端上传了三条时间戳为 12:03 的事件。对这些迟到者你有哪些选项？每个选项让下游付出什么代价？

## A zh
三种策略，按下游负担从轻到重排列：

- **丢弃（并打进指标）**：已发出的结果就是最终结果，下游保持简单——只有追加。代价：无声的少算；只有当你*监控*迟到率且它保持在可忽略水平时才可接受。
- **允许迟到（allowed lateness）——窗口保持打开并重新发出**：为窗口状态多保留一段宽限期，迟到者到达时发布修正后的聚合。代价：下游必须处理**更新而非追加**（按窗口 key 做 upsert，或处理撤回 + 新值），且状态大小随迟到容忍期增长。
- **把迟到事件旁路输出（side output）**到单独的流，带外调和（例如周期性的批修正）。代价：两条代码路径，正确性来得晚。

背后的总旋钮：watermark 的延迟本身就是**时延 vs 完整性**的交换——保守的 watermark 让窗口出得晚但一锤定音；激进的 watermark 出得快但把迟到者漏给上面的策略。把它表述成产品决策："第一个答案允许多旧？答案事后允许变吗？"
