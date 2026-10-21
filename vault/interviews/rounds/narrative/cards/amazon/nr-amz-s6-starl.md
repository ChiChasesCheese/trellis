---
id: nr-amz-s6-starl
node: amazon.outline
type: qa
step: 17
---
## Q
<p class="title">费用异常检测器 go/no-go<span class="meta">02 提纲</span></p>

STAR-L 提纲（60–90 秒）

## A
<span class="label">S</span>

- 离职的**实习生**留下一个 ML **费用异常检测器**，只在 **QA** 跑过

<span class="label">T</span>

- 决定：继续做，还是**评估**；并决定什么必须在他离开后**留得住**

<span class="label">A</span>

- 写 **go/no-go 评估**，而不是继续做
- 对比 **QA vs 生产**：6 个合成商户 vs ~**18,000**；不到 10 亿行 vs **数百亿**；峰值 ~**760M**
- 看出逐行 **numpy** 推理在生产规模会**超时**，QA 永远暴露不了
- 区分**会随离职消失**的和**可重建**的；离职前导出分析师**标注**
- 分阶段：**Phase 1** 确定性规则，纯 **SQL**；**Phase 2** ML 重训 2–3 个月，在**gate** 之后
- **冻结** Slack 告警和 CI/CD 工作，直到 gate 说 go

<span class="label">R</span>

- 不可替代的**标注已保全**；便宜的防御层有清晰路径
- 数字来自我自己的评估，尚未在生产复核

<span class="label">L</span>

- 一个经理可审计的**书面 gate**
- 宁可停一个项目，也不上线一个**凌晨 3 点**呼叫团队的项目

<div class="sources"><b>表达 · business English</b><br>• <b><i>go/no-go gate</i></b> — 放行或叫停的关卡<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I put Phase 2 behind an explicit go/no-go gate that my manager could audit.”</span><br>• <b><i>phased rollout</i></b> — 分阶段推进<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A phased rollout let us ship the cheap SQL rule first and defer the ML work.”</span><br>• <b><i>freeze the work</i></b> — 暂停相关工作<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I froze the Slack alerting work until the gate says go.”</span></div>
