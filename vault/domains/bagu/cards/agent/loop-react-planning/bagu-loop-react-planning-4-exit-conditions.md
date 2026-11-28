---
id: bagu-loop-react-planning-4-exit-conditions
node: a.agent.loop-react-planning
type: qa
step: 4
---
## Q
**死循环 · 退出条件怎么设计**｜必会

面试官：「Agent 反复调用同一个工具停不下来，怎么防止？退出条件怎么设计？」

## A
**基本回答。** 退出条件必须由执行器代码强制，不能只写在提示词里。第一，设步数（常见 5 到 20，拿评测集统计正常完成的步数分布，取 P95 再留余量）、总超时、Token 或费用预算三道闸，每次调用前先检查剩余额度；单个工具另设独立超时。第二，做重复动作检测：连续几步的工具名和规范化参数都相同，就判定无进展。第三，任务状态版本多步不变，也停止。停止后记录原因，返回已有结果或转人工；高风险动作先暂停等人确认。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<rect x="10" y="4" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="22.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">模型给出下一步</text>
<rect x="10" y="46" width="150" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="63.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">步数没超上限？</text>
<rect x="10" y="82" width="150" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="99.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没超总超时？</text>
<rect x="10" y="118" width="150" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="135.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">预算还够？</text>
<rect x="10" y="154" width="150" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="171.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不是重复动作？</text>
<rect x="10" y="196" width="150" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85.0" y="214.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">执行工具</text>
<line x1="85" y1="32" x2="85.0" y2="40.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,46.0 82.0,40.0 88.0,40.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="85" y1="72" x2="85.0" y2="76.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,82.0 82.0,76.0 88.0,76.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="85" y1="108" x2="85.0" y2="112.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,118.0 82.0,112.0 88.0,112.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="85" y1="144" x2="85.0" y2="148.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,154.0 82.0,148.0 88.0,148.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="85" y1="180" x2="85.0" y2="190.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,196.0 82.0,190.0 88.0,190.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="196" y="70" width="140" height="92" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="266.0" y="97.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">任何一道不过</text>
<text x="266.0" y="112.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">停止并记录原因</text>
<text x="266.0" y="127.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">返回已有结果</text>
<text x="266.0" y="142.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">或转人工</text>
<line x1="160" y1="59" x2="191.07178020596024" y2="80.57762514302793" stroke-width="1.2" stroke="currentColor"/>
<polygon points="196.0,84.0 189.4,83.0 192.8,78.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="160" y1="95" x2="190.26189057369197" y2="104.24668878640588" stroke-width="1.2" stroke="currentColor"/>
<polygon points="196.0,106.0 189.4,107.1 191.1,101.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="160" y1="131" x2="190.0570463609335" y2="126.82541022764812" stroke-width="1.2" stroke="currentColor"/>
<polygon points="196.0,126.0 190.5,129.8 189.6,123.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="160" y1="167" x2="190.69369148291818" y2="150.80055171734872" stroke-width="1.2" stroke="currentColor"/>
<polygon points="196.0,148.0 192.1,153.5 189.3,148.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>
每次调用工具之前都过一遍检查；任何一道不过，就停止并记录原因，而不是继续执行。
**容易错。**
- **以为在提示词里写最多十次就够：**那只是建议，模型可能不遵守，必须由执行器代码强制。
- **只设步数闸：**步数相同的任务单步耗时和成本差很多，要同时配总超时和预算。
- **重复检测直接比较原始参数：**参数顺序不同、带无关字段，就会漏检，要先规范化再比较。
- **每层重试各算各的：**SDK、网关、工具三层各试 3 次，最坏就是 27 次，要共享总截止时间。
- **停了不记原因：**事后没法知道停在哪一步、为什么停。

**业务场景。** 订单查询接口持续返回 500：模型第 1 步调 `query_order(id=1029)` 得 500，第 2 步又调同样的工具和参数，重复动作检测判定无进展，记录原因「重复动作」并回复「订单服务暂不可用」；没有检测会一直重复到 30 次，白白烧掉 Token，最后才被步数闸拦下。
