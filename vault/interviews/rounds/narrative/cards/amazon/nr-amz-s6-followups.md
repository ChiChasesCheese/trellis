---
id: nr-amz-s6-followups
node: amazon.followups
type: qa
step: 26
---
## Q
<p class="title">费用异常检测器 go/no-go<span class="meta">03 追问</span></p>

面试官会追问什么？每个怎么答？

## A
- **Who asked you to make this assessment?**
    - 见待补
- **How did you decide Phase 2 was a no-go and not just "harder"?**
    - 大 warehouse 上推理**必然超时**；精确率**无 ground truth**；告警量**每天数百万条**；估算 **5–8 人周** + **2–3 月**
- **What was the pushback?**
    - 见待补
- **How do you know your numbers are right?**
    - 来自**我自己的评估文档**，尚未从生产复核；口播用量级，这是诚实边界
- **What happened after?**
    - Jira DTBTTFOUND-3254 … 3261（label `anomaly-detector`）已开；Phase 1 / gate 当前状态见待补
- **What would make you say go?**
    - **业务驱动明确** + **shadow 精确率**达到阈值；具体阈值见待补
- **Wasn't that wasted intern work?**
    - 代码 / terraform / 训练配方（**固定 seed**）都可重建；唯一不可再生的是**标注**，已导出
- **What did you give up?**
    - 我对一个看似快速的胜利说了**不**，推迟了可见产出

<div class="sources"><b>表达 · business English</b><br>• <b><i>ground truth</i></b> — 可信的真实标签<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“We had no ground truth for precision, so a shadow run was the only honest test.”</span><br>• <b><i>alert fatigue</i></b> — 告警疲劳<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“At a 99.5 percent threshold we&#x27;d have produced millions of alerts a day, which is alert fatigue by design.”</span><br>• <b><i>sunk cost</i></b> — 沉没成本<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I didn&#x27;t rank priorities by sunk cost, I ranked them by risk-adjusted value.”</span></div>
