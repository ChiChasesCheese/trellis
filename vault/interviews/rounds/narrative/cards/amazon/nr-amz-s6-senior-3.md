---
id: nr-amz-s6-senior-3
node: amazon.followups
type: qa
step: 29
---
## Q
<p class="title">费用异常检测器 go/no-go<span class="meta">03 senior 追问</span></p>

*"What would you do to make per-row inference work at 760 million rows a day if the business did want the model?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对规模化推理的工程思路，是否能从逐行改成批量化。

<span class="label">回答框架</span>

- 先把瓶颈定位清楚：逐行 Python 调用和数据搬运，而不是模型本身
- 把推理推到数据旁边：用 Snowflake 的向量化 UDF 或把模型计算改成 set-based
- 先用规则过滤出候选，只对少量候选跑模型
- 上线前用生产量级数据做压力测试，并设超时与降级

<span class="label">为什么这是最佳实践</span>

逐行 numpy 的问题是调用开销和数据移动，不是算力不够。把计算放到数据所在的地方、先用便宜的规则缩小范围，就能把规模降几个数量级。这也是为什么 Phase 1 的纯 SQL 规则本身就能挡住大部分问题。

<div class="sources"><b>表达 · business English</b><br>• <b><i>set-based</i></b> — 基于集合的批量处理，而非逐行<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Moving from per-row to set-based processing is the first change I&#x27;d make.”</span><br>• <b><i>push compute to the data</i></b> — 把计算推到数据所在之处<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d push compute to the data instead of pulling rows out to Python.”</span></div>
