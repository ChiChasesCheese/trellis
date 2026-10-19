---
id: nr-amz-s2-senior-1
node: amazon.followups
type: qa
step: 7
---
## Q
<p class="title">Quality-check 框架<span class="meta">03 senior 追问</span></p>

*"How did you decide the granularity of readiness should be per merchant rather than per table?"*

## A
<span class="label">面试官在探</span> 面试官在探：你有没有用数据和成本论证一个设计粒度，而不是凭感觉。

<span class="label">回答框架</span>

- 先给事实：约 50 个持续失败的商户挡住 35000 个商户，也就是约 4%
- 再比较方案：VARIANT 会关闭谓词下推，flatten 会受单元格大小上限限制，新表要新基础设施
- 再说选择：汇总行加每商户失败行，复用现有结果表
- 最后说容量：只存失败行，极端情况每月约 80 万行

<span class="label">为什么这是最佳实践</span>

粒度选错的代价随规模放大，所以要用生产数据量化被误伤的范围。每个被否决的方案都用具体机制说明为什么不行，这样结论经得起别人复核。选复用现有表是因为零新基础设施，上线风险最低。

<div class="sources"><b>表达 · business English</b><br>• <b><i>quantify the impact</i></b> — 把影响量化<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I quantified the impact first: fifty bad merchants against thirty-five thousand healthy ones.”</span><br>• <b><i>capacity analysis</i></b> — 容量分析<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The capacity analysis showed that storing only failures costs about eight hundred thousand rows a month.”</span></div>
