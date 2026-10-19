---
id: nr-amz-s3-senior-3
node: amazon.followups
type: qa
step: 14
---
## Q
<p class="title">ACH 费用 NULL 事故<span class="meta">03 senior 追问</span></p>

*"How would you tell the difference between a health check that is wrong and one that is right but inconvenient?"*

## A
<span class="label">面试官在探</span> 面试官在探：你面对压力要求关掉告警时，如何用证据判断。

<span class="label">回答框架</span>

- 先拿样本：随机取一笔被告警标出的交易，手工追到底，看费用是否真的缺失
- 再看切片：缺失是否集中在一个新路径，对照组是否正常
- 再排除其他解释：时序滞后、数据绕过等
- 最后写下数字再决定，不靠嗓门大小

<span class="label">为什么这是最佳实践</span>

告警被怀疑时，最有力的反驳是一笔追到底的真实例子加一组切片数据。对照组正常、时序和绕过都被排除后，结论就很难被质疑。把数字写下来，让分歧从意见变成事实，也让别人能复核。

<div class="sources"><b>表达 · business English</b><br>• <b><i>control group</i></b> — 对照组<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Fast ACH was the control group: its sub-kind was populated and its fees were fine.”</span><br>• <b><i>evidence-based</i></b> — 以证据为依据<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I kept the discussion evidence-based by writing the numbers into the thread.”</span></div>
