---
id: nr-amz-s6-senior-1
node: amazon.followups
type: qa
step: 27
---
## Q
<p class="title">费用异常检测器 go/no-go<span class="meta">03 senior 追问</span></p>

*"How would you prove the detector is precise enough before turning it on for real alerts?"*

## A
<span class="label">面试官在探</span> 面试官在探：没有 ground truth 时你怎么设计可信的评估。

<span class="label">回答框架</span>

- 先说 shadow mode：只记录不告警，持续跑一段时间
- 让分析师对一个抽样的结果打标，建立精确率的估计
- 按商户和费用类型分层抽样，避免被前两个大商户主导
- 提前写下放行的精确率阈值和每日告警量上限

<span class="label">为什么这是最佳实践</span>

异常检测没有现成标签，精确率只能靠人工标注的抽样来估。分层抽样是关键，因为 QA 里前两个商户占 97% 的行，不分层的话结论会被少数大户主导。阈值要在看数据之前定，否则是事后合理化。

<div class="sources"><b>表达 · business English</b><br>• <b><i>shadow mode</i></b> — 影子模式：只运行不生效<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d run the model in shadow mode and let analysts label a sample.”</span><br>• <b><i>stratified sampling</i></b> — 分层抽样<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Stratified sampling matters because two merchants made up 97 percent of the QA rows.”</span></div>
