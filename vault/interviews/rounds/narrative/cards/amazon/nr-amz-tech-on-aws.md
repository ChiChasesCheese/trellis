---
id: nr-amz-tech-on-aws
node: amazon.tech
type: qa
step: 11
---
## Q
<p class="title">技术深挖<span class="meta">05 Snowflake · 数据 · AWS</span></p>

如果你加入 AWS Data Services，用 AWS 原生服务重做你的结算管线，会怎么设计？

## A
<span class="label">设计</span> 文件落到 **S3** → S3 事件触发 **Step Functions**（每一步有重试和失败分支）→ 用 **Glue** 或 **Lambda** 做解析和校验 → 用条件写或 `MERGE` 幂等地写进 **Redshift**（分析）或 **DynamoDB**（按交易查）→ 对账结果写回，金额不一致时 **CloudWatch** 告警、**EventBridge** 暂停后续步骤。

<span class="label">保留的原则</span> 每种记录类型一条独立的流、每一步可重放、错误进隔离表而不是丢弃、一个开关能停整条线。

<span class="label">取舍</span> 积木更多、胶水代码更多，但每一步可以单独扩容、单独计费、和 AWS 权限体系天然打通。

<span class="label">说法</span> *"The services change; the invariants don't: replayable stages, idempotent writes, quarantine instead of drop, and a kill switch."*

<div class="sources"><b>表达 · business English</b><br>• <b><i>invariants</i></b> — 不变的约束 / 原则<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The services change; the invariants don&#x27;t.”</span><br>• <b><i>quarantine instead of drop</i></b> — 隔离而不是丢弃（坏数据）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Bad records go to quarantine instead of being dropped, so nothing is silently lost.”</span><br>• <b><i>least privilege</i></b> — 最小权限<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Each Lambda gets least-privilege IAM to only its bucket and table.”</span></div>
