---
id: nr-amz-s6-full
node: amazon.full
type: qa
step: 6
---
## Q
<p class="title">费用异常检测器 go/no-go<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：一个即将离职的实习生留下一个机器学习费用异常检测器，它只在 QA 环境跑过。顺着惯性，应该接着做下去。
- 判断：我没有接着做，而是写了一份 go/no-go 评估。我把 QA 和生产放在一起比：QA 只有 6 个合成商户、不到 10 亿行，生产是 18,140 个商户、约 15,000 种 plan 组合，峰值一天约 7.6 亿行。它的推理是逐行 numpy，在生产规模必然超时，而 QA 永远暴露不了这一点。
- 保全：我把“会随实习生离职消失的”和“可以从代码重建的”分开。代码、terraform、训练配方（固定 seed）都能重建，唯一不可再生的是分析师的 disposition 标注，所以我在他离开前把标注导出。
- 分阶段：Phase 1 只上确定性规则（金额等于费率乘数量加固定费），纯 SQL，Snowflake 本来就能处理几十亿行。Phase 2 是模型重训加推理重构，需要 2 到 3 个月，放在明确的 go/no-go gate 后面。同时冻结 Slack 告警和 CI/CD 工作，直到 gate 给出 go。
- 结果与学到：不可替代的标注保住了，便宜的防御层有了清晰路径，数字是我自己评估文档里的量级，我会如实说明还没在生产复核。我宁可停一个项目，也不上线一个凌晨 3 点呼叫团队的项目。

<span class="label">英文口述（60–90 秒）</span>

I inherited an ML fee-anomaly detector from an intern who was leaving. It had only ever run in QA, and the easy path was to keep building. Instead I wrote a go/no-go assessment. QA had six synthetic merchants and under a billion rows; production is about eighteen thousand merchants, around fifteen thousand plan combinations, and up to about 760 million rows on a peak day. The serving design was a per-row numpy forward pass, which would time out at that scale, and QA could never have shown it. I split the problem into what disappears when the intern leaves versus what's reproducible from code: only the analysts' labels were irreplaceable, so I got those exported before their last day. Then a phased plan. Phase one ships only the deterministic consistency rule as pure SQL, which Snowflake handles at billions of rows. Phase two, retraining and a new serving design, is two to three months and sits behind an explicit go/no-go gate. I froze the Slack alerting and CI/CD work until the gate says go. I'd rather stop a project than ship one that pages the team at 3 a.m. These numbers come from my own assessment and I haven't re-verified them in production.

<div class="sources"><b>表达 · business English</b><br>• <b><i>go/no-go call</i></b> — 上线与否的决定<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I made the go/no-go call on the detector with the precision numbers in front of me.”</span><br>• <b><i>phase the rollout</i></b> — 分阶段上线<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I argued to phase the rollout instead of switching everything on at once.”</span><br>• <b><i>precision over recall</i></b> — 宁可少报、不要误报<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“For an alert people get paged on, I&#x27;d choose precision over recall.”</span></div>
