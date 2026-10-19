---
id: nr-amz-s3-followups
node: amazon.followups
type: qa
step: 11
---
## Q
<p class="title">ACH 费用 NULL 事故<span class="meta">03 追问</span></p>

面试官会追问什么？每个怎么答？

## A
- **What did you decide vs. the team?**
    - 判定**检查是对的**、费用真丢；**不加排除名单**；把数字写下来
- **Which part was yours?**
    - **根因**、**postmortem**、重载合并、legacy DROP；止血 PR 是队友的："I owned the RCA and the hardening; the stopgap landed first."
- **Did you backfill?**
    - 不说我 backfill 了；灰度阶段队友说大概不需要
    - 方法论：**fix forward**，必要时 backfill；已被下游消费的错误状态要**更正分录**，不是回滚
- **Why didn't tests catch it?**
    - 只断言**路由**；fixture 用**卡 payload**；pending 行不断言 sub_kind；没有跨 promote→fee 的测试，已补 e2e
- **How do you prevent the class of bug?**
    - **Fail loudly**；修接缝不修调用点；**单函数默认参数**使新分支选不到不完整实现
- **Why delete via versioned migration?**
    - 删掉 `R__` repeatable 文件**不会删已部署对象**
- **How did you rule out other causes?**
    - 时序：每个 age 桶覆盖率都是 0%；stream 绕过：**30 of 30** 行到了 fee staging；对照组 fast ACH 有费用
- **Impact on merchants / money actually lost?**
    - 见待补

<div class="sources"><b>表达 · business English</b><br>• <b><i>stopgap</i></b> — 临时止血措施<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A teammate landed the stopgap first, and I owned the root cause and the hardening.”</span><br>• <b><i>fix forward</i></b> — 向前修复（不回滚）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“In billing I would fix forward, and issue a correcting entry if the wrong state was consumed.”</span><br>• <b><i>test gap</i></b> — 测试盲区<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The postmortem listed four test gaps that explained why the end-to-end suite missed it.”</span></div>
