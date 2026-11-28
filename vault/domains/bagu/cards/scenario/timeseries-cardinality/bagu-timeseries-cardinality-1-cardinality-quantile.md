---
id: bagu-timeseries-cardinality-1-cardinality-quantile
node: b.scenario.timeseries-cardinality
type: qa
step: 1
---
## Q
**时序基数 · 高基数、降采样与分位数聚合**｜追问

面试官：「有人给接口延迟指标加了 user_id 标签，监控系统先于业务挂了，为什么？分位数跨机器、跨时间又怎么聚合才对？」

## A
**基本回答。** 一条时间序列由指标名加一组标签值唯一确定，序列数是各标签取值个数相乘，叫基数。3 个方法 × 50 个接口 = 150 条，加 user_id（100 万）就是 1.5 亿条；每条序列在索引和内存里有常驻开销，不管这分钟有没有数据，监控先被撑垮；随发布变化的标签（pod 名）还会不断产生新序列，旧序列仍占索引。治理：user_id、订单号这类高基数 id 放日志和追踪，不放标签；接入时按指标、租户限制序列数上限，超限拒绝并告警。降采样每个窗口保留最小、最大、总和、计数（平均 = 总和 / 计数），只留平均会抹掉峰值；分层保留，如原始 15 天、5 分钟精度 90 天、1 小时精度 2 年以上。分位数不能平均：机器 A 1000 个请求 p99 为 100 ms，B 10 个请求 p99 为 2000 ms，平均 1050 ms 既不是总体 p99，也被少量请求拉偏。要合并固定桶直方图（同桶计数相加再插值，精度受桶宽限制，边界须事先定好）或 t-digest（可合并的分位数草图，自适应聚簇，尾部 p99、p999 精度高、内存小）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 292">
<rect x="8" y="12" width="84" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">方法</text>
<text x="50" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3 个</text>
<text x="106" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">×</text>
<rect x="120" y="12" width="84" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="162" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">接口</text>
<text x="162" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">50 个</text>
<text x="218" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">×</text>
<rect x="232" y="12" width="100" height="42" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">user_id</text>
<text x="282" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">100 万个</text>
<rect x="8" y="66" width="324" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">= 1.5 亿条序列，每条都常驻索引和内存</text>
<line x1="8" y1="108" x2="332" y2="108" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="8" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">分位数不能平均，要合并</text>
<rect x="8" y="136" width="150" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="154.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">机器 A：1000 个请求</text>
<text x="83" y="169.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p99 = 100 ms</text>
<rect x="182" y="136" width="150" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="257" y="154.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">机器 B：10 个请求</text>
<text x="257" y="169.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p99 = 2000 ms</text>
<line x1="83" y1="180" x2="83" y2="190" stroke-width="1.2" stroke="currentColor"/>
<line x1="257" y1="180" x2="257" y2="190" stroke-width="1.2" stroke="currentColor"/>
<line x1="83" y1="190" x2="257" y2="190" stroke-width="1.2" stroke="currentColor"/>
<line x1="170" y1="190" x2="170" y2="198" stroke-width="1.2" stroke="currentColor"/>
<line x1="170" y1="198" x2="83" y2="214" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83.0,214.0 89.3,209.6 90.5,215.9" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<line x1="170" y1="198" x2="257" y2="214" stroke-width="1.2" stroke="currentColor"/>
<polygon points="257.0,214.0 249.5,215.9 250.7,209.6" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<rect x="8" y="214" width="150" height="56" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="83" y="231" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">直接平均</text>
<text x="83" y="246" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">= 1050 ms</text>
<text x="83" y="261" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不是总体 p99</text>
<rect x="182" y="214" width="150" height="56" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257" y="231" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">桶计数相加</text>
<text x="257" y="246" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">或合并 t-digest</text>
<text x="257" y="261" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">再算总体 p99</text>
</svg>
上半部分是标签取值相乘出来的序列数；下半部分是两台机器的 p99 平均得 1050 ms，不是总体 p99，正确做法是合并桶计数或 t-digest。
**举个例子。** A 的桶里记 1000 次延迟，B 记 10 次，相同桶相加得 1010 次，总体 p99 是按从小到大排的第 1000 位（1010 × 0.99），来自真实分布而不是 1050 ms。降采样：5 分钟窗口保留最小、最大、总和 600、计数 4，平均 150，峰值用最大值留着。
**业务场景。** 有人给支付接口延迟加了 user_id，千万用户一天生成千万条序列；写入先超租户序列上限被拒并告警，用户维度改查日志。
**容易错。**
- **以为标签越多越好查：** 无界标签让序列数爆炸。
