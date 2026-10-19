---
id: nr-amz-r3-senior-2
node: amazon.followups
type: qa
step: 73
---
## Q
<p class="title">Aiki 消费者 App<span class="meta">03 senior 追问</span></p>

*"How do you control cost, quality and failure behavior when an LLM generates learning content?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对 LLM 产品化的成本、质量和降级思维

<span class="label">回答框架</span>

- 成本：缓存已生成内容，避免重复调用，并限制每用户调用量
- 质量：对输出做结构和事实校验，让用户能反馈错误内容
- 失败：模型不可用或超时时要有降级，不能阻塞学习流程
- 迭代：用反馈数据评估提示词改动，而不是凭感觉

<span class="label">为什么这是最佳实践</span>

LLM 调用有单价且结果不稳定，所以要把生成结果当作可缓存的资产，并设置校验和回退路径。这样成本可预测，质量问题能被用户反馈回流。这是一个资深工程师会采取的做法；具体我当时的成本数字没有记录。

<div class="sources"><b>表达 · business English</b><br>• <b><i>graceful degradation</i></b> — 优雅降级<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“If the model is down, the app should degrade gracefully instead of blocking study.”</span><br>• <b><i>feedback loop</i></b> — 反馈回路<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d add a feedback loop so users can flag bad generated content.”</span></div>
